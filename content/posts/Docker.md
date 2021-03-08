---
title: "Docker"
date: 2020-10-08T11:10:44-03:00
draft: false
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
Step 2/5 : LABEL app="moranguinho"
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


#Entendendo volumes

Volumes nada mais sao do que diretorios externos ao container, que são montados diretamente nele, dessa forma bypassam seu filesystem, ou seja, não seguem aquele padrão de camadas. 

A principal função do volume é persistir os dados. Diferentemente do filesystem do container, que é volátil e toda informação escrita nele é perdida quando o container morre, quando você escreve em um volume aquele dado continua lá. independentemente do estado do container. 

=> É iniciado quando o container é criado

=> Caso ocorra de já haver dados no diretório em que você está montando como volume, ou seja, se o diretório já existe e já está populado na imagem base, aqueles dados serão copiados para o volume. 

=> Um volume pode ser reusado e compartilhado entre os containers. 

=> Alterações em um volume são feitas diretamente do volume. 

=> Alterações em um volume não irão com a imagem quando você fizer uma cópia ou snapshot de um container. 

=> Volumes continuam a existir mesmo se você deletar o container. 

#Exemplo

Criamos uma pasta para montar nosso volume no local:

```sh
root@FXSHELL ~# mkdir /opt/moranguinho
```

Volumes do tipo bind é quando eu já tenho um diretório que quero montar especifico. 

```sh
root@FXSHELL ~# docker container run -ti --mount type=bind,src=/opt/moranguinho,dst=/moranguinho debian
```
Beleza, já dentro do container crio um arquivo de teste dentro do volume. 

```sh
root@07b30662ffc0:/# cd moranguinho/
root@07b30662ffc0:/moranguinho# ls
root@07b30662ffc0:/moranguinho# ls
root@07b30662ffc0:/moranguinho# touch teste
root@07b30662ffc0:/moranguinho# exit
exit
root@FXSHELL ~# cd /opt/moranguinho/
root@FXSHELL /o/moranguinho# ls
teste
root@FXSHELL /o/moranguinho# 
```

Agora se eu executar um outro container, posso notar que o volume continua o mesmo e com o arquivo criado no passo anterior lá dentro. 

```sh
root@FXSHELL /o/moranguinho# docker container run -ti --mount type=bind,src=/opt/moranguinho,dst=/moranguinho debian
root@c72d32bd0846:/# ls
bin   dev  moranguinho  lib    media  opt   root  sbin  sys  usr
boot  etc  home      lib64  mnt    proc  run   srv   tmp  var
root@c72d32bd0846:/# cd moranguinho/
root@c72d32bd0846:/moranguinho# ls
teste
root@c72d32bd0846:/moranguinho# 
```

```sh
root@9911369c74af:/# df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay         217G  8.8G  197G   5% /
tmpfs            64M     0   64M   0% /dev
tmpfs           491M     0  491M   0% /sys/fs/cgroup
shm              64M     0   64M   0% /dev/shm
/dev/sda1       217G  8.8G  197G   5% /moranguinho
tmpfs           491M     0  491M   0% /proc/asound
tmpfs           491M     0  491M   0% /proc/acpi
tmpfs           491M     0  491M   0% /proc/scsi
tmpfs           491M     0  491M   0% /sys/firmware
root@9911369c74af:/# 
```

Este é o volume do tipo `bind`

OBS: também posso definir o volume somente como leitura definindo o parametro `ro`. 

```sh
root@FXSHELL ~# docker container run -ti --mount type=bind,src=/opt/moranguinho,dst=/moranguinho,ro debian
```

```sh
root@FXSHELL /o/moranguinho# docker container run -ti --mount type=bind,src=/opt/moranguinho,dst=/moranguinho,ro debian
root@e779e386475a:/# cd moranguinho/
root@e779e386475a:/moranguinho# ls
teste  teste2
root@e779e386475a:/moranguinho# touch teste3
touch: cannot touch 'teste3': Read-only file system
root@e779e386475a:/moranguinho# 
```

Mostrando a mensagem como read-only.

#Docker volume

Posso checar todos os volumes criados com o comando:

```sh
root@FXSHELL ~# docker volume ls
DRIVER              VOLUME NAME
root@FXSHELL ~# docker volume create moranguinho
moranguinho
root@FXSHELL ~# ls
snap/  tosko_dockerfile/
root@FXSHELL ~# docker volume ls
DRIVER              VOLUME NAME
local               moranguinho
root@FXSHELL ~# docker volume ls
DRIVER              VOLUME NAME
local               moranguinho
root@FXSHELL ~# docker volume inspect moranguinho
[
    {
        "CreatedAt": "2021-01-19T20:55:40-05:00",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/moranguinho/_data",
        "Name": "moranguinho",
        "Options": {},
        "Scope": "local"
    }
]
root@FXSHELL ~# 
```

Tudo e qualquer volume no docker, vai estar dentro de "/var/lib/docker/volumes"

```sh
root@FXSHELL ~# cd /var/lib/docker/volumes/
root@FXSHELL /v/l/d/volumes# ls
moranguinho/  metadata.db
root@FXSHELL /v/l/d/volumes# 
```

Posso colocar meus arquivos dentro da pasta _"_data" que fica dentro da pasta do volume_


```sh
root@FXSHELL /v/l/d/volumes# ls
moranguinho/  metadata.db
root@FXSHELL /v/l/d/volumes# cd moranguinho/_data/
root@FXSHELL /v/l/d/v/g/_data# touch teste1 teste2 teste3
root@FXSHELL /v/l/d/v/g/_data# ls
teste1  teste2  teste3
root@FXSHELL /v/l/d/v/g/_data# 
```

Posso montar esse volume também em um container, passando o tipo que agora não será tipo bind, mas sim _volume_

```sh
root@FXSHELL ~# docker container run -ti --mount type=volume,src=moranguinho,dst=/moranguinho debian
root@4df1fe08b1da:/# ls
bin   dev  moranguinho  lib    media  opt   root  sbin  sys  usr
boot  etc  home      lib64  mnt    proc  run   srv   tmp  var
root@4df1fe08b1da:/# cd moranguinho/
root@4df1fe08b1da:/moranguinho# ls
teste1  teste2  teste3
root@4df1fe08b1da:/moranguinho# touch teste4_final
```

Depois mato o container e vejo na pasta do volume, e eis o arquivo teste4_final está lá dentro. 

```sh
root@FXSHELL ~# cd /var/lib/docker/volumes/
root@FXSHELL /v/l/d/volumes# ls
moranguinho/  metadata.db
root@FXSHELL /v/l/d/volumes# cd moranguinho/_data/
root@FXSHELL /v/l/d/v/g/_data# ls
teste1  teste2  teste3  teste4_final
root@FXSHELL /v/l/d/v/g/_data# 
```

```sh
root@FXSHELL /v/l/d/v/g/_data# docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
4983b4a108a3        debian              "bash"              11 seconds ago      Up 10 seconds                           frosty_bartik
root@FXSHELL /v/l/d/v/g/_data# 
docker container run -ti --mount type=volume,src=moranguinho,dst=/moranguinho debian
root@13aacd8dfd58:/# ls
bin   dev  moranguinho  lib    media  opt   root  sbin  sys  usr
boot  etc  home      lib64  mnt    proc  run   srv   tmp  var
root@13aacd8dfd58:/# cd moranguinho/
root@13aacd8dfd58:/moranguinho# ls
teste1  teste2  teste3  teste4_final
root@13aacd8dfd58:/moranguinho# ⏎                                               root@FXSHELL /v/l/d/v/g/_data# ls
teste1  teste2  teste3  teste4_final
root@FXSHELL /v/l/d/v/g/_data# docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
13aacd8dfd58        debian              "bash"              14 seconds ago       Up 12 seconds                           flamboyant_moore
4983b4a108a3        debian              "bash"              About a minute ago   Up About a minute                       frosty_bartik
root@FXSHELL /v/l/d/v/g/_data# 
docker container exec -ti 13aacd8dfd58 touch /moranguinho/13aacd8dfd58
root@FXSHELL /v/l/d/v/g/_data# 
docker container exec -ti 4983b4a108a3 touch /moranguinho/4983b4a108a3
root@FXSHELL /v/l/d/v/g/_data# ls
13aacd8dfd58  4983b4a108a3  teste1  teste2  teste3  teste4_final
root@FXSHELL /v/l/d/v/g/_data# 
```

Para remover o volume basta remover todos os containers que estiverem em uso com ele. 

