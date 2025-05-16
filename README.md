# 📘 Documentação do Projeto Hugo - Site FXSHELL

---

## ♘ Visão Geral

Este projeto é um site estático desenvolvido com [Hugo](https://gohugo.io/), utilizando o tema [After Dark](https://github.com/comfusion/after-dark). O objetivo é publicar conteúdo pessoal, writeups, currículo técnico e experiências em DevOps e Segurança da Informação. O deploy é feito via **GitHub Pages**, a partir de um repositório separado dentro da pasta `public/`.

---
## 📂 Estrutura do Projeto

```
site-fxshell/
├── archetypes/              # Modelos de conteúdo
├── content/                 # Páginas, artigos, writeups
├── layouts/                 # Customizações de layout e HTML
├── public/                  # Site gerado - aponta para GitHub Pages
│   └── .git/                # Repositório separado (fxshelll.github.io)
├── static/                  # Imagens, CSS, JS estáticos
├── themes/after-dark/       # Tema Hugo clonado ou instalado
├── config.toml              # Configuração principal do Hugo
├── deploy.sh                # Script de geração e publicação
└── README.md                # Documentação do projeto
```
## 🚀 Como funciona a geração e deploy
```
1- Edição de conteúdo feita em content/, config.toml ou layouts/
2- Rodar hugo gera os arquivos estáticos em public/
3- O diretório public/ é um repositório separado (aponta para fxshelll.github.io)
4- O script deploy.sh realiza:
      - hugo
      - Commit + push em public/
      - Commit + push em site-fxshell
```
## ⚖️ Script de Deploy
```
#!/bin/bash
set -e

echo "🚀 Gerando site com Hugo..."
hugo

cd public
echo "📅 Publicando no GitHub Pages..."
git add .
git commit -m "🚀 Deploy gerado - $(date '+%d/%m/%Y %H:%M:%S')" || echo "Nada para comitar em public"
git push origin master

cd ..
echo "📄 Salvando alterações do projeto Hugo..."
git add .
git commit -m "📃 Atualizações no projeto Hugo - $(date '+%d/%m/%Y %H:%M:%S')" || echo "Nada para comitar na raiz"
git push origin master

echo "✅ Deploy finalizado com sucesso."
```
## 📅 Rodando localmente
```
cd site-fxshell
hugo server -D
```
-D inclui rascunhos

Site local roda em http://localhost:1313

## 📚 Sobre o Tema After Dark

O tema After Dark traz suporte a:

- Dark mode responsivo
- Renderização minimalista
- Busca integrada via JavaScript
- RSS e sitemap automáticos

Mais sobre o tema: https://github.com/comfusion/after-dark

## ✨ Licença

Este projeto segue a licença MIT. Veja LICENSE se aplicável.
