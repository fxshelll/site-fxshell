---
title: "Ansible"
date: 2021-03-29T21:56:17-03:00
draft: false
---

![HTB](/Ansible.jpg)

O ansible é uma forma de comunicação superluminica. Ou seja passar uma informação ao mesmo tempo para objetos. 

É uma ferramenta opensource que te possibilita realizar comunicação e interação com diversos destinos ao mesmo tempo, tudo de forma automatizada. 

```sh
- Gerenciamento de mudança
- Provisionamento
- Automação 
- Orquestração
```
## Gerenciamento de Mudança

=> Idempotente 
Executa somente uma vez as alterações, se não houve alteração ele não executa. 

=> Pode também criar rotinas automatizadas por versão, exemplo (php7 em uma maquina client, rodo o ansible que está configurado com o php 7.5, ele vai reverter tudo para o 7.5)

## Provisionamento

=> Configuração
=> Instalação 
=> Preparação
=> Alteração do System State

## Automação

=> Execução de tarefas de forma automática
=> Ordenação de tarefas (tasks)
=> Realizar decisões
=> Ad-hoc tasks

## Orquestração

=> Múltíiplos servidores
=> Muliplas aplicações
=> Diferentes tarefas
=> Ambiente  Hibrido


## Por que o Ansible?

De que forma o Ansible é diferente de outras ferramentas?

É fácil - o Ansible usa uma sintaxe simples (YAML) e é fácil para qualquer pessoa (desenvolvedores, administradores de sistemas, gerentes) entender. APIs são simples e úteis.

Sem agente - Ansible usa ssh para conectar e executar comandos. Você não precisa de nenhum agente / software adicional em execução no seu cliente.

Configuração rápida - como você não precisa instalar agentes ou daemons extras, a configuração é muito simples e rápida.

Seguro - uma vez que usa ssh para comunicação, é muito seguro e protegido. Não requer nenhuma porta extra ou daemons vulneráveis ​​em seus servidores.


## Arquitetura & funcionamento do Ansible

![HTB](/ansible_engine.png)

![HTB](/ansible_engine2.png)

## Como ele funciona?

Desenvolvido em python, versão <3.5 ou Python <2.7

Procura sempre o interpretador em /usr/bin/python
--> Variavel: ansible_python_interpreter

Utiliza-se também do serviço SSH para comunicação com os servidores linux, like ou WinRM para comunicação com servidores M$ Windows. 

-> Usuário + Senha
-> Chave SSH (Para servidores Linux)

Autenticação descentralizada

Pode-se autenticar/conectar-se com LDAP e kerberos. 

## Instalação do Ansible

Por padrão, o Ansible gerencia as máquinas por meio do protocolo SSH. Depois que o Ansible for instalado, ele não adicionará um banco de dados e não haverá daemons para iniciar ou manter em execução. Você só precisa instalá-lo em uma máquina e ele pode gerenciar uma frota inteira de máquinas remotas a partir desse ponto central. Quando o Ansible gerencia máquinas remotas, ele não deixa o software instalado ou em execução nelas, então não há dúvidas reais sobre como atualizar o Ansible ao mudar para uma nova versão.

A única dependência que o Ansible tem para instalação é o Python. O Ansible pode ser instalado diretamente usando o gerenciador de pacotes do sistema operacional com base no sistema operacional que você está executando e via pip, que é o gerenciador de pacotes do Python.

## RHEL / CentOS / Fedora:

Certifique-se de habilitar o repo EPEL antes de executar o comando abaixo para RHEL e CentOS.

```sh
sudo yum install ansible
```

Ubuntu:

```sh
$ 	
$ sudo apt-add-repository ppa:ansible/ansible 
$ sudo apt-get update 
$ sudo apt-get install ansible
```
Instalação Ansible usando pip

(caso não tenha o pip instalado faça:)
```sh
$ sudo apt-get install python3-pip
```

E depois instale o ansible:

```sh
$ sudo pip3 install ansible
```

Se precisar fazer upgrade

```sh
$ sudo pip3 install ansible --upgrade
```

![HTB](/ansible_install.png)

## Configurando o Ansible 

O principal arquivo de configuração do ansible, é o `ansible.cfg`

