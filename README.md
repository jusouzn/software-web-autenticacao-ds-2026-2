# Software Web para Autenticação de Usuários – APS Domínios de Software 2026/2 (UFG/INF)

Equipe (ordem alfabética): Júlia de Souza Nascimento · Kesley Soares da Silva · Verônica Ribeiro Oliveira Palmeira

Projeto de um software Web que **recebe credenciais, verifica se correspondem a um usuário válido e retorna a identidade do usuário** (ou um erro de autenticação). Somente verificação de credenciais.

## Como executar

Pré-requisito: Docker com Docker Compose.

```bash
docker compose up -d --build
```

Depois acesse <https://localhost>. O certificado é autoassinado, então o navegador vai pedir confirmação na primeira vez.

Usuários de teste (carregados por `db/02-carga-teste.sql`):

| Login | E-mail | Senha |
|---|---|---|
| julia | julia@exemplo.com.br | S3nh@-de-teste |
| kesley | kesley@exemplo.com.br | Kesley#2026 |
| veronica | veronica@exemplo.com.br | Veronica!2026 |

Para testar a API direto:

```bash
curl -k https://localhost/api/v1/autenticacao \
  -H "Content-Type: application/json" \
  -d '{"identificador": "julia", "senha": "S3nh@-de-teste"}'
```

Os scripts de `db/` só rodam quando o volume do banco é criado. Se mudar algum deles, recrie com `docker compose down -v && docker compose up -d --build`.

## Testes automatizados

Requer Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
```

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
