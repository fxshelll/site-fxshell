---
title: "Automatizando Backups de SQL Server no Azure com Ansible"
date: 2026-04-21
draft: false
tags: ["ansible", "sqlserver", "azure", "devops", "backup", "windows", "automation", "sre"]
---

Manter backups consistentes de múltiplos SQL Servers e armazená-los em nuvem é uma tarefa crítica que, quando feita manualmente, vira fonte de erros, esquecimentos e surpresas na hora de um restore. Este lab mostra como resolver isso com Ansible rodando em uma máquina Linux, alcançando servidores Windows via WinRM e enviando os arquivos `.bak` diretamente para o Azure Blob Storage.

## Objetivo do Lab

Construir uma automação completa que, a partir de uma máquina Linux, conecta em múltiplos SQL Servers Windows, executa os três tipos de backup que o SQL Server suporta (Full, Differential e Transaction Log) e faz o upload para o Azure Blob Storage com verificação de integridade. O projeto inclui também um playbook de restore com suporte a ponto no tempo (point-in-time recovery).

## Tecnologias Utilizadas

**Ansible** é a ferramenta de automação de infraestrutura que orquestra todo o fluxo. Ela executa tarefas em hosts remotos sem precisar instalar agentes — usa SSH para Linux e WinRM para Windows. No mercado é amplamente usada por times DevOps e SRE para padronizar operações repetitivas.

**WinRM** (Windows Remote Management) é o protocolo da Microsoft equivalente ao SSH para Windows. O Ansible usa ele, com autenticação NTLM, para executar comandos em servidores Windows sem precisar de nenhum agente instalado.

**sqlcmd** é a ferramenta de linha de comando do SQL Server para executar scripts T-SQL. O Ansible gera o script `.sql` via template Jinja2 e chama o `sqlcmd` remotamente para executá-lo.

**T-SQL** é a linguagem de consulta e administração do SQL Server. Os scripts de backup e restore são escritos em T-SQL e gerados dinamicamente pelo Ansible conforme os parâmetros de cada banco.

**azcopy** é a ferramenta CLI da Microsoft para transferir dados de e para o Azure Blob Storage. É instalada na máquina ops (Linux) e utiliza um SAS Token para autenticação sem expor credenciais de conta.

**ansible-vault** é o mecanismo de criptografia do Ansible para proteger variáveis sensíveis — senhas, tokens, chaves — dentro dos arquivos de inventário e variáveis do projeto.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKUP FLOW                                       │
│                                                                      │
│  ┌──────────────┐   WinRM/NTLM   ┌──────────┐  ┌──────────┐       │
│  │   ops-linux  │ ─────────────► │  sql01   │  │  sql02   │       │
│  │  (Ansible)   │ ◄────────────  │  sql03   │  │  ...     │       │
│  └──────┬───────┘  fetch .bak    └──────────┘  └──────────┘       │
│         │ azcopy                                                    │
│         ▼                                                           │
│  ┌──────────────────────────────────────────┐                      │
│  │           Azure Blob Storage             │                      │
│  │  📦 sql-backup-full                      │                      │
│  │  📦 sql-backup-diff                      │                      │
│  │  📦 sql-backup-log                       │                      │
│  └──────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    RESTORE FLOW                                      │
│                                                                      │
│  ┌──────────────────────────────────────────┐                      │
│  │           Azure Blob Storage             │                      │
│  │  📦 containers (full/diff/log)           │                      │
│  └──────────────────┬───────────────────────┘                      │
│                     │ azcopy download                               │
│                     ▼                                               │
│  ┌──────────────┐  win_copy + sqlcmd  ┌────────────────┐           │
│  │   ops-linux  │ ──────────────────► │   sql-target   │           │
│  └──────────────┘                     │  (RESTORE)     │           │
│                                       └────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

| Componente | Função |
|---|---|
| `ops-linux` | Máquina Ansible Controller — orquestra tudo, roda o azcopy |
| `sql01..03` | SQL Servers Windows — onde os backups são gerados |
| `sqlcmd` | Executa os scripts T-SQL de backup/restore |
| `azcopy` | Transfere os `.bak` entre a máquina ops e o Azure |
| `Azure Blob Storage` | Destino final dos backups, separados por containers |

![Diagrama animado — Ansible MSSQL Backup → Azure](/ansible-mssql-backup-azure.gif)

## Estrutura do Projeto

```
ansible-mssql-backup-azure/
├── ansible.cfg
├── inventory/
│   └── hosts.ini
├── group_vars/
│   ├── all.yml          # Azure storage + azcopy
│   └── sqlservers.yml   # credenciais SQL + lista de bancos
├── playbook-backup.yml
├── playbook-restore.yml
└── roles/
    ├── mssql_backup/
    │   ├── tasks/
    │   │   ├── main.yml
    │   │   ├── full.yml
    │   │   ├── diff.yml
    │   │   └── log.yml
    │   └── templates/
    │       ├── backup_full.sql.j2
    │       ├── backup_diff.sql.j2
    │       └── backup_log.sql.j2
    └── mssql_restore/
        ├── tasks/
        │   ├── main.yml
        │   └── restore.yml
        └── templates/
            └── restore.sql.j2
```

