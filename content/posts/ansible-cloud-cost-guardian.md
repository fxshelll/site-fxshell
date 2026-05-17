---
title: "FinOps na Prática: Automação de Custos Cloud com Ansible e Azure CLI"
date: 2026-05-17
draft: false
tags: ["ansible", "azure", "finops", "devops", "cloud", "automacao", "iac"]
images: ["ansible-cloud-cost-guardian.gif"]
description: "Como automatizar a coleta de custos Azure, detectar recursos ociosos e sem tags, e gerar relatórios FinOps automáticos usando Ansible e Azure CLI — com dados reais de uma subscription."
---

A fatura do mês chegou 40% acima do esperado. Ninguém no time sabia exatamente o que tinha crescido. Depois de duas horas consultando o portal do Azure, descobriram que um cluster AKS de homologação tinha ficado ligado no fim de semana inteiro — e ninguém percebeu porque não havia alerta nenhum. Esse é o problema que o **ansible-cloud-cost-guardian** resolve.

Este lab implementa uma automação FinOps completa usando **Ansible como orquestrador**, **Azure CLI para coleta de dados** e scripts Python para análise. O resultado é um relatório gerado automaticamente com custo atual, recursos sem tag, recursos ociosos e envio para o Microsoft Teams.

---

## O que é FinOps

**FinOps** (Financial Operations) é a prática de trazer visibilidade e controle para os gastos com infraestrutura cloud. Em times de DevOps e SRE, significa ter respostas rápidas para perguntas como: quanto estamos gastando hoje, qual serviço cresceu mais esse mês, quais recursos estão ligados sem uso, e quem é responsável por cada coisa.

Sem automação, esse trabalho é manual, inconsistente e sempre atrasado. Com automação, vira rotina.

---

## Objetivo do Lab

Construir uma automação que:

- Coleta custos mensais via Azure Cost Management
- Tira snapshot diário do inventário de recursos
- Compara com o dia anterior para detectar recursos novos
- Identifica recursos sem tags obrigatórias
- Detecta discos não associados e IPs públicos órfãos
- Gera relatório em Markdown
- Envia alerta para Microsoft Teams (quando configurado)
- Exporta dados em CSV para análise histórica

---

## Tecnologias Utilizadas

### Ansible

Ansible é uma ferramenta de automação de infraestrutura da Red Hat. Funciona sem agente — conecta via SSH ou localmente e executa tarefas declaradas em arquivos YAML chamados **playbooks**. É amplamente usado em times DevOps para configuração de servidores, deploys e, como neste lab, orquestração de processos de coleta e análise.

### Azure CLI (`az`)

Interface de linha de comando oficial da Microsoft para o Azure. Permite consultar qualquer recurso da sua subscription via terminal — custos, VMs, AKS, storage, banco de dados, redes. Neste lab, usamos para coletar dados reais de consumo e inventário.

### Python

Scripts Python processam os dados coletados: comparam snapshots de inventário, identificam diferenças, normalizam custos e exportam CSVs. Biblioteca padrão apenas — sem dependências externas além do Pillow para o diagrama.

---

## Arquitetura

```text
Ansible (localhost)
  │
  ├── azure_costs     → az consumption usage list → snapshot JSON
  ├── azure_inventory → az resource list / disk list / public-ip list
  ├── finops_analysis → compare_snapshots.py / normalize_costs.py
  └── teams_report    → POST webhook → Microsoft Teams
```

| Componente | Função |
|---|---|
| `finops-main.yml` | Playbook principal que chama todas as roles |
| `role azure_costs` | Coleta custo mensal via Azure CLI |
| `role azure_inventory` | Lista recursos, discos órfãos e IPs não associados |
| `role finops_analysis` | Compara snapshots, detecta novos recursos, exporta CSV |
| `role teams_report` | Formata e envia relatório para o Teams |
| `compare_snapshots.py` | Diff entre inventário de hoje e de ontem |
| `normalize_costs.py` | Agrupa custo por serviço e gera CSV |
| `check_tags.py` | Lista recursos sem tags obrigatórias |

