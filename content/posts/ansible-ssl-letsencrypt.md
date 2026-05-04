---
title: "Ansible SSL: Certificados Let's Encrypt Automáticos com AWX"
date: 2026-05-03T10:00:00-03:00
draft: false
tags: ["devops", "ansible", "ssl", "letsencrypt", "awx", "nginx", "segurança", "automação"]
images: ["og-ansible-ssl-letsencrypt.png"]
description: "Automatize a criação e renovação de certificados SSL em múltiplos sites com Ansible, Certbot e Let's Encrypt. Job de renovação agendado no AWX, zero intervenção manual."
---

Você já acordou às 3 da manhã com o alerta de que um certificado SSL expirou em produção? Ou descobriu que um cliente tentou acessar o site e viu a tela vermelha do browser dizendo "conexão não é segura"? Esse é o custo de gerenciar SSL na mão.

Neste lab eu automatizei o ciclo completo de criação e renovação de certificados SSL para três sites diferentes — `fxshell1.com.br`, `fxshell2.com.br` e `fxshell3.com.br` — usando Ansible + Certbot + Let's Encrypt. Cada certificado cobre o domínio raiz **e** o `www` no mesmo cert (SAN). O AWX agenda a renovação automática toda **terça-feira às 03:00 UTC**; quando disparado manualmente, um survey pergunta quais tenants renovar antes de executar. Nenhum clique desnecessário, nenhuma surpresa.

---

## Objetivo do Lab

Construir uma automação completa que:

1. Instala e configura o Certbot em múltiplos servidores
2. Emite um único certificado cobrindo `dominio.com.br` **e** `www.dominio.com.br` (SAN — Subject Alternative Names)
3. Configura o Nginx para servir o desafio ACME e depois ativa HTTPS com TLS 1.3 + HSTS
4. Agenda renovação automática no AWX toda **terça-feira às 03:00 UTC**
5. Quando executado manualmente, pergunta via survey quais tenants renovar

---

## Tecnologias Utilizadas

**Ansible** é a ferramenta de automação que conecta via SSH nos servidores e aplica as configurações descritas em playbooks YAML. Sem agente instalado, sem daemon. Um comando no control node e todos os servidores ficam no estado desejado. Usado massivamente em times DevOps para garantir que a infraestrutura seja reproduzível e auditável.

**Certbot** é o cliente oficial do protocolo ACME, mantido pela Electronic Frontier Foundation. Ele faz a comunicação com a CA do Let's Encrypt: prova que você controla o domínio (através de um arquivo temporário no servidor), recebe o certificado assinado, e salva tudo no `/etc/letsencrypt/live/<domínio>/`. No lab ele é instalado como snap — a forma recomendada atualmente, que sempre traz a versão mais recente.

**Let's Encrypt** é uma Autoridade Certificadora (CA) gratuita e automatizada, mantida por Mozilla, Cisco, EFF e outros. Emite certificados X.509 válidos por 90 dias para qualquer domínio que você consiga provar que controla. A curta validade é intencional — força automação e garante que certificados comprometidos expirem rápido.

**ACME v2** é o protocolo que Let's Encrypt usa para emissão automatizada. No método `webroot`, o Certbot cria um arquivo temporário em `/.well-known/acme-challenge/` no seu servidor web. A CA do Let's Encrypt faz uma requisição HTTP para esse arquivo e, se conseguir ler, confirma que você controla o domínio e emite o certificado.

**Nginx** é o servidor web que fica na frente da aplicação. No lab ele tem duas responsabilidades: servir o diretório do desafio ACME durante a validação, e depois servir HTTPS com o certificado emitido. Configuramos TLS 1.2/1.3, HSTS, OCSP Stapling e headers de segurança.

