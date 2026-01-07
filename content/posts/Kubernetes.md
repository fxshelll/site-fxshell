---
title: "Kubernetes"
date: 2020-09-30T20:59:51-03:00
draft: false
---


## Introdução e Arquitetura do Kubernetes
Começaremos explorando os fundamentos do Kubernetes Kubernetes, conceitos essenciais para construir uma base sólida que facilitará o entendimento da arquitetura e do funcionamento dessa plataforma de orquestração de contêineres.

## O que é Kubernetes?
O Kubernetes é uma plataforma open source para orquestração de contêineres, criada para automatizar grande parte das tarefas manuais relacionadas a implantação, administração e escalonamento de aplicações em contêineres.

```
Inicialmente criado pelo Google e atualmente mantido pela Cloud Native Computing Foundation (CNCF), o Kubernetes se consolidou como o padrão de mercado para orquestração de contêineres, sendo amplamente adotado em arquiteturas de microsserviços e computação em nuvem.
```

## Por que usar Kubernetes?

Inicialmente criado pelo Google e atualmente mantido pela Cloud Native Computing Foundation (CNCF), o Kubernetes se consolidou como o padrão de mercado para orquestração de contêineres, sendo amplamente adotado em arquiteturas de microsserviços e computação em nuvem.

## Empacotamento Consistente

As aplicações são empacotadas de forma que se comportem da mesma maneira em ambientes de desenvolvimento, teste e produção, eliminando o clássico problema do "funciona na minha máquina".


## Abstração de Infraestrutura

Desenvolvedores não precisam se preocupar com servidores específicos. O Kubernetes se encarrega de alocar recursos e encontrar o melhor local para executar cada aplicação.


## Escalabilidade sob Demanda

O Kubernetes pode escalar automaticamente as aplicações — para mais ou para menos — com base na demanda real, otimizando recursos, desempenho e custos.

## Plataforma Unificada

Permite gerenciar aplicações de forma centralizada em ambientes on-premises, na nuvem ou em arquiteturas híbridas, utilizando a mesma plataforma.

## Ecossistema Robusto

Conta com uma vasta gama de ferramentas e extensões, além de uma comunidade ativa e forte suporte comercial de provedores líderes de mercado.

## Automação do Ciclo de Vida

Desde a construção até o deploy e o monitoramento, todo o ciclo de vida da aplicação pode ser automatizado, aumentando a eficiência e reduzindo erros.

## Portabilidade

A mesma aplicação pode ser executada em diferentes provedores de nuvem (AWS, Azure, Google Cloud), ou em datacenters próprios, sem necessidade de alterações .


## O que é um Cluster do Kubernetes?
Um cluster Kubernetes (ou K8s) é um conjunto de nós de computação (ou máquinas de trabalho), que trabalham juntos para executar aplicações empacotadas em contêineres. A conteinerização é um processo de implantação e execução de software que empacota o código da aplicação junto com todos os arquivos, bibliotecas e dependências necessários para que ela funcione de forma consistente em qualquer infraestrutura.

## O Que é Um Contêiner do Kubernetes?
Um contêiner é uma unidade de software que empacota uma aplicação e todas as suas dependências, garantindo que ela seja executada de forma isolada e consistente em qualquer ambiente.

### Componentes de um Cluster:

```
\Control Plane: o "escritório da gerência" que toma decisões.

\Worker Nodes: os "funcionários" que executam o trabalho real.

\Rede: a "comunicação interna" que conecta tudo.

```

### Arquitetura do Kubernetes: Entendendo Seus Componentes Fundamentais

O Kubernetes é baseado em uma arquitetura composta por componentes especializados, que trabalham em conjunto para automatizar a implantação, o escalonamento e a operação de aplicações em contêineres de forma eficiente e resiliente

## Estrutura Básica do Cluster
Nós (Nodes) formam a infraestrutura física do cluster, divididos em:

Nós de Controle (Control Plane/Master Nodes):

    \Gerenciam o estado global do cluster;

    \Tomam decisões sobre agendamento;

    \Armazenam configurações e estado;

    \Não executam aplicações de usuário (boa prática)

Nós de Trabalho (Worker Nodes):

    Executam as cargas de trabalho (Pods);

    Recebem instruções do Control Plane.
**

