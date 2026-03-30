---
title: "Netcat"
date: 2020-07-22T23:02:18-03:00
draft: false
tags: ["segurança", "redes", "ferramentas"]
---

## Netcat

O Netcat é um utilitário que lê e grava dados nas conexões de rede, usando o protocolo TCP ou UDP. Foi projetado para ser uma ferramenta confiável de "back-end" que pode ser usada diretamente ou acionada por outros programas e scripts. É também uma ferramenta rica em recursos para depuração e exploração de rede, pois pode criar quase qualquer tipo de conexão. Usos comuns incluem:

- Proxies TCP simples
- Clientes e servidores HTTP baseados em shell-script
- Teste de daemon de rede
- SOCKS ou HTTP ProxyCommand para SSH
Sintaxe:

`$ nc -nlvp 1234`

`-n` Não faça pesquisas de serviço ou DNS em endereços, nomes de host ou portas especificados.

`-l` Usado para especificar que o nc deve escutar uma conexão de entrada em vez de iniciar uma conexão com um host remoto. É um erro usar esta opção em conjunto com as opções -p, -s ou -z. Além disso, qualquer tempo limite especificado com a opção -w é ignorado.

`-v` Faça nc dar uma saída mais detalhada.

`-p` source_port Especifica a porta de origem que a nc deve usar, sujeita a restrições e disponibilidade de privilégios.

Ou seja, com ele podemos ouvir portas TCP/UDP — basta colocar o `nc` escutando na porta 1234 aguardando uma conexão, para usar um shell reverso, por exemplo.