**AWX** é a versão open source do Ansible Automation Platform (Red Hat Tower). Ele fornece uma interface web e API para executar playbooks Ansible de forma centralizada, com controle de acesso, logs históricos, e — o que mais importa aqui — schedules (cron jobs) para execução automática de jobs.

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     AWX / Ansible Tower                     │
│   Job Template: SSL Create   Job Template: SSL Renewal      │
│   Schedule: RRULE FREQ=DAILY às 03:00 UTC                   │
└──────────────────────────┬──────────────────────────────────┘
                           │ Trigger / SSH
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Ansible Control Node                           │
│         playbook-ssl-create.yml                             │
│         playbook-ssl-renewal.yml                            │
│         roles/ssl_certbot  roles/ssl_renewal                │
└────────┬──────────────────┬────────────────────┬────────────┘
         │ SSH              │ SSH                │ SSH
         ▼                  ▼                    ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ fxshell1.com  │  │ fxshell2.com.br │  │ fxshell3.com.br│
│ Nginx + SSL  │  │ Nginx + SSL      │  │ Nginx + SSL      │
│ 192.168.1.10 │  │ 192.168.1.11     │  │ 192.168.1.12     │
└──────┬───────┘  └────────┬─────────┘  └────────┬─────────┘
       │                   │                      │
       └───────────────────┴──────────────────────┘
                           │ ACME HTTP Challenge
                           ▼
              ┌────────────────────────┐
              │   Let's Encrypt CA     │
              │   ACME v2 Protocol     │
              │   Certificado 90 dias  │
              └────────────────────────┘
```

| Componente | Função |
|---|---|
| AWX | Orquestra execução, agenda renovação diária, guarda histórico |
| Ansible Control Node | Executa roles, conecta nos servidores via SSH |
| Role `ssl_certbot` | Instala Certbot, configura Nginx HTTP, emite certificado, sobe HTTPS |
| Role `ssl_renewal` | Verifica validade, renova se <30 dias, registra log |
| Nginx | Serve ACME challenge, proxy HTTPS com TLS 1.3 + HSTS |
| Let's Encrypt CA | Valida domínio via ACME, emite certificado X.509 gratuito |

![Diagrama animado — Ansible SSL Let's Encrypt AWX](/ansible-ssl-letsencrypt.gif)

---

## Como o Fluxo Funciona

O AWX dispara o playbook `ssl-create.yml`. O Ansible conecta em cada servidor via SSH e executa a role `ssl_certbot` em sequência:

![ACME HTTP Challenge — validação webroot passo a passo](/ssl-acme-challenge.gif)

1. Instala o Certbot via snap e cria o symlink em `/usr/bin/certbot`
2. Garante que o Nginx está instalado e rodando
3. Faz o deploy do template `nginx-http.conf.j2` — configuração HTTP simples que serve o diretório `.well-known/acme-challenge/` e redireciona todo o resto para HTTPS
4. Verifica se o certificado já existe em `/etc/letsencrypt/live/<domínio>/`
5. Se não existir, executa `certbot certonly --webroot` — o Certbot cria o arquivo de desafio, a CA do Let's Encrypt faz o GET HTTP para validar, e o certificado é emitido
6. Faz o deploy do template `nginx-ssl.conf.j2` — configuração HTTPS completa com TLS 1.2/1.3, HSTS, OCSP Stapling e security headers
7. Verifica a data de expiração do certificado emitido com `openssl x509 -enddate`

Para renovação, o job `ssl-renewal.yml` roda diariamente. Para cada servidor, ele lê a data de expiração do certificado atual, calcula os dias restantes, e só executa `certbot renew` se faltarem menos de 30 dias. Se renovou, notifica o handler para recarregar o Nginx.

---

## Estrutura do Projeto

```
ansible-ssl-letsencrypt/
├── ansible.cfg                         # Config: inventory, become, pipelining
├── playbook-ssl-create.yml             # Playbook principal: emite certificados
├── playbook-ssl-renewal.yml            # Playbook de renovação: usado pelo AWX
├── awx-job-template.yml                # Definição dos Job Templates e Schedule
├── inventory/
│   └── hosts.yml                       # 3 hosts com site_domain, email, webroot
├── group_vars/
│   └── all.yml                         # Certbot config, Nginx SSL params globais
├── roles/
│   ├── ssl_certbot/
│   │   ├── tasks/main.yml              # Instala, configura Nginx, emite cert
│   │   ├── handlers/main.yml           # restart/reload nginx
│   │   └── templates/
│   │       ├── nginx-http.conf.j2      # Config HTTP + ACME challenge
│   │       └── nginx-ssl.conf.j2       # Config HTTPS + TLS 1.3 + HSTS
│   └── ssl_renewal/
│       ├── tasks/main.yml              # Verifica validade, renova, loga
│       ├── handlers/main.yml           # reload nginx após renovação
│       └── templates/
│           └── renewal-report.j2       # Relatório de renovação
└── diagrama/
    ├── ansible-ssl-letsencrypt.html    # Diagrama animado interativo
    ├── ansible-ssl-letsencrypt.gif     # GIF para blog e LinkedIn
    └── gerar_gif.py                    # Script Pillow que gerou o GIF