## Componentes do Control Plane
API Server - O Coração do Sistema: o API Server é o principal ponto de entrada para todas as operações dentro do cluster. Ele funciona como uma "recepcionista central", coordenando a comunicação entre os usuários, componentes internos e ferramentas externas.

Sua função principal é processar requisições e todos os comandos kubectl:

    \ Valida dados: Verifica se as configurações estão corretas.
    \ Autentica usuários: Controla quem pode fazer o quê.
    \ Persiste estado: Salva tudo no etcd.
    \ Expõe APIs: Interface REST para ferramentas externas.

Etcd - O Banco de Dados Distribuído: o etcd é o repositório central de dados do Kubernetes. Ele atua como um banco de dados chave-valor altamente disponível e distribuído, responsável por armazenar todo o estado do cluster.

O que armazena:

    \ Estados de todos os objetos Kubernetes;
    \ Configurações de rede e segurança;
    \ Metadados e políticas;
    \ Histórico de mudanças.

Scheduler - O Planejador Inteligente: é responsável por decidir em qual nó do cluster cada pod será executado, garantindo eficiência e balanceamento de carga.

Processo de decisão:

    \ Filtragem: Remove nós que não atendem requisitos básicos.
    \ Pontuação: Avalia nós restantes com algoritmos de scoring.
    \ Seleção: Escolhe o nó com melhor pontuação.
    \ Bind: Agenda o Pod para execução.


Controller Manager - Os Supervisores Automáticos: é o componente que executa diversos controllers, responsáveis por garantir que o estado real do cluster se mantenha conforme o estado desejado definido na configuração.

Controllers principais:

    \ Replication Controller / ReplicaSet: garante que o número desejado de réplicas de um pod esteja sempre em execução.
    \ Node Controller: monitora o status dos nós (nodes) e gerencia ações quando um nó fica indisponível.
    \ Service Account Controller: gerencia contas de serviço e tokens de autenticação para os pods.


## Componentes dos Worker Nodes

### kubelet - O Agente Local

O kubelet é o agente que roda em cada nó de trabalho, responsável por garantir que os contêineres estejam funcionando conforme definido nas especificações do cluster

Responsabilidades detalhadas:

    \ Comunicação: registra o nó no cluster via API Server.
    \ Gerenciamento de Pods: baixa imagens, inicia contêineres, monitora saúde.
    \ Health Monitoring: executa probes e reporta status.
    \ Resource Management: aplica limits e requests de recursos.
    \ Volume Management: monta e gerencia armazenamento.

### Kube-proxy - O Gerenciador de Rede
O kube-proxy é responsável por gerenciar a rede nos nós de trabalho garantindo a comunicação eficiente e o balanceamento de carga entre os pods.

Funcionalidades:

    \ Load Balancing: distribui o tráfego entre Pods de um Service.
    \ Service Discovery: mantém o mapeamento de Services para Pods.
    \ Network Rules: implementa regras de conectividade.
    \ Health Tracking: remove Pods não-saudáveis do balanceamento.


### Container Runtime - O Executor
O Container Runtime é o componente responsável por executar e gerenciar contêineres em um nó, garantindo que eles sejam baixados, iniciados e gerenciados corretamente.

Responsabilidades:

    \ Baixar imagens de contêiner;
    \ Executar contêineres;
    \ Gerenciar ciclo de vida;
    \ Implementar isolamento de recursos.

### Objetos Kubernetes Fundamentais
Pods - Unidades Básicas de Implantação

Os pods são a menor unidade executável no Kubernetes, com as seguintes características principais:

    \ Podem agrupar múltiplos contêineres;
    \ Compartilham recursos de rede e armazenamento;
    \ São sempre escalonados no mesmo nó;
    \ Funcionam como "unidades lógicas" para agrupamento de contêineres.

Estados do Pod:

    \ Pending: aguardando agendamento.
    \ Running: executando normalmente.
    \ Succeeded: terminou com sucesso.
    \ Failed: terminou com erro.
    \ Unknown: estado indeterminado.

### Componentes de Gerenciamento

Serviços (Services): no Kubernetes, os Services atuam como uma abstração de rede que proporciona balanceamento de carga automático, oferece um ponto de acesso estável via DNS e permite o desacoplamento entre front-end e back-end.

