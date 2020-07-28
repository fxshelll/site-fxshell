---
title: "GoBuster"
date: 2020-07-27T23:44:29-03:00
draft: false
---

GoBuster Primo do DIRB

O Gobuster é uma ótima ferramenta utilizada para força bruta em URI’s (diretórios e arquivos) 
    
```sh
    -fw – força o processamento de um domínio com resultados curinga.
    -np – oculta a saída do progresso.
    -m <modo> – qual modo usar, dir ou dns (padrão: dir).
    -q – desativa a saída de banner / sublinhado.
    -t <threads> – número de encadeamentos a serem executados (padrão: 10).
    -u <url / domain> – URL completo (incluindo esquema) ou nome de domínio base.
    -v – saída detalhada (mostra todos os resultados).
    -w <wordlist> – caminho para a lista de palavras usada para força bruta (use – para stdin).
```

Eu poderia usar o DIRB? Sim, por que ele vai fazer o scanning de páginas também. Ficaria assim: 

`$ dirb http://192.168.219.128:65535 /usr/share/dirb/wordlists/big.txt`

Com o GoBuster faria o brute force + o scanning de diretórios, utilizando a mesma wordlist do DIRB.

`$ gobuster dir -u http://192.168.219.128:65535 -w /usr/share/dirb/wordlists/big.txt`

```py
-w <wordlist>
-u <url>
```