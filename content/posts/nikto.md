---
title: "Nikto"
date: 2020-07-22T22:47:23-03:00
draft: false
---

## NIKTO
================

Examine o servidor da Web em busca de vulnerabilidades conhecidas, incluindo:

- Configurações incorretas de servidor e software
- Arquivos e programas padrão
- Arquivos e programas inseguros
- Servidores e programas desatualizados

Não é necessário fazer a instalação do mesmo pois ele é um script perl.

Ele vem nativo no kali, para atualizar recomendo baixar direto do git deles. 

`https://github.com/sullo/nikto`

```html
git clone https://github.com/sullo/nikto

# Main script is in program/
cd nikto/program

# Run using the shebang interpreter
./nikto.pl -h http://www.example.com

# Run using perl (if you forget to chmod)
perl nikto.pl -h http://www.example.com
```
```sh
-h + alvo (por padrão setada porta 80)
-o posso gerar relatório em html ou txt, csv. 
-p posso setar as portas que quero separados por virgula. 
```
exemplo:
========
nikto -h 192.168.0.126 -p 8081, 443 -o scan.html

Toda vez que precisar rodar o nikto em diferentes diretorios do seu alvo, é necessário colocar o 'http' na frente. 

`ex: nikto -h http://192.168.0.126/files -p 8081, 443 -o scan.html`