# Software Web para Autenticação de Usuários – APS Domínios de Software 2026/2 (UFG/INF)

Equipe (ordem alfabética): Júlia de Souza Nascimento · Kesley Soares da Silva · Verônica Ribeiro Oliveira Palmeira

Projeto de um software Web que **recebe credenciais, verifica se correspondem a um usuário válido e retorna a identidade do usuário** (ou um erro de autenticação). Somente verificação de credenciais.

## Diagramas

As fontes dos diagramas ficam em `docs/diagramas/*.mmd` (Mermaid). Para gerar a imagem:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -c docs/diagramas/mermaid.json -i docs/diagramas/<diagrama>.mmd -o docs/img/<diagrama>.png
```

## Fluxo de trabalho sugerido

1. Uma *issue* por item de informação (ver `kanban/issues.md`), com responsável = autor(a).
2. Uma *branch* por item → *pull request* → revisão pelo(a) revisor(a) indicado(a) (comentários no PR servem de evidência).
3. Docente incluída como colaboradora do repositório (adriana.silveira.souza@gmail.com).