```

---

## Inventário — Os 3 Sites

O inventário define os três servidores. Cada host tem `site_domain` (nome principal, usado como `--cert-name` pelo Certbot) e `site_domains` (lista com raiz **e** www, usada tanto no `certbot certonly` quanto nos `server_name` do Nginx).

```yaml
# inventory/hosts.yml
all:
  children:
    webservers:
      hosts:
        fxshell1_server:
          ansible_host: 192.168.1.10
          ansible_user: ubuntu
          site_domain: fxshell1.com.br          # cert-name no Certbot
          site_domains:                         # SAN: raiz + www no mesmo cert
            - fxshell1.com.br
            - www.fxshell1.com.br
          site_email: admin@fxshell1.com.br
          site_webroot: /var/www/fxshell
          nginx_config_name: fxshell1.com.br

        fxshell2_server:
          ansible_host: 192.168.1.11
          ansible_user: ubuntu
          site_domain: fxshell2.com.br
          site_domains:
            - fxshell2.com.br
            - www.fxshell2.com.br
          site_email: admin@fxshell2.com.br
          site_webroot: /var/www/fxshell2
          nginx_config_name: fxshell2.com.br

        fxshell3_server:
          ansible_host: 192.168.1.12
          ansible_user: ubuntu
          site_domain: fxshell3.com.br
          site_domains:
            - fxshell3.com.br
            - www.fxshell3.com.br
          site_email: admin@fxshell3.com.br
          site_webroot: /var/www/fxshell3
          nginx_config_name: fxshell3.com.br
```

O Certbot aceita múltiplos `--domain` num único comando. O primeiro domínio da lista vira o nome do certificado (`/etc/letsencrypt/live/fxshell1.com.br/`), e os demais entram como SANs. O resultado é um único arquivo `.pem` válido para `fxshell1.com.br` e `www.fxshell1.com.br` — sem precisar de dois certificados separados.

---

## Role `ssl_certbot` — O Coração da Emissão

A task mais importante da role verifica se o certificado já existe antes de tentar emitir. Isso garante idempotência — você pode rodar o playbook quantas vezes quiser sem gerar requisições desnecessárias para a CA (o Let's Encrypt tem rate limits).

O comando usa um loop Jinja2 para gerar múltiplos `--domain`, cobrindo `dominio.com.br` e `www.dominio.com.br` num único certificado SAN:

```yaml
# roles/ssl_certbot/tasks/main.yml (trecho)

- name: Verificar se certificado já existe
  stat:
    path: "{{ certbot_certs_dir }}/{{ site_domain }}/fullchain.pem"
  register: cert_exists

- name: Obter certificado SSL via certbot (webroot — raiz + www)
  command: >
    certbot certonly
    --webroot
    --webroot-path {{ site_webroot }}
    {% for d in site_domains %}--domain {{ d }} {% endfor %}
    --email {{ site_email }}
    --agree-tos
    --non-interactive
    {% if certbot_staging %}--staging{% endif %}
    --rsa-key-size {{ certbot_rsa_key_size }}
    --keep-until-expiring
  when: not cert_exists.stat.exists
```

Para `fxshell1_server`, o comando expandido fica:
```bash
certbot certonly --webroot --webroot-path /var/www/fxshell \
  --domain fxshell1.com.br --domain www.fxshell1.com.br \
  --email admin@fxshell1.com.br --agree-tos --non-interactive \
  --rsa-key-size 4096 --keep-until-expiring
