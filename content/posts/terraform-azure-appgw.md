---
title: "Application Gateway no Azure com Terraform — Lab de Backend API com Path Routing"
date: 2026-04-25
draft: false
tags: ["terraform", "azure", "appgateway", "devops", "cloud", "networking", "iac", "loadbalancer"]
images: ["og-terraform-azure-appgw.png"]
description: "Lab completo com Terraform provisionando Azure Application Gateway com roteamento por URL path, health probes HTTP e backend API em Python — com comparativo detalhado entre App Gateway e Load Balancer."
---

Se a sua aplicação expõe múltiplas APIs numa mesma infraestrutura e você precisa rotear o tráfego por URL — `/api/orders` para um pool, `/api/inventory` para outro — um Load Balancer tradicional não resolve. Ele opera na camada 4 (TCP/UDP), enxerga apenas IP e porta, e distribui conexões sem entender o conteúdo HTTP. O Azure Application Gateway opera na camada 7 e faz exatamente esse roteamento baseado em path, header e host — além de oferecer SSL termination, health probes HTTP e integração com WAF.

Este lab provisiona com Terraform um cenário completo: uma API backend em Python rodando em 3 VMs, um Application Gateway com URL path map, health probes customizados e backend pools separados por rota.

## Application Gateway vs Load Balancer — O Que Muda

Antes de entrar no lab, vale entender **por que** escolher um em vez do outro. A diferença fundamental é a camada OSI em que cada um opera:

| Característica | Azure Load Balancer (L4) | Azure Application Gateway (L7) |
|---|---|---|
| **Camada OSI** | 4 — TCP/UDP | 7 — HTTP/HTTPS |
| **O que enxerga** | IP de origem/destino, porta | URL, headers, cookies, hostname |
| **Roteamento** | Por IP + porta (regras de NAT) | Por URL path, header, hostname |
| **Health probe** | TCP ou HTTP (código de status) | HTTP com path, hostname e match de body |
| **SSL/TLS** | Pass-through (não termina) | SSL termination e re-encryption |
| **WAF** | Não | Sim (WAF v2 integrado ou add-on) |
| **Session affinity** | Por IP de origem (hash) | Cookie-based affinity nativo |
| **Rewrite** | Não | Headers, URL path e query string |
| **Autoscale** | Sim | Sim (Standard_v2) |
| **Custo** | Mais barato | Mais caro (paga por capacity units) |
| **Caso de uso** | Tráfego não-HTTP (DB, DNS, gaming) | APIs, microsserviços, apps web |

### Quando usar Load Balancer

- Tráfego TCP/UDP puro — bancos de dados, servidores DNS, jogos multiplayer
- Cenários onde você só precisa distribuir conexões por IP e porta
- Custo é prioridade e você não precisa de nenhum recurso HTTP
- Balanceamento interno entre VMs na mesma VNet sem exposição pública

### Quando usar Application Gateway

- APIs HTTP/HTTPS que precisam de roteamento por URL path (microsserviços)
- Aplicações que exigem SSL termination centralizado
- Cenários que precisam de WAF para proteção contra OWASP Top 10
- Session affinity por cookie (aplicações stateful)
- Redirect HTTP → HTTPS, rewrite de headers e URL

### Vantagens do Application Gateway em detalhes

**Roteamento por URL path** — O recurso central. Com `url_path_map`, o gateway inspeciona o path da requisição HTTP e direciona para backend pools diferentes. `/api/orders` pode ir para um conjunto de servidores otimizado para consultas de pedidos, enquanto `/api/inventory` vai para outro pool com mais memória. Com Load Balancer, todo tráfego na porta 80/443 vai para o mesmo backend — não há como diferenciar por rota.

**Health probes HTTP inteligentes** — O Load Balancer verifica se a porta TCP está respondendo. O Application Gateway faz um `GET /health` (ou qualquer path configurado), valida o status code HTTP e pode até verificar o conteúdo do body. Se o backend retorna 200 mas com `{"status":"degraded"}`, o probe pode detectar isso. Isso reduz drasticamente falsos positivos de "healthy" em backends que aceitam conexão TCP mas não estão funcionando corretamente.

**SSL termination (offload)** — O TLS é terminado no gateway, que faz a descriptografia e encaminha tráfego HTTP puro para os backends. Isso elimina o custo de CPU de TLS em cada VM backend e centraliza a gestão de certificados em um único ponto. Opcionalmente, o gateway pode re-encriptar o tráfego para o backend (end-to-end TLS), mas o certificado pode ser diferente — self-signed, por exemplo.

