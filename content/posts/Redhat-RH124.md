---
title: "Redhat RH124"
date: 2021-03-16T23:03:55-03:00
draft: false
---

![HTB](/redhat0.png)

##  Red Hat System Administration I

O curso Red Hat System Administration I (RH124) foi desenvolvido para profissionais de TI sem experiência anterior em administração de sistemas Linux. O recurso tem como objetivo fornecer aos alunos "habilidades de sobrevivência" de administração do Linux, com foco em tarefas centrais de administração. O Red Hat System Administration I também oferece uma base para os alunos que planejam se tornar administradores de sistemas Linux em tempo integral, apresentando os principais conceitos de linha de comando e ferramentas de nível corporativo. Esses conceitos serão mais desenvolvidos no próximo curso, Red Hat System Administration II (RH134). 

##  Fedora

Fedora é um projeto comunitário que produz e lança um sistema operacional completo, gratuito e baseado em Linux. A Red Hat patrocina a comunidade e trabalha com representantes da comunidade para integrar o mais recente software upstream a uma distribuição rápida e segura. O projeto Fedora contribui com tudo de volta para o mundo open source livre, e qualquer pessoa pode participar.

No entanto, o Fedora se concentra na inovação e na excelência, e não na estabilidade de longo prazo. Novas atualizações importantes acontecem a cada seis meses e podem trazer mudanças significativas. O Fedora é compatível somente com lançamentos por cerca de um ano (duas atualizações principais), o que o torna menos adequado para uso empresarial. 

##  Red Hat Enterprise Linux

O Red Hat Enterprise Linux (RHEL) é a distribuição do Linux da Red Hat pronta para empresas e com suporte comercial. É a plataforma líder para computação open source, não apenas uma coleção de projetos open source maduros. O RHEL é extensivamente testado, tem um grande ecossistema de suporte de parceiros, certificações de hardware e software, serviços de consultoria, treinamento e suporte de vários anos e garantias de manutenção.

A Red Hat baseia suas principais versões do RHEL no Fedora. No entanto, em função disso, a Red Hat pode escolher quais pacotes incluir, fazer outras melhorias (contribuiu com os projetos de upstream e Fedora) e tomar decisões de configuração que atendam às necessidades dos clientes. A Red Hat ajuda os fornecedores e clientes a se envolverem com a comunidade de open source e a trabalhar com o desenvolvimento upstream para desenvolver soluções e corrigir problemas.

O Red Hat Enterprise Linux usa um modelo de distribuição baseado em subscrição. Como este é um software open source, esta não é uma taxa de licença. Em vez disso, ela paga o suporte, a manutenção, as atualizações, patches de segurança, acesso à base de conhecimento no Red Hat Customer Portal (http://access.redhat.com/), certificações e assim por diante. O cliente está pagando por suporte e expertise de longo prazo, comprometimento e assistência quando necessário.

Quando grandes atualizações são disponibilizadas, os clientes podem implementá-las quando for mais conveniente para eles e sem pagar mais. Isso simplifica o gerenciamento das atualizações de sistema nos aspectos econômico e prático. 

##  CentOS

O CentOS é uma distribuição Linux orientada pela comunidade e derivada em grande parte da base de código open source da Red Hat Enterprise Linux e outras fontes. É gratuito, fácil de instalar e conta com equipe e suporte de uma comunidade ativa de voluntários que opera independentemente da Red Hat. 

##  Introdução ao ambiente GNOME de área de trabalho

O ambiente de desktop é a interface gráfica do usuário em um sistema Linux. O ambiente de área de trabalho padrão no Red Hat Enterprise Linux 8 é fornecido pelo GNOME 3. Ele fornece aos usuários uma área de trabalho integrada, além de uma plataforma de desenvolvimento unificada fornecida pelo Wayland (por padrão) ou pelo X Window System legado.

O GNOME Shell oferece as principais funções de interface de usuário do ambiente GNOME de área de trabalho. O aplicativo GNOME Shell é altamente personalizável. O padrão do Red Hat Enterprise Linux 8 para a aparência do GNOME Shell é o tema "Padrão", que é usado nesta seção. O padrão do Red Hat Enterprise Linux 7 era um tema alternativo chamado "Clássico", que estava mais perto da aparência de versões mais antigas do GNOME. O tema pode ser selecionado de modo persistente no login, clicando o ícone de engrenagem ao lado do botão Sign In depois de selecionar a conta e antes de digitar a senha. 

![HTB](/1h.png)

##  Partes do GNOME Shell

Os elementos do GNOME Shell incluem as seguintes partes, conforme ilustrado por esta captura de tela do GNOME Shell no modo de visão geral Activities:

![HTB](/2h.png)

1)	Barra superior: a barra que fica no topo da tela. Ela é exibido na visão geral Activities e nos espaços de trabalho. A barra superior oferece o botão Activities, além dos controles de volume, rede, acesso ao calendário e a alternância entre os métodos de entrada de teclado (se mais de uma estiver configurada).

2)	Activities overview: este é um modo especial que ajuda um usuário a organizar janelas e iniciar aplicativos. A visão geral Activities pode ser inserida clicando no botão Activities no canto superior esquerdo da barra superior ou pressionando a tecla Super. A tecla Super (às vezes chamada de tecla do Windows ou a tecla Command), fica perto do canto inferior esquerdo de um PC IBM de 104/105 teclas ou de um teclado Apple. As três áreas principais da visão geral Activities são o dash, à esquerda da tela, a windows overview, no centro da tela, e o workspace selector, no lado direito da tela.

3)	System menu: o menu no canto superior direito na barra superior fornece controle para ajustar o brilho da tela e para ativar ou desativar as conexões de rede. Abaixo do submenu do nome de usuário estão as opções para ajustar das configurações de conta e fazer o logout do sistema ou desligar. O menu do sistema também oferece botões para abrir a janela Settings, bloquear a tela ou desligar o sistema.

4)	Dash: é uma lista configurável de ícones dos aplicativos favoritos do usuário, dos aplicativos que estão em execução e um botão de grid na parte inferior do dash que pode ser usado para selecionar aplicativos arbitrários. Você pode iniciar os aplicativos clicando em um dos ícones ou usando a grade para encontrar um aplicativo menos usado. O dash também é, às vezes, chamado de dock.

5)	Windows overview: uma área no centro da visão geral Activities, que exibe miniaturas de todas as janelas ativas na área de trabalho atual. Isso permite que as janelas sejam mais facilmente colocadas em primeiro plano em um espaço de trabalho desordenado ou movidas para outro espaço de trabalho.

6)	Workspace selector: uma área à direita da visão geral Activities, que exibe miniaturas de todas as áreas de trabalho ativas e permite que as áreas de trabalho sejam selecionadas e as janelas sejam movidas de uma área de trabalho para outra.

7)	Bandeja de mensagens: oferece uma maneira de acessar as notificações enviadas por aplicativos ou componentes do sistema ao GNOME. Se uma notificação ocorrer, normalmente, ela será exibida primeiro brevemente como uma única linha na parte superior da tela e um indicador persistente aparecerá no centro da barra superior ao lado do relógio para informar o usuário sobre as notificações que foram recebidas recentemente. Você pode abrir a bandeja de mensagens para analisar essas notificações clicando no relógio na barra superior ou pressionando Super+m. Você pode fechar a bandeja de mensagens clicando no relógio na barra superior ou pressionando Esc ou Super+M novamente. 

![HTB](/3h.png)

Você pode visualizar e editar os atalhos de teclado do GNOME usados por sua conta. Abra o menu do sistema no lado direito da barra superior. Clique no botão Settings na parte inferior do menu à esquerda. Na janela do aplicativo que é aberta, selecione Devices → Keyborad no painel esquerdo. O painel direito exibirá suas configurações de atalho atuais.

## Nota

Pode ser difícil enviar alguns atalhos de teclado, como as teclas de função ou a tecla Super, para uma máquina virtual. Isso ocorre porque as teclas especiais usadas por esses atalhos podem ser capturadas pelo sistema operacional local ou pelo aplicativo que você está usando para acessar a área de trabalho gráfica de sua máquina virtual.

## Importante

Nos ambientes de treinamento virtual e individualizado atuais da Red Hat, usar a tecla Super pode ser um pouco complicado. Você provavelmente não poderá usar a tecla Super do teclado porque ela, muitas vezes, não é passada para a máquina virtual no ambiente de sala de aula pelo seu navegador da web.

Na parte superior da janela do navegador que exibe a interface da sua máquina virtual, deve haver um ícone de teclado no lado direito. Se você clicar nele, será aberto um teclado na tela. Clicando novamente, o teclado na tela será fechado.

O teclado na tela trata a Super como uma tecla modificadora que é frequentemente pressionada com outra tecla. Se você clicar nela uma vez, ela ficará amarela, indicando que está sendo pressionada. Então, para pressionar Super+M no teclado na tela, clique em Super e em M.

Se você desejar apenas pressionar e soltar Super no teclado na tela, deverá clicar duas vezes nela. O primeiro clique mantém a tecla Super pressionada, e o segundo clique a libera.

As outras teclas tratadas como teclas modificadoras (como a Super) pelo teclado na tela são Shift, Ctrl, Alt e Caps. As teclas Esc e Menu são tratadas como teclas normais e não como teclas modificadoras. 

