---
title: "Netcat"
date: 2020-07-22T23:02:18-03:00
draft: false
---

## Netcat
================

O Netcat é um utilitário que lê e grava dados nas conexões de rede, usando o protocolo TCP ou UDP. Ele foi projetado para ser uma ferramenta confiável de "back-end" que pode ser usada diretamente ou direcionada por outros programas e scripts. Ao mesmo tempo, é uma ferramenta de depuração e exploração de rede rica em recursos, pois pode criar quase qualquer tipo de conexão que você precisa e possui vários recursos internos interessantes. Os usos comuns incluem:

```sh
+ Proxies TCP simples

+ Clientes e servidores HTTP baseados em shell-script

+ Teste de daemon de rede

+ A Socks ou HTTP ProxyCommand para ssh
```
Sintaxe:

`$ nc -nlvp 1234`

`-n` Não faça pesquisas de serviço ou DNS em endereços, nomes de host ou portas especificados.

`-l` Usado para especificar que o nc deve escutar uma conexão de entrada em vez de iniciar uma conexão com um host remoto. É um erro usar esta opção em conjunto com as opções -p, -s ou -z. Além disso, qualquer tempo limite especificado com a opção -w é ignorado.

`-v` Faça nc dar uma saída mais detalhada.

`-p` source_port Especifica a porta de origem que a nc deve usar, sujeita a restrições e disponibilidade de privilégios.

Ou seja, com ele podemos ouvir a porta TCP/UDP podemos colocar o nc  escutando na porta 1234 uma conexão, para usar um shell reverso por exemplo. 