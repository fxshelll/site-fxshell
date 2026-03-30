---
title: "GoBuster"
date: 2020-07-27T23:44:29-03:00
draft: false
tags: ["segurança", "ctf", "ferramentas"]
---

GoBuster — primo do DIRB

O GoBuster é uma ótima ferramenta utilizada para força bruta em URIs (diretórios e arquivos).

```bash
-fw  – força o processamento de um domínio com resultados curinga.
-np  – oculta a saída do progresso.
-m <modo>  – qual modo usar: dir ou dns (padrão: dir).
-q   – desativa a saída de banner/sublinhado.
-t <threads>  – número de threads a serem executadas (padrão: 10).
-u <url/domain>  – URL completo (incluindo esquema) ou nome de domínio base.
-v   – saída detalhada (mostra todos os resultados).
-w <wordlist>  – caminho para a wordlist usada na força bruta (use - para stdin).
```

Eu poderia usar o DIRB? Sim, pois ele também faz o scanning de páginas. Ficaria assim:

`$ dirb http://192.168.219.128:65535 /usr/share/dirb/wordlists/big.txt`

Com o GoBuster, faço o brute force + scanning de diretórios, usando a mesma wordlist do DIRB.

`$ gobuster dir -u http://192.168.219.128:65535 -w /usr/share/dirb/wordlists/big.txt`

Flags mais usadas:
```
-w <wordlist>
-u <url>
```