Servidor de API: o API Server é o componente central do Kubernetes, responsável por processar todas as requisições de operação, validar e executar comandos no cluster e atuar como interface para ferramentas externas.

### Mecanismos de Alta Disponibilidade
ReplicaSets: os RepicaSets garantem a resiliência das aplicações através de:

    \ Manutenção de um número definido de réplicas.
    \ Recuperação automática de falhas.
    \ Escalabilidade horizontal simplificada.


Controladores de Ingress: gerenciam o tráfego externo para os serviços do cluster, oferecendo:

    \ Roteamento baseado em regras;
    \ Terminação SSL/TLS;
    \ Balanceamento de carga avançado.

#### Kubernetes: Capacidades Essenciais para Gestão de Aplicações em Contêineres

O Kubernetes oferece um ecossistema completo para a orquestração de contêineres, com funcionalidades avançadas que atendem aos requisitos de aplicações modernas:

## Escalabilidade Automática
    \ Ajusta dinamicamente a quantidade de instâncias em execução conforme a demanda;
    \ Otimiza a utilização de recursos da infraestrutura;
    \ Permite redução de custos operacionais sem comprometer a performance;
    \ Suporta tanto escalonamento horizontal (mais réplicas) quanto vertical (mais recursos).

## Balanceamento de Carga Inteligente
    \ Distribui automaticamente o tráfego entre os Pods disponíveis;
    \ Garante alta disponibilidade e estabilidade do sistema;
    \ Prevê e evita sobrecarga em componentes individuais;
    \ Oferece diferentes algoritmos de distribuição (Round Robin, Least Connections, etc.).


## Mecanismos de Autocura
    \ Detecta e recupera automaticamente falhas em contêineres e Pods;
    \ Mantém o estado desejado declarado pelo usuário;
    \ Reduz significativamente o tempo de indisponibilidade;
    \ Reinicia contêineres falhos ou os realoca em nós saudáveis.

## Service Discovery Integrado
    \ Simplifica a comunicação entre microsserviços;
    \ Oferece DNS interno para descoberta automática de serviços;
    \ Facilita a integração em arquiteturas distribuídas;
    \ Mantém o registro dinâmico de endpoints.

## Gerenciamento de Configurações
    \ ConfigMaps armazenam configurações não sensíveis;
    \ Secrets gerenciam dados confidenciais com criptografia;
    \ Suporte nativo a variáveis de ambiente;
    \ Permite atualizações de configuração sem reconstruir imagens.


## Estratégias Avançadas de Deploy
    \ Implementa atualizações contínuas (rolling updates);
    \ Permite rollback automático em caso de falhas;
    \ Suporta blue-green deployments e canary releases;
    \ Mantém a disponibilidade durante atualizações.

## Gestão de Recursos Granular
    \ efine requests e limits para CPU e memória;
    \ Evita contenção de recursos entre aplicações;
    \ Permite priorização de cargas de trabalho críticas;
    \ Oferece métricas detalhadas de consumo.

## Benefícios Estratégicos
    \ Redução de custos operacionais com otimização de recursos;
    \ Aumento da resiliência e disponibilidade das aplicações;
    \ Simplificação de operações complexas em ambientes distribuídos;
    \ Aceleração dos ciclos de desenvolvimento e entrega contínua.


Esta arquitetura de recursos integrados permite que as organizações gerenciem aplicações containerizadas de forma eficiente e escalável, desde ambientes de desenvolvimento até implementações críticas em produção.



## Padrões de Comunicação e Protocolos
O Kubernetes implementa um modelo de comunicação baseado em APIs RESTful sobre HTTP/HTTPS, mas com nuances importantes:

API-First Architecture: toda interação no cluster passa pela API do Kubernetes, garantindo consistência, auditoria e controle de acesso centralizado.

Watch Pattern: componentes utilizam o padrão "watch" para receber notificações em tempo real sobre mudanças de estado, reduzindo latência e uso de recursos.

Declarative State Management: o sistema trabalha com estado declarativo, onde você especifica o que quer (desired state) e o Kubernetes trabalha continuamente para alcançar esse estado.

## Control Plane - O Cérebro do Kubernetes
Visão Geral Arquitetural

O Control Plane do Kubernetes é um sistema distribuído complexo que implementa o padrão "control loop" em múltiplas camadas. Cada componente opera de forma independente, mas coordenada, criando um sistema auto-healing e auto-scaling.

