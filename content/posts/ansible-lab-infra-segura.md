---
title: "Ansible Lab: Provisionando Infraestrutura Web Segura do Zero"
date: 2026-04-21T10:00:00-03:00
draft: false
tags: ["devops", "ansible", "segurança", "linux", "infraestrutura", "nginx", "mysql", "haproxy"]
---

**Cenário**: você tem 4 VMs vazias e precisa subir uma stack web completa — load balancer, dois servidores de aplicação, banco de dados, tudo com segurança configurada desde o início — em menos de 5 minutos. Só com Ansible.

Este post documenta um lab que montei para praticar exatamente isso: infraestrutura como código, do zero até uma stack funcional e segura, reproduzível com um único comando.

---

## Objetivo do Lab

O objetivo é simular, localmente, um ambiente que existe de verdade em qualquer empresa que tenha um sistema web em produção. Em vez de provisionar um servidor por vez — conectando via SSH, instalando pacotes na mão e torcendo para não esquecer nada — o lab demonstra como automatizar todo esse processo com Ansible.

Na prática, esse tipo de automação é usado para:

- Subir novos ambientes (staging, produção, DR) de forma idêntica e rápida
- Garantir que todos os servidores estejam sempre na configuração correta, sem desvios
- Integrar o provisionamento em pipelines de CI/CD, onde um ambiente novo é criado automaticamente a cada release
- Padronizar configurações de segurança em toda a frota de servidores

---

## Tecnologias Utilizadas

Antes de entrar no código, vale entender o papel de cada ferramenta.

**Ansible** é uma ferramenta de automação de infraestrutura. Você descreve o estado desejado dos seus servidores em arquivos YAML (os chamados playbooks e roles), e o Ansible se conecta via SSH e aplica essas configurações. Sem agente instalado nos servidores, sem banco de dados, sem daemon rodando — é simples por design.

**Vagrant** é uma ferramenta para criar e gerenciar máquinas virtuais de forma automatizada. Com um único arquivo de configuração (o `Vagrantfile`), você define quantas VMs quer, qual sistema operacional, qual IP de rede, quanta memória — e o Vagrant cria tudo isso para você. É amplamente usado para criar ambientes de desenvolvimento e laboratório locais, sem precisar pagar por cloud ou configurar VMs manualmente pelo VirtualBox.

**VirtualBox** é o software de virtualização que o Vagrant usa por baixo dos panos neste lab. É ele quem de fato cria e executa as máquinas virtuais. O Vagrant é a camada de abstração que automatiza a criação delas.

**HAProxy** é um load balancer de alto desempenho. Ele recebe as requisições dos usuários e as distribui entre os servidores de aplicação disponíveis. Se um servidor cair, o HAProxy para de mandar tráfego para ele automaticamente. É usado em praticamente toda arquitetura web que precisa de escalabilidade e alta disponibilidade.

**Nginx** é um servidor web e proxy reverso. Neste lab ele serve a aplicação nos dois web servers. No mercado é comum encontrá-lo tanto como servidor de aplicação quanto como proxy na frente de outros serviços.

**PHP-FPM** é o gerenciador de processos PHP. É ele que executa o código da aplicação e responde às requisições que chegam pelo Nginx.

**MySQL** é o banco de dados relacional da stack. Armazena os dados da aplicação.

**UFW (Uncomplicated Firewall)** é a interface de gerenciamento do firewall do Linux. Com ele definimos quais portas e IPs têm permissão de se comunicar com cada servidor. No lab, por exemplo, o MySQL só aceita conexões da rede interna — não há como acessá-lo de fora.

**fail2ban** monitora os logs do sistema e bane automaticamente IPs que apresentam comportamento suspeito — como várias tentativas de login SSH com falha em sequência. É uma camada de defesa simples e muito efetiva contra ataques de força bruta.

---

## Arquitetura

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

| Servidor | Roles aplicadas |
|----------|-----------------|
| lb-01    | common, hardening, haproxy |
| web-01   | common, hardening, nginx, php |
| web-02   | common, hardening, nginx, php |
| db-01    | common, hardening, mysql |

Cada servidor recebe a role `common` (configurações base) e a role `hardening` (segurança), além das roles específicas do seu papel na stack.

<iframe src="/ansible-lab-diagram.html"
        width="100%"
        height="580"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

---

## Preparando o Ambiente com Vagrant

O Vagrant cria as 4 VMs localmente com um único `vagrant up`. Cada máquina recebe um IP fixo na rede privada `192.168.56.0/24`, o que permite que o Ansible se comunique com todas elas sem nenhuma configuração extra de rede.

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

Quando as VMs estiverem rodando, o Ansible assume o controle.

---

## Estrutura do Projeto

O projeto segue a estrutura padrão de roles do Ansible. Cada role é um diretório independente com suas tasks, templates e variáveis. Essa separação facilita reutilizar as roles em outros projetos — a role de `hardening`, por exemplo, pode ser aplicada em qualquer servidor sem nenhuma modificação.

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
    │   └── tasks/main.yml
    ├── php/
    │   └── tasks/main.yml
    └── mysql/
        ├── tasks/main.yml
        └── vars/main.yml
