---
title: "Tcpdump"
date: 2020-09-30T20:58:47-03:00
draft: false
---

TCPDump

O TCPDump funciona em linha de comando, para captura e análise de pacotes. Já vem instalado por padrão em diversas distribuições Linux, foi também portado para o Windows com o nome de Windump. O TCPDump provê uma interface de usuário para a interação com a LibPcap, biblioteca amplamente utilizada por sniffers open source, que atua diretamente no driver da placa de rede para possibilitar a captura de pacotes. 

`# tcpdump`

Rodando o comando diretamente como root, ele vai começar a filtrar todos os pacotes. Incluindo todas as interfaces. 

Para fazer uma busca especifica por uma interface, wireless por exemplo, basta setar na frente do tcpdump o nome da mesma. 

`# tcpdump -v -i wlp3s01`
