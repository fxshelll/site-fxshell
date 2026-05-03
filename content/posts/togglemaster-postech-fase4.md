---
title: "ToggleMaster — POSTECH Fase 4: Observabilidade Total em Kubernetes com OpenTelemetry"
date: 2026-05-02
draft: false
tags: ["kubernetes", "devops", "opentelemetry", "grafana", "prometheus", "loki", "gitops", "argocd", "azure", "fiap", "postech"]
images: ["togglemaster-postech-fase4.gif"]
description: "Tech Challenge Fase 4 da FIAP PosTech — instrumentação de microsserviços com OpenTelemetry, stack de observabilidade Prometheus/Loki/Grafana no AKS, alertas inteligentes com OpsGenie e Self-Healing automático via GitHub Actions."
---

Um serviço começou a falhar silenciosamente. A infraestrutura escalava tentando compensar, consumindo recursos sem parar. A equipe de engenharia demorou 6 horas para ser avisada pelos usuários — e mais 4 horas para achar a causa raiz nos logs espalhados pelos pods. Esse é o cenário real que o **Tech Challenge Fase 4 da FIAP PosTech** propõe resolver.

Esta é a conclusão da jornada com o **ToggleMaster** — um sistema de feature flags construído ao longo de 4 fases do PosTech DevOps. As Fases 1, 2 e 3 entregaram os 5 microsserviços conteinerizados, infraestrutura via Terraform, pipelines CI/CD com DevSecOps e deploy no AKS via ArgoCD. A Fase 4 adiciona **Observabilidade Total e Resposta Ativa**: se um serviço ficar lento, vemos o Trace; se der erro, temos Logs centralizados; se um limite for atingido, o time é avisado pelo OpsGenie; e o próprio sistema tenta se curar automaticamente.

---

## O que é o ToggleMaster

O ToggleMaster é uma plataforma de **feature flags** — um mecanismo que permite ativar ou desativar funcionalidades de um sistema em produção sem fazer um novo deploy. Em vez de subir código novo para habilitar uma feature para 10% dos usuários, você simplesmente liga uma flag. Isso é amplamente usado por times como Netflix, Facebook e Spotify para rollouts graduais, testes A/B e kill switches de emergência.

O sistema é composto por **5 microsserviços independentes**, cada um com responsabilidade específica:

| Serviço | Linguagem | Porta | Responsabilidade |
|---|---|---|---|
| **auth-service** | Go | 8001 | Geração e validação de chaves de API. Toda requisição passa por ele antes de chegar nos demais. |
| **flag-service** | Python (Flask) | 8002 | CRUD de feature flags — criar, listar, ativar, desativar flags. Persiste no PostgreSQL. |
| **targeting-service** | Python (Flask) | 8003 | Define regras de targeting: qual usuário, região ou percentual de tráfego recebe cada flag. |
| **evaluation-service** | Go | 8004 | Hot path do sistema. Recebe uma requisição e avalia em tempo real se uma flag está ativa para aquele contexto. Usa Redis como cache. Enfileira eventos no Azure Queue. |
| **analytics-service** | Python (Flask) | 8005 | Consome a fila de eventos e persiste dados de uso das flags no Azure SQL para análises posteriores. |

---

## Diagrama da Arquitetura Completa

