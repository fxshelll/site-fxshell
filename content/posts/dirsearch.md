---
title: ""
date: 2020-07-22T23:37:57-03:00
draft: false
---

## DIRSEARCH
================
`https://github.com/maurosoria/dirsearch`


O `dirsearch` é uma ferramenta simples de linha de comando projetada para diretórios e arquivos de força bruta em sites.

Particularmente prefiro ele ao invés do `DIRB` ou `GoBuster`, já obtive mais resultados com ele, porém depois vou escrever sobre essas outras duas ferramentas aqui também.

## Uso

git clone https://github.com/maurosoria/dirsearch.git

`$ cd dirsearch`

`python3 dirsearch.py -u <URL> -e <EXTENSION>`

## Exemplo

`$ python3 dirsearch.py -u http://sitedoalvo.com.br(ou IP) -e *`

```py
 _|. _ _  _  _  _ _|_    v0.3.9
(_||| _) (/_(_|| (_| )

Extensions:  | HTTP method: getSuffixes: CHANGELOG.md | HTTP method: get | Threads: 10 | Wordlist size: 6552 | Request count: 6552

Error Log: /root/dirsearch/logs/errors-20-06-29_23-59-23.log

Target: http://10.10.10.185

Output File: /root/dirsearch/reports/10.10.10.185/20-06-29_23-59-24

[23:59:24] Starting: 
[00:00:12] 301 -  313B  - /images  ->  http://10.10.10.185/images/
[00:00:14] 403 -  277B  - /index.shtml
[00:00:14] 200 -   67KB - /index.php
[00:00:14] 200 -   67KB - /index.php/login/
[00:00:14] 403 -  277B  - /install.sql
[00:00:17] 403 -  277B  - /localhost.sql
[00:00:17] 403 -  277B  - /log.sqlite
[00:00:18] 200 -    4KB - /login.php
[00:00:18] 403 -  277B  - /login.shtml
[00:00:19] 403 -  277B  - /logs.sqlite
```

O dirsearch vai encontrar pastas e urls uteis para a exploração de vulnerabilidades. 






