---
title: "Proxychain"
date: 2021-02-03T11:49:14-03:00
draft: false
tags: ["segurança", "redes", "ferramentas"]
---

O ProxyChains é um programa que trabalha em base UNIX, que conecta funções relacionadas à rede em programas vinculados dinamicamente por meio de uma DLL pré-carregada e redireciona as conexões por meio de proxies SOCKS4 e SOCKS5 ou HTTP.

Ao invés de realizar o roteamento para uma lista específica de proxies, podemos usar o Tor e redirecionar as requisições diretamente para a porta do Tor. Ou seja, realizamos varreduras diretamente pela rede Tor.

```sh
$ sudo apt-get install proxychains
$ sudo apt-get install tor
```
Dentro do arquivo de config do proxychains:
```sh
root@kali:~#: nano /etc/proxychains.conf  
```
Comentar a linha "strict_chain"

Descomentar a linha "dynamic_chain"

![POSTS](/proxychain1.png)

Explicação rápida sobre eles:

Strict Chain

**Strict Chain** é a opção padrão do Proxychains. Todas as conexões passam pelos proxies na ordem listada no arquivo de configuração. É útil quando você sabe que os proxies selecionados estão funcionando bem. Para usar, descomente `strict_chain` no arquivo de configuração.

**Dynamic Chain** funciona de forma similar à Strict Chain — usa todos os proxies listados, mas ignora os que estiverem mortos ou fora do ar. Para usar, descomente `dynamic_chain` e comente `random_chain` e `strict_chain`.

**Random Chain** significa aleatoriedade: as conexões passam por proxies escolhidos aleatoriamente da sua lista. Para usar, descomente `random_chain` e comente `dynamic_chain` e `strict_chain`.

Se estiver usando o `random_chain`, descomente a linha `chain_len`, que define quantos IPs da lista serão encadeados aleatoriamente.

Por padrão vem selecionado Strict Chain. Por isso comentamos `strict_chain` e descomentamos `dynamic_chain` para que o Proxychains trabalhe de forma dinâmica.

E agora no final deste mesmo arquivo, vamos adicionar a linha:

```
socks5   127.0.0.1     9050
```

![POSTS](/proxychain2.png)

# Inicializando o serviço do tor

```sh
root@kali:~#: service tor start  
root@kali:~#: service tor status  
```

# Testando a Conexão 

Abra o Firefox ou Iceweasel e acesse a URL http://www.meuip.com.br/ para pegar o seu IP atual

```sh
root@kali:~#: proxychains firefox  
```

Agora acesse o 'utrace' e coloque o IP do seu Proxy para saber a localização do servidor que você está utilizando como Gateway em http://en.utrace.de/

Se estiver tudo certo, e ele te mostrar a origem do server, está pronto!

Agora, para realizar qualquer varredura, basta executar o comando com `proxychains` na frente: `proxychains + [aplicação]`. O Proxychains vai tunelar o tráfego de qualquer aplicação.


# Realizando uma varredura via Proxychains 

```sh
root@kali:~#: proxychains nmap -sC -sS 177.126.175.230  
```

