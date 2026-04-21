#!/bin/bash
set -e

# ─────────────────────────────────────────────
#  setup.sh — Configura o ambiente do site Hugo
#  Repo: github.com/fxshelll/site-fxshell
#
#  Uso rápido (em outro computador):
#  curl -fsSL https://raw.githubusercontent.com/fxshelll/site-fxshell/master/setup.sh | bash
# ─────────────────────────────────────────────

REPO_URL="https://github.com/fxshelll/site-fxshell.git"
REPO_DIR="site-fxshell"
HUGO_MIN_VERSION="0.100.0"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
info() { echo -e "${BLUE}[--]${NC} $1"; }
warn() { echo -e "${YELLOW}[!!]${NC} $1"; }
fail() { echo -e "${RED}[ERRO]${NC} $1"; exit 1; }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   Setup — FXShell Site Hugo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 1. Sistema operacional ──────────────────────
info "Detectando sistema operacional..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &>/dev/null; then
        PKG_MANAGER="apt"
        ok "Linux (Debian/Ubuntu) detectado"
    elif command -v dnf &>/dev/null; then
        PKG_MANAGER="dnf"
        ok "Linux (Fedora/RHEL) detectado"
    elif command -v pacman &>/dev/null; then
        PKG_MANAGER="pacman"
        ok "Linux (Arch) detectado"
    else
        warn "Gerenciador de pacotes não reconhecido — instale Hugo e Git manualmente se necessário"
        PKG_MANAGER="unknown"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PKG_MANAGER="brew"
    ok "macOS detectado"
    if ! command -v brew &>/dev/null; then
        fail "Homebrew não encontrado. Instale em: https://brew.sh"
    fi
else
    fail "Sistema operacional não suportado: $OSTYPE"
fi

# ── 2. Git ──────────────────────────────────────
info "Verificando Git..."
if command -v git &>/dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    ok "Git $GIT_VERSION já instalado"
else
    warn "Git não encontrado. Instalando..."
    case "$PKG_MANAGER" in
        apt)    sudo apt-get update -qq && sudo apt-get install -y git ;;
        dnf)    sudo dnf install -y git ;;
        pacman) sudo pacman -Sy --noconfirm git ;;
        brew)   brew install git ;;
        *)      fail "Instale o Git manualmente: https://git-scm.com" ;;
    esac
    ok "Git instalado com sucesso"
fi

# ── 3. Hugo Extended ────────────────────────────
info "Verificando Hugo..."

version_gte() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}

if command -v hugo &>/dev/null; then
    CURRENT_HUGO=$(hugo version | grep -oP '\d+\.\d+\.\d+' | head -1)
    if version_gte "$CURRENT_HUGO" "$HUGO_MIN_VERSION"; then
        # Verificar se é extended (necessário para SCSS/temas)
        if hugo version | grep -qi "extended"; then
            ok "Hugo Extended $CURRENT_HUGO já instalado"
            HUGO_OK=true
        else
            warn "Hugo $CURRENT_HUGO instalado mas NÃO é a versão Extended (necessária para o tema)"
            HUGO_OK=false
        fi
    else
        warn "Hugo $CURRENT_HUGO encontrado mas versão mínima requerida é $HUGO_MIN_VERSION"
        HUGO_OK=false
    fi
else
    warn "Hugo não encontrado"
    HUGO_OK=false
fi

if [ "$HUGO_OK" != "true" ]; then
    info "Instalando Hugo Extended via pacote oficial..."
    case "$PKG_MANAGER" in
        apt)
            # Instala a versão extended disponível no repositório
            sudo apt-get update -qq && sudo apt-get install -y hugo
            # Verificar se instalou a versão extended
            if ! hugo version | grep -qi "extended"; then
                warn "Repositório apt não tem Hugo Extended. Baixando binário oficial..."
                HUGO_DEB_URL="https://github.com/gohugoio/hugo/releases/download/v0.152.2/hugo_extended_0.152.2_linux-amd64.deb"
                TMP_DEB=$(mktemp /tmp/hugo_XXXXXX.deb)
                curl -fsSL "$HUGO_DEB_URL" -o "$TMP_DEB"
                sudo dpkg -i "$TMP_DEB"
                rm -f "$TMP_DEB"
            fi
            ;;
        dnf)
            sudo dnf install -y hugo
            ;;
        pacman)
            sudo pacman -Sy --noconfirm hugo
            ;;
        brew)
            brew install hugo
            ;;
        *)
            fail "Instale Hugo Extended manualmente: https://gohugo.io/installation/"
            ;;
    esac

    CURRENT_HUGO=$(hugo version | grep -oP '\d+\.\d+\.\d+' | head -1)
    ok "Hugo $CURRENT_HUGO instalado"