## Espaços de trabalho

Os espaços de trabalho são telas separadas que têm janelas de aplicativo diferentes. Eles podem ser usados para organizar seu ambiente de trabalho agrupando janelas de aplicativo abertas por tarefas. Por exemplo, janelas usadas para executar uma determinada atividade de manutenção do sistema (como a configuração de um novo servidor remoto) podem ser agrupadas em um espaço de trabalho, enquanto e-mails e outros aplicativos de comunicação podem ser agrupados em outro espaço de trabalho.

Há dois métodos simples para alternar entre espaços de trabalho. um método, talvez o mais rápido, é pressionar Ctrl+Alt+seta para cima ou Ctrl+Alt+seta para baixo para alternar entre espaços de trabalho em sequência. O segundo é alternar para a visão geral Activities desejada e clicar no espaço de trabalho.

Uma vantagem de usar a visão geral Activities é que as janelas podem ser clicadas e arrastadas entre o espaço de trabalho usando o workspace selector à direita da tela, e a windows overview, no centro da tela. 

## Importante

Assim como a Super, nos ambientes atuais de treinamento virtual e individualizado da Red Hat, as combinações de teclas Ctrl+Alt não são geralmente passadas para a máquina virtual no ambiente de sala de aula pelo seu navegador da web.

Você pode inserir essas combinações de teclas para alternar espaços de trabalho usando o teclado na tela. Pelo menos dois espaços de trabalho precisam estar em uso. Abra o teclado na tela e clique em Ctrl, Alt e, em seguida, na seta para cima ou na seta para baixo.

No entanto, nesses ambientes de treinamento, geralmente é mais simples evitar os atalhos de teclado e o teclado na tela. Alterne espaços de trabalho clicando no botão Activities e, em seguida, no seletor de área de trabalho à direita da visão geral Activities, clicando no espaço de trabalho para o qual você deseja alternar. 

## Inicialização de um terminal

Para obter um prompt do shell no GNOME, inicie um aplicativo de terminal gráfico, como o GNOME Terminal. Há várias maneiras de fazer isso. Os dois métodos mais usados estão listados abaixo:

Na visão geral Activities, selecione Terminal no dash (na área dos favoritos, encontrando-o com o botão de grade (no agrupamento Utilities) ou usando o campo de pesquisa na parte superior da windows overview).

Pressione a combinação de teclas Alt+F2 para abrir Enter a Command e digite gnome-terminal. 

Quando uma janela de terminal for aberta, um prompt do shell será exibido ao usuário que iniciou o programa de terminal gráfico. O prompt do shell e a barra de título da janela de terminal indicam o nome de usuário atual, o nome do host e o diretório de trabalho.

## Bloqueio de tela ou logout

É possível bloquear a tela ou fazer o logout totalmente a partir do menu de sistema no lado direito da barra superior.

Para bloquear a tela, no menu do sistema no canto superior direito, clique no botão de bloqueio na parte inferior do menu ou pressione Super+L (que pode ser mais fácil de lembrar como Windows+L). A tela também é bloqueada se a sessão gráfica ficar inativa por alguns minutos.

Uma lock screen curtain (cortina de tela de bloqueio) aparece, mostrando a hora do sistema e o nome do usuário conectado. Para desbloquear a tela, pressione Enter ou espaço para levantar a cortina de bloqueio de tela; em seguida, insira a senha do usuário na tela de bloqueio.

Para fazer o logout e finalizar a sessão de login gráfico atual, selecione o menu do sistema no canto superior direito da barra superior e clique em (User) → Log Out. Uma janela é exibida, oferecendo a opção de Cancel ou confirmar a ação Log out.

## Desligamento ou reinicialização do sistema

Para desligar o sistema, no menu do sistema no canto superior direito, clique no botão liga/desliga na parte inferior do menu ou pressione Ctrl+Alt+Del. Na caixa de diálogo exibida, você pode escolher Power Off (Desligar) ou Restart (Reiniciar) a máquina; ou Cancel (Cancelar) a operação. Se você não fizer uma escolha, o sistema será desligado automaticamente após 60 segundos. 


## Sintaxe básica de comandos

O GNU Bourne-Again Shell (bash) é um programa que interpreta comandos digitados pelo usuário. Cada string digitada no shell pode ter até três partes: o comando, as opções (que geralmente começam com - ou --) e os argumentos. Cada palavra digitada no shell é separada por espaços. Comandos são os nomes dos programas que estão instalados no sistema. Cada comando tem suas próprias opções e argumentos.

Quando estiver pronto para executar um comando, pressione a tecla Enter. Digite cada comando em uma linha separada. A saída do comando é exibida antes que o próximo prompt do shell seja exibido. 

```sh
[user@host]$ whoami
user
[user@host]$ 
```

Se quiser digitar mais de um comando em uma única linha, use um ponto e vírgula (;) como separador de comandos. Um ponto e vírgula é um membro de uma classe de caracteres chamada metacaracteres que tem significados especiais para o bash. Nesse caso, a saída de ambos os comandos será exibida antes de o próximo prompt shell aparecer.

O exemplo a seguir mostra como combinar dois comandos (command1 e command2) na linha de comando. 

```sh
[user@host]$ command1;command2
```

## Exemplos de comandos simples

O comando date mostra a data e a hora atuais. Ele também pode ser usado pelo superusuário para ajustar o relógio do sistema. Um argumento que começa por um sinal de mais (+) define a string de formatação para o comando date. 

```sh
[user@host ~]$ date
Sat Jan  26 08:13:50 IST 2019
[user@host ~]$ date +%R
08:13
[user@host ~]$ date +%x
01/26/2019
```
O comando passwd altera a senha do próprio usuário. A senha original da conta deverá ser indicada para que uma alteração seja permitida. Por padrão, passwd está configurado para solicitar uma senha segura, composta por letras minúsculas, maiúsculas, números e símbolos e que não seja baseada em uma palavra do dicionário. O superusuário pode usar o comando passwd para alterar as senhas de outros usuários. 

```sh
[user@host ~]$ passwd
Changing password for user user.
Current password: old_password
New password: new_password
Retype new password: new_password
passwd: all authentication tokens updated successfully.
```

O Linux não exige extensões de nome de arquivo para classificar arquivos por tipo. O comando file varre o início do conteúdo de um arquivo e exibe seu tipo. Os arquivos a serem classificados serão passados como argumentos ao comando.

```sh
[user@host ~]$ file /etc/passwd
/etc/passwd: ASCII text
[user@host ~]$ file /bin/passwd
/bin/passwd: setuid ELF 64-bit LSB shared object, x86-64, version 1 
(SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, 
for GNU/Linux 3.2.0, BuildID[sha1]=a3637110e27e9a48dced9f38b4ae43388d32d0e4, stripped
[user@host ~]$ file /home
/home: directory
```
## Visualização do conteúdo dos arquivos

Um dos comandos mais simples e frequentemente usados no Linux é o cat. O comando cat permite criar múltiplos arquivos ou arquivos únicos, visualizar o conteúdo dos arquivos, concatenar o conteúdo de vários arquivos e redirecionar o conteúdo do arquivo a um terminal ou a arquivos.

O exemplo mostra como visualizar o conteúdo do arquivo /etc/passwd. 

```sh
[user@host ~]$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
...output omitted...
```
Use o comando a seguir para exibir o conteúdo de vários arquivos. 

```sh
[user@host ~]$ cat file1 file2
Hello World!!
Introduction to Linux commands.
```
Alguns arquivos são muito longos e podem ocupar mais espaço para serem exibidos do que o fornecido pelo terminal. O comando cat não exibe o conteúdo de um arquivo como páginas. O comando less exibe uma página de um arquivo de cada vez e permite que você percorra as páginas.

O comando less permite que você avance e volte nas páginas por meio de arquivos mais compridos que cabem em uma janela de terminal. Use as teclas de seta para cima e seta para baixo para rolar para cima e para baixo. Pressione q para sair do comando.

Os comandos head e tail exibem o início e o fim de um arquivo, respectivamente. Por padrão, esses comandos exibem 10 linhas do arquivo, mas ambos têm uma opção -n que permite especificar um número diferente de linhas. O arquivo a ser exibido será passado como um argumento para esses comandos. 

```sh
[user@host ~]$ head /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
[user@host ~]$ tail -n 3 /etc/passwd
gdm:x:42:42::/var/lib/gdm:/sbin/nologin
gnome-initial-setup:x:977:977::/run/gnome-initial-setup/:/sbin/nologin
avahi:x:70:70:Avahi mDNS/DNS-SD Stack:/var/run/avahi-daemon:/sbin/nologin
```

O comando wc conta linhas, palavras e caracteres em um arquivo. É preciso de uma opção -l, -w ou -c para exibir apenas linhas, palavras ou caracteres, respectivamente. 

```sh
[user@host ~]$ wc /etc/passwd
  45  102 2480 /etc/passwd
[user@host ~]$ wc -l /etc/passwd ; wc -l /etc/group
45 /etc/passwd
70 /etc/group
[user@host ~]$ wc -c /etc/group /etc/hosts
 966 /etc/group
 516 /etc/hosts
1482 total
```

## Preenchimento com Tab

