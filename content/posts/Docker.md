---
title: "Docker"
date: 2020-10-08T11:10:44-03:00
draft: false
tags: ["devops", "docker", "linux", "containers", "infraestrutura"]
---

Docker é a plataforma de containers mais usada no mercado. Com ela você empacota uma aplicação e todas as suas dependências em uma unidade portátil que roda de forma idêntica em qualquer ambiente — do laptop do dev até a produção em cloud.

O conceito central é **isolamento**: cada container roda de forma completamente isolada dos demais e do host, usando recursos do próprio kernel Linux.

---

## Dois tipos de isolamento

**Lógico — Namespaces:** isolam processos, redes, usuários e sistemas de arquivos. Cada container enxerga apenas o que é seu.

**Físico — Cgroups:** limitam o uso de CPU, memória e disco. Garantem que um container não consuma recursos dos outros.

---

## Arquitetura

<iframe src="/docker-arquitetura.html"
        width="100%"
        height="530"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

O Docker Engine usa três módulos do kernel Linux:

- **`Namespaces`** — isolamento lógico de processos, redes, usuários
- **`Cgroups`** — isolamento físico de CPU, memória, I/O
- **`Netfilter`** — roteamento de rede, NAT e redirecionamento de pacotes

**Imagens em camadas:** todas as camadas são read-only, exceto a camada superior de cada container (onde as alterações acontecem). Se você tem 5 containers baseados na mesma imagem de 500 MB, o disco não aloca 2,5 GB — todos compartilham a mesma base. Só a camada de escrita de cada container é individual.

---

## Instalação

```sh
curl -fsSL https://get.docker.com/ | bash
docker version
docker container ls
```

Para usar sem `sudo`, adicione seu usuário ao grupo docker:

```sh
sudo usermod -aG docker $USER
```

---

## Ciclo de Vida do Container

<iframe src="/docker-lifecycle.html"
        width="100%"
        height="490"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

### Rodando o primeiro container

```sh
docker container run hello-world
```

### Flags essenciais do `run`

| Flag | Função |
|------|--------|
| `-d` | Daemon — roda em background |
| `-ti` | Terminal interativo (bash, sh) |
| `-p 8080:80` | Mapeia porta do host para o container |
| `-m 128M` | Limita memória |
| `--cpus 0.5` | Limita a 50% de um núcleo |
| `--name` | Define nome do container |
| `--rm` | Remove o container ao encerrar |

### Containers interativos

```sh
# Entrar dentro de um ubuntu
docker container run -ti ubuntu

# Ver processos (apenas os do container)
root@2fd8c26be92e:/# ps -ef
UID   PID  CMD
root    1  /bin/bash
root    8  ps -ef
```

`CTRL+D` encerra o container (mata o processo principal).
`CTRL+P+Q` sai sem matar o container.

### Containers em background (daemon)

Para serviços como nginx, **nunca use `-ti`** — o entrypoint não é o bash:

```sh
docker container run -d nginx
```

Para executar comandos dentro de um container em execução, use `exec`:

```sh
docker container exec -ti <id> bash
docker container exec -ti <id> ls /etc/nginx
```

### Gerenciamento

```sh
docker container ls        # containers em execução
docker container ls -a     # todos (incluindo parados)
docker container stop <id>
docker container start <id>
docker container restart <id>
docker container pause <id>
docker container unpause <id>
docker container rm <id>         # remove parado
docker container rm -f <id>      # força remoção
docker container logs -f <id>    # logs em tempo real
docker container inspect <id>    # detalhes completos em JSON
docker container stats <id>      # uso de CPU/memória em tempo real
docker container top <id>        # processos rodando no container
```

---

## Limitando Recursos

Definir limites na criação:

```sh
docker container run -d -m 128M --cpus 0.5 nginx
```

Atualizar em container já em execução:

```sh
docker container update --cpus 0.8 --memory 64M <id>
```

Testar pressão com `stress` (instalar dentro do container):

```sh
apt-get install -y stress
stress --cpu 1 --vm-bytes 128M --vm 1
```

---