```
┌─────────────────────────── CI/CD PIPELINE ─────────────────────────────┐
│ GitHub → Security (Trivy/SAST) → Docker → ACR → ArgoCD → GitOps Repo  │
│                                                          ↑ Terraform    │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓ sync
┌────────────────────── AKS KUBERNETES ──────────────────────────────────┐
│  auth  │  flag  │  targeting  │  eval  │  analytics                    │
│  :8001 │  :8002 │    :8003    │  :8004 │    :8005                      │
│   Go   │ Python │   Python    │   Go   │   Python                      │
│        └────────┴─────────────┴────────┴────────────→ OTel Collector   │
└──────────────────────────────────────────────────────────── ↓ ─────────┘
                                                        Prometheus | Loki
                                                              ↓
                                                          Grafana Dashboard
                                                              ↓ alerta
                                                       Alertmanager → OpsGenie
                                                              ↓
                                                     Slack #alerts + Self-Healing
┌──────────────────── DATA LAYER ────────────────────────────────────────┐
│  PostgreSQL (auth/flags/targeting) │ Redis (eval cache) │ Azure SQL    │
│  Azure Storage Queue (eval→analytics)                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

![Diagrama animado — ToggleMaster POSTECH Fase 4](/togglemaster-postech-fase4.gif)

---

## Stack de Tecnologias

### Infraestrutura como Código — Terraform

O cluster AKS (Azure Kubernetes Service) e o ACR (Azure Container Registry) são provisionados inteiramente via Terraform. Nenhum recurso é criado manualmente no portal Azure. Isso garante que o ambiente é reproduzível: destruir e recriar leva minutos, e o estado é versionado.

### CI/CD com DevSecOps — GitHub Actions

Cada microsserviço tem seu próprio pipeline no GitHub Actions. O pipeline compartilhado (`shared-ci.yml`) faz:

1. **Detecção de linguagem** — Go ou Python automaticamente
2. **Build e testes** — `go build`, `go test`, `pytest`
3. **Lint** — `golangci-lint` para Go, `pylint` + `flake8` para Python
4. **SAST** — `gosec` para Go, `bandit` para Python
5. **SCA** — `trivy` varredura de dependências (CRITICAL)
6. **Build da imagem Docker** e push no ACR
7. **Container Scan** — trivy na imagem final
8. **GitOps Update** — atualiza o `deployment.yaml` no repositório GitOps com a nova tag

### GitOps com ArgoCD

O ArgoCD monitora o repositório GitOps e aplica automaticamente qualquer mudança nos manifestos do cluster. Quando o CI faz push de uma nova tag de imagem, o ArgoCD detecta em segundos e sincroniza o cluster. O fluxo é completamente declarativo: o estado desejado está no Git, e o cluster converge para ele.

---

## Observabilidade — A Fase 4

### Por que OpenTelemetry?

OpenTelemetry (OTel) é o padrão aberto da CNCF para instrumentação de aplicações. Em vez de cada ferramenta ter seu próprio SDK proprietário (Datadog agent, New Relic agent), o OTel define um protocolo único (OTLP) e cada linguagem tem bibliotecas que emitem Traces, Métricas e Logs nesse formato. O **OTel Collector** recebe tudo e roteia para os backends corretos.

Isso significa que os microsserviços não precisam saber que existe Prometheus ou Loki — eles simplesmente enviam para o Collector via gRPC na porta 4317.

### Instrumentação dos Serviços

**Serviços Go** (auth-service, evaluation-service):
```go
// otelhttp envolve o mux HTTP e gera métricas e traces automaticamente
handler := otelhttp.NewHandler(mux, "auth-service")
```
A biblioteca `otelhttp` intercepta cada requisição HTTP e registra automaticamente a duração, método, status code e cria spans de trace.

**Serviços Python** (flag, targeting, analytics):
```python
# FlaskInstrumentor injeta middleware automaticamente
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()   # rastreia chamadas HTTP externas
Psycopg2Instrumentor().instrument()   # rastreia queries no PostgreSQL
```

### OTel Collector

O Collector roda como deployment no namespace `observability` e opera três pipelines:

```yaml
pipelines:
  metrics:
    receivers: [otlp, prometheus]        # recebe OTLP dos serviços + scrape próprio
    processors: [memory_limiter, batch]
    exporters: [prometheusremotewrite]   # → Prometheus Server
  logs:
    receivers: [otlp]
    exporters: [otlphttp/loki]           # → Loki
  traces:
    receivers: [otlp]
    exporters: [debug]                   # futuro: Tempo/Jaeger
```

### Prometheus

Armazena métricas de infraestrutura (CPU, memória, disco dos nodes via `node-exporter`) e de aplicação (requisições HTTP, latência p99/p50, restarts de pods via `kube-state-metrics`). O Prometheus recebe dados de duas fontes: scrape direto dos pods e remote write do OTel Collector.

### Loki + Promtail

O Promtail roda como DaemonSet em todos os nodes e coleta os logs de todos os containers automaticamente, etiquetando com `namespace`, `pod` e `container`. O Loki indexa esses logs e os expõe via LogQL para o Grafana. O OTel Collector também envia logs estruturados dos serviços via OTLP HTTP.

### Grafana Dashboard

Um único dashboard centralizado (`ToggleMaster — Saúde do Ecossistema`) cobre:

- **CI/CD Pipeline** — pods em ImagePullBackOff, CrashLoopBackOff, replicas disponíveis vs desejadas
- **OTel Collector** — throughput de spans/métricas/logs por segundo, uso de memória e CPU do collector
- **Microsserviços — HTTP** — requisições por segundo, latência p99/p50, taxa de erros 4xx/5xx
- **Cluster AKS** — CPU, memória e disco do cluster em gauges, pods reiniciando
- **Recursos por serviço** — CPU e memória em millicores por namespace
- **Redis** — uso de CPU e memória do cache
- **Logs em tempo real** — todos os microsserviços, filtro de ERROR/WARN/FATAL, volume de erros por serviço por minuto

---

## Alertas Inteligentes e Self-Healing

### Alerta de 5xx

Configurado no Grafana Alertmanager: se a taxa de erros HTTP 5xx do auth-service ultrapassar 5% por mais de 2 minutos, o alerta dispara.

```promql
sum(rate(http_server_duration_milliseconds_count{http_status_code=~"5.."}[2m])) by (job)
/ sum(rate(http_server_duration_milliseconds_count[2m])) by (job) > 0.05
```

### OpsGenie — Gerenciamento de Incidentes

O Alertmanager notifica o OpsGenie, que abre automaticamente um incidente com prioridade P2, atribui ao time on-call e inicia o cronômetro de SLA. O incidente inclui a query que disparou, os labels do alerta e um link direto para o dashboard do Grafana.

### Slack — ChatOps

Simultaneamente, uma notificação detalhada chega no canal `#alerts` do Slack com:
- Qual serviço está com problema
- Qual métrica ultrapassou o threshold
- Link para o Grafana
- Runbook de resposta