O preenchimento com Tab permite que o usuário complete comandos ou nomes de arquivo rapidamente depois de digitar uma parte suficiente no prompt para torná-los exclusivos. Se os caracteres digitados não forem únicos, pressionar a tecla Tab duas vezes mostra todos os comandos iniciados pelos caracteres já digitados. 

```sh
[user@host ~]$ pas1Tab+Tab
passwd       paste        pasuspender
[user@host ~]$ pass2Tab
[user@host ~]$ passwd 
Changing password for user user.
Current password: 
```
1 Pressione Tab duas vezes.

2 Pressione Tab uma vez. 

O preenchimento com Tab pode ser usado para completar os nomes de arquivo ao digitá-los como argumentos de comandos. Quando a tecla Tab é pressionada, ela preenche o nome do arquivo, tanto quanto possível. Pressionar Tab uma segunda vez fará com que o shell liste todos os arquivos que correspondam ao padrão atual. Digite caracteres adicionais até o nome ser exclusivo e use o preenchimento com Tab para completar o comando. 

```sh
[user@host ~]$ ls /etc/pas1Tab
[user@host ~]$ ls /etc/passwd2Tab
passwd   passwd-
```
1 2 Pressione Tab uma vez. 

É possível corresponder argumentos e opções usando o preenchimento com Tab para muitos comandos. O comando useradd é usado pelo superusuário, root, para criar usuários adicionais no sistema. Muitas opções podem ser usadas para controlar como esse comando se comporta. O preenchimento com Tab após uma opção parcial pode ser utilizado para concluir a opção sem precisar digitar muito. 

```sh
[root@host ~]## useradd --1Tab+Tab
--base-dir        --groups          --no-log-init     --shell
--comment         --help            --non-unique      --skel
--create-home     --home-dir        --no-user-group   --system
--defaults        --inactive        --password        --uid
--expiredate      --key             --root            --user-group
--gid             --no-create-home  --selinux-user
[root@host ~]## useradd --
```
1 Pressione Tab duas vezes. 

## Continuação de um longo comando em outra linha

Comandos com muitas opções e argumentos podem rapidamente se tornar longos e são automaticamente envolvidos pela janela de comando quando o cursor atinge a margem direita. Em vez disso, para facilitar a legibilidade do comando, você pode digitar um comando longo usando mais de uma linha.

Para fazer isso, você usará um caractere de barra invertida (\), referido como o caractere escape, para ignorar o significado do caractere imediatamente após a barra invertida. Você aprendeu que inserir um caractere de nova linha, pressionando a tecla Enter, informa ao shell que a entrada do comando está completa e que o comando deve ser executado. Ao usar o escape para o caractere de nova linha, o shell é instruído a mudar para uma nova linha de comando sem o executar. O shell reconhece a solicitação exibindo um prompt de continuação, chamado de prompt secundário, usando o caractere maior do que (>) por padrão em uma nova linha vazia. Os comandos podem ser continuados em muitas linhas. 

```sh
[user@host]$ head -n 3 \
> /usr/share/dict/words \
> /usr/share/dict/linux.words
==> /usr/share/dict/words <==
1080
10-point
10th

==> /usr/share/dict/linux.words <==
1080
10-point
10th
[user@host ~]$ 
```
## Importante

O exemplo de tela anterior mostra como um comando continuado aparece para um usuário típico. No entanto, promover esse realismo em materiais didáticos, como este livro, geralmente causa confusão. Os novos alunos podem inserir por engano o caractere maior do que adicional como parte do comando digitado. O shell interpreta um caractere maior do que digitado como redirecionamento de processo, o que não era o objetivo do usuário. O redirecionamento de processos é discutido em um próximo capítulo.

Para evitar essa confusão, este livro não mostrará prompts secundários nas saídas da tela. Um usuário ainda verá o prompt secundário em sua janela do shell, mas o material do curso exibe intencionalmente apenas caracteres para serem digitados, conforme demonstrado no exemplo abaixo. Compare com o exemplo de tela anterior. 

```sh
[user@host]$ head -n 3 \
/usr/share/dict/words \
/usr/share/dict/linux.words
==> /usr/share/dict/words <==
1080
10-point
10th

==> /usr/share/dict/linux.words <==
1080
10-point
10th
[user@host ~]$ 
```
## Histórico de comandos

O comando history exibe uma lista de comandos executados anteriormente precedidos por um número.

O caractere ponto de exclamação (!) é um metacaractere usado para expandir comandos anteriores sem precisar redigitá-los. O comando !number expande o comando que corresponde ao número indicado. O comando !string expande o comando mais recente que começa com a string especificada. 

```sh
[user@host ~]$ history
   ...output omitted...
   23  clear
   24  who
   25  pwd
   26  ls /etc
   27  uptime
   28  ls -l
   29  date
   30  history
[user@host ~]$ !ls
ls -l
total 0
drwxr-xr-x. 2 user user 6 Mar 29 21:16 Desktop
...output omitted...
[user@host ~]$ !26
ls /etc
abrt                     hosts                     pulse
adjtime                  hosts.allow               purple
aliases                  hosts.deny                qemu-ga
...output omitted...
```
As teclas de seta podem ser usadas para navegar pelos comandos anteriores no histórico do shell. A seta para cima edita o comando anterior na lista do histórico. A seta para baixo edita o próximo comando na lista do histórico. A seta para a esquerda e a seta para a direita movem o cursor para a esquerda e para a direita no comando atual da lista de histórico, para que você possa editá-lo antes de executá-lo.

Você pode usar a combinação de teclas Esc+. ou Alt+. para inserir a última palavra do comando anterior na localização atual do cursor. O uso repetido da combinação de teclas substituirá esse texto pela última palavra dos comandos anteriores do histórico. A combinação de teclas Alt+. é particularmente conveniente porque você pode segurar Alt e pressionar . repetidamente para percorrer facilmente pelos comandos anteriores.

## Edição da linha de comando

Quando usado de forma interativa, bash tem um recurso de edição de linha de comando. Isso permite que o usuário utilize os comandos do editor de texto para se mover e modificar o comando atual sendo digitado. O movimento no comando atual e a passagem pelo histórico de comandos usando as teclas de seta foram introduzidos anteriormente nesta sessão. Comandos de edição mais poderosos são apresentados na tabela a seguir. 

Atalho = Descrição

Ctrl+A => Ir para o início da linha de comando.

Ctrl+E => Ir para o final da linha de comando.

Ctrl+U => Limpar do cursor ao início da linha de 
comando.

Ctrl+K => Limpar do cursor até o final da linha de comando.

Ctrl+seta => para a esquerda 	Ir para o início da palavra anterior na linha de comando.

Ctrl+seta => para a direita 	Ir para o final da próxima palavra na linha de comando.

Ctrl+R => Pesquisar um padrão na lista de histórico de comandos. 

Há vários outros comandos de edição de linha de comando disponíveis, mas esses são os comandos mais úteis para novos usuários. Os outros comandos podem ser encontrados na página do man bash

1) Use o comando date para exibir a data e a hora atuais
```sh
[student@workstation ~]$ date
Thu Jan 22 10:13:04 PDT 2019
```

2) Mostrar a hora atual no formato de 12 horas (por exemplo, 11:42:11 AM). Dica: a string de formato que exibe a saída é %r. 
```sh
[student@workstation ~]$ date +%r
10:14:07 AM
```
3)  Qual tipo de arquivo é /home/student/zcat? Ele é legível? 
```sh
➜  ~ file /usr/bin/zcat
/usr/bin/zcat: POSIX shell script, ASCII text executable
```
4) Use o comando wc e os atalhos do Bash para exibir o tamanho de zcat. 
```sh
➜  ~ wc /usr/bin/zcat 
  51  299 1984 /usr/bin/zcat
```
5)  Exiba as 10 primeiras linhas de zcat. 
```sh
➜  ~ head h10 /usr/bin/zcat 
head: não foi possível abrir 'h10' para leitura: Arquivo ou diretório inexistente
==> /usr/bin/zcat <==
#!/bin/sh
# Uncompress files to standard output.

# Copyright (C) 2007, 2010-2018 Free Software Foundation, Inc.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
```
6)  Exiba as 10 últimas linhas do arquivo zcat. 
```sh
➜  ~ tail -n 10 /usr/bin/zcat
With no FILE, or when FILE is -, read standard input.

Report bugs to <bug-gzip@gnu.org>."

case $1 in
--help)    printf '%s\n' "$usage"   || exit 1; exit;;
--version) printf '%s\n' "$version" || exit 1; exit;;
esac

exec gzip -cd "$@"
```
7)  Repita o comando anterior exato pressionando as teclas três vezes ou menos. 

Repita o comando anterior exato. Pressione a tecla de seta para cima uma vez para voltar no histórico do comando e pressione Enter (duas vezes), ou digite o comando de atalho !! e, depois, pressione Enter (três vezes) para executar o comando mais recente no histórico de comandos. (Tente usar ambos.) 

```sh
[student@workstation]$ !!
tail zcat
With no FILE, or when FILE is -, read standard input.

Report bugs to <bug-gzip@gnu.org>."

case $1 in
--help)    printf '%s\n' "$usage"   || exit 1;;
--version) printf '%s\n' "$version" || exit 1;;
esac

exec gzip -cd "$@"
```

