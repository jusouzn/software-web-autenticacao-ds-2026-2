#!/usr/bin/env bash
# Cria as issues do kanban/issues.md no repositório (requer GitHub CLI autenticado: gh auth login).
set -euo pipefail
REPO="jusouzn/software-web-autenticacao-ds-2026-2"
tail -n +6 "$(dirname "$0")/issues.md" | grep '^| [0-9]' | while IFS='|' read -r _ num titulo autor revisor arquivo _; do
  titulo="$(echo "$titulo" | xargs)"; autor="$(echo "$autor" | xargs)"; revisor="$(echo "$revisor" | xargs)"; arquivo="$(echo "$arquivo" | xargs)"
  gh issue create -R "$REPO" -t "$titulo" -b "Autoria: $autor
Revisão: $revisor
Arquivo: \`$arquivo\`

Critério de pronto: conteúdo verificado contra as referências citadas, revisão registrada em comentário no PR, build do PDF sem erros."
done