```

O flag `--keep-until-expiring` garante que, mesmo se o certificado já existir, o Certbot não vai renovar antes de 30 dias. O flag `--staging` permite testar o fluxo completo sem consumir os rate limits de produção do Let's Encrypt.

---

## Template Nginx HTTPS

![TLS Handshake — Certificate, OCSP Stapling, HSTS e sessão segura](/ssl-tls-handshake.gif)

O template `nginx-ssl.conf.j2` gera uma config com as melhores práticas de TLS:

```nginx
server {
    listen 443 ssl http2;
    server_name {{ site_domain }} www.{{ site_domain }};

    ssl_certificate     {{ certbot_certs_dir }}/{{ site_domain }}/fullchain.pem;
    ssl_certificate_key {{ certbot_certs_dir }}/{{ site_domain }}/privkey.pem;
    ssl_trusted_certificate {{ certbot_certs_dir }}/{{ site_domain }}/chain.pem;

    ssl_protocols             TLSv1.2 TLSv1.3;
    ssl_ciphers               ECDHE-RSA-AES256-GCM-SHA512:...;
    ssl_prefer_server_ciphers off;
    ssl_session_cache         shared:SSL:50m;
    ssl_stapling              on;
    ssl_stapling_verify       on;

    # HSTS: força HTTPS por 1 ano em todos os subdomínios
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
}
```

O OCSP Stapling (`ssl_stapling on`) reduz a latência das conexões: em vez de o browser consultar a CA para verificar se o certificado foi revogado, o servidor já faz essa consulta periodicamente e inclui a resposta assinada no handshake TLS.

---

## Role `ssl_renewal` — Lógica de Renovação

![Lógica de Renovação SSL — AWX Schedule → decisão por site](/ssl-renewal-logic.gif)

A task de renovação calcula os dias restantes com `openssl` e `date`, e só chama o `certbot renew` se a condição for verdadeira:

```yaml
- name: Calcular dias restantes
  shell: |
    end_date="{{ cert_end_date.stdout }}"
    today=$(date +%s)
    expiry=$(date -d "$end_date" +%s)
    echo $(( (expiry - today) / 86400 ))
  register: days_remaining

- name: Renovar certificado se faltam menos de 30 dias
  command: >
    certbot renew
    --cert-name {{ site_domain }}
    --non-interactive
    --quiet
  when: days_remaining.stdout | int < 30
  notify: reload nginx
```

Cada execução registra uma linha em `/var/log/certbot-renewal.log` com data, domínio, dias restantes e se foi renovado.

---

## AWX — Job Templates e Schedule

A configuração do AWX está documentada no arquivo `awx-job-template.yml`. Os dois jobs principais são:

**SSL - Criar Certificado**: roda sob demanda com survey para o operador escolher domínio e ambiente (staging/produção).

**SSL - Renovar Certificados**: tem dois modos de uso:
- **Schedule automático** — toda terça-feira às 03:00 UTC, renova todos os hosts do grupo `webservers`
- **Execução manual com survey** — antes de executar, o AWX exibe um formulário para o operador selecionar quais tenants renovar

O survey de seleção de tenants funciona assim: o campo `tenants` aceita o nome de um ou mais hosts separados por vírgula (ex: `fxshell1_server,fxshell2_server`) ou o grupo `webservers` para renovar todos. Esse valor é passado para a diretiva `hosts:` do playbook, que funciona como um `--limit` dinâmico.

```yaml
# O playbook usa o valor do survey como filtro de hosts
- name: Renovar certificados SSL Let's Encrypt
  hosts: "{{ tenants | default('webservers') }}"
```

O schedule usa a sintaxe RFC 5545 (iCalendar RRULE), que é o formato que o AWX aceita:

```
DTSTART:20240102T030000Z RRULE:FREQ=WEEKLY;BYDAY=TU
# BYDAY=TU = Tuesday (terça-feira)
# FREQ=WEEKLY = toda semana
# Hora: 03:00 UTC
```

Para configurar manualmente na interface do AWX:

```
Projects     → Criar projeto apontando para o repositório git
Inventories  → Importar hosts.yml com os 3 servidores
Credentials  → Adicionar chave SSH dos servidores
Job Templates → SSL - Criar Certificado (playbook-ssl-create.yml)
Job Templates → SSL - Renovar (playbook-ssl-renewal.yml)
              → Habilitar Survey com campo "tenants"
              → Habilitar ask_limit_on_launch: true
