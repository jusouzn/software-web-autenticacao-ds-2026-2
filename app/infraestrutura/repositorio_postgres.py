import psycopg
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool

from app.servico.modelos import RepositorioIndisponivel, Usuario

_POR_LOGIN = "SELECT id, login, email, nome, hash_senha FROM usuario WHERE login = %s"
_POR_EMAIL = "SELECT id, login, email, nome, hash_senha FROM usuario WHERE email = %s"


class RepositorioUsuarioPostgres:
    def __init__(self, pool: ConnectionPool):
        self._pool = pool

    def buscar_por_login(self, login: str) -> Usuario | None:
        return self._buscar(_POR_LOGIN, login)

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self._buscar(_POR_EMAIL, email)

    def _buscar(self, consulta: str, valor: str) -> Usuario | None:
        try:
            with self._pool.connection() as conexao:
                with conexao.cursor(row_factory=class_row(Usuario)) as cursor:
                    cursor.execute(consulta, (valor,))
                    return cursor.fetchone()
        except psycopg.OperationalError as erro:
            # PoolTimeout também herda de OperationalError
            raise RepositorioIndisponivel() from erro
