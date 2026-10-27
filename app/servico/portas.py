from typing import Protocol

from app.servico.modelos import Usuario


class RepositorioUsuario(Protocol):
    def buscar_por_login(self, login: str) -> Usuario | None: ...

    def buscar_por_email(self, email: str) -> Usuario | None: ...


class VerificadorSenha(Protocol):
    def verificar(self, senha: str, hash_senha: str) -> bool: ...

    def verificar_ficticio(self, senha: str) -> None:
        """Gasta o mesmo tempo de uma verificação real quando o usuário não existe."""
        ...
