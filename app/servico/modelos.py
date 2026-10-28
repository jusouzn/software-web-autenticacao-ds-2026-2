from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class IdentidadeUsuario:
    id: UUID
    login: str
    email: str
    nome: str


@dataclass(frozen=True)
class Usuario:
    id: UUID
    login: str
    email: str
    nome: str
    hash_senha: str

    def identidade(self) -> IdentidadeUsuario:
        # RN05: a identidade nunca leva a senha nem o hash
        return IdentidadeUsuario(self.id, self.login, self.email, self.nome)


class FalhaAutenticacao(Exception):
    """Usuário inexistente ou senha incorreta. Os dois casos são tratados igual (RN04)."""


class RepositorioIndisponivel(Exception):
    """O banco de dados não respondeu."""