fi

# ── 4. curl (para downloads opcionais) ──────────
info "Verificando curl..."
if command -v curl &>/dev/null; then
    ok "curl já instalado"
else
    case "$PKG_MANAGER" in
        apt)    sudo apt-get install -y curl ;;
        dnf)    sudo dnf install -y curl ;;
        pacman) sudo pacman -Sy --noconfirm curl ;;
        brew)   brew install curl ;;
    esac
    ok "curl instalado"
fi

# ── 5. Configuração do Git ───────────────────────
echo ""
info "Verificando configuração do Git..."

GIT_NAME=$(git config --global user.name 2>/dev/null || true)
GIT_EMAIL=$(git config --global user.email 2>/dev/null || true)

if [ -z "$GIT_NAME" ]; then
    echo -e "${YELLOW}[!!]${NC} git user.name não configurado"
    read -rp "    Digite seu nome para o Git: " INPUT_NAME
    git config --global user.name "$INPUT_NAME"
    ok "git user.name configurado: $INPUT_NAME"
else
    ok "git user.name: $GIT_NAME"
fi

if [ -z "$GIT_EMAIL" ]; then
    echo -e "${YELLOW}[!!]${NC} git user.email não configurado"
    read -rp "    Digite seu e-mail para o Git: " INPUT_EMAIL
    git config --global user.email "$INPUT_EMAIL"
    ok "git user.email configurado: $INPUT_EMAIL"
else
    ok "git user.email: $GIT_EMAIL"
fi

# ── 6. Autenticação GitHub ───────────────────────
echo ""
info "Verificando autenticação no GitHub..."

GITHUB_AUTH=false

# Testar SSH
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    ok "SSH com GitHub autenticado"
    GITHUB_AUTH=true
fi

# Testar token via credential helper
if [ "$GITHUB_AUTH" = "false" ]; then
    if git ls-remote "$REPO_URL" &>/dev/null; then
        ok "HTTPS com GitHub funcionando"
        GITHUB_AUTH=true
    else
        warn "Sem autenticação com GitHub configurada"
        echo ""
        echo "  Opções para autenticar:"
        echo "  1) SSH Key: adicione sua chave pública em https://github.com/settings/keys"
        echo "  2) Token:   crie em https://github.com/settings/tokens e use como senha no HTTPS"
        echo "  3) GitHub CLI: instale 'gh' e rode 'gh auth login'"
        echo ""
        read -rp "  Pressione Enter para continuar mesmo assim (pode falhar no push)... "
    fi
fi

# ── 7. Clone do repositório ──────────────────────
echo ""
info "Clonando repositório..."

if [ -d "$REPO_DIR" ]; then
    warn "Diretório '$REPO_DIR' já existe"
    read -rp "    Deseja remover e clonar novamente? [s/N] " RESP
    if [[ "$RESP" =~ ^[sS]$ ]]; then
        rm -rf "$REPO_DIR"
        info "Diretório removido"
    else
        info "Usando diretório existente"
        cd "$REPO_DIR"
        SKIP_CLONE=true
    fi
fi

if [ "${SKIP_CLONE:-false}" = "false" ]; then
    git clone "$REPO_URL" "$REPO_DIR"
    cd "$REPO_DIR"
    ok "Repositório clonado em ./$REPO_DIR"
fi

# ── 8. Submodule (public → fxshelll.github.io) ──
echo ""
info "Inicializando submodule public/..."
git submodule update --init --recursive
ok "Submodule inicializado"

info "Verificando branch do submodule..."
cd public
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "HEAD detached")
if [ "$CURRENT_BRANCH" != "master" ]; then
    git checkout master 2>/dev/null || git checkout -b master
fi
ok "Submodule public/ na branch master"
cd ..

# Garantir que o submodule rastreia a branch correta
git config submodule.public.update rebase
ok "Submodule configurado para rebase automático"

# ── 9. Permissão do deploy.sh ────────────────────
echo ""
info "Configurando permissões..."
chmod +x deploy.sh
ok "deploy.sh marcado como executável"

# ── 10. Teste do Hugo ────────────────────────────
echo ""
info "Testando build do Hugo..."
if hugo --minify --quiet; then
    ok "Build do Hugo funcionou corretamente"
else
    warn "Build do Hugo retornou erro — verifique o tema e as configurações"
fi

# ── Resumo final ─────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}   Setup concluído!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Diretório: $(pwd)"
echo "  Hugo:      $(hugo version | head -1)"
echo "  Git:       $(git --version)"
echo ""
echo "  Para publicar:"
echo "    ./deploy.sh"
echo ""
echo "  Para desenvolvimento local:"
echo "    hugo server -D"
echo ""
