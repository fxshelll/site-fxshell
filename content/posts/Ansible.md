---
title: "Ansible"
date: 2021-03-29T21:56:17-03:00
draft: false
tags: ["devops", "ansible", "linux", "automação", "infraestrutura"]
---

O Ansible é uma ferramenta de automação de infraestrutura open source que permite gerenciar configurações, provisionar servidores e orquestrar tarefas complexas em dezenas ou centenas de máquinas ao mesmo tempo — tudo a partir de um único ponto de controle, sem instalar nenhum agente nos servidores alvo.

O nome vem da ficção científica: um "ansible" é um dispositivo de comunicação superlumínica que transmite informação instantaneamente para múltiplos destinos. A metáfora é precisa.

---

## Os quatro pilares do Ansible

**Gerenciamento de Mudança** — O Ansible é idempotente: executa uma tarefa somente se for necessário. Se o estado desejado já existe, ele não faz nada. Isso permite rodar o mesmo playbook várias vezes sem efeitos colaterais.

**Provisionamento** — Instala pacotes, configura serviços, cria usuários, aplica permissões — prepara um servidor do zero para uma função específica.

**Automação** — Executa tarefas de forma ordenada, permite tomar decisões condicionais e encadear operações complexas com YAML simples.

**Orquestração** — Coordena múltiplos servidores e aplicações em sequência: atualiza o banco antes dos app servers, drena o load balancer antes de reiniciar um nó.

---

## Por que o Ansible?

**Sem agente.** Não há software para instalar nos servidores gerenciados. O Ansible usa SSH (Linux) e WinRM (Windows) — protocolos que já existem em qualquer servidor.

**YAML simples.** Os playbooks são legíveis por qualquer pessoa da equipe — dev, ops ou gerência. Não é uma DSL exótica, é YAML com lógica.

**Configuração rápida.** Sem daemon, sem banco de dados, sem porta extra. Instale o Ansible no control node e comece a usar.

**Seguro.** SSH é o canal de comunicação. Suporte nativo a chaves SSH, LDAP e Kerberos para autenticação.

---

## Arquitetura

<iframe src="/ansible-arquitetura.html"
        width="100%"
        height="540"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

O Control Node é a única máquina com Ansible instalado. A partir dele, o Ansible se conecta via SSH aos hosts Linux e via WinRM aos hosts Windows, empurra os módulos Python temporariamente, executa as tarefas e remove tudo ao final. Nenhum rastro fica nos hosts gerenciados.

---

## Como funciona

O Ansible é desenvolvido em Python e requer Python ≥ 2.7 ou ≥ 3.5. Ele sempre busca o interpretador em `/usr/bin/python` por padrão — isso pode ser ajustado com a variável `ansible_python_interpreter`.

A comunicação acontece via:
- **SSH** para servidores Linux (usuário + senha ou chave SSH)
- **WinRM** para servidores Windows

A autenticação é descentralizada — pode ser feita com LDAP ou Kerberos para ambientes corporativos.

---

## Fluxo de execução de um Playbook

<iframe src="/ansible-playbook-flow.html"
        width="100%"
        height="500"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

Ao executar `ansible-playbook site.yml -i hosts`, o Ansible:

1. Lê o playbook YAML e interpreta as plays
2. Consulta o inventário para descobrir quais hosts executam cada play
3. Determina quais módulos precisam ser executados (apt, copy, service, template...)
4. Conecta via SSH/WinRM nos hosts alvos
5. Aplica cada task, reporta o estado (ok / changed / failed) e aciona handlers se necessário

---

## Instalação

O Ansible não adiciona banco de dados, daemon ou software persistente nos hosts. A única dependência é Python.

**RHEL / CentOS / Fedora** — habilite o EPEL antes:

```sh
sudo yum install ansible
```

**Ubuntu / Debian:**

```sh
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

**Via pip (qualquer distro):**

```sh
sudo apt-get install python3-pip   # se não tiver pip
sudo pip3 install ansible
sudo pip3 install ansible --upgrade   # para atualizar
```

Após instalar, configure o acesso SSH:

```sh
ssh-keygen -t rsa          # gere sua chave
ssh-copy-id user@host      # copie para os hosts
```

---

## Configuração — ansible.cfg

O arquivo principal de configuração é o `ansible.cfg`. A ordem de leitura (da menor para a maior precedência):

1. `/etc/ansible/ansible.cfg` (global)
2. `~/.ansible.cfg` (usuário)
3. `./ansible.cfg` (diretório corrente)
4. Variável de ambiente `ANSIBLE_CONFIG`

Um `ansible.cfg` funcional e comentado:

```ini
[defaults]

# Execução paralela em até 5 hosts simultaneamente
forks                   = 5
log_path                = /var/log/ansible.log
module_name             = command
executable              = /bin/bash

# Caminhos
inventory               = /etc/ansible/hosts
roles_path              = /etc/ansible/roles
remote_tmp              = ~/.ansible/tmp
local_tmp               = ~/.ansible/tmp

# Autenticação
remote_user             = root
ask_pass                = no

# SSH
remote_port             = 22
timeout                 = 10
host_key_checking       = False
private_key_file        = ~/.ssh/id_rsa

[privilege_escalation]
become                  = True
become_method           = sudo
become_user             = root
become_ask_pass         = False

[ssh_connection]
scp_if_ssh              = smart
transfer_method         = smart
retries                 = 3
```

---

## Inventário — Hosts, Grupos e Sub-grupos

O inventário define quais servidores o Ansible conhece e como eles se organizam. Pode ser um arquivo estático (`/etc/ansible/hosts`) ou dinâmico (script que consulta cloud providers).

<iframe src="/ansible-inventory.html"
        width="100%"
        height="510"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

**Hosts individuais:**

```ini
192.168.1.151
192.168.1.234
```

**Grupos:**

```ini
[servidores_bd]
192.168.1.151

