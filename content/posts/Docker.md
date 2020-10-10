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

#Executando e administrando containers Docker 

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

Ou seja neste caso não pode estar rodando como daemon. 

Neste caso não vou utilizar ele com o `-ti` mas sim como `-d`, para rodar como daemon e não com interatividade. 

# $ docker container run nginx

Primeiro eu rodo o `run` sem a flag `-d` para ele baixar o container pra mim localmente. Ai então rodo com a flag para ele deixar o processo do nginx como daemon. 

# $ docker container run -d nginx

```sh
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
fecca31902c0        nginx               "/docker-entrypoint.…"   About a minute ago   Up About a minute   80/tcp              affectionate_dijkstra
ca53ed399c0d        centos              "/bin/bash"              34 hours ago         Up 34 hours                             pensive_turing

```

Agora tenho o CentOS e o Nginx rodando. 

Para que eu possa acessar esse container do nginx, visto que o entrypoint dele é o próprio processo, eu executo o comando `exec`


O comando `exec` me permite rodar comandos no container e me trás os resultados em tela, neste caso posso executar comandos como "ls, cat" normalmente. 


```sh
root@osboxes:~# docker container exec -ti fecca31902c0 ls
bin   dev		   docker-entrypoint.sh  home  lib64  mnt  proc  run   srv  tmp  var
boot  docker-entrypoint.d  etc			 lib   media  opt  root  sbin  sys  usr

```
Para ficar melhor, posso executar o bash diretamente. 

```sh
root@osboxes:~# docker container exec -ti fecca31902c0 bash
root@fecca31902c0:/# cat /etc/issue
Debian GNU/Linux 10 \n \l
```

Posso ver até mesmo que o nginx está configurado com a página de boas vindas certinho. 

```sh
root@fecca31902c0:/usr/share/nginx# curl localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Se eu der um CTRL+D para sair do container, ele não vai matar o container por que o processo principal não era o bash, mas sim o daemon que rodei lá atrás. 

```sh
root@fecca31902c0:/usr/share/nginx# exit
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
fecca31902c0        nginx               "/docker-entrypoint.…"   21 minutes ago      Up 21 minutes       80/tcp              affectionate_dijkstra
ca53ed399c0d        centos              "/bin/bash"              34 hours ago        Up 34 hours                             pensive_turing
```

Rodar como daemon é não rodar este cara em primeiro plano, eu coloco -d nos casos que não quero ter interatividade, só quero que a aplicação rode. 


E o comando `stop` eu paro os containers criados. 

```sh
root@osboxes:~# docker container stop fecca31902c0
fecca31902c0
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
ca53ed399c0d        centos              "/bin/bash"         34 hours ago        Up 34 hours                             pensive_turing
root@osboxes:~# docker container stop ca53ed399c0d
ca53ed399c0d
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
root@osboxes:~# 

```

Assim como também posso startar novamente

```sh
root@osboxes:~# docker container start fecca31902c0
fecca31902c0
root@osboxes:~# docker container start ca53ed399c0d
ca53ed399c0d
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
fecca31902c0        nginx               "/docker-entrypoint.…"   37 minutes ago      Up 11 seconds       80/tcp              affectionate_dijkstra
ca53ed399c0d        centos              "/bin/bash"              34 hours ago        Up 3 seconds                            pensive_turing

