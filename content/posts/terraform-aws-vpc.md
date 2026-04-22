---
title: "Terraform AWS — Provisionando uma VPC Segura com ALB, EC2 e RDS"
date: 2026-04-21
draft: false
tags: ["terraform", "aws", "devops", "infraestrutura", "iac", "cloud"]
---

Toda vez que um time precisa criar um novo ambiente — seja para testes, staging ou produção — o processo manual de clicar no console da AWS abre espaço para erros, inconsistências e ambientes que ninguém sabe exatamente como foram configurados. Infraestrutura como Código resolve isso: você escreve a infraestrutura em arquivos de texto, versiona no Git e aplica com um comando.

Neste lab, construo uma VPC completa na AWS usando Terraform, com balanceador de carga, servidores web em subnets privadas, banco de dados MySQL e state remoto no S3.

## Objetivo do Lab

Provisionar, via Terraform, uma infraestrutura web segura na AWS contendo:

- VPC com subnets públicas e privadas em duas zonas de disponibilidade
- Application Load Balancer nas subnets públicas
- Duas instâncias EC2 com Nginx nas subnets privadas
- RDS MySQL 8 em subnet privada, sem acesso público
- Bastion host para acesso SSH operacional
- NAT Gateway para que as instâncias privadas acessem a internet
- State remoto no S3 com lock via DynamoDB

## Tecnologias Utilizadas

**Terraform** é uma ferramenta de infraestrutura como código criada pela HashiCorp. Você descreve os recursos que quer criar (VMs, redes, bancos de dados) em arquivos `.tf` e o Terraform se encarrega de criar, modificar ou destruir esses recursos na cloud. É amplamente usada em times de DevOps e SRE para gerenciar infraestrutura de forma consistente e reproduzível.

**AWS VPC** (Virtual Private Cloud) é uma rede virtual isolada dentro da AWS onde você controla o espaço de endereçamento IP, as rotas e as regras de acesso. Tudo que você cria na AWS precisa estar dentro de uma VPC.

**Subnets públicas e privadas** dividem a VPC em camadas. Recursos em subnets públicas têm IP público e acesso direto à internet via Internet Gateway. Recursos em subnets privadas ficam isolados da internet — só se comunicam com o mundo externo via NAT Gateway, sem exposição direta.

**Application Load Balancer (ALB)** distribui o tráfego HTTP/HTTPS entre as instâncias de destino. Fica nas subnets públicas e repassa as requisições para os servidores web nas subnets privadas, aplicando health checks automaticamente.

**EC2** (Elastic Compute Cloud) são as máquinas virtuais da AWS. Neste lab uso instâncias `t3.micro` com Amazon Linux 2023 e Nginx.

**RDS** (Relational Database Service) é o serviço gerenciado de banco de dados da AWS. A AWS cuida de backups, patches e failover. Uso MySQL 8 em instância `db.t3.micro` isolada em subnet privada.

**S3 backend** armazena o `terraform.tfstate` — arquivo que registra o estado atual da infraestrutura — em um bucket S3 com criptografia ativada. O DynamoDB garante que dois operadores não apliquem mudanças ao mesmo tempo (locking).

## Arquitetura

```
INTERNET
    │
    ▼
[Internet Gateway]
    │
    ▼
┌─────────────────────────────────────────────┐
│ VPC — 10.0.0.0/16                           │
│                                             │
│  ┌── us-east-1a ──┐  ┌── us-east-1b ──┐    │
│  │ public subnet  │  │ public subnet  │    │
│  │  10.0.1.0/24   │  │  10.0.2.0/24   │    │
│  │  [bastion]     │  │  [nat-gw]      │    │
│  └────────────────┘  └────────────────┘    │
│         │                    │              │
│  [Application Load Balancer]                │
│         │                    │              │
│  ┌── private ─────┐  ┌── private ─────┐    │
│  │  10.0.10.0/24  │  │  10.0.20.0/24  │    │
│  │  [web-01 EC2]  │  │  [web-02 EC2]  │    │
│  └────────────────┘  └────────────────┘    │
│              │                              │
│         [RDS MySQL]                         │
│         10.0.10.0/24 (private)              │
└─────────────────────────────────────────────┘
            │
     [S3 — tfstate]
```

| Recurso            | Tipo           | Subnet   | Acesso         |
|--------------------|----------------|----------|----------------|
| Internet Gateway   | aws_internet_gateway | —     | Internet       |
| ALB                | aws_lb         | Pública  | Internet → EC2 |
| Bastion            | EC2 t3.nano    | Pública  | SSH operador   |
| NAT Gateway        | aws_nat_gateway | Pública | Saída privada  |
| web-01 / web-02    | EC2 t3.micro   | Privada  | Via ALB        |
| RDS MySQL 8        | db.t3.micro    | Privada  | Via EC2        |
| S3 (tfstate)       | aws_s3_bucket  | —        | Terraform      |

<iframe src="/terraform-aws-vpc.html"
        width="100%"
        height="580"
        style="border:none; border-radius:10px; overflow:hidden; display:block; margin: 1.5rem 0;">
</iframe>

## Estrutura dos Arquivos