## Volumes — Persistindo Dados

O filesystem do container é **volátil** — quando o container é removido, tudo dentro dele some. Volumes existem fora do container e persistem independentemente.

<iframe src="/docker-volumes.html"
        width="100%"
        height="510"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

### Bind Mount — você define o caminho

```sh
# Montar diretório do host no container
docker container run -ti \
  --mount type=bind,src=/opt/meuapp,dst=/app \
  debian

# Somente leitura
docker container run -ti \
  --mount type=bind,src=/opt/meuapp,dst=/app,ro \
  debian
```

### Docker Volume — gerenciado pelo Docker

```sh
# Criar volume
docker volume create dbdados

# Usar volume no container
docker container run -d \
  --mount type=volume,src=dbdados,dst=/data \
  postgres:16

# Listar volumes
docker volume ls

# Inspecionar
docker volume inspect dbdados

# Remover (só se não estiver em uso)
docker volume rm dbdados

# Remover todos os volumes não utilizados
docker volume prune
```

Todos os volumes ficam em `/var/lib/docker/volumes/`.

### Compartilhando volume entre containers

```sh
docker container run -d -p 5432:5432 --name pgsql1 \
  --mount type=volume,src=dbdados,dst=/data \
  postgres:16

docker container run -d -p 5433:5432 --name pgsql2 \
  --mount type=volume,src=dbdados,dst=/data \
  postgres:16
```

Ambos os containers leem e escrevem no mesmo volume.

### Backup de volume

```sh
mkdir /opt/backup

docker container run --rm \
  --mount type=volume,src=dbdados,dst=/data \
  --mount type=bind,src=/opt/backup,dst=/backup \
  debian tar -cvf /backup/bkp-banco.tar /data
```

---

## Dockerfile — Criando Suas Imagens

O Dockerfile descreve como construir uma imagem. Cada instrução cria uma nova camada.

### Instruções principais

| Instrução | Descrição |
|-----------|-----------|
| `FROM` | Imagem base — sempre a primeira linha |
| `RUN` | Executa comando no build, cria camada |
| `CMD` | Comando padrão ao iniciar o container |
| `ENTRYPOINT` | Executável principal do container |
| `COPY` | Copia arquivos para o filesystem |
| `ADD` | Como COPY, mas aceita TAR e URLs |
| `ENV` | Define variáveis de ambiente |
| `EXPOSE` | Documenta a porta que o container escuta |
| `VOLUME` | Declara ponto de montagem de volume |
| `WORKDIR` | Define diretório de trabalho |
| `USER` | Define usuário (padrão: root) |
| `LABEL` | Adiciona metadados à imagem |
| `ARG` | Variável de build-time (não fica na imagem) |

### Exemplo: container com stress

```dockerfile
FROM debian

LABEL app="stress-test"
ENV AMBIENTE="dev"

RUN apt-get update && apt-get install -y stress && apt-get clean

CMD stress --cpu 1 --vm-bytes 64M --vm 1
```

```sh
docker image build -t meu-stress:1.0 .
docker container run -d meu-stress:1.0
```

### Exemplo: Apache com ENTRYPOINT

```dockerfile
FROM debian

RUN apt-get update && apt-get install -y apache2 && apt-get clean

ENV APACHE_LOCK_DIR="/var/lock"
ENV APACHE_PID_FILE="/var/run/apache2/apache2.pid"
ENV APACHE_RUN_USER="www-data"
ENV APACHE_RUN_GROUP="www-data"
ENV APACHE_LOG_DIR="/var/log/apache2"

LABEL description="Webserver" version="1.0.0"

VOLUME /var/www/html/
EXPOSE 80

ENTRYPOINT ["/usr/sbin/apachectl"]
CMD ["-D", "FOREGROUND"]
```

### Multi-stage build — imagem final mínima

Compila em uma imagem pesada, copia apenas o binário para uma imagem leve:

```dockerfile
# Stage 1: build
FROM golang AS build

WORKDIR /src
ADD . /src
RUN go build -o goapp

# Stage 2: imagem final
FROM alpine:3.19

WORKDIR /app
COPY --from=build /src/goapp /app
ENTRYPOINT ["./goapp"]
```

