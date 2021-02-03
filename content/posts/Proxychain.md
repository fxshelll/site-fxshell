---
title: "Proxychain"
date: 2021-02-03T11:49:14-03:00
draft: false
---

O ProxyChains é um programa que trabalha em base UNIX, que conecta funções relacionadas à rede em programas vinculados dinamicamente por meio de uma DLL pré-carregada e redireciona as conexões por meio de proxies SOCKS4 e SOCKS5 ou HTTP.

Ao invés do Proxychains realizar o roteamento para uma lista específica de proxys, podemos usar o Tor Router e redirecionar as requisições diretamente para a porta do Tor. Ou seja, iremos realizar varreduras diretamente pela Tor.

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

*Strict Chain* é a opção padrão em proxychains. Nesta opção, todas as conexões passam pelos proxies na ordem listada no arquivo de configuração. Strict Chain é muito útil quando você deseja sua localização e sabe que os proxies selecionados estão funcionando bem. Para usar Strict Chain, é necessário descomentar “strict_chain” no arquivo de configuração.
Dynamic Chain

*Dynamic Chain* funciona da mesma maneira que uma Strict Chain, é usado todos os proxies que estão no arquivo de configuração, mas é ignorado ou exclui os proxies da cadeia que está morta ou não está funcionando no momento. Para usar uma Dynamic Chain, remova o comentário de “Dynamic_Chain” e comente “random_chain” e “strict_chain” no arquivo de configuração.
Random Chain

*Random Chain* significa aleatoriedade, o que significa que todas as conexões passam por um proxy listado no seu arquivo de configuração, mas aleatoriamente, ninguém adivinha quais proxies são os próximos. Para usar Random Chain, é necessário descomentar “random_chain” e comentar “dynamic chain” e “strict_chain” no arquivo de configuração.

Se você estiver usando o random_chain, descomente a linha “chain_len”, que permite o encadeamento dinâmico. Ele conecta um número de endereços IP na cadeia que são gerados aleatoriamente a partir da sua lista de proxies.

Por padrão vem selecionado Strict Chain, nós iremos comentar strict_chain e descomentar dynamic_chain para que o proxychains trabalhe a partir do dynamic_chain como demonstrado na imagem abaixo.

E agora no final deste mesmo arquivo, vamos adicionar a linha:

socks5   127.0.0.1     9050  

![POSTS](/proxychain2.png)

#Inicializando o serviço do tor

```sh
root@kali:~#: service tor start  
root@kali:~#: service tor status  
```

#Testando a Conexão 

Abra o Firefox ou Iceweasel e acesse a URL http://www.meuip.com.br/ para pegar o seu IP atual

```sh
 root@kali:~#: proxychains firefox  
```

Agora acesse o 'utrace' e coloque o IP do seu Proxy para saber a localização do servidor que você está utilizando como Gateway em http://en.utrace.de/

Se estiver tudo certo, e ele te mostrar a origem do server, está pronto!

Agora quando for realizar alguma varredura é só executar o comando com o proxychains na frente, utilizando o terminal digite proxychains + [ aplicação ]. O proxychains para tunelar o seu tráfego em qualquer aplicação.


#Realizando uma varredura via Proxychains 

```sh
root@kali:~#: proxychains nmap -sC -sS 177.126.175.230  
```

