---
title: "Docker"
date: 2020-10-08T11:10:44-03:00
draft: true
---


Quando falamos de container, estamos falando de 
isolamento. Esse container está sendo executado 
dentro de um servidor, este fica completamente 
isolado da maquina. E dentro deste cercado eu 
tenho processos locais do container. Claro consigo 
ver os processos do meu host local, o servidor 
fisico que está rodando este container.

Duas formas de isolamento, lógica e física. 

Lógica (namespaces): redes, usuários, processos
Física (Cgroups): CPU, memoria, disco.


#O que é o Docker?

Todos as imagens em camadas são read-only exceto a primeira camada ou seja a ultima é alterada. Se eu tenho 5 Containers de 500mb rodando, não será 5GB de espaço alocado no disco do servidor. Continuará sendo 500MB, pois ele usa a mesma imagem em todas as camadas. 

O módulo do kernel Linux é o responsável por criar rotas, redirects e boa parte da tarefa de roteamento de pacotes para o Docker é o `Netfilter`

O módulo do kernel Linux é o responsável pelo isolamento de recursos como CPU e memória é o `Cgroups`

O módulo do kernel Linux é o responsável pelo isolamento de processos, é o `namespaces`

# Instalando o Docker 

Comandos Utilizados:

# curl -fsSL https://get.docker.com/ | bash
# docker version
# docker container ls

a versão paga do Docker é a versão Docker EE (enterprise)

Mas vamos utilizar a versão CE, versão gratuita.

```sh
osboxes@osboxes:~$ docker version
Client: Docker Engine - Community
 Version:           19.03.13
 API version:       1.40
 Go version:        go1.13.15
 Git commit:        4484c46d9d
 Built:             Wed Sep 16 17:02:52 2020
 OS/Arch:           linux/amd64
 Experimental:      false
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.40/version: dial unix /var/run/docker.sock: connect: permission denied

```

A primeira coisa a se fazer é o famoso hello-word

Algo como:

#$ docker container run hello-world

```sh
root@osboxes:~# docker container run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

```

Para visualizar todos os containers que estão em execução, parados ou mortos, eu utilizo o comando:

#$ docker container ls -a

```sh
root@osboxes:~# docker container ls -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
fc4253022db8        hello-world         "/hello"            36 seconds ago      Exited (0) 34 seconds ago                       reverent_neumann
106fbfd9aba4        hello-world         "/hello"            8 minutes ago       Exited (0) 8 minutes ago                        hungry_kapitsa

```

Outra coisa interessante é usar o comando `-ti` para cair dentro do container que acabou de subir, ou seja eu quero um terminal com interatividade, no caso seria algo como: 

```sh
root@osboxes:~# docker container run -ti ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
d72e567cc804: Pull complete 
0f3630e5ff08: Pull complete 
b6a83d81d1f4: Pull complete 
Digest: sha256:bc2f7250f69267c9c6b66d7b6a81a54d3878bb85f1ebb5f951c896d13e6ba537
Status: Downloaded newer image for ubuntu:latest
root@2fd8c26be92e:/# 
```

Perceba que já está dentro do ubuntu que subiu, vamos ver os processos dele agora:

```sh
root@2fd8c26be92e:/# ps -ef
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 17:15 pts/0    00:00:00 /bin/bash
root           8       1  0 17:17 pts/0    00:00:00 ps -ef
```

Se eu der um CTRL+D eu saiu do container criado e ele morre. 

Todo container tem um entrypoint, neste caso é o próprio bash, então quando saimos dele, ele é finalizado também. 

```sh
root@osboxes:~# docker container run -ti centos
Unable to find image 'centos:latest' locally
latest: Pulling from library/centos
3c72a8ed6814: Pull complete 
Digest: sha256:76d24f3ba3317fa945743bb3746fbaf3a0b752f10b10376960de01da70685fbd
Status: Downloaded newer image for centos:latest
[root@ca53ed399c0d /]# 
```

Agora subi um CentOS, e já estou dentro dele. 

```sh
[root@ca53ed399c0d /]# cat /etc/redhat-release 
CentOS Linux release 8.2.2004 (Core) 
```

Se eu quero sair do container mas sem matar o container, eu digito `ctrl+p+q` quando eu volto para o meu host, posso visualizar que ela ainda está rodando.

```sh
root@osboxes:~# docker container ls 
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
ca53ed399c0d        centos              "/bin/bash"         2 minutes ago       Up 2 minutes                            pensive_turing
root@osboxes:~# 
```

Como faço para voltar, agora utilizo o comando `docker container attach + [CONTAINER ID]`


#$docker container attach ca53ed399c0d

```sh
root@osboxes:~# docker container attach ca53ed399c0d
[root@ca53ed399c0d /]# cat /etc/redhat-release 
CentOS Linux release 8.2.2004 (Core) 
```

Agora se eu subir um container do nginx por exemplo, nunca use a flag `-ti` vai parecer que está travado, acontece que você pediu para ele criar o container do nginx com interatividade, mas acontece que ele vai tentar abrir uma console, só que o entrypoint do `nginx` não é o bash, é o próprio processo. 

Todo processo tem que estar em execução em primeiro plano, em foreign ground.

Mesmo se você attachar o nginx para tentar acessa-lo ficara parecendo que esta travando, novamente, o nginx está rodando em primeiro plano, se você entrar nele e sair, vai matar o container dele. 
