![K8S](/kub1.png)
Figura 1 - Control Plane
API Server - O Gateway Inteligente: o API Server é muito mais do que um simples gateway HTTP. É um servidor altamente sofisticado que implementa múltiplas funcionalidades críticas:

```yml
Arquitetura Interna do API Server

Request Pipeline: cada requisição passa por uma pipeline de processamento rigorosamente definida:

Authentication: verifica a identidade do requisitante usando certificados X.509, tokens JWT, ou plugins externos.
Authorization: determina se o usuário tem permissão para realizar a operação usando RBAC, ABAC ou webhooks.
Admission Control: aplica políticas de negócio e validações antes de persistir o objeto.
Validation: verifica se o objeto está sintática e semanticamente correto.
Persistence: armazena o objeto no etcd.
Response: retorna confirmação ou erro para o cliente.
```

## etcd - O Sistema Nervoso Central
O etcd é um banco de dados distribuído que utiliza o algoritmo de consenso Raft para garantir consistência em um cluster. É o único local onde o Kubernetes armazena seu estado.

## Arquitetura e Funcionamento do Raft
O protocolo Raft garante que todas as operações sejam aplicadas na mesma ordem em todos os nós do cluster:

Leader Election: um nó é eleito leader e é responsável por todas as escritas Log Replication: O leader replica todas as mudanças para os followers Safety: Garante que logs commitados nunca sejam perdidos.

![K8S](/kub2.png)
Figura 2 - Estrutura de Dados no etcd

Scheduler - O Estrategista de Recursos: o Kubernetes Scheduler é um componente sofisticado que toma decisões de placement usando algoritmos complexos de otimização.

Processo de Scheduling Detalhado: o processo de scheduling acontece em duas fases principais:

Fase 1 - Filtering (Predicates):
```yml
NodeResourcesFit: verifica se o nó tem recursos suficientes (CPU, memória, storage).

NodeAffinity: aplica regras de afinidade de nó.

PodAffinity/AntiAffinity: considera afinidade entre pods.

Taints and Tolerations: respeita restrições de scheduling.

VolumeBinding: verifica disponibilidade de volumes.
```
Fase 2 - Scoring (Priorities):

```yml
NodeResourcesFit: pontua nós com base em utilização de recursos.

ImageLocality: favorece nós que já têm a imagem do container.

InterPodAffinity: pontua baseado em afinidade entre pods.

NodeAffinity: aplica pesos às preferências de afinidade.
```
Controller Manager - O Maestro dos Control Loops: o Controller Manager é uma coleção de controllers que implementam a lógica de negócio do Kubernetes. Cada controller executa um "control loop" independente.

## Worker Nodes - Os Executores Especializados
Arquitetura Detalhada dos Worker Nodes: cada Worker Node é um ambiente de execução completo que deve ser capaz de:

```yml
Executar containers de forma isolada e segura;

Manter comunicação com o Control Plane;

Implementar políticas de rede;

Coletar métricas e logs;

Gerenciar recursos locais (CPU, memória, storage).
```

![K8S](/kub3.png)
Figura 3 - Worker Nodes

kubelet - O Agente Node Superinteligente: o kubelet é o agente mais complexo do Kubernetes, responsável por traduzir especificações declarativas em ações concretas no sistema operacional.

kube-proxy - O Maestro da Rede: o kube-proxy implementa a abstração de Services do Kubernetes, fornecendo load balancing e service discovery.

```yml

Comunicação e Fluxos de Dados Avançados;

Fluxos Críticos de Operação;

Criação Completa de um Pod;

Alta Disponibilidade e Topologias de Cluster;

Control Plane HA - Arquitetura Stacked etcd.

```

![K8S](/kub4.png)
Figura 4 - Kubelet

![K8S](/kub5.png)
Figura 5 - Load Balancer

```yml
Troubleshooting e Diagnósticos Avançados;

Problemas Críticos do Control Plane;

API Server Troubleshooting;

Sintoma: API Server não responde ou responde lentamente.
```

Soluções Comuns:

```yml
Aumentar limites de file descriptors;

Otimizar configurações de timeout;

Verificar e renovar certificados;

Analisar admission controllers demorados.
```