**WAF integrado** — O Application Gateway com SKU `WAF_v2` inclui proteção contra ataques OWASP Top 10 (SQL injection, XSS, CSRF) sem precisar de um appliance separado. As regras são gerenciadas centralmente e atualizadas pela Microsoft. Com Load Balancer, proteção WAF exige uma solução externa.

**Autoscale zone-redundant (v2)** — O SKU `Standard_v2` escala automaticamente as instâncias do gateway baseado no tráfego e pode ser distribuído entre Availability Zones, eliminando o gateway como ponto único de falha.

## Objetivo do Lab

Provisionar com Terraform um Application Gateway que recebe requisições HTTP, roteia por URL path para backend pools distintos e monitora a saúde dos backends com health probes HTTP customizados. A aplicação backend é uma API Python minimalista que serve `/api/orders`, `/api/inventory` e `/health`.

## Tecnologias Utilizadas

**Terraform** é a ferramenta de Infrastructure as Code que provisiona todos os recursos no Azure de forma declarativa e versionável.

**Azure Application Gateway** é o balanceador de carga de camada 7 da Microsoft que inspeciona o conteúdo HTTP das requisições e roteia para diferentes backend pools baseado em regras de URL path, headers e hostnames.

**Azure Virtual Network** isola a infraestrutura com subnets dedicadas — uma para o Application Gateway (requisito obrigatório) e outra para os backends.

**Cloud-init** configura as VMs no primeiro boot, instalando Python e iniciando a API backend como um serviço systemd, sem necessidade de acesso SSH manual.

## Arquitetura

```
┌──────────────────────────────────────────────────────────────────────┐
│                    REQUEST FLOW                                       │
│                                                                       │
│  ┌───────────┐  HTTPS    ┌────────────────────────────┐              │
│  │  Usuario   │ ────────► │   Application Gateway      │              │
│  │ (Internet) │           │   Standard_v2               │              │
│  └───────────┘           │                              │              │
│                           │  Listener :80                │              │
│                           │  URL Path Map:               │              │
│                           │    /api/orders → pool-orders │              │
│                           │    /api/inventory → pool-inv │              │
│                           │  Health Probe: GET /health   │              │
│                           └──────────┬───────────────────┘              │
│                                      │  :8080                          │
│                           ┌──────────┼──────────┐                      │
│                           ▼          ▼          ▼                      │
│                     ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│                     │backend-1 │ │backend-2 │ │backend-3 │            │
│                     │10.10.2.4 │ │10.10.2.5 │ │10.10.2.6 │            │
│                     │ Python   │ │ Python   │ │ Python   │            │
│                     │ API:8080 │ │ API:8080 │ │ API:8080 │            │
│                     └──────────┘ └──────────┘ └──────────┘            │
└──────────────────────────────────────────────────────────────────────┘
```

| Componente | Função |
|---|---|
| `Application Gateway` | Recebe tráfego HTTP, roteia por URL path, monitora health dos backends |
| `Listener` | Escuta na porta 80 com o IP público do gateway |
| `URL Path Map` | Mapeia `/api/orders` e `/api/inventory` para backend pools diferentes |
| `Health Probe` | Verifica `/health` a cada 15s — remove backend do pool após 3 falhas |
| `Backend Pool` | Grupo de VMs que recebe o tráfego roteado pelo gateway |
| `vm-backend-1..3` | VMs Ubuntu com API Python servindo na porta 8080 |

![Diagrama animado — Azure Application Gateway](/terraform-azure-appgw.gif)

## Como Funciona o Path-Based Routing

Quando uma requisição chega ao Application Gateway, o processamento segue esta sequência:

1. O **Listener** aceita a conexão HTTP na porta 80 (ou 443 com TLS)
2. A **Request Routing Rule** associa o listener ao **URL Path Map**
3. O **URL Path Map** inspeciona o path da URL e encontra a `path_rule` correspondente
4. A requisição é encaminhada para o **Backend Pool** definido na regra, usando as configurações do **Backend HTTP Settings** (porta 8080, timeout, affinity)
5. O gateway mantém um **Health Probe** periódico que faz `GET /health` em cada backend — backends que falham são removidos do pool automaticamente

Se nenhuma `path_rule` corresponde ao path da requisição, o gateway usa o `default_backend_address_pool` definido no path map.

> **Subnet dedicada:** O Application Gateway v2 exige uma subnet dedicada (sem outras VMs ou serviços). O Terraform cria `snet-appgw` exclusivamente para o gateway e `snet-backend` para as VMs — não tente colocar ambos na mesma subnet.

## Estrutura do Projeto