### Self-Healing via GitHub Actions

O Alertmanager envia um webhook para um GitHub Actions workflow. Quando o alerta dispara, o workflow executa automaticamente:

```bash
kubectl rollout restart deployment/auth-service -n auth-service-prd
```

O pod é reiniciado sem intervenção humana. Se o problema for transiente (memory leak, conexão travada), o serviço volta ao estado saudável em segundos. O mesmo mecanismo funciona para qualquer serviço — basta o alerta correspondente disparar.

---

## Estrutura dos Repositórios

```
ToggleMaster-AppRepo/
├── auth-service/         # Go — auth + otelhttp
├── flag-service/         # Python — Flask + FlaskInstrumentor
├── targeting-service/    # Python — Flask + FlaskInstrumentor
├── evaluation-service/   # Go — eval + Redis + Azure Queue
├── analytics-service/    # Python — Azure SQL consumer
└── .github/workflows/
    ├── shared-ci.yml     # pipeline reutilizável
    ├── auth-ci.yml       # trigger por path
    ├── flag-ci.yml
    └── ...

ToggleMaster-gitops/
└── environments/prd/
    ├── observability/
    │   ├── prometheus-app.yaml          # Helm chart via ArgoCD
    │   ├── loki-app.yaml                # SingleBinary mode
    │   ├── grafana-app.yaml             # com sidecar de dashboard
    │   ├── otel-collector.yaml          # Deployment + ConfigMap
    │   └── grafana-dashboard-configmap.yaml
    ├── auth-service/
    ├── flag-service/
    ├── targeting-service/
    ├── evaluation-service/
    └── analytics-service/
```

---

## Para Que Serve no Mercado

O padrão implementado aqui — OTel + Prometheus + Loki + Grafana + AlertManager + PagerDuty/OpsGenie — é exatamente o que times de SRE usam em empresas como Nubank, iFood e Mercado Livre. A observabilidade não é opcional em sistemas distribuídos: sem ela, a depuração de problemas em produção é caçar agulha em palheiro.

O Self-Healing automático reduz o MTTR (Mean Time to Recovery) de horas para minutos e permite que o time de on-call durma tranquilo — o sistema reage antes que o usuário perceba.

---

## Conclusão

O maior aprendizado desta fase não é técnico — é cultural. Observabilidade não é uma feature que você adiciona no final. É uma disciplina que precisa estar no DNA do sistema desde o primeiro commit. Instrumentar um microsserviço com OTel leva menos de 20 linhas de código e devolve visibilidade total de como ele se comporta em produção.

O ToggleMaster termina a jornada de 4 fases com um sistema que não apenas funciona — mas que **sabe que está funcionando**, avisa quando não está, e tenta se consertar sozinho.

---

## Referências

- [OpenTelemetry — Documentação Oficial](https://opentelemetry.io/docs/)
- [Prometheus — Getting Started](https://prometheus.io/docs/introduction/overview/)
- [Grafana Loki — Documentação](https://grafana.com/docs/loki/latest/)
- [ArgoCD — Core Concepts](https://argo-cd.readthedocs.io/en/stable/core_concepts/)
- [Azure Kubernetes Service](https://learn.microsoft.com/en-us/azure/aks/)
- [OTel Go Contrib — otelhttp](https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp)
- [OTel Python — FlaskInstrumentor](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/flask/flask.html)