## Inventário e Variáveis

O inventário separa claramente os dois tipos de host: a máquina ops (conexão local) e os SQL Servers (WinRM):

```ini
[ops]
ops01 ansible_host=192.168.1.10 ansible_connection=local

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

Em `group_vars/all.yml`, as credenciais do Azure ficam protegidas com vault:

```yaml
azure_storage_account: "minhaconta"
azure_container_full:  "sql-backup-full"
azure_container_diff:  "sql-backup-diff"
azure_container_log:   "sql-backup-log"

vault_azure_sas_token: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  <criptografado>
```

Para criar o vault:

```bash
ansible-vault encrypt_string 'seu-sas-token' --name 'vault_azure_sas_token'
```

## Os Três Tipos de Backup

### Full — Backup Completo

O backup Full captura o banco inteiro. É sempre o ponto de partida para qualquer cadeia de restore.

```bash
ansible-playbook playbook-backup.yml -e backup_type=full --ask-vault-pass
```

O script T-SQL gerado pelo template:

```sql
BACKUP DATABASE [AppDB]
TO DISK = N'C:\SQLBackups\Staging\sql01_AppDB_FULL_20240715_030000.bak'
WITH
    FORMAT, INIT,
    NAME = N'AppDB - Full Backup 2024-07-15 03:00:00',
    COMPRESSION,
    STATS = 10,
    CHECKSUM;
```

Após o backup, o Ansible executa `RESTORE VERIFYONLY` para confirmar que o arquivo não está corrompido antes de enviá-lo ao Azure.

### Differential — Backup Diferencial

Captura apenas os dados que mudaram desde o último Full. Muito mais rápido e menor em tamanho, ideal para execuções diárias quando o Full é semanal.

```bash
ansible-playbook playbook-backup.yml -e backup_type=diff --ask-vault-pass
```

```sql
BACKUP DATABASE [AppDB]
TO DISK = N'C:\SQLBackups\Staging\sql01_AppDB_DIFF_20240715_120000.bak'
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
-- Verifica modelo de recuperação antes de prosseguir
IF (SELECT recovery_model_desc FROM sys.databases WHERE name = 'AppDB') = 'SIMPLE'
BEGIN
    RAISERROR('Banco AppDB usa modelo SIMPLE — backup de log não suportado.', 16, 1);
    RETURN;
END

BACKUP LOG [AppDB]
TO DISK = N'C:\SQLBackups\Staging\sql01_AppDB_LOG_20240715_150000.bak'
WITH
    COMPRESSION,
    STATS = 10,
    CHECKSUM;
```

## Fluxo Interno de Cada Backup

Para cada banco, a role `mssql_backup` executa na sequência:

1. Define o nome do arquivo com hostname + banco + tipo + timestamp
2. Gera o script `.sql` via `win_template` (Jinja2)
3. Executa o backup com `sqlcmd` via `win_shell`
4. Verifica a integridade com `RESTORE VERIFYONLY` (quando `verify_backup: true`)
5. Faz o `fetch` do `.bak` para a máquina ops (`/tmp/mssql-backups/`)
6. Executa o `azcopy copy` via `delegate_to: localhost` para enviar ao Azure
7. Remove o arquivo da máquina ops e do SQL Server (staging limpo)

O `delegate_to: localhost` é um detalhe importante: embora a task seja definida dentro do play dos `sqlservers`, o azcopy precisa rodar na máquina ops, que é quem tem acesso ao Azure. Isso instrui o Ansible a executar aquela task específica na máquina de controle.

## Playbook de Restore

O restore suporta quatro modos:

| Modo | O que aplica |
|---|---|
| `full` | Somente backup Full |
| `full_diff` | Full + Differential mais recente |
| `full_diff_log` | Full + Diff + todos os Logs em sequência |
| `point_in_time` | Full + Diff + Logs até um STOPAT específico |

```bash
# Restore simples
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_mode=full \
  --ask-vault-pass

# Point-in-time recovery
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_mode=point_in_time \
  -e restore_stopat="2024-07-15 14:30:00" \
  --ask-vault-pass

# Restaurar com nome diferente (não sobrescreve o banco original)
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_new_name=AppDB_RestoreTest \
  -e restore_mode=full_diff \
  --ask-vault-pass
```

O script T-SQL de restore gerencia o estado do banco durante a sequência:

```sql
-- Força desconexão de sessões ativas
ALTER DATABASE [AppDB] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

-- FULL com NORECOVERY (banco fica em "restaurando" para aceitar diff/log)
RESTORE DATABASE [AppDB]
FROM DISK = N'C:\SQLBackups\Restore\sql01_AppDB_FULL_20240715_030000.bak'
WITH NORECOVERY, REPLACE, STATS = 10;