```sh
root@FXSHELL /v/l/d/v/g/_data [1]# docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS               NAMES
4df1fe08b1da        debian              "bash"                   9 minutes ago       Exited (0) 7 minutes ago                        zealous_tereshkova
e779e386475a        debian              "bash"                   21 minutes ago      Exited (1) 20 minutes ago                       brave_meitner

root@FXSHELL /v/l/d/v/g/_data# docker container rm -f 4df1fe08b1da
4df1fe08b1da
root@FXSHELL /v/l/d/v/g/_data# docker container rm -f e779e386475a
e779e386475a

root@FXSHELL /v/l/d/v/g/_data# docker volume rm moranguinho
moranguinho
root@FXSHELL /v/l/d/v/g/_data# ls

```
E assim dentro da pasta /var/lib não temos mais nada do volume moranguinho.

Posso ver as propriedades do volume criado com o comando:

```sh
root@FXSHELL /v/l/d/v/g/_data# 
docker container run -ti --mount type=volume,src=bolacha,dst=/bolacha debian


root@FXSHELL /v/l/d/v/g/_data [1]# docker container inspect 9d5997be4321

        "Mounts": [
            {
                "Type": "volume",
                "Name": "bolacha",
                "Source": "/var/lib/docker/volumes/bolacha/_data",
                "Destination": "/bolacha",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }

```
Se dou um ls volume, o bolacha ainda estará lá. 

```sh
root@FXSHELL /v/l/d/v/g/_data# docker volume ls
DRIVER              VOLUME NAME
local               bolacha
```

Posso utilizar o comando docker volume prune, para remover todos os volumes que estejam não estejam sendo utilizados. 

```sh
root@FXSHELL ~# docker volume prune
WARNING! This will remove all local volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
Deleted Volumes:
bolacha

Total reclaimed space: 0B
```
Posso fazer a mesma coisa para os containers que não estou utilizando mais. 

```sh
root@FXSHELL ~# docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
9911369c74af20bcbf144e1487c326d3d06dd23a0293d7b561e54049f5ddbc56
c72d32bd0846e51a0cbd495909440ee14b64b474611b356704ee3170bf1931b7
07b30662ffc0b0068862768cd6d7c92eafc372d71f5dffc17baca8079cfadf59
ebb965d5043752debf60498d0eac5620ffaecc079af3b557c145539d3d721508
493a598735c5cb1ec6f658df0a4ad5b157562cb462789d19521f1d1fcccbc5fc
acda8e5ec1adaaf1f2632be1fa8c2d6aedf9744be643991fea48d0d310fc3150
d7a861d6ea3811ed0273ac32ada6744a26ec85e14ff3b6c6ff5e3462004c3216
bcee760fd5702bb215b99da66109a3a59158aa5a47aae437d7ff4b516f93c38c
3d7c4a379d3e3d6a6710d581034d6199002942990f7d34ae5cb97617dd98ef32
2c6bcccf8f1727817a5da2c9b59edb7afdbb0790e3b3ba16a6298448d3cbb5a6
d21df8a6681620d956610f5e6808b21a0cd960d3c5a5c88da767b39efec4b674
ea431a856eff6fd17ff13d87ae498bfe91fb61fe6566744a528f62c1731689b5
8f88a55195f7defa35196f1d506a1d179af0099afbfcb34a9fd7fefef78240b6
40ab9db51e4a8c6e5603bdb51c60f37925e89d60afab8bda1ddf06071cb06ecc

Total reclaimed space: 870.3MB
```

```sh
root@FXSHELL ~# docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
root@FXSHELL ~# docker container ls -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
root@FXSHELL ~# 
```

Assim limpando tudo. 

Agora um outro teste

```sh
root@FXSHELL ~# docker container create -v /opt/bolacha:/data --name dbdados centos
49eeb1ffb2453b206028478bc24f13582f5c1cb2ed2dbb378702ea10a7c5fb0c
```
Com isso, apenas criamos o container e especificamos um volume para ele, mas ainda não o iniciamos. 

Sabemos que no container o volume se encontra montado em "/data".

Agora vamos criar os containers que rodarão o Postgresql utilizando o volume "/data" do container "dbdados" para guardar os dados. 

Para isso precisamos entender dois parâmetros importantes:

--volume-from : É utilizado quando queremos montar um volme disponibilizado por outro container. 

-e : É utilizado para informar váriaveis de um ambiente para o container. No exemplo, estamos passando as variáveis de ambiente do PostgreSQL.