![Diagrama animado — ansible-cloud-cost-guardian](/ansible-cloud-cost-guardian.gif)

---

## Contexto Real: Subscription Azure ToggleMaster

Este lab foi construído com dados reais de uma subscription Azure usada no projeto **ToggleMaster** (FIAP PosTech Fase 4). A subscription `Azure subscription 1` contém atualmente **34 recursos** distribuídos entre dois resource groups principais.

Resultado real da coleta de inventário:

```text
Total de recursos:      34
Recursos sem tags:      16  (47% do total)
Clusters AKS:           1   (aks-togglemaster | centralus | 2 nodes Standard_D2_v4)
PostgreSQL Flexible:    3   (flag, targeting, auth)
CosmosDB:               1
Redis Cache:            1
Container Registry:     1
Storage Accounts:       2
VNets:                  2
Private Endpoints:      3
PVCs (discos AKS):      5
```

Recursos sem nenhuma tag (candidatos a revisão):

```text
- safiaptechchallangetf4   (Storage Account)
- satogglemasterf4         (Storage Account)
- redis-togglemaster-fase-4 (Redis)
- cosmosdb-togglemaster-fase-4 (CosmosDB)
- vnet-fiap-tech           (VNet)
- toggleacrfase4           (Container Registry)
- pe-postgresql-flag       (Private Endpoint)
- pe-postgresql-auth       (Private Endpoint)
- pe-postgresql-targeting  (Private Endpoint)
```

Tags obrigatórias que este lab configura como padrão:

```yaml
tags:
  required:
    - ambiente
    - aplicacao
    - squad
    - owner
    - centro_custo
```

---

## Relatório Executivo — Exemplo de Saída

Esse é o checklist que o playbook gera e envia para o Teams ao final de cada execução. Grande o suficiente para ser lido num canal sem abrir nada.

```text
╔══════════════════════════════════════════════════════════════════╗
║         FINOPS CLOUD GUARDIAN — RELATORIO MENSAL                ║
║   Subscription: Azure subscription 1  |  17/05/2026  08:00     ║
╚══════════════════════════════════════════════════════════════════╝

STATUS GERAL:   ⚠  ATENCAO  (+28.6% vs mes anterior)

┌─────────────────────┬──────────────────────┬────────────────────┐
│   CUSTO ATUAL       │  PREVISAO FECHAMENTO  │  MES ANTERIOR      │
│   R$ 38.420         │  R$ 52.000            │  R$ 29.870         │
└─────────────────────┴──────────────────────┴────────────────────┘

─── TOP 5 SERVICOS ─────────────────────────────────────────────────
 1. AKS Producao        (aks-togglemaster)    R$ 12.300  ████████░░
 2. PostgreSQL Flexible  (3 instancias)        R$  8.900  ██████░░░░
 3. Storage Backup      (satogglemasterf4)     R$  5.100  ███░░░░░░░
 4. Redis Cache         (redis-togglemaster)   R$  3.400  ██░░░░░░░░
 5. CosmosDB            (cosmosdb-toggle)      R$  2.800  █░░░░░░░░░

─── ALERTAS ────────────────────────────────────────────────────────
 [CRITICO]  16 recursos sem tags obrigatorias
            owner, squad, centro_custo ausentes
            Recursos: redis, cosmosdb, acr, storage, vnet...

 [ATENCAO]  AKS nodepool cresceu 24% vs mes anterior
            aks-togglemaster | Standard_D2_v4 | 2 nodes

 [ATENCAO]  CosmosDB sem tag de ambiente
            Sem chargeback definido para este recurso

─── INVENTARIO ─────────────────────────────────────────────────────
 Total de recursos:        34
 Recursos sem tags:        16  (47%)
 Novos recursos (24h):      0
 Discos orfaos:             0
 IPs publicos nao usados:   0
 Clusters AKS:              1  (aks-togglemaster | centralus)
 PostgreSQL Flexible:       3  (flag, targeting, auth)

─── RECOMENDACOES ──────────────────────────────────────────────────
 → Adicionar tags obrigatorias nos 16 recursos sem governanca
 → Revisar crescimento do AKS — avaliar nodepool de hml
 → Validar necessidade do CosmosDB 24x7 em ambiente de testes
 → Exportar CSV gerado para dashboard Grafana de tendencias

Gerado por ansible-cloud-cost-guardian
https://fxshelll.github.io/posts/ansible-cloud-cost-guardian/
```

