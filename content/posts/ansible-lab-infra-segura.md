---
title: "Ansible Lab: Provisionando Infraestrutura Web Segura do Zero"
date: 2026-04-21T10:00:00-03:00
draft: false
tags: ["devops", "ansible", "segurança", "linux", "infraestrutura", "nginx", "mysql", "haproxy"]
---

**Cenário**: você tem 4 VMs vazias e precisa subir uma stack web completa com load balancer, dois servidores de aplicação, banco de dados — tudo com segurança configurada desde o início — em menos de 5 minutos. Só com Ansible.

---

## Arquitetura do Lab

```
┌─────────────────────────────────────────────────────────┐
│                   ANSIBLE CONTROL NODE                   │
│                  (seu terminal / CI/CD)                  │
└──────────────────────┬──────────────────────────────────┘
                       │ SSH (porta 22)
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  lb-01   │  │  web-01  │  │  web-02  │  │  db-01   │
   │ HAProxy  │  │  Nginx   │  │  Nginx   │  │  MySQL   │
   │:80/:443  │  │  PHP-FPM │  │  PHP-FPM │  │  :3306   │
   └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

**Roles aplicadas:**
| Servidor | Roles |
|----------|-------|
| lb-01    | common, hardening, haproxy |
| web-01   | common, hardening, nginx, php |
| web-02   | common, hardening, nginx, php |
| db-01    | common, hardening, mysql |

---

## Setup do Ambiente

### Vagrantfile

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"

  nodes = {
    "lb-01"  => "192.168.56.10",
    "web-01" => "192.168.56.11",
    "web-02" => "192.168.56.12",
    "db-01"  => "192.168.56.13"
  }

  nodes.each do |name, ip|
    config.vm.define name do |node|
      node.vm.hostname = name
      node.vm.network "private_network", ip: ip
      node.vm.provider "virtualbox" do |vb|
        vb.memory = "512"
        vb.cpus = 1
      end
    end
  end
end
```

```bash
vagrant up
```

---

## Estrutura do Projeto Ansible

```
ansible-lab/
├── ansible.cfg
├── inventory/
│   └── hosts.ini
├── playbook.yml
└── roles/
    ├── common/
    │   └── tasks/main.yml
    ├── hardening/
    │   ├── tasks/main.yml
    │   └── templates/
    │       └── sshd_config.j2
    ├── haproxy/
    │   ├── tasks/main.yml
    │   └── templates/
    │       └── haproxy.cfg.j2
    ├── nginx/
    │   ├── tasks/main.yml
    │   └── templates/
    │       └── nginx.conf.j2
    ├── php/
    │   └── tasks/main.yml
    └── mysql/
        ├── tasks/main.yml
        └── vars/main.yml
```

### ansible.cfg

```ini
[defaults]
inventory         = inventory/hosts.ini
remote_user       = vagrant
private_key_file  = ~/.vagrant.d/insecure_private_key
host_key_checking = False
forks             = 5
log_path          = ansible.log

[privilege_escalation]
become            = True
become_method     = sudo
become_user       = root
become_ask_pass   = False
```

### inventory/hosts.ini

```ini
[loadbalancer]
lb-01 ansible_host=192.168.56.10

[webservers]
web-01 ansible_host=192.168.56.11
web-02 ansible_host=192.168.56.12

[database]
db-01 ansible_host=192.168.56.13

[all:vars]
ansible_python_interpreter=/usr/bin/python3

[webservers:vars]
db_host=192.168.56.13

[loadbalancer:vars]
web_backends=["192.168.56.11", "192.168.56.12"]
```

---

## As Roles

### Role: common

Pacotes base, usuários, sincronização de tempo.

```yaml
# roles/common/tasks/main.yml
---
- name: Atualizar cache do apt
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Instalar pacotes base
  apt:
    name:
      - vim
      - curl
      - wget
      - htop
      - net-tools
      - chrony
    state: present

- name: Garantir chrony rodando
  service:
    name: chrony
    state: started
    enabled: yes
```

### Role: hardening