```sh
root@FXSHELL ~# docker container run -d -p 5432:5432 --name pgsql1 --volumes-from dbdados -e POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql

```

```sh
root@FXSHELL ~# docker container run -d -p 5433:5432 --name pgsql2 --volumes-from dbdados -e POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql
```

Criei duas. 


```sh
root@FXSHELL ~# docker container ls -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                    NAMES
79e408793331        kamui/postgresql    "/usr/local/bin/run"   8 seconds ago       Up 7 seconds        0.0.0.0:5433->5432/tcp   pgsql2
2c2161d46619        kamui/postgresql    "/usr/local/bin/run"   6 minutes ago       Up 6 minutes        0.0.0.0:5432->5432/tcp   pgsql1
49eeb1ffb245        centos              "/bin/bash"            10 minutes ago      Created                                      dbdados
root@FXSHELL ~# 
```

Fazendo da forma nova e atualizada:

```sh
root@FXSHELL ~# docker volume create dbdados
dbdados

root@FXSHELL ~# docker container run -d -p 5432:5432 --name pgsql1  --mount type=volume,src=dbdados,dst=/data -e POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql
1fbdf3f70d206cebb44049c737e2d08359118df654bcf9481a5a46c99ab47ccc
root@FXSHELL ~# docker container run -d -p 5433:5432 --name pgsql2  --mount type=volume,src=dbdados,dst=/data -e POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql
368bc32d8ca3203dd8962ced0a6a4b999f56751462f121d3100c00169e43e4a8
root@FXSHELL ~# docker container ls
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                    NAMES
368bc32d8ca3        kamui/postgresql    "/usr/local/bin/run"   5 seconds ago       Up 3 seconds        0.0.0.0:5433->5432/tcp   pgsql2
1fbdf3f70d20        kamui/postgresql    "/usr/local/bin/run"   16 seconds ago      Up 14 seconds       0.0.0.0:5432->5432/tcp   pgsql1
root@FXSHELL ~# docker volume ls
DRIVER              VOLUME NAME
local               dbdados
root@FXSHELL ~# 
```

E assim os dados do postgreSQL estão la dentro:

```sh
root@FXSHELL ~# cd /var/lib/docker/volumes/dbdados/_data
root@FXSHELL /v/l/d/v/d/_data# ls
base/          pg_multixact/  pg_stat_tmp/  pg_xlog/         server.key@
global/        pg_notify/     pg_subtrans/  postgresql.conf
pg_clog/       pg_serial/     pg_tblspc/    postmaster.opts
pg_hba.conf    pg_snapshots/  pg_twophase/  postmaster.pid
pg_ident.conf  pg_stat/       PG_VERSION    server.crt@
root@FXSHELL /v/l/d/v/d/_data# 
```

Supondo que quero fazer um backup deste cara, e encarrego outro container de fazer isso, posso fazer algo assim:

```sh
root@FXSHELL ~# mkdir /opt/backup
root@FXSHELL ~# 
root@FXSHELL ~# 
root@FXSHELL ~# 
root@FXSHELL ~# 
root@FXSHELL ~# docker container run -ti --mount type=volume,src=dbdados,dst=/data --mount type=bind,src=/opt/backup,dst=/backup debian tar -cvf /backup/bkp-banco.tar /data
```

montando um volume do tipo bind dentro deste novo container e empacotando com o tar, o bkp.

#EXEMPLO DE COMANDOS
```sh
# docker container run -ti --mount type=bind,src=/volume,dst=/volume ubuntu
# docker container run -ti --mount type=bind,src=/root/primeiro_container,dst=/volume ubuntu
# docker container run -ti --mount type=bind,src=/root/primeiro_container,dst=/volume,ro ubuntu
# docker volume create moranguinho
# docker volume rm moranguinho
# docker volume inspect moranguinho
# docker volume prune
# docker container run -d --mount type=volume,source=moranguinho,destination=/var/opa  nginx
# docker container create -v /data --name dbdados centos
# docker run -d -p 5432:5432 --name pgsql1 --volumes-from dbdados -e POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql
# docker run -d -p 5433:5432 --name pgsql2 --volumes-from dbdados -e  POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql
# docker run -ti --volumes-from dbdados -v $(pwd):/backup debian tar -cvf /backup/backup.tar /data
```

#Criando um dockerfile

$ vim dockerfiles/1/Dockerfile

