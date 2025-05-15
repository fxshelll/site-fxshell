#!/bin/bash
set -e

echo "🚀 Gerando site com Hugo..."
hugo

cd public
git add .
git commit -m "🚀 Deploy gerado - $(date '+%d/%m/%Y %H:%M:%S')" || echo "⚠️ Nada para commitar"
git push origin master

cd ..
git add .
git commit -m "📚 Atualizações no conteúdo Hugo - $(date '+%d/%m/%Y %H:%M:%S')" || echo "⚠️ Nada para commitar"
git push origin master

echo "✅ Deploy concluído com sucesso!"