Esta é a role mais importante do ponto de vista de segurança. Aplica endurecimento de SSH, firewall e fail2ban.

```yaml
# roles/hardening/tasks/main.yml
---
- name: Instalar ferramentas de segurança
  apt:
    name:
      - ufw
      - fail2ban
      - unattended-upgrades
    state: present

- name: Configurar UFW - política padrão
  ufw:
    state: enabled
    policy: deny
    direction: incoming

- name: Permitir SSH
  ufw:
    rule: allow
    port: "22"
    proto: tcp

- name: Configurar SSH hardening
  template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: "0600"
    validate: /usr/sbin/sshd -t -f %s
  notify: Reiniciar SSH

- name: Ativar fail2ban
  service:
    name: fail2ban
    state: started
    enabled: yes

- name: Configurar atualizações automáticas de segurança
  copy:
    dest: /etc/apt/apt.conf.d/50unattended-upgrades
    content: |
      Unattended-Upgrade::Allowed-Origins {
        "${distro_id}:${distro_codename}-security";
      };
      Unattended-Upgrade::Automatic-Reboot "false";
```

```jinja2
{# roles/hardening/templates/sshd_config.j2 #}
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Autenticação
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Segurança
X11Forwarding no
AllowTcpForwarding no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

UsePAM yes
PrintLastLog yes
```

> **Por que isso importa?** Desabilitar `PasswordAuthentication` e `PermitRootLogin` elimina a classe inteira de ataques de brute-force direto ao root. Fail2ban baneia IPs após tentativas repetidas.

### Role: haproxy

```yaml
# roles/haproxy/tasks/main.yml
---
- name: Instalar HAProxy
  apt:
    name: haproxy
    state: present

- name: Permitir porta 80 no firewall
  ufw:
    rule: allow
    port: "80"
    proto: tcp

- name: Configurar HAProxy
  template:
    src: haproxy.cfg.j2
    dest: /etc/haproxy/haproxy.cfg
    validate: haproxy -c -f %s
  notify: Reiniciar HAProxy

- name: Garantir HAProxy rodando
  service:
    name: haproxy
    state: started
    enabled: yes
```

```jinja2
{# roles/haproxy/templates/haproxy.cfg.j2 #}
global
    log /dev/log local0
    chroot /var/lib/haproxy
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

frontend web_frontend
    bind *:80
    default_backend web_backends

backend web_backends
    balance roundrobin
    option httpchk GET /health
    {% for backend in web_backends %}
    server web-{{ loop.index }} {{ backend }}:80 check
    {% endfor %}
```

### Role: nginx + php

```yaml
# roles/nginx/tasks/main.yml
---
- name: Instalar Nginx
  apt:
    name: nginx
    state: present

- name: Permitir porta 80 no firewall (apenas do LB)
  ufw:
    rule: allow
    src: "192.168.56.10"
    port: "80"
    proto: tcp

- name: Criar página de health check
  copy:
    dest: /var/www/html/health
    content: "OK"
    owner: www-data
    group: www-data

- name: Criar página de identificação
  copy:
    dest: /var/www/html/index.html
    content: "<h1>Servidor: {{ inventory_hostname }}</h1>"
    owner: www-data
    group: www-data

- name: Garantir Nginx rodando
  service:
    name: nginx
    state: started
    enabled: yes
```

### Role: mysql

```yaml
# roles/mysql/tasks/main.yml
---
- name: Instalar MySQL
  apt:
    name:
      - mysql-server
      - python3-mysqldb
    state: present

- name: Garantir MySQL rodando
  service:
    name: mysql
    state: started
    enabled: yes

- name: Criar usuário da aplicação
  mysql_user:
    name: "{{ db_user }}"
    password: "{{ db_password }}"
    priv: "{{ db_name }}.*:ALL"
    host: "192.168.56.%"
    state: present

- name: Criar banco de dados
  mysql_db:
    name: "{{ db_name }}"
    state: present

- name: Restringir bind-address ao IP interno
  lineinfile:
    path: /etc/mysql/mysql.conf.d/mysqld.cnf
    regexp: "^bind-address"
    line: "bind-address = 192.168.56.13"
  notify: Reiniciar MySQL

- name: Bloquear acesso externo ao MySQL via UFW
  ufw:
    rule: allow
    src: "192.168.56.0/24"
    port: "3306"
    proto: tcp
```