```

E também tenho o restart do container, caso precise. 

```sh
root@osboxes:~# docker container restart fecca31902c0
fecca31902c0
```

O comando `insepect` vai trazer os detalhes daquele container. 

```sh
root@osboxes:~# docker container inspect fecca31902c0
[
    {
        "Id": "fecca31902c05350d920db4c3ed35793d64b155e06894ce15c026a8632c74e2e",
        "Created": "2020-10-10T03:11:02.088105653Z",
        "Path": "/docker-entrypoint.sh",
        "Args": [
            "nginx",
            "-g",
            "daemon off;"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 83380,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2020-10-10T03:49:45.95038292Z",
            "FinishedAt": "2020-10-10T03:49:45.218821799Z"
        },
        "Image": "sha256:992e3b7be0465856d44bed9b3d5596267205a4cfaec4241439be42f77b3539a3",
        "ResolvConfPath": "/var/lib/docker/containers/fecca31902c05350d920db4c3ed35793d64b155e06894ce15c026a8632c74e2e/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/fecca31902c05350d920db4c3ed35793d64b155e06894ce15c026a8632c74e2e/hostname",
        "HostsPath": "/var/lib/docker/containers/fecca31902c05350d920db4c3ed35793d64b155e06894ce15c026a8632c74e2e/hosts",
        "LogPath": "/var/lib/docker/containers/fecca31902c05350d920db4c3ed35793d64b155e06894ce15c026a8632c74e2e/fecca31902c05350d920db4c3ed35793d64b155e06894ce15c026a8632c74e2e-json.log",
        "Name": "/affectionate_dijkstra",
        "RestartCount": 0,
        "Driver": "overlay2",
        "Platform": "linux",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "docker-default",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": null,
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "default",
            "PortBindings": {},
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "CapAdd": null,
            "CapDrop": null,
            "Capabilities": null,
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": null,
            "GroupAdd": null,
            "IpcMode": "private",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": false,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "ConsoleSize": [
                0,
                0
            ],
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "NanoCpus": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": [],
            "BlkioDeviceReadBps": null,
            "BlkioDeviceWriteBps": null,
            "BlkioDeviceReadIOps": null,
            "BlkioDeviceWriteIOps": null,
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": [],
            "DeviceCgroupRules": null,
            "DeviceRequests": null,
            "KernelMemory": 0,
            "KernelMemoryTCP": 0,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": null,
            "OomKillDisable": false,
            "PidsLimit": null,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0,
            "MaskedPaths": [
                "/proc/asound",
                "/proc/acpi",
                "/proc/kcore",
                "/proc/keys",
                "/proc/latency_stats",
                "/proc/timer_list",
                "/proc/timer_stats",
                "/proc/sched_debug",
                "/proc/scsi",
                "/sys/firmware"
            ],
            "ReadonlyPaths": [
                "/proc/bus",
                "/proc/fs",
                "/proc/irq",
                "/proc/sys",
                "/proc/sysrq-trigger"
            ]
        },
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/26828e39601076b546dccc85c380c95cf5cc0b522e323146d1b95d11ea7937f0-init/diff:/var/lib/docker/overlay2/84650e899c555dc002159c3c23c29e89e034100f74fd3cbb06e780ad664becf9/diff:/var/lib/docker/overlay2/1e436d1da6e23864fe43e1edc99b400aedf747d7c40c233334adc8dc8d605863/diff:/var/lib/docker/overlay2/ea346940afd1708c365a570cc67b1736ff34fe3abee91a19cd79ce0456dcfc80/diff:/var/lib/docker/overlay2/7a5860acc38166730e81c14f29786ca662e46d9a3470b89db74bf2c6f22373e9/diff:/var/lib/docker/overlay2/5fe8bdb9845162cbb357ac3c5d2a24ebedacca1d689eb69c1658d408fb5896db/diff",
                "MergedDir": "/var/lib/docker/overlay2/26828e39601076b546dccc85c380c95cf5cc0b522e323146d1b95d11ea7937f0/merged",
                "UpperDir": "/var/lib/docker/overlay2/26828e39601076b546dccc85c380c95cf5cc0b522e323146d1b95d11ea7937f0/diff",
                "WorkDir": "/var/lib/docker/overlay2/26828e39601076b546dccc85c380c95cf5cc0b522e323146d1b95d11ea7937f0/work"
            },
            "Name": "overlay2"
        },
        "Mounts": [],
        "Config": {
            "Hostname": "fecca31902c0",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "80/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "NGINX_VERSION=1.19.3",
                "NJS_VERSION=0.4.4",
                "PKG_RELEASE=1~buster"
            ],
            "Cmd": [
                "nginx",
                "-g",
                "daemon off;"
            ],
            "Image": "nginx",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": [
                "/docker-entrypoint.sh"
            ],
            "OnBuild": null,
            "Labels": {
                "maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"
            },
            "StopSignal": "SIGTERM"
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "025bdf57c2c369552c5538135b7e5007d4491807375357f7bce90a802291915a",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {
                "80/tcp": null
            },
            "SandboxKey": "/var/run/docker/netns/025bdf57c2c3",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "61173c80ab6b1c9c01b93c48df85a8dfb3612d644d38a084e3abad2a7e24f0d0",
            "Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "MacAddress": "02:42:ac:11:00:02",
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "6bf2ac8e47d6de141905be78499c34f36b89ace5586c89a38be3090a8881365c",
                    "EndpointID": "61173c80ab6b1c9c01b93c48df85a8dfb3612d644d38a084e3abad2a7e24f0d0",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
        }
    }
]
root@osboxes:~# 
```
Posso também pausar um container com o comando `pause`

```sh
root@osboxes:~# docker container pause fecca31902c0
fecca31902c0
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                  PORTS               NAMES
fecca31902c0        nginx               "/docker-entrypoint.…"   43 minutes ago      Up 5 minutes (Paused)   80/tcp              affectionate_dijkstra
ca53ed399c0d        centos              "/bin/bash"              35 hours ago        Up 6 minutes                                pensive_turing
root@osboxes:~# docker container unpause fecca31902c0
fecca31902c0
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
fecca31902c0        nginx               "/docker-entrypoint.…"   43 minutes ago      Up 5 minutes        80/tcp              affectionate_dijkstra
ca53ed399c0d        centos              "/bin/bash"              35 hours ago        Up 6 minutes                            pensive_turing

