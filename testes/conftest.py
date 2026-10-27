from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.principal import criar_app
from app.servico.modelos import Usuario
from app.servico.servico_autenticacao import ServicoAutenticacao

JULIA = Usuario(
    id=UUID("6f1c2a9e-4b7d-4c3e-9a51-2f0d8e7b1c44"),
    login="julia",
    email="julia@exemplo.com.br",
    nome="Júlia de Souza Nascimento",
    hash_senha="hash:S3nh@-de-teste",
)
SENHA_JULIA = "S3nh@-de-teste"


class RepositorioEmMemoria:
    def __init__(self, *usuarios: Usuario):
        self.usuarios = list(usuarios)

    def buscar_por_login(self, login):
        return next((u for u in self.usuarios if u.login == login), None)

    def buscar_por_email(self, email):
        return next((u for u in self.usuarios if u.email == email), None)


class VerificadorFalso:
    """Compara texto puro e conta as chamadas, para os testes não dependerem do Argon2."""

    def __init__(self):
        self.chamadas = 0
        self.chamadas_ficticias = 0

    def verificar(self, senha, hash_senha):
        self.chamadas += 1
        return hash_senha == f"hash:{senha}"

    def verificar_ficticio(self, senha):
        self.chamadas_ficticias += 1


@pytest.fixture
def repositorio():
    return RepositorioEmMemoria(JULIA)


@pytest.fixture
def verificador():
    return VerificadorFalso()


@pytest.fixture
def servico(repositorio, verificador):
    return ServicoAutenticacao(repositorio, verificador)


@pytest.fixture
def cliente(servico):
    with TestClient(criar_app(servico)) as cliente:
        yield cliente