8)  Repita o comando anterior, mas use a opção -n 20 para exibir as últimas 20 linhas no arquivo. Use a edição de linha de comando para fazer isso com o mínimo de pressionamento de teclas. 

```sh
➜  ~ tail -n 20 /usr/bin/zcat
  -l, --list        list compressed file contents
  -q, --quiet       suppress all warnings
  -r, --recursive   operate recursively on directories
  -S, --suffix=SUF  use suffix SUF on compressed files
      --synchronous synchronous output (safer if system crashes, but slower)
  -t, --test        test compressed file integrity
  -v, --verbose     verbose mode
      --help        display this help and exit
      --version     display version information and exit

With no FILE, or when FILE is -, read standard input.

Report bugs to <bug-gzip@gnu.org>."

case $1 in
--help)    printf '%s\n' "$usage"   || exit 1; exit;;
--version) printf '%s\n' "$version" || exit 1; exit;;
esac

exec gzip -cd "$@"
```

9)  Use o histórico do shell para executar o comando date +%r novamente. 

```sh
[student@workstation ~]$ history
1   date
2   date +%r
3   file zcat
4   wc zcat
5   head zcat
6   tail zcat
7   tail -n 20 zcat
8   history
[student@workstation ~]$ !2
date +%r
10:49:56 AM
```

=> O shell Bash é um interpretador de comandos que solicita aos usuários interativos que especifiquem os comandos do Linux.

=> Muitos comandos têm uma opção --help que exibe uma tela ou mensagem de uso.

=> A utilização de espaços de trabalho facilita a organização de várias janelas de aplicativos.

=> O botão Activities no canto superior esquerdo da barra superior fornece um modo de visão geral que ajuda o usuário a organizar janelas e iniciar aplicativos.

=> O comando file varre o início do conteúdo de um arquivo e exibe seu tipo.

=> Os comandos head e tail exibem o início e o fim de um arquivo, respectivamente.

=> Você pode usar o preenchimento Tab para preencher nomes de arquivos ao digitá-los como argumentos para os comandos. 

https://rha.ole.redhat.com/rha/app/courses/rh124-8.2/pages/ch03

## Capítulo 3. Gerenciamento de arquivos na linha de comando

A hierarquia do sistema de arquivos

Todos os arquivos em um sistema Linux são armazenados em sistemas de arquivos, que são organizados em uma única árvore de diretório invertida, conhecida como hierarquia do sistema de arquivos. Essa árvore é invertida porque dizemos que a raiz dela está na parte superior da hierarquia e os ramos de diretórios e subdiretórios se estendem abaixo da raiz (root). 

![HTB](/4h.png)

O diretório / é o diretório root no topo da hierarquia do sistema de arquivos. O caractere / também é usado como separador de diretórios nos nomes de arquivos. Por exemplo, se etc for um subdiretório do diretório /, é possível chamá-lo de /etc. Do mesmo modo, se o diretório /etc contiver um arquivo chamado issue, é possível referir-se ao arquivo como /etc/issue. 

Os subdiretórios de / são usados com fins padronizados para organizar arquivos por tipo e finalidade. Assim, fica mais fácil encontrar arquivos. Por exemplo, no diretório root, o subdiretório /boot é utilizado para armazenar os arquivos necessários para o boot do sistema. 

## Nota

Os seguintes termos ajudam a descrever o conteúdo do diretório do sistema de arquivos:

=> O conteúdo estático permanece inalterado até que seja editado ou reconfigurado.

=> O conteúdo dinâmico ou variável pode ser modificado ou inserido pelos processos ativos.

=> O conteúdo persistente permanece após uma reinicialização, como definições de configuração.

=> O conteúdo de tempo de execução é específico de processos ou sistemas e é excluído por uma reinicialização. 

## Diretórios importantes do Red Hat Enterprise Linux

/usr
```sh
Software instalado, bibliotecas compartilhadas, arquivos incluídos e dados de programas somente leitura. Subdiretórios importantes incluem:

/usr/bin: comandos de usuário.

/usr/sbin: comandos de administração do sistema.

/usr/local: software personalizado localmente. 
```

/etc
```sh
Arquivos de configuração específicos deste sistema. 
```

/var
```sh
Dados variáveis específicos deste sistema que devem persistir entre boots do sistema. Os arquivos que mudam de modo dinâmico; por exemplo, bancos de dados, diretórios de cache, arquivos de log, documentos com spool de impressora e conteúdo de sites podem ser encontrados em /var.  
```

/run
```sh
 Dados de tempo de execução de processos iniciados desde o último boot. Isso inclui arquivos de ID de processos e arquivos de bloqueio, entre outros. O conteúdo desse diretório é recriado na reinicialização. Este diretório consolida /var/run e /var/lock de versões anteriores do Red Hat Enterprise Linux. 
```

/home
```sh
Diretórios pessoais são os locais onde os usuários normais armazenam seus dados pessoais e arquivos de configuração. 
```

/root
```sh
Diretório pessoal do superusuário administrativo, root. 
```

/tmp
```sh
Um espaço gravável para arquivos temporários. Arquivos não acessados, alterados nem modificados por 10 dias são excluídos automaticamente desse diretório. Há outro diretório temporário, /var/tmp, no qual os arquivos que não tiverem sido acessados, alterados ou modificados por mais de 30 dias serão excluídos automaticamente. 
```

/boot 
```sh
Arquivos necessários para começar o processo de boot. 
```

/dev
```sh
Contém arquivos de dispositivos especiais que são usados pelo sistema para acessar o hardware. 
```

## Importante

No Red Hat Enterprise Linux 7 e posteriores, quatro diretórios mais antigos em / têm o mesmo conteúdo de suas contrapartes localizadas em /usr:

/bin e /usr/bin

/sbin e /usr/sbin

/lib e /usr/lib

/lib64 e /usr/lib64 

Em versões anteriores do Red Hat Enterprise Linux, esses diretórios eram diferentes e continham conjuntos distintos de arquivos.

No Red Hat Enterprise Linux 7 e posteriores, os diretórios em / são links simbólicos para as pastas correspondentes em /usr. 

## Especificação de arquivos por nome

![HTB](/5h.png)

A visualização do navegador de arquivos comum (à esquerda) é equivalente à visualização descendente (à direita). 

O caminho de um arquivo ou diretório especifica o local exclusivo no sistema de arquivos. Seguir o caminho de um arquivo atravessa um ou mais subdiretórios nomeados, delimitados por uma barra (/), até chegar ao destino. Os diretórios, também chamados de pastas, contêm outros arquivos e outros subdiretórios. Eles podem ser referenciados da mesma maneira que os arquivos. 

## Importante

Um caractere de espaço é aceitável como parte de um nome de arquivo do Linux. No entanto, espaços também são usados pelo shell para separar opções e argumentos na linha de comando. Se você inserir um comando que inclua um arquivo que tenha um espaço no nome, o shell poderá interpretar erroneamente o comando e entender que você deseja iniciar um novo nome de arquivo ou outro argumento no espaço.

É possível evitar isso colocando nomes de arquivos entre aspas. No entanto, se você não precisar usar espaços em nomes de arquivos, pode ser mais simples simplesmente evitá-los. 

=> Caminhos absolutos

Um caminho absoluto é um nome totalmente qualificado, especificando a localização exata dos arquivos na hierarquia do sistema de arquivos. Ele começa no diretório raiz (/) e especifica cada subdiretório que deve ser percorrido para alcançar o arquivo específico. Cada arquivo em um sistema de arquivos tem um nome de caminho absoluto exclusivo, reconhecido por uma regra simples: um nome de arquivo com uma barra (/) como primeiro caractere é um nome de caminho absoluto. Por exemplo, o nome de caminho absoluto do arquivo de log do sistema de mensagens é /var/log/messages. Nomes de caminhos absolutos podem ser longos, por isso, os arquivos também podem ser localizados em relação ao diretório de trabalho atual para o prompt do shell. 

=> O diretório de trabalho atual e caminhos relativos

Quando um usuário fizer login e abrir uma janela de comando, normalmente a localização inicial será o diretório pessoal do usuário. Os processos do sistema também têm um diretório inicial. Usuários e processos navegam a outros diretórios, conforme necessário; os termos diretório de trabalho ou diretório de trabalho atual são referentes ao local atual.

Assim como um caminho absoluto, um caminho relativo identifica um único arquivo, especificando somente o caminho necessário para acessar o arquivo no diretório de trabalho local. O reconhecimento de nomes de caminho relativos segue uma regra simples: um nome de caminho com qualquer caractere diferente de uma barra como primeiro caractere é um nome de caminho relativo. Um usuário no diretório /var pode fazer referência ao arquivo de log de mensagens de modo relativo como log/messages. 

Sistemas de arquivos Linux, incluindo, entre outros, ext4, XFS, GFS2 e GlusterFS, diferenciam maiúsculas de minúsculas. A criação de FileCase.txt e filecase.txt no mesmo diretório resulta em dois arquivos exclusivos. 

Sistemas de arquivos que não são do Linux podem funcionar de modo diferente. Por exemplo, o VFAT, o NTFS da Microsoft e o HFS+ da Apple, têm um comportamento de preservação de maiúsculas e minúsculas. Embora esses sistemas de arquivos não diferenciem maiúsculas de minúsculas, eles exibem os nomes de arquivo com as letras originais usada durante a criação do arquivo. Portanto, se você tentou criar os arquivos no exemplo anterior em um sistema de arquivos VFAT, ambos os nomes seriam tratados como apontando para o mesmo arquivo em vez de dois arquivos diferentes. 

Caminhos de navegação

O comando pwd exibe o nome do caminho completo do diretório de trabalho atual para esse shell. Isso pode ajudar você a determinar a sintaxe para acessar arquivos usando nomes de caminho relativos. O comando ls lista o conteúdo do diretório especificado ou, caso um diretório não seja fornecido, do diretório de trabalho atual. 

```sh
[user@host ~]$ pwd
/home/user
[user@host ~]$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
[user@host ~]$
```
Use o comando cd para alterar o diretório de trabalho atual do shell. Se você não especificar nenhum argumento para o comando, ele será alterado para o diretório pessoal. 

No exemplo a seguir, uma mistura de caminhos absolutos e relativos é usada com o comando cd para alterar o diretório de trabalho atual para o shell. 

```sh
[user@host ~]$ pwd
/home/user
[user@host ~]$ cd Videos
[user@host Videos]$ pwd
/home/user/Videos
[user@host Videos]$ cd /home/user/Documents
[user@host Documents]$ pwd
/home/user/Documents
[user@host Documents]$ cd
[user@host ~]$ pwd
/home/user
[user@host ~]$
```
Como você pode ver no exemplo anterior, o prompt de shell padrão também exibe o último componente do caminho absoluto para o diretório de trabalho atual. 

Por exemplo, para /home/user/Videos, somente Videos é exibido. O prompt exibe o caractere til '~' quando o diretório de trabalho atual é o diretório pessoa.

O comando touch normalmente atualiza o carimbo de data e hora de um arquivo para a data e a hora atuais, sem modificá-lo. Isso é útil para a criação de arquivos vazios, que podem ser usados para prática, pois o uso desse comando em um nome de arquivo que não existe faz com que o arquivo seja criado. No exemplo a seguir, o comando touch cria arquivos de prática nos subdiretórios Documents e Videos.  

```sh
[user@host ~]$ touch Videos/blockbuster1.ogg
[user@host ~]$ touch Videos/blockbuster2.ogg
[user@host ~]$ touch Documents/thesis_chapter1.odf
[user@host ~]$ touch Documents/thesis_chapter2.odf
[user@host ~]$
```
O comando ls tem várias opções para a exibição de atributos nos arquivos. As mais comuns e úteis são -l (formato de listagem longa), -a (todos os arquivos, incluindo os ocultos) e -R (recursão, para incluir o conteúdo de todos os subdiretórios). 

```sh
[user@host ~]$ ls -l
total 15
drwxr-xr-x.  2 user user 4096 Feb  7 14:02 Desktop
drwxr-xr-x.  2 user user 4096 Jan  9 15:00 Documents
drwxr-xr-x.  3 user user 4096 Jan  9 15:00 Downloads
drwxr-xr-x.  2 user user 4096 Jan  9 15:00 Music
drwxr-xr-x.  2 user user 4096 Jan  9 15:00 Pictures
drwxr-xr-x.  2 user user 4096 Jan  9 15:00 Public
drwxr-xr-x.  2 user user 4096 Jan  9 15:00 Templates
drwxr-xr-x.  2 user user 4096 Jan  9 15:00 Videos
[user@host ~]$ ls -la
total 15
drwx------. 16 user user   4096 Feb  8 16:15 .
drwxr-xr-x.  6 root root   4096 Feb  8 16:13 ..
-rw-------.  1 user user  22664 Feb  8 00:37 .bash_history
-rw-r--r--.  1 user user     18 Jul  9  2013 .bash_logout
-rw-r--r--.  1 user user    176 Jul  9  2013 .bash_profile
-rw-r--r--.  1 user user    124 Jul  9  2013 .bashrc
drwxr-xr-x.  4 user user   4096 Jan 20 14:02 .cache
drwxr-xr-x.  8 user user   4096 Feb  5 11:45 .config
drwxr-xr-x.  2 user user   4096 Feb  7 14:02 Desktop
drwxr-xr-x.  2 user user   4096 Jan  9 15:00 Documents
drwxr-xr-x.  3 user user   4096 Jan 25 20:48 Downloads
drwxr-xr-x. 11 user user   4096 Feb  6 13:07 .gnome2
drwx------.  2 user user   4096 Jan 20 14:02 .gnome2_private
-rw-------.  1 user user  15190 Feb  8 09:49 .ICEauthority
drwxr-xr-x.  3 user user   4096 Jan  9 15:00 .local
drwxr-xr-x.  2 user user   4096 Jan  9 15:00 Music
drwxr-xr-x.  2 user user   4096 Jan  9 15:00 Pictures
drwxr-xr-x.  2 user user   4096 Jan  9 15:00 Public
drwxr-xr-x.  2 user user   4096 Jan  9 15:00 Templates
drwxr-xr-x.  2 user user   4096 Jan  9 15:00 Videos
[user@host ~]$
```

Os dois diretórios especiais no topo da lista se referem ao diretório atual (.) e ao diretório pai (..). Esses diretórios especiais existem em todos os diretórios do sistema. Você descobrirá a utilidade deles quando começar a usar comandos de gerenciamento de arquivos. 

## Importante

Nomes de arquivos começando com um ponto (.) indicam arquivos ocultos; não é possível visualizá-los na exibição normal usando ls e outros comando. Esse não é um recurso de segurança. Os arquivos ocultos impedem que os arquivos de configuração do usuário necessários sobrecarreguem diretórios pessoais. Muitos comandos processam arquivos ocultos apenas com opções de linha de comando especificas, evitando que a configuração de um usuário seja acidentalmente copiada para outros diretórios ou usuários. 

Proteger o conteúdo dos arquivos de visualizações inadequadas exige o uso de permissões de arquivo. 

```sh
[user@host ~]$ ls -R
.:
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos

./Desktop:

./Documents:
thesis_chapter1.odf  thesis_chapter2.odf

./Downloads:

./Music:

./Pictures:

./Public:

./Templates:

./Videos:
blockbuster1.ogg  blockbuster2.ogg
[user@host ~]$
```

O comando cd tem várias opções. Algumas são tão úteis que é importante praticá-las o mais cedo possível e usá-las com frequência. O comando cd - passa para o diretório anterior, no qual o usuário estava antes do diretório atual. O exemplo a seguir ilustra esse comportamento, alternando entre dois diretórios, o que é útil ao processar uma série de tarefas semelhantes. 

```sh
[user@host ~]$ cd Videos
[user@host Videos]$ pwd
/home/user/Videos
[user@host Videos]$ cd /home/user/Documents
[user@host Documents]$ pwd
/home/user/Documents
[user@host Documents]$ cd -
[user@host Videos]$ pwd
/home/user/Videos
[user@host Videos]$ cd -
[user@host Documents]$ pwd
/home/user/Documents
[user@host Documents]$ cd -
[user@host Videos]$ pwd
/home/user/Videos
[user@host Videos]$ cd
[user@host ~]$
```
O comando cd .. usa o diretório oculto .. para subir um nível até o diretório pai sem precisar saber o nome exato desse diretório. O outro diretório oculto (.) especifica o diretório atual nos comandos em que a localização atual é o argumento de origem ou de destino, evitando a necessidade de digitar o nome de caminho absoluto do diretório. 

```sh
[user@host Videos]$ pwd
/home/user/Videos
[user@host Videos]$ cd .
[user@host Videos]$ pwd
/home/user/Videos
[user@host Videos]$ cd ..
[user@host ~]$ pwd
/home/user
[user@host ~]$ cd ..
[user@host home]$ pwd
/home
[user@host home]$ cd ..
[user@host /]$ pwd
/
[user@host /]$ cd
[user@host ~]$ pwd
/home/user
[user@host ~]$
```

## Gerenciamento de arquivos usando ferramentas de linha de comando

Para gerenciar arquivos, você precisa ser capaz de criar, remover, copiar e mover os arquivos. Você também precisa organizá-los logicamente em diretórios, os quais você também precisa ser capaz de criar, remover, copiar e mover.

A tabela a seguir resume alguns dos comandos mais comuns de gerenciamento de arquivos. O restante desta seção discutirá maneiras de usar esses comandos em mais detalhes. 

Atividade => Sintaxe do comando
Criar um novo diretório => 	mkdir directory
Copiar um arquivo => cp file new-file
Copiar um diretório e seu conteúdo  => cp -r directory new-directory
Mover ou renomear um arquivo ou diretório => mv file new-file
Remover um arquivo 	=> rm file
Remover um diretório contendo arquivos 	=> rm -r directory
Remover um diretório vazio => rmdir directory


## Criação de diretórios


 O comando mkdir cria um ou mais diretórios ou subdiretórios. Ele considera como argumentos uma lista de caminhos para os diretórios que você deseja criar.

O comando mkdir falhará com um erro se o diretório já existir ou se você estiver tentando criar um subdiretório em um diretório que não existe. A opção -p (pai) cria diretórios pais ausentes para o destino solicitado. Tenha cautela ao usar o comando mkdir -p pois erros de digitação acidentais podem criar diretórios não pretendidos sem gerar mensagens de erro.