-- DIFF com NORECOVERY
RESTORE DATABASE [AppDB]
FROM DISK = N'C:\SQLBackups\Restore\sql01_AppDB_DIFF_20240715_120000.bak'
WITH NORECOVERY, STATS = 10;

-- LOG final com RECOVERY (encerra a sequência) e STOPAT opcional
RESTORE LOG [AppDB]
FROM DISK = N'C:\SQLBackups\Restore\sql01_AppDB_LOG_20240715_150000.bak'
WITH STOPAT = '2024-07-15 14:30:00', RECOVERY;

-- Volta para multi-user
ALTER DATABASE [AppDB] SET MULTI_USER;
```

O uso de `NORECOVERY` em todos os passos exceto o último é obrigatório — ele mantém o banco em modo de restauração para aceitar os próximos arquivos. Apenas o último comando usa `RECOVERY`, que finaliza a sequência e coloca o banco online.

## Segurança

Todos os segredos ficam no vault — nunca em texto plano:

```bash
# Criptografar SAS token do Azure
ansible-vault encrypt_string 'sv=2022-11-02&ss=b...' --name 'vault_azure_sas_token'

# Criptografar senha WinRM
ansible-vault encrypt_string 'SenhaDoServico123!' --name 'vault_winrm_password'

# Criptografar senha SQL
ansible-vault encrypt_string 'SenhaSql123!' --name 'mssql_password'
```

O SAS Token é passado via variável de ambiente para o `azcopy`, evitando que apareça no histórico do shell:

```bash
AZCOPY_SAS_TOKEN="{{ vault_azure_sas_token }}" azcopy copy ...
```

O usuário SQL usado (`backup_svc`) precisa apenas das permissões mínimas:

```sql
-- No SQL Server, criar usuário com privilégios mínimos
CREATE LOGIN backup_svc WITH PASSWORD = 'SenhaSql123!';
GRANT CONNECT SQL TO backup_svc;
-- Em cada banco:
EXEC sp_addrolemember 'db_backupoperator', 'backup_svc';
GRANT VIEW DATABASE STATE TO backup_svc;
```

## Executando

```bash
# Testar conectividade antes de tudo
ansible sqlservers -m win_ping --ask-vault-pass

# Backup Full de todos os bancos
ansible-playbook playbook-backup.yml -e backup_type=full --ask-vault-pass

# Backup Full de um banco específico
ansible-playbook playbook-backup.yml -e backup_type=full -e target_db=AppDB --ask-vault-pass

# Backup Differential
ansible-playbook playbook-backup.yml -e backup_type=diff --ask-vault-pass

# Backup de Log
ansible-playbook playbook-backup.yml -e backup_type=log --ask-vault-pass

# Restore full + diff + log
ansible-playbook playbook-restore.yml \
  -e restore_db=AppDB \
  -e restore_mode=full_diff_log \
  --ask-vault-pass
```

## Para Que Serve no Mercado

Times de DBA e SRE que gerenciam ambientes com SQL Server Windows enfrentam o desafio de manter backups consistentes sem depender de jobs do SQL Server Agent configurados manualmente em cada instância. Com Ansible, a política de backup fica no código, versionada no Git, aplicável a qualquer número de servidores com um único comando.

O modelo de ter a máquina ops como intermediária (Linux orquestrando Windows) é um padrão real em empresas que já adotaram Ansible para outros fins e querem unificar a automação. O Azure Blob Storage como destino elimina a necessidade de gerenciar servidores de backup e oferece retenção configurável, geo-redundância e custos baixos para armazenamento frio.

O suporte a point-in-time recovery é o que diferencia um backup operacional de um backup de compliance — em caso de corrupção de dados, ransomware ou erro humano, a capacidade de restaurar para um momento específico pode ser a diferença entre minutos e horas de downtime.

## Conclusão

Automatizar backups não é apenas uma questão de conveniência — é uma prática de resiliência. Quando o restore precisa acontecer, não é hora de descobrir que o backup estava corrompido, desatualizado ou mal documentado. Este projeto aplica verificação de integridade antes do upload, cadeia de restore estruturada no código e segredos protegidos por vault, tornando o processo auditável e reproduzível da mesma forma em desenvolvimento e produção.

## Referências

- [Documentação do Ansible para Windows](https://docs.ansible.com/ansible/latest/os_guide/windows_usage.html)
- [Documentação do azcopy](https://learn.microsoft.com/pt-br/azure/storage/common/storage-use-azcopy-v10)
- [T-SQL BACKUP DATABASE](https://learn.microsoft.com/pt-br/sql/t-sql/statements/backup-transact-sql)
- [T-SQL RESTORE DATABASE](https://learn.microsoft.com/pt-br/sql/t-sql/statements/restore-statements-transact-sql)
- [ansible-vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