```sh
FROM debian #qual imagem vou me basear

RUN apt-get update && apt-get install -y apache2 && apt-get clean  #executa oque vai fazer
ENV APACHE_LOCK_DIR="/var/lock"   #Variavel de ambiente para não ter dois apache rodando
ENV APACHE_PID_FILE="/var/run/apache2.pid"  #Variavel de ambiente de identificação do processo
ENV APACHE_RUN_USER="www.data"         #Variavel de ambiente usuário responsável pelo apache
ENV APACHE_RUN_GROUP="www-data"         #Variavel de ambiente grupo responsável pelo apache
ENV APACHE_LOG_DIR="/var/log/apache2" #onde vai salvar os logs do apache

LABEL description="Webserver" #faz uma descrição (qualquer chave=valor)
LABEL version="1.0.0"

VOLUME /var/www/html #docker vai criar automaticamente esse volume
EXPOSE 80 #com a flag -P irá pegar o expose qualquer porta = 80
```

Para criar o container eu faço um docker build. 

```sh
root@FXSHELL ~# docker build .

ou

root@FXSHELL ~# docker image build -t meu_apache:1.0 .
```

#Exemplos de Dockerfiles

```sh
FROM debian

RUN apt-get update && apt-get install -y apache2 && apt-get clean
ENV APACHE_LOCK_DIR="/var/lock"
ENV APACHE_PID_FILE="/var/run/apache2.pid"
ENV APACHE_RUN_USER="www-data"
ENV APACHE_RUN_GROUP="www-data"
ENV APACHE_LOG_DIR="/var/log/apache2"

LABEL description="Webserver"

VOLUME /var/www/html/
EXPOSE 80
```


```sh
FROM debian

RUN apt-get update && apt-get install -y apache2 && apt-get clean
ENV APACHE_LOCK_DIR="/var/lock"
ENV APACHE_PID_FILE="/var/run/apache2/apache2.pid"
ENV APACHE_RUN_USER="www-data"
ENV APACHE_RUN_DIR="/var/run/apache2"
ENV APACHE_RUN_GROUP="www-data"
ENV APACHE_LOG_DIR="/var/log/apache2"

LABEL description="Webserver"

VOLUME /var/www/html/
EXPOSE 80

ENTRYPOINT ["/usr/sbin/apachectl"]
CMD ["-D", "FOREGROUND"]
```

```sh
package main
import "fmt"

func main() {
    fmt.Println("GIROPOPS STRIGUS GIRUS - LINUXTIPS")
}
```

```sh
FROM golang

WORKDIR /app
ADD . /app
RUN go build -o goapp
ENTRYPOINT ./goapp
```

```sh
FROM golang AS buildando

ADD . /src
WORKDIR /src
RUN go build -o goapp


FROM alpine:3.1

WORKDIR /app
COPY --from=buildando /src/goapp /app
ENTRYPOINT ./goapp
```

ADD => Copia novos arquivos, diretórios, arquivos TAR ou arquivos remotos e os adicionam ao filesystem do container;

CMD => Executa um comando, diferente do RUN que executa o comando no momento em que está "buildando" a imagem, o CMD executa no início da execução do container;

LABEL => Adiciona metadados a imagem como versão, descrição e fabricante;

COPY => Copia novos arquivos e diretórios e os adicionam ao filesystem do container;

ENTRYPOINT => Permite você configurar um container para rodar um executável, e quando esse executável for finalizado, o container também será;

ENV => Informa variáveis de ambiente ao container;

EXPOSE => Informa qual porta o container estará ouvindo;

FROM => Indica qual imagem será utilizada como base, ela precisa ser a primeira linha do Dockerfile;

MAINTAINER => Autor da imagem; 

RUN => Executa qualquer comando em uma nova camada no topo da imagem e "commita" as alterações. Essas alterações você poderá utilizar nas próximas instruções de seu Dockerfile;

USER => Determina qual o usuário será utilizado na imagem. Por default é o root;

VOLUME => Permite a criação de um ponto de montagem no container;

WORKDIR => Responsável por mudar do diretório / (raiz) para o especificado nele;