No exemplo a seguir, digamos que você está tentando criar um diretório no Videosdiretório nomeadoWatched, mas acidentalmente deixou a letra "s" em Videos no comando mkdir. 

```sh
[user@host ~]$ mkdir Video/Watched
mkdir: cannot create directory `Video/Watched': No such file or directory
```

O comando mkdir falhou porque Videos foi digitado incorretamente e o diretório Video não existe. Se você tivesse usado o comando mkdir com a opção -p, o diretório Video seria criado, o que não era o pretendido, e o subdiretório Watched seria criado nesse diretório incorreto.

Depois de escrever corretamente o diretório pai Videos, a criação do subdiretório Watched será bem-sucedida. 

```sh
[user@host ~]$ mkdir Videos/Watched
[user@host ~]$ ls -R Videos
Videos/:
blockbuster1.ogg  blockbuster2.ogg  Watched

Videos/Watched:
```

No exemplo a seguir, os arquivos e diretórios são organizados abaixo do diretório /home/user/Documents. Use o comando mkdir e uma lista de nomes de diretórios separada por espaços para criar vários diretórios. 

```sh
[user@host ~]$ cd Documents
[user@host Documents]$ mkdir ProjectX ProjectY
[user@host Documents]$ ls
ProjectX  ProjectY
```
Use o comando mkdir -p e caminhos relativos separados por espaços para cada um dos nomes de subdiretórios para criar vários diretórios pai com subdiretórios. 

```sh
[user@host Documents]$ mkdir -p Thesis/Chapter1 Thesis/Chapter2 Thesis/Chapter3
[user@host Documents]$ cd
[user@host ~]$ ls -R Videos Documents
Documents:
ProjectX  ProjectY  Thesis

Documents/ProjectX:

Documents/ProjectY:

Documents/Thesis:
Chapter1  Chapter2  Chapter3

Documents/Thesis/Chapter1:

Documents/Thesis/Chapter2:

Documents/Thesis/Chapter3:

Videos:
blockbuster1.ogg  blockbuster2.ogg  Watched

Videos/Watched:
```

O último comando mkdir criou subdiretórios de três subdiretórios ChapterN com um comando. A opção -p criou o diretório pai Thesis ausente. 

## Cópia de arquivos

O comando cp copia um arquivo, criando um novo arquivo no diretório atual ou em um diretório especificado. Ele também pode copiar vários arquivos para um diretório. 

## Atenção

Se o arquivo de destino já existir, o comando cp substitui o arquivo. 

```sh
[user@host ~]$ cd Videos
[user@host Videos]$ cp blockbuster1.ogg blockbuster3.ogg
[user@host Videos]$ ls -l
total 0
-rw-rw-r--. 1 user user    0 Feb  8 16:23 blockbuster1.ogg
-rw-rw-r--. 1 user user    0 Feb  8 16:24 blockbuster2.ogg
-rw-rw-r--. 1 user user    0 Feb  8 16:34 blockbuster3.ogg
drwxrwxr-x. 2 user user 4096 Feb  8 16:05 Watched
[user@host Videos]
```
Ao copiar vários arquivos com um comando, o último argumento deverá ser um diretório. Os arquivos copiados mantêm seus nomes originais no novo diretório. Se um arquivo com o mesmo nome existir no diretório de destino, o arquivo existente será substituído. Por padrão, o cp não copia diretórios, mas os ignora.

No exemplo a seguir, dois diretórios são listados, Thesis e ProjectX. Apenas o último argumento, ProjectX, é válido como destino. O diretório Thesis é ignorado.

```sh
[user@host Videos]$ cd ../Documents
[user@host Documents]$ cp thesis_chapter1.odf thesis_chapter2.odf Thesis ProjectX
cp: omitting directory `Thesis'
[user@host Documents]$ ls Thesis ProjectX
ProjectX:
thesis_chapter1.odf  thesis_chapter2.odf

Thesis:
Chapter1  Chapter2  Chapter3
```

No primeiro comando cp, a cópia do diretório Thesis falhou, mas os arquivos thesis_chapter1.odf e thesis_chapter2.odf foram copiados com êxito.

Se você desejar copiar um arquivo para o diretório de trabalho atual, poderá usar o diretório .: 

```sh
[user@host ~]$ cp /etc/hostname .
[user@host ~]$ cat hostname
host.example.com
[user@host ~]$ 
```
Use o comando copy com a opção -r (recursiva) para copiar o diretório Thesis e seu conteúdo para o diretório ProjectX. 

```sh
[user@host Documents]$ cp -r Thesis ProjectX
[user@host Documents]$ ls -R ProjectX
ProjectX:
Thesis  thesis_chapter1.odf  thesis_chapter2.odf

ProjectX/Thesis:
Chapter1  Chapter2  Chapter3

ProjectX/Thesis/Chapter1:

ProjectX/Thesis/Chapter2:
thesis_chapter2.odf

ProjectX/Thesis/Chapter3:
```
## Movimentação de arquivos

O comando mv move arquivos de um local para outro. Se você pensar no caminho absoluto para um arquivo como seu nome completo, mover um arquivo será efetivamente o mesmo que renomear um arquivo. O conteúdo do arquivo permanecerá inalterado.

Use o comando mv para renomear um arquivo. 

```sh
[user@host Videos]$ cd ../Documents
[user@host Documents]$ ls -l thesis*
-rw-rw-r--. 1 user user 0 Feb  6 21:16 thesis_chapter1.odf
-rw-rw-r--. 1 user user 0 Feb  6 21:16 thesis_chapter2.odf
[user@host Documents]$ mv thesis_chapter2.odf thesis_chapter2_reviewed.odf
[user@host Documents]$ ls -l thesis*
-rw-rw-r--. 1 user user 0 Feb  6 21:16 thesis_chapter1.odf
-rw-rw-r--. 1 user user 0 Feb  6 21:16 thesis_chapter2_reviewed.odf
```
Use o comando mv para mover um arquivo para outro diretório. 

```sh
[user@host Documents]$ ls Thesis/Chapter1
[user@host Documents]$
[user@host Documents]$ mv thesis_chapter1.odf Thesis/Chapter1
[user@host Documents]$ ls Thesis/Chapter1
thesis_chapter1.odf
[user@host Documents]$ ls -l thesis*
-rw-rw-r--. 1 user user 0 Feb  6 21:16 thesis_chapter2_reviewed.odf
```

## Remoção de arquivos e diretórios

O comando rm remove arquivos. Por padrão, rm não removerá diretórios que contenham arquivos, a menos que você adicione as opções -r ou --recursive. 

## Importante

Não existe um recurso de cancelamento de exclusão na linha de comando ou uma Lixeira da qual restaurar arquivos programados para exclusão.

É uma boa ideia verificar seu diretório de trabalho atual antes de remover um arquivo ou diretório. 

```sh
[user@host Documents]$ pwd
/home/student/Documents
```

Use o comando rm para remover um único arquivo do seu diretório de trabalho. 

```sh
[user@host Documents]$ ls -l thesis*
-rw-rw-r--. 1 user user 0 Feb  6 21:16 thesis_chapter2_reviewed.odf
[user@host Documents]$ rm thesis_chapter2_reviewed.odf
[user@host Documents]$ ls -l thesis*
ls: cannot access 'thesis*': No such file or directory
```

Se você tentar usar o comando rm para remover um diretório sem usar a opção -r, o comando falhará. 

```sh
[user@host Documents]$ rm Thesis/Chapter1
rm: cannot remove `Thesis/Chapter1': Is a directory
```

Use o comando rm -r para remover um subdiretório e seu conteúdo. 

```sh
[user@host Documents]$ ls -R Thesis
Thesis/:
Chapter1  Chapter2  Chapter3

Thesis/Chapter1:
thesis_chapter1.odf

Thesis/Chapter2:
thesis_chapter2.odf

Thesis/Chapter3:
[user@host Documents]$ rm -r Thesis/Chapter1
[user@host Documents]$ ls -l Thesis
total 8
drwxrwxr-x. 2 user user 4096 Feb 11 12:47 Chapter2
drwxrwxr-x. 2 user user 4096 Feb 11 12:48 Chapter3
```

O comando rm -r percorre cada subdiretório primeiro, removendo individualmente seus arquivos antes de remover cada diretório. Você pode usar o comando rm -ri para solicitar interativamente a confirmação antes da exclusão. Isso é essencialmente o oposto de usar a opção -f, que força a remoção sem solicitar a confirmação do usuário. 

```sh
[user@host Documents]$ rm -ri Thesis
rm: descend into directory `Thesis'? y
rm: descend into directory `Thesis/Chapter2'? y
rm: remove regular empty file `Thesis/Chapter2/thesis_chapter2.odf'? y
rm: remove directory `Thesis/Chapter2'? y
rm: remove directory `Thesis/Chapter3'? y
rm: remove directory `Thesis'? y
[user@host Documents]$
```

## Atenção

Se você especificar as opções -i e -f, a opção -f tem prioridade e você não será solicitado para confirmação antes que rm exclua arquivos.

No exemplo a seguir, o comando rmdir remove apenas o diretório que está vazio. Assim como no exemplo anterior, você deve usar o comando rm -r para remover um diretório que contenha conteúdo. 

```sh
[user@host Documents]$ pwd
/home/student/Documents
[user@host Documents]$ rmdir ProjectY
[user@host Documents]$ rmdir ProjectX
rmdir: failed to remove `ProjectX': Directory not empty
[user@host Documents]$ rm -r ProjectX
[user@host Documents]$ ls -lR
.:
total 0
[user@host Documents]$
```

