# Software Web para Autenticação de Usuários – APS Domínios de Software 2026/2 (UFG/INF)

Equipe (ordem alfabética): Júlia de Souza Nascimento · Kesley Soares da Silva · Verônica Ribeiro Oliveira Palmeira

Projeto de um software Web que **recebe credenciais, verifica se correspondem a um usuário válido e retorna a identidade do usuário** (ou um erro de autenticação). Somente verificação de credenciais.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `docs/00-controle.md` | Controle de autoria/revisão e declaração de uso de IA |
| `docs/01-ambiente/` | Seção 1 – ambiente operacional (navegador, DNS, Nginx, Uvicorn, PostgreSQL, Docker) |
| `docs/02-projeto/` | Seção 2 – requisitos, arquitetura, componentes, dados, API, comportamento, segurança, rastreabilidade |
| `docs/apendices/` | Prompts de IA, plano de trabalho e riscos, registros de reuniões |
| `docs/diagramas/*.mmd` | Fontes Mermaid dos diagramas (versionáveis) |
| `docs/img/` | Diagramas renderizados |
| `docs/referencias.yml` | Referências bibliográficas (ABNT) |
| `build/build.py` | Gera o PDF único de entrega |
| `kanban/` | Lista de issues e script para criar o quadro Kanban |

Cada item de informação começa com `@meta(IT-x.y, autor, revisor)`; o build gera a tabela artefato/autor/revisor, numera figuras e tabelas, cria o sumário navegável e **falha** se houver citação sem referência, âncora quebrada ou autor = revisor.

## Gerar o PDF

```bash
sudo apt install pandoc            # ou equivalente
pip install weasyprint pyyaml
npm install -g @mermaid-js/mermaid-cli   # só se for alterar diagramas
python3 build/build.py                  # --diagramas para re-renderizar os .mmd
# saída: build/APS-Autenticacao-Web.pdf
```

## Fluxo de trabalho sugerido

1. Uma *issue* por item de informação (ver `kanban/issues.md`), com responsável = autor(a).
2. Uma *branch* por item → *pull request* → revisão pelo(a) revisor(a) indicado(a) (comentários no PR servem de evidência).
3. Docente incluída como colaboradora do repositório (adriana.silveira.souza@gmail.com).
