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