Schedules    → Adicionar no job de renovação:
              → Recurrence: Weekly, Day: Tuesday, Time: 03:00 UTC
              → Default tenants: webservers (todos)
```

---

## Executando

```bash
# 1. Testar conectividade com todos os servidores
ansible all -m ping

# 2. Testar com staging primeiro (não gasta rate limit)
ansible-playbook playbook-ssl-create.yml -e "certbot_staging=true"

# 3. Verificar o que seria feito (dry-run parcial)
ansible-playbook playbook-ssl-create.yml --check

# 4. Emitir certificados reais para todos os sites
ansible-playbook playbook-ssl-create.yml

# 5. Emitir só para um site específico
ansible-playbook playbook-ssl-create.yml -l fxshell1_server

# 6. Forçar renovação manualmente
ansible-playbook playbook-ssl-renewal.yml -e "force_renewal=true"

# 7. Testar HTTPS após emissão
curl -I https://fxshell1.com.br
curl -I https://fxshell2.com.br
curl -I https://fxshell3.com.br
```

Para verificar os headers de segurança:

```bash
curl -sI https://fxshell1.com.br | grep -E "Strict-Transport|X-Frame|X-Content"
```

---

## Monitoramento e Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| `certbot: command not found` | Snap não instalou ou symlink faltando | Verificar `snap list certbot` e recriar symlink |
| `Challenge failed: connection refused` | Nginx não está rodando ou porta 80 bloqueada | `systemctl status nginx` e verificar firewall |
| `Too many certificates already issued` | Rate limit do Let's Encrypt atingido | Usar `--staging` para testes; aguardar 7 dias |
| `nginx: configuration file test failed` | Caminho do certificado errado no template | Verificar se `/etc/letsencrypt/live/<domínio>/` existe |
| `SSL certificate has expired` | Renovação automática falhou | Verificar `/var/log/certbot-renewal.log` e `/var/log/letsencrypt/` |
| AWX job falha com `Permission denied` | Usuário SSH sem sudo configurado | Verificar `become: true` e sudoers no servidor |

```bash
# Verificar logs do certbot
cat /var/log/letsencrypt/letsencrypt.log | tail -50

# Verificar log de renovação customizado
cat /var/log/certbot-renewal.log

# Testar validade do certificado manualmente
openssl s_client -connect fxshell1.com.br:443 -servername fxshell1.com.br < /dev/null 2>/dev/null \
  | openssl x509 -noout -enddate
```

---

## Para Que Serve no Mercado

Times DevOps e SRE que gerenciam dezenas ou centenas de domínios usam exatamente esse padrão. As variações incluem:

- **Wildcard certificates** com validação DNS ao invés de HTTP (necessário quando os servidores não têm porta 80 pública)
- **Integração com Vault** para armazenar as credenciais dos provedores DNS e automatizar renovação de wildcards
- **Pipeline de CI/CD** que dispara o playbook quando um novo site é adicionado ao inventário
- **Certificados internos** usando a mesma lógica com uma CA própria (CFSSL, Vault PKI) para serviços internos que não precisam de CA pública

O princípio é o mesmo em qualquer escala: infraestrutura declarativa, idempotente, auditável. Um certificado expirado em produção é a prova de que existe um processo manual em algum lugar esperando para falhar.

---

## Conclusão

O que resolve esse lab não é só a automação do `certbot` — é a combinação de idempotência do Ansible com a orquestração do AWX. Você pode executar esse playbook mil vezes e o resultado é sempre o mesmo: se o certificado existe e está válido, nada muda. Se está para expirar, é renovado. Se não existe, é criado. Esse nível de previsibilidade é o que separa infraestrutura mantida de infraestrutura gerenciada.

---

## Referências

- [Certbot Documentation](https://certbot.eff.org/docs/)
- [Let's Encrypt — Rate Limits](https://letsencrypt.org/docs/rate-limits/)
- [ACME Protocol RFC 8555](https://tools.ietf.org/html/rfc8555)
- [Nginx SSL Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [AWX Project](https://github.com/ansible/awx)
- [Ansible Documentation](https://docs.ansible.com/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