---

## Estrutura do Projeto

```text
ansible-cloud-cost-guardian/
├── inventories/
│   └── hosts.ini                  # localhost connection
├── group_vars/
│   └── all.yml                    # thresholds, tags obrigatórias, config
├── playbooks/
│   ├── finops-main.yml            # orquestrador principal
│   ├── collect-costs.yml          # coleta custo mensal
│   ├── collect-inventory.yml      # snapshot de recursos
│   ├── detect-new-resources.yml   # diff de inventário
│   └── send-teams-report.yml      # envio para Teams
├── roles/
│   ├── azure_costs/tasks/main.yml
│   ├── azure_inventory/tasks/main.yml
│   ├── finops_analysis/tasks/main.yml
│   └── teams_report/tasks/main.yml
├── scripts/
│   ├── compare_snapshots.py       # detecta recursos novos/removidos
│   ├── normalize_costs.py         # agrupa custo por serviço → CSV
│   └── check_tags.py              # lista recursos sem tags
└── data/
    ├── snapshots/                 # JSONs diários de custo e inventário
    ├── reports/                   # relatórios Markdown gerados
    └── exports/                   # CSVs para histórico e Grafana
```

---

## Configuração

### Pré-requisitos

```bash
# Azure CLI autenticado
az login
az account set --subscription "sua-subscription-id"

# Ansible instalado
pip install ansible

# Verificar acesso
az account show
```

### Variáveis principais (`group_vars/all.yml`)

```yaml
azure:
  subscription_id: "{{ lookup('env', 'AZURE_SUBSCRIPTION_ID') }}"
  resource_group: "rg-producao"
  currency: "BRL"

thresholds:
  cost_growth_attention: 15   # % — gera aviso
  cost_growth_critical: 30    # % — gera alerta crítico

tags:
  required:
    - ambiente
    - aplicacao
    - squad
    - owner
    - centro_custo

idle:
  check_unattached_disks: true
  check_unassociated_public_ips: true
```

### Exportar variáveis de ambiente

```bash
export AZURE_SUBSCRIPTION_ID="ae352d8a-54b2-4e9c-adc6-3690dba03c13"
export TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/..."  # opcional
```

---

## Executando

### Coleta completa (modo principal)

```bash
ansible-playbook playbooks/finops-main.yml -i inventories/hosts.ini
```

### Somente inventário e tags

```bash
ansible-playbook playbooks/collect-inventory.yml -i inventories/hosts.ini
ansible-playbook playbooks/detect-new-resources.yml -i inventories/hosts.ini
```

### Ver recursos sem tags na mão

```bash
az resource list -o json | python3 scripts/check_tags.py
# REQUIRED_TAGS=ambiente,aplicacao,squad,owner,centro_custo
```

### Normalizar custos e exportar CSV

```bash
python3 scripts/normalize_costs.py \
  --input data/snapshots/costs-$(date +%Y-%m-%d).json \
  --output data/exports/finops-$(date +%Y-%m-%d).csv
```

### Comparar inventários manualmente

```bash
python3 scripts/compare_snapshots.py \
  --today data/snapshots/resources-$(date +%Y-%m-%d).json \
  --yesterday data/snapshots/resources-$(date -d yesterday +%Y-%m-%d).json
```

---

## Exemplo de Saída

### Inventário coletado

