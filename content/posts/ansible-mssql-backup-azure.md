---
title: "Automatizando Backups de SQL Server no Azure com Ansible"
date: 2026-04-21
draft: false
tags: ["ansible", "sqlserver", "azure", "devops", "backup", "windows", "automation", "sre"]
images: ["og-ansible-mssql-backup-azure.png"]
description: "Automação de backup e restore de SQL Server direto para Azure Blob Storage com Ansible, via BACKUP TO URL e RESTORE FROM URL."
---

Manter backups consistentes de múltiplos SQL Servers e armazená-los em nuvem é uma tarefa crítica que, quando feita manualmente, vira fonte de erros, esquecimentos e surpresas na hora de um restore. Este lab mostra como resolver isso com Ansible rodando em uma máquina Linux, acionando servidores Windows via WinRM e fazendo o backup ir direto do SQL Server para o Azure Blob Storage — sem que nenhum arquivo passe pela máquina de controle.

## Objetivo do Lab

Construir uma automação completa que, a partir de uma máquina Linux, conecta em múltiplos SQL Servers Windows via WinRM, cria um SQL Server CREDENTIAL com o SAS Token do Azure, e dispara os três tipos de backup nativos do SQL Server (Full, Differential e Transaction Log) diretamente para o Azure Blob Storage via `BACKUP TO URL`. O projeto inclui também um playbook de restore com suporte a ponto no tempo (point-in-time recovery), onde o SQL Server lê os arquivos diretamente do Azure via `RESTORE FROM URL`.

## Tecnologias Utilizadas

**Ansible** é a ferramenta de automação de infraestrutura que orquestra todo o fluxo. Ela executa tarefas em hosts remotos sem precisar instalar agentes — usa SSH para Linux e WinRM para Windows. No mercado é amplamente usada por times DevOps e SRE para padronizar operações repetitivas.

**WinRM** (Windows Remote Management) é o protocolo da Microsoft equivalente ao SSH para Windows. O Ansible usa ele, com autenticação NTLM, para executar comandos em servidores Windows sem precisar de nenhum agente instalado.

**sqlcmd** é a ferramenta de linha de comando do SQL Server para executar scripts T-SQL. O Ansible gera o script `.sql` via template Jinja2 e chama o `sqlcmd` remotamente para executá-lo.

**BACKUP TO URL / RESTORE FROM URL** é o mecanismo nativo do SQL Server (disponível desde 2012 SP1) para fazer backup e restore diretamente de e para o Azure Blob Storage, sem staging local. O SQL Server autentica via um objeto `CREDENTIAL` que contém o SAS Token — nenhum dado transita pela máquina Ansible.

**SQL Server CREDENTIAL** é um objeto de segurança do SQL Server que armazena a identidade e o segredo de autenticação para um recurso externo. Neste projeto, o CREDENTIAL aponta para a URL base da conta de armazenamento e usa o SAS Token como `SECRET`. O Ansible cria ou atualiza esse CREDENTIAL antes de cada execução de backup.