```

Para que eu possa ver os logs deste container, utilizo o comando `logs` seguido da flag `-f` e ID para ficar monitorando.

```sh
root@osboxes:~# docker container logs -f fecca31902c0
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
127.0.0.1 - - [10/Oct/2020:03:26:52 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
```

Para remover um container, basta utilizar o comando rm, porém se o mesmo estiver em execução, ele não vai deixar. Para isso basta fazer um `rm -f`

```sh
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
425c61ede184        nginx               "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes        80/tcp              romantic_hofstadter
ca53ed399c0d        centos              "/bin/bash"              35 hours ago        Up 15 minutes                           pensive_turing
root@osboxes:~# docker container rm 425c61ede184
Error response from daemon: You cannot remove a running container 425c61ede184f202b4ae9c3678c429735296fa916253dc953d723414cd3d52cb. Stop the container before attempting removal or force remove
root@osboxes:~# docker container rm -f 425c61ede184
425c61ede184
root@osboxes:~# docker container rm -f 425c61ede184
425c61ede184
root@osboxes:~# docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
ca53ed399c0d        centos              "/bin/bash"         35 hours ago        Up 18 minutes                           pensive_turing

```


# Configurando CPU e memória para os meus containers 

Para checar como está o uso de recursos do container, eu utilizo o comando `stats`

```sh
root@osboxes:~# docker container stats 7f824cb8005e
```
Para testar os recursos pode-se utilizar o programa Stress.

`root@7f824cb8005e:/# apt-get install stress`

Para ver detalhes do seu uso, utilize

# $ stress --help

Fiz o seguinte comando 

`stress --cpu 1 --vm-bytes 128 --vm 1`

Posso utilizar para ver os dados também o famoso `top`

```sh
root@osboxes:~# docker container top 7f824cb8005e
```
Claro, se o mesmo estiver instalado no container


Para criar um container do nginx por exemplo com limitação de memória e cpu, eu posso definir isso na criação. Exemplo:

```sh
root@osboxes:~# docker container run -d -m 128M --cpus 0.5 nginx
```

Neste caso estou definindo 128MB de ram para o container e que ele se limite a usar só 50% de CPU.

Posso testar utilizando o stress.

Agora quero mudar quero que utilize 80% de CPU, então eu posso fazer um update.

```sh
root@osboxes:~# docker container update --cpus 0.8  --memory 64M 7f824cb8005e
```
Agora ele vai utilizar 80% de CPU e 64MB de memória, para o ID que no caso é do nginx.


# Criando um Dockerfile 

Depois de criar uma pasta para alocar o Dockerfile, eu crio um arquivo no vim

```sh
FROM debian

LABEL app="BIKER"
ENV FXSHELL="Devops"

RUN apt-get update && apt-get install -y stress && apt-get clean

CMD stress --cpu 1 --vm-bytes 64M --vm 1
```
Depois de criado, vou buildar 

# $ docker image build -t toskeira:1.0

```sh
root@osboxes:~/tosko_dockerfile# docker image build -t toskeira:1.0 .
Sending build context to Docker daemon  2.048kB
Step 1/5 : FROM debian
latest: Pulling from library/debian
57df1a1f1ad8: Pull complete 
Digest: sha256:439a6bae1ef351ba9308fc9a5e69ff7754c14516f6be8ca26975fb564cb7fb76
Status: Downloaded newer image for debian:latest
 ---> f6dcff9b59af
Step 2/5 : LABEL app="Giropops"
 ---> Running in c329bf2c69e1
Removing intermediate container c329bf2c69e1
 ---> d59dacfad6f9
Step 3/5 : ENV FELIPE="Lindo"
 ---> Running in 8c2387746f05
Removing intermediate container 8c2387746f05
 ---> 36c9c0b6beb9
Step 4/5 : RUN apt-get update && apt-get install -y stress && apt-get clean
 ---> Running in f4b8d2261527
Get:1 http://security.debian.org/debian-security buster/updates InRelease [65.4 kB]
Get:2 http://deb.debian.org/debian buster InRelease [121 kB]
Get:3 http://deb.debian.org/debian buster-updates InRelease [51.9 kB]
Get:4 http://deb.debian.org/debian buster/main amd64 Packages [7906 kB]
Get:5 http://security.debian.org/debian-security buster/updates/main amd64 Packages [233 kB]
Get:6 http://deb.debian.org/debian buster-updates/main amd64 Packages [7868 B]
Fetched 8387 kB in 11s (794 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following NEW packages will be installed:
  stress
0 upgraded, 1 newly installed, 0 to remove and 1 not upgraded.
Need to get 21.8 kB of archives.
After this operation, 55.3 kB of additional disk space will be used.
Get:1 http://deb.debian.org/debian buster/main amd64 stress amd64 1.0.4-4 [21.8 kB]
debconf: delaying package configuration, since apt-utils is not installed
Fetched 21.8 kB in 8s (2708 B/s)
Selecting previously unselected package stress.
(Reading database ... 6677 files and directories currently installed.)
Preparing to unpack .../stress_1.0.4-4_amd64.deb ...
Unpacking stress (1.0.4-4) ...
Setting up stress (1.0.4-4) ...
Removing intermediate container f4b8d2261527
 ---> 3662327fda9e
Step 5/5 : CMD stress --cpu 1 --vm-bytes 64M --vm 1
 ---> Running in 83774952c3c4
Removing intermediate container 83774952c3c4
 ---> d24fe1c0773b
Successfully built d24fe1c0773b
Successfully tagged toskeira:1.0
root@osboxes:~/tosko_dockerfile# 
```

Certo, agora se eu der um comando, `docker image ls` ele vai exibir a nossa imagem recem criada. 


```sh 
root@osboxes:~/tosko_dockerfile# docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
toskeira            1.0                 d24fe1c0773b        About a minute ago   133MB
```

Para executar

```sh
docker container run -d toskeira:1.0
```
Limitando memoria

```sh
docker container run -d --memory 64M  toskeira:1.0
```
Posso também utilizar o comando update. 

```sh
root@osboxes:~# docker container update --cpus 0.8  --memory 64M [CONTAINER ID]
```

Limitando CPU para 80% e memoria para 64M

























