```

### ansible.cfg

O arquivo de configuração do Ansible define o comportamento padrão da ferramenta: onde está o inventário, qual usuário usar para se conectar, se deve escalar privilégios automaticamente, entre outros. Isso evita ter que repetir essas opções em todo comando que você rodar.

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

O inventário é onde você diz ao Ansible quais servidores existem e como agrupá-los. Grupos permitem aplicar roles e variáveis diferentes para cada tipo de servidor — tudo o que estiver em `[webservers]` recebe as configurações de web server, tudo em `[database]` recebe as de banco de dados, e assim por diante.

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

### common

Responsável pelas configurações base que todo servidor precisa ter: pacotes essenciais e sincronização de hora via `chrony`. Simples, mas garante uma base consistente em todas as máquinas — sem isso, você pode ter servidores com versões diferentes de ferramentas ou relógios dessincronizados, o que causa problemas sutis difíceis de depurar.

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

### hardening

Esta é a role mais importante do ponto de vista de segurança. Ela configura o firewall, restringe o acesso SSH e ativa o bloqueio automático de IPs suspeitos — aplicado em todos os servidores, sem exceção.

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

- name: Configurar UFW - política padrão deny
  ufw:
    state: enabled
    policy: deny
    direction: incoming

- name: Permitir SSH
  ufw:
    rule: allow
    port: "22"
    proto: tcp

- name: Aplicar configurações de segurança no SSH
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

O template do SSH — arquivos `.j2` são templates Jinja2, que permitem usar variáveis e lógica dentro de arquivos de configuração — desabilita login por senha e acesso direto como root, dois dos vetores de ataque mais comuns em servidores expostos na internet.

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

# Restrições
X11Forwarding no
AllowTcpForwarding no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

UsePAM yes
PrintLastLog yes
```

Com `PasswordAuthentication no`, ataques de força bruta por senha simplesmente não funcionam — o servidor nem aceita esse tipo de autenticação. O `fail2ban` complementa banindo automaticamente IPs que insistem em tentar.

### haproxy

O load balancer distribui o tráfego entre os dois web servers em round-robin — cada requisição vai alternadamente para `web-01` e `web-02` — e verifica a saúde de cada servidor antes de repassar requisições. Se um web server cair, o HAProxy detecta pelo health check e para de mandar tráfego para ele até que volte.

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

Note o `validate` na task de configuração: o Ansible só aplica o arquivo se o HAProxy confirmar que a sintaxe está correta. Isso evita derrubar o serviço por conta de um erro de configuração.

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

### nginx + php

Os web servers aceitam conexões apenas do load balancer — qualquer acesso direto pela porta 80 de outro IP é bloqueado pelo UFW. Isso garante que todo tráfego passe obrigatoriamente pelo HAProxy, sem atalhos.

```yaml
# roles/nginx/tasks/main.yml
---
- name: Instalar Nginx
  apt:
    name: nginx
    state: present

- name: Permitir porta 80 apenas do load balancer
  ufw:
    rule: allow
    src: "192.168.56.10"
    port: "80"
    proto: tcp

- name: Criar endpoint de health check
  copy:
    dest: /var/www/html/health
    content: "OK"
    owner: www-data
    group: www-data

- name: Criar página de identificação do servidor
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

### mysql

O MySQL é configurado para escutar apenas no IP interno e aceitar conexões somente da sub-rede `192.168.56.0/24`. Usuário de aplicação criado com privilégios mínimos — sem acesso root, sem acesso de fora da rede interna.

```yaml
# roles/mysql/tasks/main.yml
---
- name: Instalar MySQL e dependências Python
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

- name: Criar banco de dados da aplicação
  mysql_db:
    name: "{{ db_name }}"
    state: present

- name: Criar usuário com acesso restrito por IP
  mysql_user:
    name: "{{ db_user }}"
    password: "{{ db_password }}"
    priv: "{{ db_name }}.*:ALL"
    host: "192.168.56.%"
    state: present

- name: Restringir MySQL ao IP interno
  lineinfile:
    path: /etc/mysql/mysql.conf.d/mysqld.cnf
    regexp: "^bind-address"
    line: "bind-address = 192.168.56.13"
  notify: Reiniciar MySQL

- name: Liberar acesso ao MySQL apenas da rede interna
  ufw:
    rule: allow
    src: "192.168.56.0/24"
    port: "3306"
    proto: tcp
```

A senha do banco nunca deve ir em texto plano no repositório. O `ansible-vault` criptografa valores sensíveis dentro dos arquivos YAML — você commita o arquivo normalmente, mas só quem tem a chave consegue descriptografar.

```bash
ansible-vault encrypt_string 'SuaSenha' --name 'vault_db_password'
```

```yaml
# roles/mysql/vars/main.yml
---
db_name: appdb
db_user: appuser
db_password: "{{ vault_db_password }}"
```

---

## Playbook Principal

O playbook é o arquivo que orquestra tudo — ele define qual conjunto de roles é aplicado em qual grupo de servidores, e em qual ordem. É o ponto de entrada da automação.

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

## Executando

Antes de rodar de verdade, vale sempre fazer um dry-run com `--check --diff` para visualizar exatamente o que seria alterado em cada servidor, sem modificar nada:

```bash
# Verificar conectividade com todos os nós
ansible all -m ping