[servidores_web]
192.168.1.234
```

**Sub-grupos (children):**

```ini
[servidores:children]
servidores_web
servidores_bd
```

**Variáveis por grupo:**

```ini
[servidores_bd:vars]
ansible_ssh_port=22
ansible_ssh_user=osboxes
ansible_ssh_pass=osboxes.org
ansible_become=yes
ansible_become_method=sudo
```

**Alias por host:**

```ini
mysql ansible_ssh_host=192.168.1.234
```

---

## Comandos Ad-hoc

Ad-hoc são comandos pontuais executados sem playbook — ideais para operações rápidas.

**Sintaxe base:**

```sh
ansible <hosts> -u <user> -k [-b] -m <módulo> -a "<args>"
```

**Flags:**

| Flag | Função |
|------|--------|
| `-u` | usuário remoto |
| `-k` | solicita senha SSH |
| `-K` | solicita senha para `sudo` |
| `-b` | executa com elevação (become) |
| `-m` | módulo a usar |
| `-a` | argumento do módulo |
| `-i` | inventário alternativo |

**Ping em todos os hosts:**

```sh
ansible all -m ping -u osboxes -k
```

```
192.168.1.151 | SUCCESS => { "changed": false, "ping": "pong" }
192.168.1.234 | SUCCESS => { "changed": false, "ping": "pong" }
```

**Coletar facts do sistema:**

```sh
ansible 192.168.1.234 -u osboxes -k -m setup
```

**Reiniciar serviço SSH:**

```sh
ansible 192.168.1.151 -u osboxes -k -b -m systemd -a "name=ssh state=restarted"
```

**Executar comando shell:**

```sh
ansible 192.168.1.151 -u osboxes -k -b -m shell -a "systemctl status ssh"
```

**Comando direto (módulo `command` por padrão):**

```sh
ansible 192.168.1.151 -u osboxes -k -a "pwd"
```

**Filtrar por grupo:**

```sh
ansible -i hosts servidores_bd -m ping -u osboxes -k
```

Para ignorar o aviso de Python legado, adicione ao `ansible.cfg`:

```ini
interpreter_python = auto_legacy_silent
```

---

## Roles — Automação Modular e Reutilizável

Roles são a forma correta de organizar automação complexa. Em vez de um playbook gigante, você cria unidades independentes e reutilizáveis — uma role para nginx, outra para mysql, outra para hardening — e as compõe no playbook principal.

<iframe src="/ansible-roles-estrutura.html"
        width="100%"
        height="530"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

**Estrutura de diretórios padrão:**

```
playbook.yml
└── roles/
    └── nginx/
        ├── tasks/
        │   └── main.yml      # lista de tarefas (obrigatório)
        ├── handlers/
        │   └── main.yml      # acionados por notify nas tasks
        ├── templates/
        │   └── nginx.conf.j2 # Jinja2 com variáveis dinâmicas
        ├── files/            # arquivos estáticos para cópia
        ├── vars/
        │   └── main.yml      # variáveis com prioridade alta
        ├── defaults/
        │   └── main.yml      # defaults facilmente sobrescritíveis
        └── meta/
            └── main.yml      # dependências entre roles (lido primeiro)
```

**Chamando roles no playbook:**

```yaml
---
- hosts: webserver
  roles:
    - common    # executada primeiro
    - nginx
    - php
    - mysql
```

> A execução de uma role é definida pelas tasks em `tasks/main.yml`. O diretório `meta` é analisado primeiro para resolver dependências.

---

## Variáveis e Facts

As variáveis permitem que o mesmo playbook funcione de forma diferente em cada host ou ambiente.

<iframe src="/ansible-vars-priority.html"
        width="100%"
        height="490"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

**Ordem de prioridade (menor → maior):**

```
1. role/defaults/main.yml      ← mais fácil de sobrescrever
2. inventory file vars
3. group_vars/all
4. group_vars/*
5. host_vars/*
6. host facts (módulo setup)
7. role/vars/main.yml
8. set_fact / registered vars
9. extra vars (-e)             ← prioridade máxima
```

**Ansible Facts** — o módulo `setup` descobre automaticamente informações de cada host:

```sh
ansible hostname -m setup
```

Retorna sistema operacional, IPs, memória, CPUs, discos, variáveis de ambiente e muito mais. Essas informações ficam disponíveis como variáveis nos playbooks: `{{ ansible_os_family }}`, `{{ ansible_default_ipv4.address }}`, etc.

**Exemplo de estrutura com `group_vars`:**

```
├── group_vars/
│   └── servidores     ← variáveis aplicadas ao grupo
├── hosts
├── host_vars/
└── roles/
```

**Usar variável extra na linha de comando (maior prioridade):**

```sh
ansible-playbook site.yml -e "nginx_port=8080"
```

---

## Próximos passos

Com esse conhecimento base, você está pronto para:

- Criar **playbooks completos** que provisionam stacks inteiras
- Organizar infraestrutura com **roles reutilizáveis** (inclusive via Ansible Galaxy)
- Integrar Ansible em **pipelines CI/CD** (GitHub Actions, GitLab CI, Jenkins)
- Gerenciar **secrets** com Ansible Vault
- Escalar para centenas de servidores com inventários **dinâmicos** (AWS, Azure, GCP)

Veja os posts relacionados para laboratórios práticos com Ansible em ação:
