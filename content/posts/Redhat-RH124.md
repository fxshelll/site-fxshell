---
title: "Redhat RH124"
date: 2021-03-16T23:03:55-03:00
draft: false
---

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

Por exemplo, para /home/user/Videos, somente Videos é exibido. O prompt exibe o caractere til '~' quando o diretório de trabalho atual é o diretório pessoa

O comando touch normalmente atualiza o carimbo de data e hora de um arquivo para a data e a hora atuais, sem modificá-lo. Isso é útil para a criação de arquivos vazios, que podem ser usados para prática, pois o uso desse comando em um nome de arquivo que não existe faz com que o arquivo seja criado. No exemplo a seguir, o comando touch cria arquivos de prática nos subdiretórios Documents e Videos.  

__