```
terraform-aws-vpc/
├── main.tf             ← provider, backend S3
├── variables.tf        ← todas as variáveis com descrição e validação
├── outputs.tf          ← DNS do ALB, IPs, endpoint RDS
├── vpc.tf              ← VPC, subnets, IGW, NAT, route tables
├── security_groups.tf  ← SGs separados por recurso
├── ec2.tf              ← instâncias web e bastion
├── alb.tf              ← ALB, target group, listener, S3 de logs
└── rds.tf              ← RDS MySQL, subnet group
```

Separar em arquivos por responsabilidade facilita a leitura e evita um `main.tf` com centenas de linhas.

## Backend S3 — State Remoto

O state do Terraform registra exatamente o que foi criado na AWS. Sem state remoto, cada pessoa da equipe teria seu próprio estado local — o que é um desastre em times. O backend S3 centraliza o state com criptografia e o DynamoDB evita que dois `apply` aconteçam ao mesmo tempo.

Antes de qualquer coisa, crie o bucket e a tabela DynamoDB (só precisa fazer uma vez):

```bash
aws s3api create-bucket \
  --bucket fxshell-terraform-state \
  --region us-east-1

aws s3api put-bucket-versioning \
  --bucket fxshell-terraform-state \
  --versioning-configuration Status=Enabled

aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

## VPC — Rede e Roteamento

A VPC cria o espaço de rede isolado. As subnets públicas têm rota para o Internet Gateway; as privadas têm rota para o NAT Gateway — assim o tráfego de saída das instâncias privadas passa pelo NAT sem expor as máquinas diretamente.

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = { Name = "${var.project_name}-vpc" }
}
```

O `enable_dns_hostnames = true` é necessário para que o RDS receba um hostname DNS resolvível dentro da VPC.

## Security Groups — Princípio do Menor Privilégio

Cada recurso tem seu próprio Security Group com regras mínimas. O EC2 aceita HTTP apenas do ALB, não da internet. O RDS aceita MySQL apenas do EC2. O bastion aceita SSH apenas do IP configurado.

```hcl
# EC2 só aceita tráfego do ALB
ingress {
  description     = "HTTP do ALB"
  from_port       = 80
  to_port         = 80
  protocol        = "tcp"
  security_groups = [aws_security_group.alb.id]
}

# RDS só aceita do EC2
ingress {
  description     = "MySQL das EC2"
  from_port       = 3306
  to_port         = 3306
  protocol        = "tcp"
  security_groups = [aws_security_group.ec2.id]
}
```

Referenciar o ID de outro Security Group como origem (em vez de um CIDR) é mais seguro: se uma instância for substituída e ganhar novo IP, a regra continua válida.

## EC2 — Instâncias com IMDSv2

As instâncias usam `user_data` para instalar e configurar o Nginx automaticamente na inicialização. O `http_tokens = "required"` força o uso do IMDSv2 — a versão mais segura do serviço de metadados das instâncias, que exige um token de sessão antes de responder.

```hcl
metadata_options {
  http_tokens = "required"
}
```

## ALB — Balanceamento com Health Check

O ALB distribui requisições entre as instâncias usando o algoritmo Round Robin. O health check testa a rota `/` a cada 30 segundos: se uma instância não responder com HTTP 200 por 3 verificações consecutivas, ela é removida do pool até se recuperar.

```hcl
health_check {
  healthy_threshold   = 2
  unhealthy_threshold = 3
  interval            = 30
  path                = "/"
  matcher             = "200"
}
```

## Executando

Antes de aplicar, sempre revise o plan:

```bash
# Inicializa o provider e o backend
terraform init

# Mostra o que será criado — sem alterar nada
terraform plan -out=tfplan

# Aplica o plan aprovado
terraform apply tfplan
```

A senha do banco nunca deve estar no código. Passe via variável de ambiente:

```bash
export TF_VAR_db_password="sua-senha-segura"
terraform apply
```

Após o apply, os outputs mostram os dados importantes:

```bash
terraform output alb_dns_name      # DNS para acessar a aplicação
terraform output bastion_public_ip # IP para SSH de manutenção
terraform output rds_endpoint      # Endpoint do banco (sensitive)
```

## Para Destruir o Lab

```bash
terraform destroy
```

O Terraform remove todos os recursos na ordem correta, respeitando as dependências.

## Para Que Serve no Mercado

Times de cloud usam esse padrão (VPC + ALB + EC2 + RDS em subnets privadas) como base para praticamente qualquer aplicação web na AWS. O que muda é o tamanho das instâncias, o número de AZs e os serviços adicionais.

Com Terraform, essa infraestrutura vira um módulo reutilizável. Um time pode criar um ambiente de staging idêntico ao de produção em minutos, com certeza de que as configurações são as mesmas — algo impossível de garantir clicando manualmente no console.

## Conclusão

Infraestrutura como código não é só sobre automação — é sobre confiança. Quando a infra está em arquivos `.tf` versionados no Git, qualquer pessoa do time pode entender o que existe, revisar mudanças em pull requests e reverter para um estado anterior se algo der errado. O `terraform plan` funciona como um diff da infraestrutura: você vê exatamente o que vai mudar antes de mudar.

## Referências

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