Sua localização padrão é /etc/ansible/ansible.cfg

Alterações e configurações são interpretadas respeitando a seguinte ordem.:

-> Váriavel ANSIBLE_CONFIG
-> ansible.cfg no diretorio corrente
-> .ansible.cfg diretorio home
-> /etc/ansible/ansible.cfg 


A primeira coisa a se fazer é fazer uma cópia do 'ansible.cfg', que fica dentro do /etc/ansible/

Preservei o original e joguei um arquivo mais resumido com as opções mais utilizadas do ansible.

```sh
[defaults]

#--- General settings
forks                   = 5
log_path                = /var/log/ansible.log
module_name             = command
executable              = /bin/bash
ansible_managed         = Ansible managed

#--- Files/Directory settings
inventory               = /etc/ansible/hosts
library                 = /usr/share/my_modules
remote_tmp              = ~/.ansible/tmp
local_tmp               = ~/.ansible/tmp
roles_path              = /etc/ansible/roles

#--- Users settings
remote_user             = root
sudo_user               = root
ask_pass                = no
ask-sudo_pass           = no

#--- SSH settings
remote_port             = 22
timeout                 = 10
host_key_checking       = False
ssh_executable          = /usr/bin/ssh
private_key_file        = ~/.ssh/id_rsa

[privilege_scalation]

become                  = True
become_method           = sudo
become_user             = root
become_ask_pass         = False

[ssh_connection]

scp_if_ssh              = smart
transfer_method         = smart
retries                 = 3
```
 
## Testando na maquina alvo

```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.151 -u osboxes -k -m ping
[WARNING]: log file at /var/log/ansible.log is not writeable and we cannot create it, aborting

SSH password: 
[DEPRECATION WARNING]: Distribution debian 10.0 on host 192.168.1.151 should 
use /usr/bin/python3, but is using /usr/bin/python for backward compatibility 
with prior Ansible releases. A future Ansible release will default to using the
 discovered platform python for this host. See https://docs.ansible.com/ansible
/2.10/reference_appendices/interpreter_discovery.html for more information. 
This feature will be removed in version 2.12. Deprecation warnings can be 
disabled by setting deprecation_warnings=False in ansible.cfg.
192.168.1.151 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
osboxes@FXSHELL:/etc/ansible$ 
```

```sh
[DEPRECATION WARNING]: Distribution debian 10.0 on host 192.168.1.234 should 
use /usr/bin/python3, but is using /usr/bin/python for backward compatibility 
with prior Ansible releases. A future Ansible release will default to using the
 discovered platform python for this host. See https://docs.ansible.com/ansible
/2.10/reference_appendices/interpreter_discovery.html for more information. 
This feature will be removed in version 2.12. Deprecation warnings can be 
disabled by setting deprecation_warnings=False in ansible.cfg.
192.168.1.234 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "invocation": {
        "module_args": {
            "data": "pong"
        }
    },
    "ping": "pong"
}
META: ran handlers
META: ran handlers
osboxes@FXSHELL:/etc/ansible$ 
```

Podemos também explicitar para ele ignorar a mensagem do python. 

basta adicionar no ansible.cfg a linha

```sh
interpreter_python    = auto_legacy_silent
```

```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.234 -u osboxes -k -m ping
[WARNING]: log file at /var/log/ansible.log is not writeable and we cannot create it, aborting

SSH password: 
192.168.1.234 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
osboxes@FXSHELL:/etc/ansible$ 
```

Existe um modulo bem interessante chamado ansible facts, varrendo todos os targets montando uma especie de inventário deles. 

Para buscar essas informações basta executar o modulo 'setup'

```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.234 -u osboxes -k -m setup
```

Também existe um modulo chamado systemd com o argumento '-a' com "name=ssh state=restarted"

Ficando dessa forma:

```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.151 -u osboxes -k -b -m systemd -a "name=ssh state=restarted"
```
```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.151 -u osboxes -k -b -m systemd -a "name=ssh state=restarted"
[WARNING]: log file at /var/log/ansible.log is not writeable and we cannot create it, aborting

SSH password: 
192.168.1.151 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "name": "ssh",
    "state": "started",
    "status": {
        "ActiveEnterTimestamp": "Wed 2021-04-07 22:52:06 EDT",
        "ActiveEnterTimestampMonotonic": "246017520",
        "ActiveExitTimestampMonotonic": "0",
        "ActiveState": "active",
        "After": "system.slice -.mount network.target auditd.service systemd-journald.socket basic.target sysinit.target",
        "AllowIsolate": "no",
        "AmbientCapabilities": "",
        "AssertResult": "yes",
        "AssertTimestamp": "Wed 2021-04-07 22:52:06 EDT",
        "AssertTimestampMonotonic": "245980232",
        "Before": "multi-user.target shutdown.target",
        "BlockIOAccounting": "no",
        "BlockIOWeight": "[not set]",
        "CPUAccounting": "no",
        "CPUQuotaPerSecUSec": "infinity",
        "CPUSchedulingPolicy": "0",
        "CPUSchedulingPriority": "0",
        "CPUSchedulingResetOnFork": "no",
        "CPUShares": "[not set]",
        "CPUUsageNSec": "[not set]",
        "CPUWeight": "[not set]",
        "CacheDirectoryMode": "0755",
        "CanIsolate": "no",
        "CanReload": "yes",
        "CanStart": "yes",
        "CanStop": "yes",
        "CapabilityBoundingSet": "cap_chown cap_dac_override cap_dac_read_search cap_fowner cap_fsetid cap_kill cap_setgid cap_setuid cap_setpcap cap_linux_immutable cap_net_bind_service cap_net_broadcast cap_net_admin cap_net_raw cap_ipc_lock cap_ipc_owner cap_sys_module cap_sys_rawio cap_sys_chroot cap_sys_ptrace cap_sys_pacct cap_sys_admin cap_sys_boot cap_sys_nice cap_sys_resource cap_sys_time cap_sys_tty_config cap_mknod cap_lease cap_audit_write cap_audit_control cap_setfcap cap_mac_override cap_mac_admin cap_syslog cap_wake_alarm cap_block_suspend",
        "CollectMode": "inactive",
        "ConditionResult": "yes",
        "ConditionTimestamp": "Wed 2021-04-07 22:52:06 EDT",
        "ConditionTimestampMonotonic": "245980220",
        "ConfigurationDirectoryMode": "0755",
        "Conflicts": "shutdown.target",
        "ControlGroup": "/system.slice/ssh.service",
        "ControlPID": "0",
        "DefaultDependencies": "yes",
        "Delegate": "no",
        "Description": "OpenBSD Secure Shell server",
        "DevicePolicy": "auto",
        "Documentation": "man:sshd(8) man:sshd_config(5)",
        "DynamicUser": "no",
        "EnvironmentFiles": "/etc/default/ssh (ignore_errors=yes)",
        "ExecMainCode": "0",
        "ExecMainExitTimestampMonotonic": "0",
        "ExecMainPID": "2270",
        "ExecMainStartTimestamp": "Wed 2021-04-07 22:52:06 EDT",
        "ExecMainStartTimestampMonotonic": "246010909",
        "ExecMainStatus": "0",
        "ExecReload": "{ path=/bin/kill ; argv[]=/bin/kill -HUP $MAINPID ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }",
        "ExecStart": "{ path=/usr/sbin/sshd ; argv[]=/usr/sbin/sshd -D $SSHD_OPTS ; ignore_errors=no ; start_time=[Wed 2021-04-07 22:52:06 EDT] ; stop_time=[n/a] ; pid=2270 ; code=(null) ; status=0/0 }",
        "ExecStartPre": "{ path=/usr/sbin/sshd ; argv[]=/usr/sbin/sshd -t ; ignore_errors=no ; start_time=[Wed 2021-04-07 22:52:06 EDT] ; stop_time=[Wed 2021-04-07 22:52:06 EDT] ; pid=2269 ; code=exited ; status=0 }",
        "FailureAction": "none",
        "FailureActionExitStatus": "-1",
        "FileDescriptorStoreMax": "0",
        "FinalKillSignal": "9",
        "FragmentPath": "/lib/systemd/system/ssh.service",
        "GID": "[not set]",
        "GuessMainPID": "yes",
        "IOAccounting": "no",
        "IOSchedulingClass": "0",
        "IOSchedulingPriority": "0",
        "IOWeight": "[not set]",
        "IPAccounting": "no",
        "IPEgressBytes": "18446744073709551615",
        "IPEgressPackets": "18446744073709551615",
        "IPIngressBytes": "18446744073709551615",
        "IPIngressPackets": "18446744073709551615",
        "Id": "ssh.service",
        "IgnoreOnIsolate": "no",
        "IgnoreSIGPIPE": "yes",
        "InactiveEnterTimestamp": "Wed 2021-04-07 22:48:07 EDT",
        "InactiveEnterTimestampMonotonic": "5387216",
        "InactiveExitTimestamp": "Wed 2021-04-07 22:52:06 EDT",
        "InactiveExitTimestampMonotonic": "245983310",
        "InvocationID": "6561c69561a14f76842d4a1ce3592f4a",
        "JobRunningTimeoutUSec": "infinity",
        "JobTimeoutAction": "none",
        "JobTimeoutUSec": "infinity",
        "KeyringMode": "private",
        "KillMode": "process",
        "KillSignal": "15",
        "LimitAS": "infinity",
        "LimitASSoft": "infinity",
        "LimitCORE": "infinity",
        "LimitCORESoft": "0",
        "LimitCPU": "infinity",
        "LimitCPUSoft": "infinity",
        "LimitDATA": "infinity",
        "LimitDATASoft": "infinity",
        "LimitFSIZE": "infinity",
        "LimitFSIZESoft": "infinity",
        "LimitLOCKS": "infinity",
        "LimitLOCKSSoft": "infinity",
        "LimitMEMLOCK": "65536",
        "LimitMEMLOCKSoft": "65536",
        "LimitMSGQUEUE": "819200",
        "LimitMSGQUEUESoft": "819200",
        "LimitNICE": "0",
        "LimitNICESoft": "0",
        "LimitNOFILE": "524288",
        "LimitNOFILESoft": "1024",
        "LimitNPROC": "3795",
        "LimitNPROCSoft": "3795",
        "LimitRSS": "infinity",
        "LimitRSSSoft": "infinity",
        "LimitRTPRIO": "0",
        "LimitRTPRIOSoft": "0",
        "LimitRTTIME": "infinity",
        "LimitRTTIMESoft": "infinity",
        "LimitSIGPENDING": "3795",
        "LimitSIGPENDINGSoft": "3795",
        "LimitSTACK": "infinity",
        "LimitSTACKSoft": "8388608",
        "LoadState": "loaded",
        "LockPersonality": "no",
        "LogLevelMax": "-1",
        "LogRateLimitBurst": "0",
        "LogRateLimitIntervalUSec": "0",
        "LogsDirectoryMode": "0755",
        "MainPID": "2270",
        "MemoryAccounting": "yes",
        "MemoryCurrent": "5312512",
        "MemoryDenyWriteExecute": "no",
        "MemoryHigh": "infinity",
        "MemoryLimit": "infinity",
        "MemoryLow": "0",
        "MemoryMax": "infinity",
        "MemoryMin": "0",
        "MemorySwapMax": "infinity",
        "MountAPIVFS": "no",
        "MountFlags": "",
        "NFileDescriptorStore": "0",
        "NRestarts": "0",
        "Names": "ssh.service",
        "NeedDaemonReload": "no",
        "Nice": "0",
        "NoNewPrivileges": "no",
        "NonBlocking": "no",
        "NotifyAccess": "main",
        "OOMScoreAdjust": "0",
        "OnFailureJobMode": "replace",
        "Perpetual": "no",
        "PrivateDevices": "no",
        "PrivateMounts": "no",
        "PrivateNetwork": "no",
        "PrivateTmp": "no",
        "PrivateUsers": "no",
        "ProtectControlGroups": "no",
        "ProtectHome": "no",
        "ProtectKernelModules": "no",
        "ProtectKernelTunables": "no",
        "ProtectSystem": "no",
        "RefuseManualStart": "no",
        "RefuseManualStop": "no",
        "RemainAfterExit": "no",
        "RemoveIPC": "no",
        "Requires": "sysinit.target -.mount system.slice",
        "RequiresMountsFor": "/run/sshd",
        "Restart": "on-failure",
        "RestartUSec": "100ms",
        "RestrictNamespaces": "no",
        "RestrictRealtime": "no",
        "Result": "success",
        "RootDirectoryStartOnly": "no",
        "RuntimeDirectory": "sshd",
        "RuntimeDirectoryMode": "0755",
        "RuntimeDirectoryPreserve": "no",
        "RuntimeMaxUSec": "infinity",
        "SameProcessGroup": "no",
        "SecureBits": "0",
        "SendSIGHUP": "no",
        "SendSIGKILL": "yes",
        "Slice": "system.slice",
        "StandardError": "inherit",
        "StandardInput": "null",
        "StandardInputData": "",
        "StandardOutput": "journal",
        "StartLimitAction": "none",
        "StartLimitBurst": "5",
        "StartLimitIntervalUSec": "10s",
        "StartupBlockIOWeight": "[not set]",
        "StartupCPUShares": "[not set]",
        "StartupCPUWeight": "[not set]",
        "StartupIOWeight": "[not set]",
        "StateChangeTimestamp": "Wed 2021-04-07 22:52:06 EDT",
        "StateChangeTimestampMonotonic": "246017520",
        "StateDirectoryMode": "0755",
        "StatusErrno": "0",
        "StopWhenUnneeded": "no",
        "SubState": "running",
        "SuccessAction": "none",
        "SuccessActionExitStatus": "-1",
        "SyslogFacility": "3",
        "SyslogLevel": "6",
        "SyslogLevelPrefix": "yes",
        "SyslogPriority": "30",
        "SystemCallErrorNumber": "0",
        "TTYReset": "no",
        "TTYVHangup": "no",
        "TTYVTDisallocate": "no",
        "TasksAccounting": "yes",
        "TasksCurrent": "1",
        "TasksMax": "1138",
        "TimeoutStartUSec": "1min 30s",
        "TimeoutStopUSec": "1min 30s",
        "TimerSlackNSec": "50000",
        "Transient": "no",
        "Type": "notify",
        "UID": "[not set]",
        "UMask": "0022",
        "UnitFilePreset": "enabled",
        "UnitFileState": "enabled",
        "UtmpMode": "init",
        "WantedBy": "multi-user.target",
        "WatchdogSignal": "6",
        "WatchdogTimestampMonotonic": "0",
        "WatchdogUSec": "0"
    }
}
```

