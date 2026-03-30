---
title: "Seu terminal pode ser muito mais produtivo com Zsh"
date: 2026-03-30T00:00:00-03:00
draft: false
---

Se você passa boa parte do dia no terminal, vale muito a pena investir alguns minutos configurando o Zsh com Oh My Zsh. A diferença na produtividade é real — autocomplete inteligente, highlight de sintaxe, histórico gigante e plugins que evitam você digitar a mesma coisa mil vezes.

Esse post é baseado na minha configuração pessoal do `.zshrc`. Bora ver o que tem dentro.

---

## Instalando o Zsh e Oh My Zsh

```sh
# Instalar o Zsh (Debian/Ubuntu)
sudo apt install zsh

# Definir como shell padrão
chsh -s $(which zsh)

# Instalar o Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

---

## Tema

O tema padrão que uso é o `robbyrussell` — simples, limpo e mostra o branch do git direto no prompt.

```sh
ZSH_THEME="robbyrussell"
```

Se quiser algo mais visual com ícones e informações de contexto (k8s, cloud, etc.), vale testar o **Powerlevel10k**:

```sh
# Instalar o Powerlevel10k
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# No .zshrc:
ZSH_THEME="powerlevel10k/powerlevel10k"
```

---

## Plugins essenciais

```sh
plugins=(
   git
   dnf
   zsh-syntax-highlighting
   zsh-autosuggestions
)
```

### zsh-autosuggestions

Sugere comandos em cinza enquanto você digita, baseado no seu histórico. Pressione `→` para aceitar. Um dos plugins mais úteis que existem.

```sh
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

### zsh-syntax-highlighting

Colore os comandos em tempo real — verde se o comando existe, vermelho se não existe. Evita muito erro de digitação.

```sh
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### git

Plugin built-in do Oh My Zsh. Traz dezenas de aliases prontos:

```sh
gst   # git status
gco   # git checkout
gcmsg # git commit -m
gp    # git push
gl    # git pull
glog  # git log bonito
```

---

## Histórico gigante e inteligente

Essa é uma das partes que mais uso. Um histórico bem configurado vale ouro — principalmente quando você precisa lembrar aquele comando raro que rodou meses atrás.

```sh
HISTFILE=${ZDOTDIR:-$HOME}/.zsh_history
SAVEHIST=1000000
HISTSIZE=1000000
HIST_STAMPS="yyyy-mm-dd"

setopt INC_APPEND_HISTORY        # Grava no arquivo imediatamente (não só ao fechar o shell)
setopt SHARE_HISTORY             # Compartilha histórico entre todas as sessões abertas
setopt HIST_EXPIRE_DUPS_FIRST    # Remove duplicatas primeiro quando o histórico encher
setopt HIST_IGNORE_DUPS          # Não grava se o comando foi o mesmo do anterior
setopt HIST_IGNORE_ALL_DUPS      # Remove entradas antigas se o mesmo comando for repetido
setopt HIST_FIND_NO_DUPS         # Não mostra duplicatas ao navegar com ↑
setopt HIST_IGNORE_SPACE         # Não grava comandos que começam com espaço (útil para senhas)
setopt HIST_SAVE_NO_DUPS         # Não escreve duplicatas no arquivo de histórico
setopt HIST_REDUCE_BLANKS        # Remove espaços desnecessários antes de gravar

alias history="history 0"        # Mostra o histórico completo (sem limite de linhas)
```

O `HIST_IGNORE_SPACE` é especialmente útil: qualquer comando precedido de espaço não entra no histórico — ótimo pra quando você cola uma senha ou token diretamente no terminal.

---

## fzf — busca fuzzy no histórico

O `fzf` transforma o `Ctrl+R` em uma busca interativa e fuzzy pelo histórico inteiro. Essencial.

```sh
# Instalar
sudo apt install fzf
# ou via git
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install
```

No `.zshrc`:

```sh
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

Depois é só apertar `Ctrl+R` e digitar qualquer trecho do comando que você procura.

---

## Meu `.zshrc` completo

```sh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

HISTFILE=${ZDOTDIR:-$HOME}/.zsh_history
SAVEHIST=1000000
HISTSIZE=1000000
HIST_STAMPS="yyyy-mm-dd"

setopt INC_APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_SAVE_NO_DUPS
setopt HIST_REDUCE_BLANKS

alias history="history 0"

plugins=(
   git
   dnf
   zsh-syntax-highlighting
   zsh-autosuggestions
)

source $ZSH/oh-my-zsh.sh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
export PATH="$HOME/.local/bin:$PATH"
```

---

Com isso você já tem um terminal muito mais agradável de usar. Os plugins de autosuggestions e syntax highlighting sozinhos já valem a instalação. O histórico inteligente é o tipo de coisa que você sente falta quando usa uma máquina sem ele.