```yaml
# roles/mysql/vars/main.yml
---
db_name: appdb
db_user: appuser
db_password: "{{ vault_db_password }}"
```

> **Nota**: usar `ansible-vault encrypt_string` para a senha do banco — nunca em texto plano no repositório.

---

## Playbook Principal

```yaml
# playbook.yml
---
- name: Provisionar Load Balancer
  hosts: loadbalancer
  roles:
    - common
    - hardening
    - haproxy

- name: Provisionar Servidores Web
  hosts: webservers
  roles:
    - common
    - hardening
    - nginx
    - php

- name: Provisionar Banco de Dados
  hosts: database
  roles:
    - common
    - hardening
    - mysql
```

---

## Executando o Lab

```bash
# Verificar conectividade
ansible all -m ping

# Dry run (ver o que seria alterado)
ansible-playbook playbook.yml --check --diff

# Executar
ansible-playbook playbook.yml

# Resultado esperado:
# PLAY RECAP
# lb-01  : ok=14  changed=12  unreachable=0  failed=0
# web-01 : ok=17  changed=15  unreachable=0  failed=0
# web-02 : ok=17  changed=15  unreachable=0  failed=0
# db-01  : ok=16  changed=14  unreachable=0  failed=0
```

---

## Testando a Infraestrutura

```bash
# Testar load balancer (deve alternar entre web-01 e web-02)
for i in {1..6}; do curl -s http://192.168.56.10; echo; done
# Servidor: web-01
# Servidor: web-02
# Servidor: web-01
# Servidor: web-02
# ...

# Testar health check
curl http://192.168.56.10/health
# OK

# Verificar fail2ban ativo em todos os nós
ansible all -m shell -a "fail2ban-client status"

# Verificar UFW ativo
ansible all -m shell -a "ufw status verbose"
```

---

## Idempotência em Ação

Rode o playbook novamente — sem alterar nada — e veja o resultado:

```bash
ansible-playbook playbook.yml

# PLAY RECAP
# lb-01  : ok=14  changed=0  unreachable=0  failed=0
# web-01 : ok=17  changed=0  unreachable=0  failed=0
# web-02 : ok=17  changed=0  unreachable=0  failed=0
# db-01  : ok=16  changed=0  unreachable=0  failed=0
```

`changed=0` — isso é idempotência. O Ansible verifica o estado atual antes de alterar. Se já está como deveria, não faz nada.

---

## Bônus: Ad-hoc para Triagem Rápida

```bash
# Ver uso de memória em todos os servidores
ansible all -m shell -a "free -h"

# Reiniciar nginx nos web servers
ansible webservers -m service -a "name=nginx state=restarted"

# Coletar facts para inventário dinâmico
ansible all -m setup -a "filter=ansible_distribution*"

# Checar se portas estão abertas
ansible all -m shell -a "ss -tlnp"
```

---

## Conclusão

Em ~5 minutos e algumas dezenas de linhas de YAML, provisionamos:

- **Load Balancer** com HAProxy em round-robin com health checks
- **2 Web Servers** com Nginx e identificação de host
- **Banco de Dados** MySQL com usuário restrito por IP
- **Hardening** em todos: SSH sem senha, UFW, fail2ban, atualizações automáticas

A infraestrutura é reproduzível, versionável e auditável. Próximo passo natural: integrar esse playbook em um pipeline CI/CD (GitHub Actions ou GitLab CI) e adicionar testes com **Molecule + Testinfra**.

---

**Referências:**
- [Documentação oficial Ansible](https://docs.ansible.com)
- [Ansible Galaxy - roles de segurança](https://galaxy.ansible.com)
- [CIS Benchmarks para Linux](https://www.cisecurity.org/cis-benchmarks)