Um modulo muito legal também é o modulo 'shell' que posso executar qualquer comando dentro do meu alvo.

```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.151 -u osboxes -k -b -m shell -a "systemctl status ssh"
[WARNING]: log file at /var/log/ansible.log is not writeable and we cannot create it, aborting

SSH password: 
192.168.1.151 | CHANGED | rc=0 >>
● ssh.service - OpenBSD Secure Shell server
   Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2021-04-07 23:22:56 EDT; 6min ago
     Docs: man:sshd(8)
           man:sshd_config(5)
  Process: 2437 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
 Main PID: 2438 (sshd)
    Tasks: 1 (limit: 1138)
   Memory: 2.4M
   CGroup: /system.slice/ssh.service
           └─2438 /usr/sbin/sshd -D

Apr 07 23:22:56 node2 systemd[1]: Starting OpenBSD Secure Shell server...
Apr 07 23:22:56 node2 sshd[2438]: Server listening on 0.0.0.0 port 22.
Apr 07 23:22:56 node2 sshd[2438]: Server listening on :: port 22.
Apr 07 23:22:56 node2 systemd[1]: Started OpenBSD Secure Shell server.
Apr 07 23:26:56 node2 sshd[2446]: Accepted password for osboxes from 192.168.1.168 port 52234 ssh2
Apr 07 23:26:56 node2 sshd[2446]: pam_unix(sshd:session): session opened for user osboxes by (uid=0)
Apr 07 23:29:11 node2 sshd[2478]: Accepted password for osboxes from 192.168.1.168 port 52236 ssh2
Apr 07 23:29:11 node2 sshd[2478]: pam_unix(sshd:session): session opened for user osboxes by (uid=0)
```

