# site-fxshell

Esse site

Este site usa o hugo , um gerador estático de sites. Não há razões particulares para eu escolher hugo, quis escolher uma nova linguagem, que está no hype neste momento que é o Go. Existem inúmeras outras soluções disponíveis mas queria um lugar para colocar os writeups e informações sobre meus estudos sobre hacking e pentest, eu precisava de algo simples o suficiente para evitar o incômodo de aprender uma nova linguagem ou quebrar a cabeça com isso. Ai o Google me levou ao hugo.

#Instalação
Pra instalar no Debian ou Ubuntu precisa dessas dependências instaladas

# dependências
>sudo apt-get install build-essential curl file git 

# instala o brew para linux
>sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

# configura o brew
>test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)

>test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)

>test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile

>echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile


# Instalando o Hugo (linux)
Agora digite a linha abaixo é tudo o que você precisa para usar o Hugo será instalado:

>> brew install hugo

# download do repositório do sublime-text3
>wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

Estou usando o sublime como meu editor de código, você pode usar um editor que goste, atom, vim, emacs.

# habilita o repositório
>echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list

# atualiza os repositórios
>sudo apt update

# instala
>sudo apt install sublime-text fish

O 'fish' é questão de gosto, é apenas para facilitar e auto completar comandos no bash. 

# instala
brew install hugo


# criar o diretório que irá armazenar o seu site
>~/Documentos/meu-site/fxshell 


# ir para o diretório
>cd ~/Documentos/meu-site/fxshell


# mudar de bash para fish
>fish

```
Essa pasta, "fxshell" ou seu site, vai concentrar tudo o que eu preciso prara o desenvolvimento do projeto: git init, hugo e os demais arquivos, como css, html, js, md etc.
```


    É muito importante que você domine isso: saber aonde está e para onde vai. Cada vez que você digita ../ você volta um nível para o diretório ascendente. Veja:

```
# ir para um diretório a frente
~/Documentos [1] $ cd /home/fpmatta/Documentos/fxshell

# saber onde estou
fpmatta@T-REX ~/D/f/site> pwd
/home/fpmatta/Documentos/fxshell/site

# voltar um diretório
fpmatta@T-REX ~/D/f/s/fxshell (master)> cd ../
fpmatta@T-REX ~/D/f/site> 


# voltar diretórios
fpmatta@T-REX ~/D/f/s/fxshell (master)> cd ../
fpmatta@T-REX ~/D/f/site> 

# saber onde estou
~/D/a/b/go_youtube $ pwd
/home/tmenegaz/Documentos/aula/blog/go_youtube

# voltar diretórios
fpmatta@T-REX ~/D/fxshell> cd ..

# saber onde estou
fpmatta@T-REX ~/Documentos> pwd
/home/fpmatta/Documentos
```
#Então treine navegar pelos diretório e subdiretório, se você ainda não domina isso.

Então vamos usar Hugo: digite ai no seu terminal, e tenha certeza de que está no diretório do seu projeto:

>fpmatta@T-REX ~/D/f/s/fxshell (master)> pwd
/home/fpmatta/Documentos/fxshell/site/fxshell


#Criando um novo site
>hugo new mynewsite


# ir para dentro do seu site
>cd mynewsite

`Agora vou iniciar o git para o projeto no meu github e também para poder pegar themes.`

`O repositório já existe no meu github.`

# cria uma pasta oculta chamada .git com as configurações necessárias para usar o git, a partir daqui
>git init


# posso salvar e recuperar arquivos do meu projeto no meu repositório github
>git remote add origin git@github.com:fxshelll/site-fxshell.git


#Temas

Hugo usa temas eu peguei um tema sombrio e minimalista, curti muito ele. A instalação é bem fácil, basta clonar o git do proprio projeto deles, para dentro da pasta themas. (~/mynewsite/themes/):

``` projeto
https://after-dark.habd.as/feature/quick-install/
```
>> git clone https://git.habd.as/comfusion/after-dark.git

#Configuração

O nome do tema precisa ser adicionado config.toml(ele usa toml por padrão)

`theme = "after-dark"`

#Nova postagem

`hugo new posts/my-first-post.md`

# iniciar o servidor pra exibir o conteúdo que ainda é um rascunho
hugo server -D


#Alguns hacks

Aqui as coisas interessantes começam. O comportamento padrão não estava funcionando silenciosamente, conforme desejado. Primeiro, queria que a primeira página fosse estática, em vez de exibir a lista das postagens. Esse comportamento é tratado nos layouts de tema ( layouts/index.html). Ele usa uma linguagem de modelo (que lembra Jinja ).

```html
{{ define "title" -}}
  {{ .Site.Title }}
{{- end }}
{{ define "header" }}
  {{ partial "menu.html" . }}
{{ end }}
{{ define "main" }}
  <header>
    <h1>{{ .Title }}</h1>
  </header>
  {{ range (.Paginate (where .Data.Pages "Type" "post")).Pages }}
    {{ partial "page-summary.html" . }}
  {{ end }}
{{ end }}
{{ define "footer" }}
  {{ partial "pagination.html" . }}
  {{ partial "powered-by.html" . }}
{{ end }}
```
Sem saber os detalhes de como isso está funcionando, é bastante óbvio descobrir o que faz:

  > Exibir o título do site
  > Injetar o conteúdo do menu
  > Outro título
  > Passe pelas postagens 
  > Colocar algumas coisas no rodapé

O loop é a peça interessante. Queremos substituir esse comportamento. Será substituído pelo seguinte:

```html
{{ define "title" -}}
  {{ .Site.Title }}
{{- end }}
{{ define "header" }}
  {{ partial "menu.html" . }}
{{ end }}
{{ define "main" }}
  {{ range .Data.Pages }}
    {{if eq .Type "index" }} 
      {{.Content}}
    {{end}}
  {{ end }}
{{ end }}
{{ define "footer" }}
  {{ partial "powered-by.html" . }}
{{ end }}
```
Isso percorre as páginas e, se encontrar uma página de um tipo index, ela será exibida. A indexpágina será salva no conteúdo ( index.md), com o seguinte cabeçalho:


>title: ""
type: index


Também vamos remover o título, que não é realmente necessário na página inicial.

Poderíamos substituir o layout do tema, mas é melhor mantê-lo como está. Podemos sobrescrever o layout do tema, tendo index.htmlna layouts/pasta do site. Uma estratégia semelhante é usada para layouts/partials/page-summary.htmlalterar a exibição da lista de postagens.
Implantando com GitHub

Estou seguindo o hugo doc oficial para isso.

Existem dois repositórios Git: um para a fonte e outro para o site gerado. O local é gerado na public/pasta de repo fonte (com na fonte evitar controlar duas vezes o local gerado)public/.gitignore

Digitar hugoa penas gera o site em public/. hugo `serve` usado para exibição local.