**ansible-vault** é o mecanismo de criptografia do Ansible para proteger variáveis sensíveis — senhas, tokens, chaves — dentro dos arquivos de inventário e variáveis do projeto.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKUP FLOW                                       │
│                                                                      │
│  ┌──────────────┐  WinRM/NTLM    ┌──────────┐  ┌──────────┐       │
│  │   ops-linux  │ ─────────────► │  sql01   │  │  sql02   │       │
│  │  (trigger)   │                │  sql03   │  │  ...     │       │
│  └──────────────┘                └────┬─────┘  └────┬─────┘       │
│                                       │ BACKUP TO URL│             │
│                                       ▼              ▼             │
│                          ┌──────────────────────────────────────┐  │
│                          │        Azure Blob Storage            │  │
│                          │  📦 sql-backup-full                  │  │
│                          │  📦 sql-backup-diff                  │  │
│                          │  📦 sql-backup-log                   │  │
│                          └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    RESTORE FLOW                                      │
│                                                                      │
│  ┌──────────────┐  lista blobs   ┌──────────────────────────────┐  │
│  │   ops-linux  │ ─────────────► │     Azure Blob Storage       │  │
│  │  (orquestra) │ ◄─ URLs ─────  │  📦 containers (full/diff/log│  │
│  └──────┬───────┘                └──────────────────────────────┘  │
│         │ WinRM + URLs                          ▲                   │
│         ▼                                       │ RESTORE FROM URL  │
│  ┌──────────────────┐ ──────────────────────────┘                   │
│  │    sql-target    │                                               │
│  │    (RESTORE)     │                                               │
│  └──────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────┘
```

| Componente | Função |
|---|---|
| `ops-linux` | Ansible Controller — dispara o backup via WinRM e orquestra o restore (somente metadados) |
| `sql01..03` | SQL Servers Windows — executam `BACKUP TO URL` e `RESTORE FROM URL` diretamente |
| `sqlcmd` | Executa os scripts T-SQL de backup/restore no SQL Server |
| `SQL CREDENTIAL` | Objeto no SQL Server que autentica no Azure via SAS Token |
| `Azure Blob Storage` | Destino e origem dos backups, separados por containers |

![Diagrama animado — Ansible MSSQL Backup → Azure](/ansible-mssql-backup-azure.gif)

## Como Funciona o Backup e Restore Direto

Com `BACKUP TO URL` e `RESTORE FROM URL`, o SQL Server abre uma conexão TLS direto para o endpoint do Azure Blob Storage e faz o stream do backup sem criar arquivo intermediário em nenhum ponto do caminho. A máquina ops envia apenas o script T-SQL (alguns KB) via WinRM e aguarda a conclusão. Nenhum byte de dados de backup trafega pela máquina de controle — ela funciona exclusivamente como orquestradora.

> **Atenção ao horário:** o stream TLS direto do SQL Server para o Azure consome banda de rede da máquina de banco de dados. Em backups Full de bancos grandes (centenas de GB), o upload pode saturar a interface de rede e impactar a latência de queries em produção. **Recomenda-se agendar backups Full e o restore na madrugada** — janela de menor carga — e reservar o horário comercial para backups Differential e Log, que são muito menores.

## Estrutura do Projeto

```
ansible-mssql-backup-azure/
├── ansible.cfg
├── inventory/
│   └── hosts.ini
├── group_vars/
│   ├── all.yml          # Azure storage + SAS Token (vault)
│   └── sqlservers.yml   # credenciais SQL + lista de bancos
├── playbook-backup.yml
├── playbook-restore.yml
└── roles/
    ├── mssql_backup/
    │   ├── tasks/
    │   │   ├── main.yml   # cria CREDENTIAL + direciona por tipo
    │   │   ├── full.yml
    │   │   ├── diff.yml
    │   │   └── log.yml
    │   └── templates/
    │       ├── backup_full.sql.j2
    │       ├── backup_diff.sql.j2
    │       └── backup_log.sql.j2
    └── mssql_restore/
        ├── tasks/
        │   ├── main.yml    # cria CREDENTIAL + chama restore.yml
        │   └── restore.yml
        └── templates/
            └── restore.sql.j2
```

## Inventário e Variáveis

O inventário declara os SQL Servers (Windows, via WinRM). A máquina ops não precisa mais estar no inventário para os backups:

```ini
[sqlservers]
sql01 ansible_host=192.168.1.20
sql02 ansible_host=192.168.1.21
sql03 ansible_host=192.168.1.22

[sqlservers:vars]
ansible_user=ansible_svc
ansible_password="{{ vault_winrm_password }}"
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
ansible_port=5985
```

Em `group_vars/sqlservers.yml`, cada banco é declarado com seu modelo de recuperação, o que determina se backup de log é possível:

```yaml
databases:
  - name: "AppDB"
    recovery_model: "FULL"
  - name: "LegacyDB"
    recovery_model: "SIMPLE"    # só aceita full e diff

backup_compression: true
verify_backup: true
```

Em `group_vars/all.yml`, a URL base da conta é usada tanto para construir as URLs dos blobs quanto como nome do `CREDENTIAL` no SQL Server:

```yaml
azure_storage_account: "minhaconta"
azure_container_full:  "sql-backup-full"
azure_container_diff:  "sql-backup-diff"
azure_container_log:   "sql-backup-log"

# SAS Token: permissões read + write + create + list
vault_azure_sas_token: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  <criptografado>

azure_blob_base_url: "https://{{ azure_storage_account }}.blob.core.windows.net"
```

Para criar o vault:

```bash
ansible-vault encrypt_string 'sv=2022-11-02&ss=b&...' --name 'vault_azure_sas_token'
```

## SQL Server CREDENTIAL

Antes de executar qualquer backup, a role cria (ou atualiza) um `CREDENTIAL` no SQL Server com o SAS Token. Esse objeto é o que permite o SQL Server autenticar no Azure sem precisar de credenciais da conta de armazenamento:

```sql
CREATE CREDENTIAL [https://minhaconta.blob.core.windows.net]
WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
SECRET = 'sv=2022-11-02&ss=b&srt=co&sp=rwdlc&se=2027-01-01...&sig=...';
```

O Ansible executa esse script via `win_shell` + `sqlcmd` com `no_log: true`, garantindo que o SAS Token nunca apareça nos logs da execução.

## Os Três Tipos de Backup

### Full — Backup Completo

O backup Full captura o banco inteiro. É sempre o ponto de partida para qualquer cadeia de restore.

```bash
ansible-playbook playbook-backup.yml -e backup_type=full --ask-vault-pass
```

O script T-SQL gerado pelo template aponta direto para a URL do blob no Azure:

```sql
BACKUP DATABASE [AppDB]
TO URL = N'https://minhaconta.blob.core.windows.net/sql-backup-full/sql01/2026-04-24/sql01_AppDB_FULL_20260424030000.bak'
WITH
    FORMAT, INIT,
    NAME = N'AppDB - Full Backup 20260424030000',
    COMPRESSION,
    STATS = 10,
    CHECKSUM;
```

Após o backup, o SQL Server executa `RESTORE VERIFYONLY FROM URL` para confirmar a integridade do arquivo diretamente no Azure, antes do Ansible registrar o resultado.

### Differential — Backup Diferencial

Captura apenas os dados que mudaram desde o último Full. Muito mais rápido e menor em tamanho, ideal para execuções diárias quando o Full é semanal.

```bash
ansible-playbook playbook-backup.yml -e backup_type=diff --ask-vault-pass
```

```sql
BACKUP DATABASE [AppDB]
TO URL = N'https://minhaconta.blob.core.windows.net/sql-backup-diff/sql01/2026-04-24/sql01_AppDB_DIFF_20260424120000.bak'
WITH
    DIFFERENTIAL,
    COMPRESSION,
    STATS = 10,
    CHECKSUM;
```

### Transaction Log — Backup de Log de Transações

Captura todas as transações registradas no log desde o último backup de log. Permite restaurar o banco para qualquer ponto no tempo (point-in-time recovery). Requer que o banco use o modelo de recuperação FULL ou BULK_LOGGED — o script verifica isso antes de executar.

```bash
ansible-playbook playbook-backup.yml -e backup_type=log --ask-vault-pass
```

```sql
BACKUP LOG [AppDB]
TO URL = N'https://minhaconta.blob.core.windows.net/sql-backup-log/sql01/2026-04-24/sql01_AppDB_LOG_20260424150000.bak'
WITH
    COMPRESSION,
    STATS = 10,
    CHECKSUM;
```

## Fluxo Interno de Cada Backup

Para cada banco, a role `mssql_backup` executa na sequência:

1. Cria ou atualiza o SQL Server CREDENTIAL com o SAS Token (via `win_shell` + `sqlcmd`, `no_log: true`)
2. Monta a URL de destino: `{conta}/{container}/{host}/{data}/{host}_{banco}_{tipo}_{timestamp}.bak`
3. Gera o script `.sql` via `win_template` (Jinja2) e salva em `C:\Windows\Temp\`
4. Executa o backup com `sqlcmd` — o SQL Server abre conexão TLS direto para o Azure e faz o stream
5. Verifica integridade com `RESTORE VERIFYONLY FROM URL` (quando `verify_backup: true`)
6. Remove o script `.sql` temporário do SQL Server

A máquina ops envia apenas texto (script SQL + comandos WinRM). Nenhum byte de dados de backup trafega por ela.

## Playbook de Restore

O restore suporta quatro modos:

| Modo | O que aplica |
|---|---|
| `full` | Somente backup Full |
| `full_diff` | Full + Differential mais recente |
| `full_diff_log` | Full + Diff + todos os Logs em sequência |
| `point_in_time` | Full + Diff + Logs até um STOPAT específico |

O playbook lista os blobs disponíveis no Azure via API REST (apenas metadados, sem download) usando o módulo `uri` do Ansible, e passa as URLs para o SQL Server executar `RESTORE FROM URL`:

```bash
# Restore simples
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_target_host=sql01 \
  -e restore_date=2026-04-24 \
  --ask-vault-pass

# Point-in-time recovery
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_target_host=sql01 \
  -e restore_date=2026-04-24 \
  -e restore_mode=point_in_time \
  -e restore_stopat="2026-04-24T14:30:00" \
  --ask-vault-pass

# Restaurar com nome diferente (não sobrescreve o banco original)
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_new_name=AppDB_RestoreTest \
  -e restore_target_host=sql01 \
  -e restore_date=2026-04-24 \
  -e restore_mode=full_diff \
  --ask-vault-pass
```

O script T-SQL de restore lê os arquivos diretamente do Azure, gerenciando o estado do banco durante a sequência:

```sql
-- FULL com NORECOVERY (banco fica em "restaurando" para aceitar diff/log)
RESTORE DATABASE [AppDB]
FROM URL = N'https://minhaconta.blob.core.windows.net/sql-backup-full/sql01/2026-04-24/sql01_AppDB_FULL_20260424030000.bak'
WITH NORECOVERY, REPLACE, STATS = 10;

-- DIFF com NORECOVERY
RESTORE DATABASE [AppDB]
FROM URL = N'https://minhaconta.blob.core.windows.net/sql-backup-diff/sql01/2026-04-24/sql01_AppDB_DIFF_20260424120000.bak'
WITH NORECOVERY, STATS = 10;

-- LOG final com RECOVERY (encerra a sequência) e STOPAT opcional
RESTORE LOG [AppDB]
FROM URL = N'https://minhaconta.blob.core.windows.net/sql-backup-log/sql01/2026-04-24/sql01_AppDB_LOG_20260424150000.bak'
WITH STOPAT = '2026-04-24 14:30:00', RECOVERY;

-- Volta para multi-user
ALTER DATABASE [AppDB] SET MULTI_USER;
```

O uso de `NORECOVERY` em todos os passos exceto o último é obrigatório — ele mantém o banco em modo de restauração para aceitar os próximos arquivos. Apenas o último comando usa `RECOVERY`, que finaliza a sequência e coloca o banco online.

## Segurança

Todos os segredos ficam no vault — nunca em texto plano:

```bash
# Criptografar SAS token do Azure (permissões: read + write + create + list)
ansible-vault encrypt_string 'sv=2022-11-02&ss=b...' --name 'vault_azure_sas_token'

# Criptografar senha WinRM
ansible-vault encrypt_string 'SenhaDoServico123!' --name 'vault_winrm_password'

# Criptografar senha SQL
ansible-vault encrypt_string 'SenhaSql123!' --name 'mssql_password'
```

O SAS Token é passado para o SQL Server dentro do script T-SQL gerado em `C:\Windows\Temp\` com `no_log: true` no Ansible, e o arquivo temporário é removido imediatamente após a execução. O token nunca aparece nos logs do Ansible nem no histórico do shell.

O usuário SQL usado (`backup_svc`) precisa das permissões mínimas para `BACKUP TO URL`:

```sql
CREATE LOGIN backup_svc WITH PASSWORD = 'SenhaSql123!';
GRANT CONNECT SQL TO backup_svc;
-- Em cada banco:
EXEC sp_addrolemember 'db_backupoperator', 'backup_svc';
GRANT VIEW DATABASE STATE TO backup_svc;
-- Para criar o CREDENTIAL (necessário para BACKUP TO URL):
GRANT ALTER ANY CREDENTIAL TO backup_svc;
```

## Executando

```bash
# Testar conectividade antes de tudo
ansible sqlservers -m win_ping --ask-vault-pass

# Backup Full de todos os bancos (recomendado: madrugada — ex: 02:00)
ansible-playbook playbook-backup.yml -e backup_type=full --ask-vault-pass

# Backup Full de um banco específico
ansible-playbook playbook-backup.yml -e backup_type=full -e target_db=AppDB --ask-vault-pass

# Backup Differential (pode rodar durante o dia — arquivo menor, menos impacto de rede)
ansible-playbook playbook-backup.yml -e backup_type=diff --ask-vault-pass

# Backup de Log (pode rodar a cada hora — arquivo pequeno, impacto mínimo)
ansible-playbook playbook-backup.yml -e backup_type=log --ask-vault-pass

# Restore full + diff + log (recomendado: madrugada — evita concorrência com queries ativas)
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_target_host=sql01 \
  -e restore_date=2026-04-24 \
  -e restore_mode=full_diff_log \
  --ask-vault-pass
```

### Agendamento sugerido (cron no controller)

```cron
# Full todo domingo às 02:00
0 2 * * 0  cd /opt/ansible/mssql-backup && ansible-playbook playbook-backup.yml -e backup_type=full  --vault-password-file=.vault_pass

# Differential de segunda a sábado às 02:00
0 2 * * 1-6 cd /opt/ansible/mssql-backup && ansible-playbook playbook-backup.yml -e backup_type=diff  --vault-password-file=.vault_pass

# Transaction Log a cada hora (bancos com recovery_model FULL)
0 * * * *   cd /opt/ansible/mssql-backup && ansible-playbook playbook-backup.yml -e backup_type=log   --vault-password-file=.vault_pass
```

## Lifecycle Management — Reduzindo Custo de Armazenamento

O `BACKUP TO URL` grava os arquivos no tier **Hot** por padrão. Isso faz sentido nos primeiros dias, quando a chance de precisar de um restore rápido é maior. Mas backups são arquivos que você escreve uma vez e só lê em emergência — manter meses de backups no tier Hot é jogar dinheiro fora.

O Azure Blob Storage oferece quatro tiers de armazenamento, cada um com custo e latência de acesso diferentes:

| Tier | Custo/GB/mês (aprox.) | Acesso | Uso ideal |
|---|---|---|---|
| **Hot** | ~$0.018 | Imediato | Backups recentes (últimos 7 dias) |
| **Cool** | ~$0.010 | Imediato | Backups da última semana a um mês |
| **Cold** | ~$0.0036 | Imediato | Backups de 1 a 3 meses |
| **Archive** | ~$0.002 | Horas para reidratar | Retenção longa ou compliance |

A diferença é significativa: um backup de 100 GB no tier Hot custa ~$1.80/mês, no Cold custa ~$0.36/mês. Em um ambiente com vários servidores e meses de retenção, a economia acumula rápido.

### Lifecycle Management Policy

Em vez de mover blobs manualmente entre tiers, o Azure permite criar uma **Lifecycle Management Policy** no Storage Account. Essa política é avaliada automaticamente uma vez por dia e move os blobs entre tiers com base na idade — sem script, sem cron, sem custo de operação.

A estratégia recomendada para backups:

```
0-7 dias   → Hot      (restore imediato se precisar)
7-30 dias  → Cool     (metade do custo)
30-90 dias → Cold     (1/5 do custo)
90+ dias   → Archive ou deletar (conforme retenção exigida)
```

### Configurando via Azure CLI

Primeiro, crie um arquivo JSON com a política de lifecycle. Este exemplo aplica a movimentação progressiva entre tiers e deleta backups com mais de 365 dias:

```json
{
  "rules": [
    {
      "enabled": true,
      "name": "backup-lifecycle",
      "type": "Lifecycle",
      "definition": {
        "actions": {
          "baseBlob": {
            "tierToCool": {
              "daysAfterModificationGreaterThan": 7
            },
            "tierToCold": {
              "daysAfterModificationGreaterThan": 30
            },
            "tierToArchive": {
              "daysAfterModificationGreaterThan": 90
            },
            "delete": {
              "daysAfterModificationGreaterThan": 365
            }
          }
        },
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": [
            "sql-backup-full/",
            "sql-backup-diff/",
            "sql-backup-log/"
          ]
        }
      }
    }
  ]
}
```

O filtro `prefixMatch` garante que a política se aplica apenas aos containers de backup, sem afetar outros blobs na mesma Storage Account.

Agora aplique a política na Storage Account:

```bash
# Aplicar a lifecycle policy
az storage account management-policy create \
  --account-name minhaconta \
  --resource-group meu-rg \
  --policy @lifecycle-policy.json