Se eu não tivesse um usuário comum com poderes de elevação de privilégio eu posso usar a flag '-K' maiusculo para solicitar a senha de super usuário para elevação. (isso caso meu usuário comum não tivesse permissões)

```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.151 -u osboxes -k -K -m shell -a "systemctl status ssh"
[WARNING]: log file at /var/log/ansible.log is not writeable and we cannot create it, aborting

SSH password: 
BECOME password[defaults to SSH password]: 
192.168.1.151 | CHANGED | rc=0 >>
● ssh.service - OpenBSD Secure Shell server
   Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2021-04-07 23:22:56 EDT; 8min ago
     Docs: man:sshd(8)
           man:sshd_config(5)
  Process: 2437 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
 Main PID: 2438 (sshd)
    Tasks: 1 (limit: 1138)
   Memory: 2.4M
   CGroup: /system.slice/ssh.service
           └─2438 /usr/sbin/sshd -D

```
Uma outra opção seria também não especificar nenhum modulo, ele vai pegar o modulo command por padrão.

exemplo:

```sh
osboxes@FXSHELL:/etc/ansible$ ansible 192.168.1.151 -u osboxes -k -a "pwd"

SSH password: 
192.168.1.151 | CHANGED | rc=0 >>
/home/osboxes

```

=> flag -u, determino usuário

