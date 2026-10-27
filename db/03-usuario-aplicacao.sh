#!/bin/sh
# Cria o usuário de banco usado pela aplicação, só com permissão de leitura.
# É um .sh (e não .sql) porque precisa ler a senha da variável de ambiente.
set -e

psql -v ON_ERROR_STOP=1 -v senha="$APP_DB_SENHA" \
     --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'SQL'
CREATE ROLE app_autenticacao LOGIN PASSWORD :'senha';
GRANT SELECT ON usuario TO app_autenticacao;
SQL