# Verificar a política aplicada
az storage account management-policy show \
  --account-name minhaconta \
  --resource-group meu-rg
```

### Considerações sobre Archive e Restore

O tier Archive tem o menor custo de armazenamento, mas a reidratação leva horas (Standard: até 15 horas, High Priority: até 1 hora com custo maior). Se o restore precisa ser rápido, considere usar Cold como tier final em vez de Archive — o custo é ligeiramente maior, mas o acesso é imediato.

Para verificar em qual tier cada blob está:

```bash
# Listar blobs com o tier de acesso
az storage blob list \
  --account-name minhaconta \
  --container-name sql-backup-full \
  --query "[].{name:name, tier:properties.blobTier, modified:properties.lastModified}" \
  --output table \
  --auth-mode login
```

A Lifecycle Policy é avaliada uma vez por dia pelo Azure. Após criar a política, os blobs existentes serão movidos gradualmente nas próximas 24-48 horas conforme as regras definidas.

## Para Que Serve no Mercado

Times de DBA e SRE que gerenciam ambientes com SQL Server Windows enfrentam o desafio de manter backups consistentes sem depender de jobs do SQL Server Agent configurados manualmente em cada instância. Com Ansible, a política de backup fica no código, versionada no Git, aplicável a qualquer número de servidores com um único comando.

O modelo `BACKUP TO URL` faz o SQL Server enviar o backup diretamente ao Azure via TLS, sem staging intermediário. A máquina de controle funciona apenas como orquestradora — sem impacto de I/O de dados, independente do tamanho dos backups. Isso permite escalar o número de servidores e bancos sem aumentar disco na infraestrutura Ansible.

O suporte a point-in-time recovery é o que diferencia um backup operacional de um backup de compliance — em caso de corrupção de dados, ransomware ou erro humano, a capacidade de restaurar para um momento específico pode ser a diferença entre minutos e horas de downtime.

## Conclusão

Automatizar backups não é apenas uma questão de conveniência — é uma prática de resiliência. Quando o restore precisa acontecer, não é hora de descobrir que o backup estava corrompido, desatualizado ou mal documentado. Este projeto aplica verificação de integridade no próprio Azure após cada backup (`RESTORE VERIFYONLY FROM URL`), cadeia de restore estruturada no código, segredos protegidos por vault e zero impacto de disco na máquina de controle — tornando o processo auditável, reproduzível e escalável.

## Referências

- [Documentação do Ansible para Windows](https://docs.ansible.com/ansible/latest/os_guide/windows_usage.html)
- [BACKUP TO URL — SQL Server para Microsoft Azure](https://learn.microsoft.com/pt-br/sql/relational-databases/backup-restore/sql-server-backup-to-url)
- [Criar um SQL Server Credential para autenticação no Azure](https://learn.microsoft.com/pt-br/sql/relational-databases/backup-restore/sql-server-backup-to-url#credential)
- [T-SQL BACKUP DATABASE](https://learn.microsoft.com/pt-br/sql/t-sql/statements/backup-transact-sql)
- [T-SQL RESTORE DATABASE](https://learn.microsoft.com/pt-br/sql/t-sql/statements/restore-statements-transact-sql)
- [ansible-vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [Lifecycle Management Policy — Azure Blob Storage](https://learn.microsoft.com/pt-br/azure/storage/blobs/lifecycle-management-overview)
- [Access Tiers — Hot, Cool, Cold, Archive](https://learn.microsoft.com/pt-br/azure/storage/blobs/access-tiers-overview)