=> flag -k, senha

=> flag -i, inventário que será utilizado

=> flag -K, solicita a elevação de privilégio

=> flag -b, executar elevação de privilégio (especificar no ansible.cfg)

=> flag -m, modulo que será utilizado

=> flag -a, argumento do modulo

para obter ajuda pode fazer também o --help = ajuda. 

Posso também dar um comando 'all' se meus targets estiverem dentro do arquivo hosts. 

```sh
root@FXSHELL /e/ansible# cat hosts
192.168.1.151
192.168.1.234
```


```sh
root@FXSHELL /e/ansible# ansible all -m ping -u osboxes -k
SSH password: 
192.168.1.151 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
192.168.1.234 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

Imagine que eu preciso executar isso em muitos hosts, para facilitar isso existe uma forma de trabalhar com grupos, dentro do arquivo de hosts. 

Exemplo, no arquivo hosts:

```sh
[servidores_bd]
192.168.1.151

[servidores_web]
192.168.1.234
```
```sh
ansible -i hosts servidores_bd -m ping -u osboxes -k
```

Também posso colocar um subgrupo, exemplo:

```sh
[servidores:children]
servidores_web
servidores_bd
```

Ele visualizara todos os subgrupos dele e executará os comandos. 

Também posso utilizar variáveis para ajudar na identificação dos hosts, como por exemplo. 

Posso setar a variavél 

```sh
mysql ansible_ssh_host=192.168.1.234
```

Posso aplicar regras também para grupos de servidores como por exemplo:

```sh
[servidores_bd:vars]
ansible_ssh+port=22
ansible_ssh_user=osboxes
ansible_ssh_pass=osboxes.org 
ansible_become=yes
ansible_become_method=sudo
ansible_become_user=osboxes
ansible_become_pass=osboxes
ansible_connection=ssh
```
Com isso basta eu executar só o comando com o modulo 'ping'.

```sh
root@FXSHELL /e/ansible# ansible -i hosts servidores_web -m ping
192.168.1.234 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

## Oque são Roles

As roles (funções) são um conjunto de intes independentes destinados a provisionar uma determinada aplicação/infraestrutura.

Itens:

=> Variaveis

=> Modulos

=> Modelos

=> Tarefas

=> Ações

Pode-se associar-se roles com projetos. 

As roles possuem uma estrutura padrão de diretórios para seus projetos:

```yml
playbook.yml
roles/
	common/
		tasks/
		handlers/
		files/
		templates/
		vars/
		defaults/
		meta/
```

Tasks => lista de tarefas para serem executadas em uma role. 

handlers => são manipuladores/eventos acionados por uma task.

files => arquivos utilizados para deploy dentro de uma role.

templates => modelos para deploy dentro de uma role (permite o uso de variáveis)

vars => variáveis adicionais de uma role.

defaults => variáveis padrão de uma role. Prioridade máxima. 

meta => traga dependências de uma role para outra role - primeiro diretório a ser analisado.

nota: dentro dos diretorios taks, handlers, vars, defaults e meta, deverá existir um arquivo com o nome de main.yml para que o mesmo seja interpretado. 