```
terraform-azure-appgw/
├── main.tf                       # Provider, backend, módulos
├── variables.tf                  # Variáveis de entrada
├── outputs.tf                    # Outputs (IP público, FQDN)
├── modules/
│   ├── networking/
│   │   ├── main.tf               # VNet, subnets, NSGs
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── backend_app/
│   │   ├── main.tf               # VMs + cloud-init (API Python)
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── app_gateway/
│       ├── main.tf               # AppGW, listeners, path map, probes
│       ├── variables.tf
│       └── outputs.tf
└── diagrama/
    ├── terraform-azure-appgw.html
    ├── terraform-azure-appgw.gif
    └── gerar_gif.py
```

## Networking — VNet e Subnets

A VNet usa o CIDR `10.10.0.0/16` com duas subnets isoladas:

```
10.10.0.0/16  (vnet-appgw-lab)
├── 10.10.1.0/24  snet-appgw     ← Application Gateway (dedicada)
└── 10.10.2.0/24  snet-backend   ← VMs backend
```

O NSG da subnet do gateway permite HTTP (80), HTTPS (443) e o range de portas de gerenciamento `65200-65535` (obrigatório para o Application Gateway v2 funcionar — sem essa regra, o health do gateway fica degraded).

```hcl
security_rule {
  name                       = "AllowGatewayManager"
  priority                   = 120
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = "65200-65535"
  source_address_prefix      = "GatewayManager"
  destination_address_prefix = "*"
}
```

O NSG da subnet de backend permite tráfego apenas da subnet do gateway na porta 8080 — nenhum acesso direto da internet aos backends:

```hcl
security_rule {
  name                       = "AllowAppGwToBackend"
  priority                   = 100
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = "8080"
  source_address_prefix      = "10.10.1.0/24"
  destination_address_prefix = "*"
}
```

## Backend API — Python com cloud-init

Cada VM backend roda uma API HTTP em Python puro (sem framework) na porta 8080, provisionada automaticamente via cloud-init no primeiro boot. A API serve três endpoints:

| Endpoint | Retorno |
|---|---|
| `GET /health` | `{"status": "healthy"}` — usado pelo health probe |
| `GET /api/orders` | Lista de pedidos fictícios + hostname do servidor |
| `GET /api/inventory` | Lista de estoque fictício + hostname do servidor |

O hostname no response permite verificar qual backend respondeu — útil para confirmar que o round-robin está funcionando.

```python
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        elif self.path == "/api/orders":
            data = {
                "server": socket.gethostname(),
                "orders": [
                    {"id": 1, "product": "Widget A", "qty": 10},
                    {"id": 2, "product": "Widget B", "qty": 5},
                ]
            }
            # ...
```

A API roda como serviço systemd (`api-backend.service`) com `Restart=always`, garantindo que ela reinicie automaticamente em caso de crash.

## Application Gateway — Path Map e Health Probes

O gateway é o componente central. O Terraform configura:

### URL Path Map

```hcl
url_path_map {
  name                               = "url-path-map"
  default_backend_address_pool_name  = "pool-orders"
  default_backend_http_settings_name = "http-settings-default"

  path_rule {
    name                       = "rule-orders"
    paths                      = ["/api/orders", "/api/orders/*"]
    backend_address_pool_name  = "pool-orders"
    backend_http_settings_name = "http-settings-default"
  }

  path_rule {
    name                       = "rule-inventory"
    paths                      = ["/api/inventory", "/api/inventory/*"]
    backend_address_pool_name  = "pool-inventory"
    backend_http_settings_name = "http-settings-default"
  }
}
```

O `default_backend_address_pool` captura qualquer path que não tenha regra explícita — sem ele, o gateway retorna 502.

### Health Probe

```hcl
probe {
  name                = "probe-health"
  host                = "127.0.0.1"
  path                = "/health"
  protocol            = "Http"
  interval            = 15
  timeout             = 10
  unhealthy_threshold = 3
}
```

O probe faz `GET /health` a cada 15 segundos. Se um backend não responder 200 em 3 tentativas consecutivas (45 segundos), ele é removido do pool. Quando volta a responder, é readicionado automaticamente.

### Backend HTTP Settings

```hcl
backend_http_settings {
  name                  = "http-settings-default"
  cookie_based_affinity = "Disabled"
  port                  = 8080
  protocol              = "Http"
  request_timeout       = 30
  probe_name            = "probe-health"
}
```

O `cookie_based_affinity` está desabilitado porque a API é stateless — cada requisição pode ir para qualquer backend. Em aplicações stateful (sessões), habilitar isso faz o gateway inserir um cookie `ApplicationGatewayAffinity` que fixa o usuário no mesmo backend.