* Um Dockerfile serve para criar uma imagem de um container 
  
  A finalidade da instrução FROM no Dockerfile é para indicar uma imagem base
  
  Para "buildar" uma nova imagem, utilizo o comando, 'docker build -t nomedaimagem:1.0 .'
 
  As instruções para que o Dockerfile adicione um arquivo, são 'ADD' ou 'COPY'
  
  No momento de criação da imagem o Dockerfile executa o comando 'RUN'
  
  Os comandos que executam um comando na inicialização do container são 'ENTRYPOINT' ou 'CMD'
  
  A instrução que indica qual usuário que será utilizado no container é o 'USER'
  
  Indica que determinado diretório no container será um volume com o comando 'VOLUME'
  
  É possível ter duas instruções FROM dentro do mesmo Dockerfile.
  
  Para referenciá-lo em outra parte do arquivo utilizo o 'FROM debian AS giropops'
  
  Para listar todas as imagens do container eu faço 'docker image ls'
 
  É possível criar uma imagem a partir de um container em execução.

  Com o comando "docker commit" eu crio uma imagem apartir de um container em execução.

**

#SUBINDO UMA IMAGEM PARA SUA CONTA DO DOCKERHUB

```sh
root@FXSHELL ~/d/2# docker image ls
REPOSITORY      TAG       IMAGE ID       CREATED         SIZE
fpmatta/toddy   1.0       e1c0c1113bca   6 minutes ago   267MB
ubuntu          latest    f63181f19b2f   12 days ago     72.9MB

root@FXSHELL ~/d/2# docker login
Authenticating with existing credentials...
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

root@FXSHELL ~/d/2# docker push fpmatta/toddy:1.0
The push refers to repository [docker.io/fpmatta/toddy]
b43d9cffa997: Pushing [==============================================>    ]  178.2MB/193.7MB
02473afd360b: Mounted from library/ubuntu 
dbf2c0f42a39: Preparing 
9f32931c9d28: Preparing 
```

#Não confio na internet; posso criar o meu registry local

Subindo o registry local:
```sh
root@FXSHELL ~# docker container run -d -p 5000:5000 --restart=always --name registry registry:2
```
Consigo ver o container do registry rodando bem como sua imagem.
```sh
root@FXSHELL ~# docker container ls
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                    NAMES
49fbebd0365b   registry:2   "/entrypoint.sh /etc…"   34 seconds ago   Up 32 seconds   0.0.0.0:5000->5000/tcp   registry
root@FXSHELL ~# docker image ls
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
fpmatta/toddy   1.0       e1c0c1113bca   31 minutes ago   267MB
registry        2         678dfa38fcfa   6 weeks ago      26.2MB
root@FXSHELL ~# 
```

Preciso retagear o nome da minha imagem, passando o meu registry local que no caso é o 'localhost:5000'
```sh
root@FXSHELL ~# docker image ls
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
fpmatta/toddy   1.0       e1c0c1113bca   31 minutes ago   267MB
registry        2         678dfa38fcfa   6 weeks ago      26.2MB
root@FXSHELL ~# docker tag e1c0c1113bca localhost:5000/fpmatta/toddy:1.0
root@FXSHELL ~# docker image ls
REPOSITORY                     TAG       IMAGE ID       CREATED          SIZE
fpmatta/toddy                  1.0       e1c0c1113bca   35 minutes ago   267MB
localhost:5000/fpmatta/toddy   1.0       e1c0c1113bca   35 minutes ago   267MB
registry                       2         678dfa38fcfa   6 weeks ago      26.2MB
root@FXSHELL ~# docker image push localhost:5000/fpmatta/toddy:1.0
The push refers to repository [localhost:5000/fpmatta/toddy]
b43d9cffa997: Pushing [==================================================>]  199.9MB
02473afd360b: Pushed 
dbf2c0f42a39: Pushed 
9f32931c9d28: Pushed 
```
Para checar sua imagem dentro do registry fica no caminho abaixo:
```sh
/var/lib/registry/docker/registry/v2/repositories/fpmatta/toddy 
```

