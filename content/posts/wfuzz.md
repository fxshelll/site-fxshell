---
title: "Wfuzz"
date: 2020-07-31T01:13:20-03:00
draft: false
tags: ["segurança", "ctf", "ferramentas"]
---

É uma ferramenta de fuzzing criada para facilitar a avaliação de aplicações web. Baseia-se num conceito simples: substitui qualquer referência à palavra-chave `FUZZ` pelo valor de um determinado payload. Um payload no Wfuzz é uma fonte de dados.

```sh
wfuzz -c -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt --hc 404 http://10.15.0.1/FUZZ
```

`-c` colorir saída

`-w` caminho da wordlist

`--hc` ignorar códigos de resposta (ex: 404)