# Dry run — simula a execução sem alterar nada
ansible-playbook playbook.yml --check --diff

# Execução real
ansible-playbook playbook.yml
```

Resultado esperado:

```
PLAY RECAP
lb-01  : ok=14  changed=12  unreachable=0  failed=0
web-01 : ok=17  changed=15  unreachable=0  failed=0
web-02 : ok=17  changed=15  unreachable=0  failed=0
db-01  : ok=16  changed=14  unreachable=0  failed=0
```

---

## Verificando a Stack

```bash
# O load balancer deve alternar entre web-01 e web-02
for i in {1..6}; do curl -s http://192.168.56.10; echo; done
# Servidor: web-01
# Servidor: web-02
# Servidor: web-01
# Servidor: web-02
# ...

# Health check do HAProxy
curl http://192.168.56.10/health
# OK

# Confirmar fail2ban ativo em todos os servidores
ansible all -m shell -a "fail2ban-client status"

# Confirmar firewall ativo
ansible all -m shell -a "ufw status verbose"
```

---

## Idempotência

Um conceito central no Ansible — e na automação de infraestrutura em geral — é a **idempotência**: a capacidade de executar a mesma operação várias vezes e sempre chegar ao mesmo resultado, sem efeitos colaterais.

Rode o playbook novamente sem ter alterado nada:

```bash
ansible-playbook playbook.yml

PLAY RECAP
lb-01  : ok=14  changed=0  unreachable=0  failed=0
web-01 : ok=17  changed=0  unreachable=0  failed=0
web-02 : ok=17  changed=0  unreachable=0  failed=0
db-01  : ok=16  changed=0  unreachable=0  failed=0
```

`changed=0` em todos os servidores. Antes de executar qualquer task, o Ansible verifica se o recurso já está no estado desejado. Se o pacote já está instalado, não instala de novo. Se o arquivo de configuração já está correto, não sobrescreve. Isso significa que você pode rodar o mesmo playbook quantas vezes quiser — em manutenção, em auditoria, em CI/CD — sem risco de quebrar o ambiente.

---

## Comandos Ad-hoc para o Dia a Dia

Nem tudo precisa de um playbook. Para tarefas pontuais, o Ansible permite rodar comandos diretamente em um grupo de servidores sem precisar criar um arquivo YAML:

```bash
# Ver uso de memória em todos os servidores
ansible all -m shell -a "free -h"

# Reiniciar nginx nos web servers
ansible webservers -m service -a "name=nginx state=restarted"

# Coletar informações do sistema (distribuição, versão, etc.)
ansible all -m setup -a "filter=ansible_distribution*"

# Verificar quais portas estão abertas
ansible all -m shell -a "ss -tlnp"
```

---

## Para Que Isso Serve no Mercado

Este lab reproduz, em escala reduzida, um padrão que existe em praticamente qualquer empresa com infraestrutura web:

**Times de DevOps/SRE** usam automação como essa para garantir que todos os ambientes — desenvolvimento, homologação, produção — sejam idênticos. Um bug que aparece só em produção muitas vezes é causado por diferença de configuração entre ambientes. Com IaC, isso deixa de ser um problema.

**Onboarding de novos servidores** vira um processo de minutos. Quando um servidor novo entra na frota, o Ansible aplica toda a configuração padrão automaticamente — sem checklist manual, sem risco de esquecer um passo.

**Auditorias de segurança** ficam muito mais simples. Em vez de acessar cada servidor para verificar se as configurações de segurança estão corretas, você roda o playbook e o resultado mostra exatamente o que está diferente do esperado.

**Resposta a incidentes** ganha velocidade. Se um servidor fica comprometido e precisa ser reconstruído do zero, o processo inteiro leva minutos — não horas ou dias tentando lembrar como aquele servidor foi configurado originalmente.

---

## Conclusão

Em menos de 5 minutos e algumas dezenas de linhas de YAML, a stack está de pé:

- **Load Balancer** com HAProxy, round-robin e health check automático
- **2 Web Servers** com Nginx respondendo e identificando o host
- **Banco de dados** MySQL com acesso restrito à rede interna
- **Segurança** aplicada em todos: SSH por chave, firewall ativo, bloqueio de força bruta e atualizações automáticas

O ponto mais importante desse tipo de lab não é a tecnologia em si — é o fato de que a infraestrutura vira código. Ela fica versionada, documentada, reproduzível em qualquer ambiente e auditável linha a linha.

O próximo passo natural é integrar esse playbook em um pipeline CI/CD (GitHub Actions ou GitLab CI) e adicionar testes de infraestrutura com **Molecule + Testinfra**.

---

**Referências:**
- [Documentação oficial do Ansible](https://docs.ansible.com)
- [Ansible Galaxy](https://galaxy.ansible.com)
- [CIS Benchmarks para Linux](https://www.cisecurity.org/cis-benchmarks)