O comando rm sem opções não pode remover um diretório vazio. Você deve usar os comandos rmdir, rm -d (que é equivalente a rmdir) ou rm -r. 

## Criação de links entre arquivos

É possível criar vários nomes que apontam para o mesmo arquivo. Existem duas maneiras de fazer isso: criando um link físico para o arquivo ou criando um link simbólico (às vezes chamado de ligação simbólica) para o arquivo. Cada um tem suas vantagens e desvantagens. 

## Criação de links físicos

Todo arquivo inicia com um único link físico, desde seu nome inicial até os dados no sistema de arquivos. Quando você cria um novo link físico para um arquivo, cria outro nome que aponta para os mesmos dados. O novo link físico age exatamente como o nome do arquivo original. Uma vez criado, você não verá diferença entre o novo link físico e o nome original do arquivo. 

Você pode descobrir se um arquivo tem vários links físicos com o comando ls -l. Uma das coisas que ele relata é a contagem de links de cada arquivo, o número de links físicos que o arquivo possui. 

```sh
[user@host ~]$ pwd
/home/user
[user@host ~]$ ls -l newfile.txt
-rw-r--r--. 1 user user 0 Mar 11 19:19 newfile.txt
```

No exemplo anterior, a contagem de links de newfile.txt é 1. Ele tem exatamente um caminho absoluto, que é /home/user/newfile.txt .

Você pode usar o comando ln para criar um novo link físico (outro nome) que aponte para um arquivo existente. O comando precisa de pelo menos dois argumentos, um caminho para o arquivo existente e o caminho para o link físico que você deseja criar.

O exemplo a seguir cria um link físico chamado newfile-link2.txt para o arquivo existente newfile.txt no diretório /tmp. 

```sh
[user@host ~]$ ln newfile.txt /tmp/newfile-hlink2.txt
[user@host ~]$ ls -l newfile.txt /tmp/newfile-hlink2.txt
-rw-rw-r--. 2 user user 12 Mar 11 19:19 newfile.txt
-rw-rw-r--. 2 user user 12 Mar 11 19:19 /tmp/newfile-hlink2.txt
```

Se você desejar descobrir se dois arquivos são links físicos um do outro, uma maneira é usar a opção -i com o comando ls para listar o número de inode dos arquivos. Se os arquivos estiverem no mesmo sistema de arquivos (discutido a seguir) e seus números de inode forem os mesmos, os arquivos são links físicos apontando para os mesmos dados. 

```sh
[user@host ~]$ ls -il newfile.txt /tmp/newfile-hlink2.txt
8924107 -rw-rw-r--. 2 user user 12 Mar 11 19:19 newfile.txt
8924107 -rw-rw-r--. 2 user user 12 Mar 11 19:19 /tmp/newfile-hlink2.txt
```

## Importante

Todos os links físicos que fazem referência ao mesmo arquivo terão as mesmas permissões, contagem de links, propriedade de usuário e grupo, carimbos de data e hora e conteúdo de arquivo. Se uma dessas informações for alterada em um link físico, todos os outros links físicos que apontem para o mesmo arquivo também exibirão a nova informação. Isso ocorre porque cada link físico aponta para os mesmos dados no dispositivo de armazenamento.

Mesmo que o arquivo original seja excluído, o conteúdo do arquivo ainda estará disponível, desde que pelo menos um link físico exista. Os dados só são excluídos do armazenamento quando o último link físico é excluído. 

```sh
[user@host ~]$ rm -f newfile.txt
[user@host ~]$ ls -l /tmp/newfile-hlink2.txt
-rw-rw-r--. 1 user user 12 Mar 11 19:19 /tmp/newfile-hlink2.txt
[user@host ~]$ cat /tmp/newfile-hlink2.txt
Hello World
```
## Limitações de links físicos

Os links físicos têm algumas limitações. Em primeiro lugar, os links físicos só podem ser usados com arquivos regulares. Você não pode usar ln para criar um link físico para um diretório ou arquivo especial.

Em segundo lugar, os links físicos só podem ser usados se ambos os arquivos estiverem no mesmo sistema de arquivos. A hierarquia do sistema de arquivos pode ser composta de vários dispositivos de armazenamento. Dependendo da configuração do sistema, quando você mudar para um novo diretório, esse diretório e seu conteúdo poderão ser armazenados em um sistema de arquivos diferente.

Você pode usar o comando df para listar os diretórios que estão em sistemas de arquivos diferentes. Por exemplo, você pode ver a saída desta maneira: 

```sh
[user@host ~]$ df
Filesystem                   1K-blocks    Used Available Use% Mounted on
devtmpfs                        886788       0    886788   0% /dev
tmpfs                           902108       0    902108   0% /dev/shm
tmpfs                           902108    8696    893412   1% /run
tmpfs                           902108       0    902108   0% /sys/fs/cgroup
/dev/mapper/rhel_rhel8--root  10258432 1630460   8627972  16% /
/dev/sda1                      1038336  167128    871208  17% /boot
tmpfs                           180420       0    180420   0% /run/user/1000
[user@host ~]$ 
```

Arquivos em dois diretórios "montados em" diferentes e seus subdiretórios estão em sistemas de arquivos diferentes. (A correspondência mais específica vence.) Assim, no sistema deste exemplo, você pode criar um link físico entre /var/tmp/link1 e /home/user/file porque ambos são subdiretórios de / mas não de qualquer outro diretório na lista. No entanto, você não pode criar um link físico entre /boot/test/badlink e /home/user/file porque o primeiro arquivo está em um subdiretório de /boot (na lista "montado em") e o segundo arquivo não. 

## Criação de softlinks

O comando ln -s cria um softlink, também chamado de "link simbólico". Um link simbólico não é um arquivo normal, mas um tipo especial de arquivo que aponta para outro arquivo ou diretório existente.

Os links simbólicos têm algumas vantagens sobre links físicos:

=> Eles podem vincular dois arquivos em diferentes sistemas de arquivos.

=> Eles podem apontar para um diretório ou arquivo especial, não apenas um arquivo comum. 

No exemplo a seguir, o comando ln -s é usado para criar um novo link flexível para o arquivo existente /home/user/newfile-link2.txt que será nomeado /tmp/newfile-symlink.txt. 

```sh
[user@host ~]$ ln -s /home/user/newfile-link2.txt /tmp/newfile-symlink.txt
[user@host ~]$ ls -l newfile-link2.txt /tmp/newfile-symlink.txt
-rw-rw-r--. 1 user user 12 Mar 11 19:19 newfile-link2.txt
lrwxrwxrwx. 1 user user 11 Mar 11 20:59 /tmp/newfile-symlink.txt -> /home/user/newfile-link2.txt
[user@host ~]$ cat /tmp/newfile-symlink.txt
Soft Hello World
```
No exemplo anterior, o primeiro caractere da listagem longa para /tmp/newfile-symlink.txt é l, em vez de -. Isso indica que o arquivo é um link simbólico e não um arquivo normal. (Um d indicaria que o arquivo é um diretório.)

Quando o arquivo regular original é excluído, o link simbólico continua apontando para o arquivo, mas o destino some. Um link simbólico que esteja apontando para um arquivo ausente é denominado "link simbólico pendente". 

```sh
[user@host ~]$ rm -f newfile-link2.txt
[user@host ~]$ ls -l /tmp/newfile-symlink.txt
lrwxrwxrwx. 1 user user 11 Mar 11 20:59 /tmp/newfile-symlink.txt -> /home/user/newfile-link2.txt
[user@host ~]$ cat /tmp/newfile-symlink.txt
cat: /tmp/newfile-symlink.txt: No such file or directory
```

Importante

Um efeito colateral do link simbólico pendente no exemplo anterior é que, se você criar posteriormente um novo arquivo com o mesmo nome do arquivo excluído (/home/user/newfile-link2.txt), o link não estará mais "pendurado" e apontará para o novo arquivo.

Os links físicos não funcionam assim. Se você excluir um link físico e, em seguida, usar ferramentas normais ( ao invés de ln) para criar um novo arquivo com o mesmo nome, o novo arquivo não será vinculado ao arquivo antigo.

Uma maneira de comparar links físicos e links simbólicos que pode ajudar você a entender como eles funcionam:

=> Um link físico aponta um nome para dados em um dispositivo de armazenamento

=> Um link simbólico aponta um nome para outro nome, que aponta para dados em um dispositivo de armazenamento 

Um link simbólico pode apontar para um diretório. Nesse caso, o link simbólico atuará como um diretório. Alterar para o link simbólico com cd fará com que o diretório de trabalho atual seja o diretório vinculado. Algumas ferramentas podem acompanhar o fato de você ter seguido um link simbólico para chegar lá. Por exemplo, por padrão cd atualizará seu diretório de trabalho atual usando o nome do link simbólico, em vez do nome do diretório real. (Existe uma opção, -P, que o atualizará com o nome do diretório real.) 

 No exemplo a seguir, um link simbólico denominado /home/user/configfiles é criado que aponta para o diretório /etc. 