A imagem final tem apenas o binário + Alpine (~5 MB), sem o toolchain Go.

### Buildar e publicar

```sh
# Build local
docker image build -t minha-imagem:1.0 .

# Ver camadas e histórico
docker history minha-imagem:1.0

# Login no Docker Hub
docker login

# Push
docker image tag minha-imagem:1.0 usuario/minha-imagem:1.0
docker push usuario/minha-imagem:1.0
```

---

## Registry Local

Para manter suas imagens em ambiente privado sem depender do Docker Hub:

```sh
# Subir um registry local na porta 5000
docker container run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  registry:2

# Taguear imagem para o registry local
docker tag minha-imagem:1.0 localhost:5000/minha-imagem:1.0

# Push para o registry local
docker push localhost:5000/minha-imagem:1.0
```

Imagens ficam em `/var/lib/registry/docker/registry/v2/repositories/`.

---

## Docker Swarm — Orquestração em Cluster

O Swarm transforma múltiplos hosts Docker em um cluster com load balancing e failover automáticos.

<iframe src="/docker-swarm.html"
        width="100%"
        height="510"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

**Manager** — conhece o estado do cluster, agenda containers, expõe a API.  
**Worker** — executa os containers distribuídos pelo manager.

### Criando o cluster

```sh
# No host manager (gera um token)
docker swarm init

# Nos hosts workers (usar o token gerado)
docker swarm join --token <token> <manager-ip>:2377

# Ver todos os nodes
docker node ls
```

### Gerenciando nodes

```sh
# Ver token para adicionar workers
docker swarm join-token worker

# Ver token para adicionar managers
docker swarm join-token manager

# Promover worker a manager
docker node promote fxshell-02

# Rebaixar manager a worker
docker node demote fxshell-02

# Pausar node (não recebe novos containers)
docker node update --availability pause fxshell-02

# Dreno para manutenção (migra containers para outros nodes)
docker node update --availability drain fxshell-02

# Reativar node
docker node update --availability active fxshell-02

# Remover node do cluster
docker swarm leave           # rodar no próprio node
docker node rm fxshell-02    # rodar no manager
```

### Services — o coração do Swarm

Um Service define quantas réplicas de um container devem rodar, em quais ports e com quais configs. O Swarm distribui as réplicas pelos workers e garante que o número desejado esteja sempre disponível.

```sh
# Criar service com 5 réplicas de nginx
docker service create \
  --name webserver \
  --replicas 5 \
  -p 8080:80 \
  nginx

# Listar services
docker service ls

# Ver em quais nodes estão rodando
docker service ps webserver

# Detalhes completos
docker service inspect webserver

# Escalar para 10 réplicas
docker service scale webserver=10

# Logs de todos os containers do service
docker service logs -f webserver

# Remover service
docker service rm webserver
```

### Service com volume

```sh
docker service create \
  --name webserver \
  --replicas 5 \
  -p 8080:80 \
  --mount type=volume,src=dados,dst=/app \
  nginx
```

O volume `dados` fica disponível em todos os containers do service, em todos os nodes.

---

## Limpeza

```sh
# Remover containers parados
docker container prune

# Remover volumes não utilizados
docker volume prune

# Remover imagens não utilizadas
docker image prune

# Limpeza completa (containers, imagens, redes, cache de build)
docker system prune -a
```

---

## Referência rápida

```sh
# Containers
docker container run -d -p 8080:80 --name web nginx
docker container exec -ti <id> bash
docker container logs -f <id>
docker container stats
docker container inspect <id>

# Imagens
docker image ls
docker image pull ubuntu:22.04
docker image build -t app:1.0 .
docker image push usuario/app:1.0
docker image rm <id>

# Volumes
docker volume create dados
docker volume ls
docker volume inspect dados
docker volume rm dados

# Swarm
docker swarm init
docker node ls
docker service create --name app --replicas 3 -p 80:80 nginx
docker service scale app=5
docker service ps app
```