```sh
root@FXSHELL ~# docker container ls
CONTAINER ID   IMAGE                              COMMAND                  CREATED          STATUS          PORTS                    NAMES
a3c92b51fe5b   localhost:5000/fpmatta/toddy:1.0   "/bin/bash"              13 minutes ago   Up 13 minutes                            exciting_heyrovsky
49fbebd0365b   registry:2                         "/entrypoint.sh /etc…"   30 minutes ago   Up 30 minutes   0.0.0.0:5000->5000/tcp   registry
root@FXSHELL ~# docker exec -ti 49fbebd0365b sh
/ # ls
bin            entrypoint.sh  home           media          opt            root           sbin           sys            usr
dev            etc            lib            mnt            proc           run            srv            tmp            var
/ # cd /var/
cache/  empty/  lib/    local/  lock/   log/    mail/   opt/    run/    spool/  tmp/
/ # cd /var/lib/
apk/       misc/      registry/  udhcpd/
/ # cd /var/lib/registry/docker/registry/v2/
/var/lib/registry/docker/registry/v2 # ls
blobs         repositories
/var/lib/registry/docker/registry/v2 # cd repositories/
/var/lib/registry/docker/registry/v2/repositories # ls
fpmatta
/var/lib/registry/docker/registry/v2/repositories # cd fpmatta/
/var/lib/registry/docker/registry/v2/repositories/fpmatta # ls
toddy
/var/lib/registry/docker/registry/v2/repositories/fpmatta # cd toddy/
/var/lib/registry/docker/registry/v2/repositories/fpmatta/toddy # ls
_layers     _manifests  _uploads
/var/lib/registry/docker/registry/v2/repositories/fpmatta/toddy # 
```

#DockerHub e Registry - Exemplo comandos 
 docker image inspect debian
 
 docker history linuxtips/apache:1.0
 
 docker login
 
 docker login registry.suaempresa.com
 
 docker push linuxtips/apache:1.0
 
 docker pull linuxtips/apache:1.0
 
 docker image ls
 
 docker container run -d -p 5000:5000 --restart=always --name registry registry:2
 
 docker tag IMAGEMID localhost:5000/apache

# Docker Machine

Para fazer a instalação do Docker Machine no Linux, faça:

```sh
# curl -L https://github.com/docker/machine/releases/download/v0.16.1
/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine
# chmod +x /tmp/docker-machine 
# sudo cp /tmp/docker-machine /usr/local/bin/docker-machine


Para seguir com a instalação no macOS:

# curl -L https://github.com/docker/machine/releases/download/v0.16.1
/docker-machine-`uname -s`-`uname -m` >/usr/local/bin/docker-machine 
# chmod +x /usr/local/bin/docker-machine

Para seguir com a instalação no Windows caso esteja usando o Git bash:

# if [[ ! -d "$HOME/bin" ]]; then mkdir -p "$HOME/bin"; fi
# curl -L https://github.com/docker/machine/releases/download/v0.16.1
/docker-machine-Windows-x86_64.exe > "$HOME/bin/docker-machine.exe"
# chmod +x "$HOME/bin/docker-machine.exe"


Para verificar se ele foi instalado e qual a sua versão, faça:

# docker-machine version

# docker-machine create --driver virtualbox linuxtips

# docker-machine ls

# docker-machine env linuxtips

# eval "$(docker-machine env linuxtips)"

# docker container ls

# docker container run busybox echo "LINUXTIPS, VAIIII"

# docker-machine ip linuxtips

# docker-machine ssh linuxtips

# docker-machine inspect linuxtips

# docker-machine stop linuxtips

# docker-machine ls 

# docker-machine start linuxtips

# docker-machine rm linuxtips

# eval $(docker-machine env -u)
```

# Docker Swarm

Você consegue construir clusters de containers com caracateristicas importantes como balanceador de cargas e failover.

Para criar um clustercom o docker  swarm, basta indicar quais os hosts que ele irá supervisionar e o restante é com ele.

Cuida automaticamente do balanceamento de carga.

O Docker Swarm é bastante simples e se resume a um manager e diversos workers. O manager é o responsavel por orquestrar os containers e distribui-los entre os hosts workers. Os workers são os que carregam o piano, e hospedam os containers.

Worker = Container em execução

Manager = Conhece os detalhes do cluster, sabe todos os containers e serviços.

Para testar, podemos subir três maquinas e instalar o docker em cada uma delas. 

```sh
root@FXSHELL-01 ~# 
root@FXSHELL-02 ~# 
root@FXSHELL-03 ~# 
```

Feito isso, basta rodar na maquina 01, o comando:

```sh
docker swarm init
```

Será gerado um token, que iremos utilizar e rodar nas maquinas do node, que serão as maquinas 02 e 03. 

Depois podera visualizar na maquina manager, todos os nodes que estão adicionados com o comando:

```sh
docker node ls
```

Para visualizar o token da maquina 02 para adiciona-la commo manager e não como worker, basta fazer:

```sh
docker swarm join-token manager
```

Com isso será exibido o token de manager, para ser executado no seu outro host.

Mesma coisa caso fosse um worker

```sh
docker swarm join-token worker
```

Para promover um node worker para manager basta fazer:

```sh
docker node promote maquina-02
```
```sh
docker node demote maquina-02
```

Agora se você quiser remover o node do cluster basta digitar o comando:

```sh
docker swarm leave
```

Também remova ele do nosso manager ativo, com o comando

```sh
docker node rm maquina-02
```
Para remover um node manager, é necessário forçar com a flag --force

```sh
docker swarm leave --force
```

E depois remover do node manager

```sh
docker node rm maquina-03
```

# Docker Services

O service é um VIP ou DNS que realizara o balanceamento de requisições entre os containers. Podemos estabelecer um numero x de containers respondendo por um service e esses containers estarão espalhados pelo nosso cluster, entre nossos nodes, garantindo alta disponibilidade e balanceamento de carga. Tudo isso nativamente.

Os services é uma forma, já utlizada no kubernetes, de você conseguir gerenciar melhor seus containers. Também uma maneira muito simples e efetiva para escalar seu ambiente. Aumentando ou diminuindo a quantidade de containers que responderá para determinado service. 

Exemplo:

Nome do service que desejo criar: webserver

Quantidade de containers que desejo debaixo do service: 5

Portas que iremos blindar, entre o service e o node: 8080:80

Imagem dos containers que irei utilizar: NGINX

O comando ficaria assim =>

```sh
docker service create --name webserver --replicas 5 -p 8080:80 nginx
```

Para testar faça um curl em qualquer ip dos nodes que subiu:8080

Para listar os services faça

```sh 
docker service ls
```

Se quisermos saber onde estão rodando nossos containers, em quais nodes eles estçao sendo executados, basta digitar o seguinte comando:

```sh
docker service ps webserver
```
Assim conseguiremos saber onde está rodando cada container e ainda o seu status. 

Se precisamos saber maiores detalhes sobre o service, basta utlizar o subcomando "inspect".

```sh
docker service inspect webserver
```
Na saída do "inspect" conseguiremos pegar informações importantes sobre nosso service, como portas expostas, volumes, containers, limitações, entre outras coisas. 

Lembre-se meu cenário de nodes é:

```sh
root@FXSHELL-01 ~# 
root@FXSHELL-02 ~# 
root@FXSHELL-03 ~# 
```
Posso ter muitas replicas divididas e distribuidas e balanceadas nesses 3 nodes. 


Uma informação muito importante é o endereço do VIP do service, que estara listado no comando "insepect".

Esse é o endereço do IP do balanceador desse service, ou seja, sempre que acessarem via esse IP, ele distribuirá a conexão entre os containers. 


Agora se quisermos aumentar o número de containers debaixo desse service, é muito simples. Basta executar o comando a seguir: 

```sh
docker service scale webserver=5
```
Pronto, agora temos dez containers respondendo requisições debaido do nosso service webserver.

Para visualizar basta executar:

```sh
docker service ls
```

Ah não quero que um determinado node receba mais containers, posso dar um pause neste cara, com o comando abaixo:

```sh
docker node update --availability pause FXSHELL-02
```

Para ativa-lo novamente:
```sh
docker node update --availability active FXSHELL-02
```

Para retirar temporariamente um node para manutenção por exemplo, faça:
```sh
docker node update --availability drain FXSHELL-02
```

Todos os containers que estavam no FXSHELL-02, vão ser realocados para os outros 2. 

Para visualizar basta executar:

```sh
docker service ps webserver
```

Para saber em quais nodes eseles estão em execução, lembre-se do 'docker service ls webserver'

Para acessar os logs desse service, basta digitar:

```sh
docker service logs -f webserver
```
Assim você terá acesso aos logs de todos os containers desse service. 

Para remover o service é simples

```sh
docker service rm webserver
```

Você pode checar com o comando 

```sh
docker service ls
```

Criar um service com um volume conectado é bastante simples, basta fazer:

```sh
docker service create --name webserver --replicas 5 -p 8080:80 --mount type=volume,src=teste,dst=/app, nginx
```

Quando criamos um service com um volume conectado a ele, isso indica que esse volume estará disponivel em todos os nossos containers desse service, ou seja, o volume com o nome de "teste" estara montado em todos os containers no diretorio "/app".


