```sh
[user@host ~]$ ln -s /etc /home/user/configfiles
[user@host ~]$ cd /home/user/configfiles
[user@host configfiles]$ pwd
/home/user/configfiles
```

## Correspondência de nomes de arquivos com expansões de shell

O shell Bash apresenta várias maneiras de expandir uma linha de comando, incluindo a correspondência de padrões, a expansão de diretório pessoal, a expansão de string e a substituição de variável. Talvez a mais poderosa delas seja a capacidade de correspondência de nome de caminhos, historicamente chamada de globbing. O recurso de globbing do Bash, por vezes chamado de “wildcards”, facilita o gerenciamento de grandes números de arquivos. Ao usar metacaracteres que se “expandem” para corresponder a nomes de caminho e de arquivo que são procurados, os comandos são executados em um conjunto específico de arquivos de uma só vez. 

Correspondência de padrões

Globbing é uma operação de análise de comandos do shell que expande um padrão de caracteres curinga em uma lista de nomes de caminho correspondentes. Metacaracteres de linha de comando são substituídos pela lista de correspondência antes da execução do comando. Os padrões que não retornam correspondências exibem a solicitação de padrão original como texto literal. Os itens a seguir são metacaracteres e classes de padrões comuns. 

Tabela 3.3. Tabela de metacaracteres e correspondências

```sh
* =>  Qualquer string com zero ou mais caracteres. 

? => Qualquer caractere único. 


[abc...] => Qualquer caractere na classe entre colchetes. 

[!abc...] => Qualquer caractere que não esteja na classe entre colchetes. 

[^abc...] => Qualquer caractere que não esteja na classe entre colchetes. 

[[:alpha:]] => Qualquer caractere alfabético. 

[[:lower:]] => Qualquer caractere em minúsculas.

[[:upper:]] => Qualquer caractere em maiúsculas. 

[[:alnum:]] => Qualquer caractere alfabético ou numérico. 

[[:punct:]] => Qualquer caractere imprimível que não seja alfanumérico nem um espaço. 

[[:digit:]] => Qualquer dígito único de 0 a 9. 

[[:space:]] => Qualquer caractere de espaço único. Isso pode incluir recuos, novas linhas, retornos, avanços de página ou espaços. 
```
Para os próximos exemplos, digamos que você executou os comandos a seguir para criar alguns arquivos de amostra. 

```sh
[user@host ~]$ mkdir glob; cd glob
[user@host glob]$ touch alfa bravo charlie delta echo able baker cast dog easy
[user@host glob]$ ls
able  alfa  baker  bravo  cast  charlie  delta  dog  easy  echo
[user@host glob]$ 
```

O primeiro exemplo usará combinações de padrão simples com os caracteres asterisco * e ponto de interrogação '?' e uma classe de caracteres para corresponder a alguns desses nomes de arquivo.

##  Expansão de til

O caractere til '~' corresponde ao diretório pessoal do usuário atual. Se uma string diferente de uma barra '/' for iniciada, o shell interpretará a string até essa barra como um nome de usuário, se houver uma correspondência, e substituirá a cadeia pelo caminho absoluto para o diretório pessoal desse usuário. Se nenhum nome de usuário for correspondente, um til real seguido da string será usado.

No exemplo a seguir, o comando echo é usado para exibir o valor do caractere til. O comando echo também pode ser usado para exibir os valores de chaves e caracteres de expansão de variáveis, entre outros. 

```sh
[user@host glob]$ echo ~root
/root
[user@host glob]$ echo ~user
/home/user
[user@host glob]$ echo ~/glob
/home/user/glob
[user@host glob]$ 
```
## Expansão de chave

A expansão de chave é usada para gerar strings de caracteres distintas. As chaves contêm uma lista de strings separadas por vírgula ou uma expressão de sequência. O resultado inclui o texto anterior ou o posterior à definição de chave. As expansões de chave podem ser aninhadas uma dentro da outra. Além disso, a sintaxe de dois pontos (..) é expandida para uma sequência tal que {m..p} será expandido para m n o p. 

```sh
[user@host glob]$ echo {Sunday,Monday,Tuesday,Wednesday}.log
Sunday.log Monday.log Tuesday.log Wednesday.log
[user@host glob]$ echo file{1..3}.txt
file1.txt file2.txt file3.txt
[user@host glob]$ echo file{a..c}.txt
filea.txt fileb.txt filec.txt
[user@host glob]$ echo file{a,b}{1,2}.txt
filea1.txt filea2.txt fileb1.txt fileb2.txt
[user@host glob]$ echo file{a{1,2},b,c}.txt
filea1.txt filea2.txt fileb.txt filec.txt
[user@host glob]$ 
```

Um uso prático da expansão de chaves é criar rapidamente vários arquivos ou diretórios. 

```sh
[user@host glob]$ mkdir ../RHEL{6,7,8}
[user@host glob]$ ls ../RHEL*
RHEL6 RHEL7 RHEL8
[user@host glob]$ 
```

## Expansão variável

Uma variável age como um contêiner nomeado que pode armazenar um valor na memória. As variáveis facilitam o acesso e modificam os dados armazenados a partir da linha de comando ou dentro de um script de shell.

Você pode atribuir dados como um valor a uma variável usando a seguinte sintaxe: 

```sh
[user@host ~]$ VARIABLENAME=value
```
Você pode usar a expansão variável para converter o nome da variável para o valor na linha de comando. Se uma string começar com um cifrão ($), o shell tentará usar o restante dessa cadeia como um nome de variável e o substituirá por qualquer valor que a variável tenha. 

```sh
[user@host ~]$ USERNAME=operator
[user@host ~]$ echo $USERNAME
operator
```
Para ajudar a evitar erros devido a outras expansões de shell, você pode colocar o nome da variável entre chaves, por exemplo ${VARIABLENAME} . 

```sh
[user@host ~]$ USERNAME=operator
[user@host ~]$ echo ${USERNAME}
operator
```
As variáveis do shell e as formas de usá-las serão abordadas com mais profundidade posteriormente neste curso. 

## Substituição de comandos

A substituição de comandos permite que a saída de um comando substitua o próprio comando. A substituição de comandos ocorre quando um comando é colocado entre parênteses e precedido por um cifrão ($). A forma $(command) pode aninhar várias expansões de comandos, uma dentro da outra. 

```sh
[user@host glob]$ echo Today is $(date +%A).
Today is Wednesday.
[user@host glob]$ echo The time is $(date +%M) minutes past $(date +%l%p).
The time is 26 minutes past 11AM.
[user@host glob]$ 
```
## Proteção de argumentos da expansão

Vários caracteres têm significado especial no shell Bash. Para evitar que o shell execute expansões de shell em partes de sua linha de comando, você pode usar aspas e escapes em caracteres e strings. 

A barra invertida (\) é um caractere de escape no shell Bash. Ela protegerá contra expansão o caractere que vem imediatamente depois. 

```sh
[user@host glob]$ echo The value of $HOME is your home directory.
The value of /home/user is your home directory.
[user@host glob]$ echo The value of \$HOME is your home directory.
The value of $HOME is your home directory.
[user@host glob]$ 
```

No exemplo anterior, proteger o cifrão de expansão fez com que o Bash o tratasse como um caractere regular e não executou a expansão de variável em $HOME .

Para proteger strings mais longas, aspas simples (') ou duplas (") são usadas para delimitar strings. Elas têm efeitos ligeiramente diferentes. As aspas simples param toda a expansão do shell. As aspas duplas param a maior parte da expansão do shell. 

Use aspas duplas para suprimir globbing e a expansão do shell, mas ainda permitir substituição de comandos e de variáveis. 

```sh
[user@host glob]$ myhost=$(hostname -s); echo $myhost
host
[user@host glob]$ echo "***** hostname is ${myhost} *****"
***** hostname is host *****
[user@host glob]$ 
```

Use aspas simples para interpretar todo o texto literalmente. 

```sh
[user@host glob]$ echo "Will variable $myhost evaluate to $(hostname -s)?"
Will variable host evaluate to host?
[user@host glob]$ echo 'Will variable $myhost evaluate to $(hostname -s)?'
Will variable $myhost evaluate to $(hostname -s)?
[user@host glob]$ 
```

Neste capítulo, você aprendeu que:

Os arquivos em um sistema Linux são organizados em uma única árvore de diretório invertida, conhecida como hierarquia do sistema de arquivos.

Os caminhos absolutos começam com um / e especificam a localização de um arquivo na hierarquia do sistema de arquivos.

Os caminhos relativos não começam com um / e especificam a localização de um arquivo em relação ao diretório de trabalho atual.

Cinco comandos principais são usados para gerenciar arquivos: mkdir , rmdir , cp , mv e rm .

Os links físicos e os links simbólicos são maneiras diferentes de ter vários nomes de arquivos apontando para os mesmos dados.

O shell Bash fornece recursos de correspondência, expansão e substituição de padrões para ajudar você a executar comandos de maneira eficiente. 

## Capítulo 4. Ajuda no Red Hat Enterprise Linux