```text
TASK [azure_inventory : Exibir resumo do inventário]
ok: [localhost] => {
    "msg": [
        "Total de recursos: 34",
        "Discos não associados: 0",
        "IPs públicos órfãos: 0",
        "Clusters AKS: 1"
    ]
}
```

### Recursos sem tags

```text
Recursos sem tags obrigatórias (9 encontrados):
  safiaptechchallangetf4 (storageAccounts) — faltando: ambiente, aplicacao, squad, owner, centro_custo
  redis-togglemaster-fase-4 (Redis) — faltando: ambiente, aplicacao, squad, owner, centro_custo
  cosmosdb-togglemaster-fase-4 (databaseAccounts) — faltando: ambiente, aplicacao, squad, owner, centro_custo
  toggleacrfase4 (registries) — faltando: ambiente, aplicacao, squad, owner, centro_custo
```

### Novos recursos detectados (diff entre dias)

```text
Novos recursos detectados:
  + vm-hml-api-03 (virtualMachines) — RG: rg-homologacao
  + disk-backup-sql-02 (disks) — RG: rg-homologacao

Recursos removidos:
  - pip-test-01 (publicIPAddresses) — RG: rg-testes
```

---

## Monitoramento e Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| `az consumption usage list` retorna vazio | Subscription sem dados de custo no período | Verificar período e permissão de Cost Management Reader |
| `compare_snapshots.py` falha | Snapshot do dia anterior não existe | Normal na primeira execução — criar snapshot hoje |
| Tags check retorna erro JSON | `az resource list` retornou erro de auth | Reautenticar com `az login` |
| Webhook Teams não entrega | URL expirada ou firewall | Recriar webhook no Teams e exportar nova URL |
| Discos órfãos sempre zero | Query `diskState=='Unattached'` sem resultado | Confirmar permissão de leitura no resource group |

---

## Agendamento com Cron

Para rodar diariamente às 8h:

```bash
# crontab -e
0 8 * * * cd /opt/ansible-cloud-cost-guardian && \
  AZURE_SUBSCRIPTION_ID=... \
  ansible-playbook playbooks/finops-main.yml -i inventories/hosts.ini \
  >> /var/log/finops.log 2>&1
```

---

## Para Que Serve no Mercado

Em times de DevOps e SRE, essa automação substitui um processo manual de 2-3 horas por semana de revisão do portal do Azure. Os casos de uso mais comuns:

- **FinOps reviews semanais** — relatório automático chega no canal do Teams toda segunda antes da reunião
- **Governança de tags** — todo recurso novo sem tag gera alerta antes de virar problema de chargeback
- **Rightsizing** — histórico de CPU e custo por recurso suporta decisões de reduzir SKU
- **Detecção de shadow IT** — recursos criados fora do processo aparecem no diff do dia seguinte
- **Auditoria de fim de projeto** — recursos esquecidos aparecem no relatório de ociosos

---

## Conclusão

FinOps não é sobre cortar custo — é sobre ter visibilidade para tomar decisões melhores. Um time que sabe exatamente o que está rodando, quem é responsável e quanto custa consegue agir antes da fatura chegar. Esta automação transforma essa visibilidade em rotina: um playbook Ansible que roda todo dia, coleta, compara, analisa e avisa.

O próximo passo natural é conectar o CSV gerado a um dashboard Grafana para acompanhar tendências ao longo do tempo — algo que o arquivo de exportação já está formatado para receber.

---

## Referências

- [Azure Cost Management + Billing](https://learn.microsoft.com/pt-br/azure/cost-management-billing/)
- [Azure CLI — az consumption](https://learn.microsoft.com/pt-br/cli/azure/consumption)
- [Ansible Documentation](https://docs.ansible.com/)
- [FinOps Foundation](https://www.finops.org/)
- [Azure Resource Tags — boas práticas](https://learn.microsoft.com/pt-br/azure/azure-resource-manager/management/tag-resources)