## Executando

```bash
# Inicializar
terraform init

# Revisar o plano
terraform plan -var="admin_password=SenhaSegura123!"

# Aplicar
terraform apply -var="admin_password=SenhaSegura123!"

# Testar os endpoints (após ~5 min para provisionamento + cloud-init)
curl http://$(terraform output -raw appgw_public_ip)/api/orders
curl http://$(terraform output -raw appgw_public_ip)/api/inventory
curl http://$(terraform output -raw appgw_public_ip)/health
```

Executando múltiplas requisições, o campo `server` no JSON alterna entre `vm-backend-1`, `vm-backend-2` e `vm-backend-3` — confirmando que o round-robin distribui o tráfego entre os backends.

```bash
# Verificar distribuição round-robin
for i in $(seq 1 10); do
  curl -s http://$(terraform output -raw appgw_public_ip)/api/orders | jq .server
done
```

## Monitoramento e Troubleshooting

### Verificar health dos backends

```bash
# Via Azure CLI — mostra o estado de cada backend no pool
az network application-gateway show-backend-health \
  --resource-group rg-appgw-lab \
  --name appgw-lab \
  --query 'backendAddressPools[].backendHttpSettingsCollection[].servers[]' \
  --output table
```

### Logs de diagnóstico

O Application Gateway gera logs de acesso e performance que podem ser enviados para um Log Analytics Workspace:

```bash
# Habilitar diagnostic settings
az monitor diagnostic-settings create \
  --name appgw-diagnostics \
  --resource $(az network application-gateway show -g rg-appgw-lab -n appgw-lab --query id -o tsv) \
  --workspace $(az monitor log-analytics workspace show -g rg-appgw-lab -n law-appgw-lab --query id -o tsv) \
  --logs '[{"category":"ApplicationGatewayAccessLog","enabled":true},{"category":"ApplicationGatewayPerformanceLog","enabled":true}]'
```

### Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| Gateway health: Unhealthy | Falta da regra NSG para portas 65200-65535 | Adicionar regra `AllowGatewayManager` |
| Backend: Unhealthy | Health probe falhando (API não está rodando) | Verificar `systemctl status api-backend` na VM |
| HTTP 502 | Nenhum backend healthy no pool | Verificar NSG da subnet backend e porta 8080 |
| HTTP 504 | Backend demora mais que o `request_timeout` | Aumentar timeout no `backend_http_settings` |

## Para Que Serve no Mercado

O Application Gateway é o ponto de entrada padrão para aplicações web e APIs no Azure. Em arquiteturas de microsserviços, ele substitui a necessidade de um reverse proxy (Nginx/HAProxy) gerenciado manualmente, centralizando roteamento, TLS e WAF em um serviço gerenciado com autoscale.

A capacidade de rotear por URL path permite que uma única URL pública (`api.empresa.com`) distribua tráfego para dezenas de microsserviços diferentes, cada um em seu backend pool — sem que o cliente precise saber quantos serviços existem por trás.

Para times que já usam Terraform, o Application Gateway é um recurso complexo de configurar pela primeira vez (listeners, rules, probes, pools — tudo é interdependente), mas uma vez modularizado como neste lab, fica trivial replicar para novos ambientes.

## Conclusão

O Application Gateway resolve um problema que o Load Balancer não consegue: rotear tráfego HTTP com inteligência. Se a sua aplicação é web ou API, o gateway oferece roteamento por path, health probes inteligentes, SSL termination e WAF — tudo em um único serviço gerenciado. O Load Balancer continua sendo a escolha certa para tráfego não-HTTP (bancos de dados, protocolos customizados), mas para qualquer coisa que fala HTTP, o Application Gateway é a ferramenta adequada.

## Referências

- [Azure Application Gateway — Documentação oficial](https://learn.microsoft.com/pt-br/azure/application-gateway/overview)
- [URL path-based routing overview](https://learn.microsoft.com/pt-br/azure/application-gateway/url-route-overview)
- [Application Gateway vs Load Balancer](https://learn.microsoft.com/pt-br/azure/architecture/guide/technology-choices/load-balancing-overview)
- [Health probes — Application Gateway](https://learn.microsoft.com/pt-br/azure/application-gateway/application-gateway-probe-overview)
- [WAF on Application Gateway](https://learn.microsoft.com/pt-br/azure/web-application-firewall/ag/ag-overview)
- [Terraform azurerm_application_gateway](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_gateway)
- [Subnet requirements for Application Gateway v2](https://learn.microsoft.com/pt-br/azure/application-gateway/configuration-infrastructure)
