import pytest

from app.servico.modelos import RepositorioIndisponivel
from conftest import SENHA_JULIA

URL = "/api/v1/autenticacao"


def test_cv01_sucesso(cliente):
    resposta = cliente.post(URL, json={"identificador": "julia@exemplo.com.br", "senha": SENHA_JULIA})

    assert resposta.status_code == 200
    assert resposta.headers["cache-control"] == "no-store"
    assert resposta.json() == {
        "autenticado": True,
        "usuario": {
            "id": "6f1c2a9e-4b7d-4c3e-9a51-2f0d8e7b1c44",
            "login": "julia",
            "email": "julia@exemplo.com.br",
            "nome": "Júlia de Souza Nascimento",
        },
    }
    assert "senha" not in resposta.text
    assert "hash" not in resposta.text


def test_cv03_cv04_falhas_sao_identicas(cliente):
    inexistente = cliente.post(URL, json={"identificador": "ninguem", "senha": SENHA_JULIA})
    senha_errada = cliente.post(URL, json={"identificador": "julia", "senha": "errada"})

    for resposta in (inexistente, senha_errada):
        assert resposta.status_code == 401
        assert resposta.headers["content-type"] == "application/problem+json"
        assert resposta.headers["www-authenticate"] == 'Formulario realm="autenticacao"'
        assert resposta.headers["cache-control"] == "no-store"

    assert inexistente.json() == senha_errada.json()
    assert inexistente.json()["detail"] == "Login, e-mail ou senha inválidos."


@pytest.mark.parametrize(
    "corpo",
    [
        {"identificador": "julia"},  # CV06: sem senha
        {"senha": SENHA_JULIA},
        {"identificador": "julia", "senha": SENHA_JULIA, "lembrar": True},  # campo extra
        {"identificador": 123, "senha": SENHA_JULIA},
        {"identificador": "", "senha": SENHA_JULIA},
        {"identificador": "a" * 255, "senha": SENHA_JULIA},
        {"identificador": "julia", "senha": ""},
    ],
)
def test_cv06_requisicao_invalida(cliente, corpo):
    resposta = cliente.post(URL, json=corpo)

    assert resposta.status_code == 400
    assert resposta.headers["content-type"] == "application/problem+json"


def test_cv06_json_malformado(cliente):
    resposta = cliente.post(URL, content=b'{"identificador": ', headers={"Content-Type": "application/json"})
    assert resposta.status_code == 400


def test_cv07_senha_longa_nao_calcula_hash(cliente, verificador):
    resposta = cliente.post(URL, json={"identificador": "julia", "senha": "x" * 129})

    assert resposta.status_code == 400
    assert verificador.chamadas == 0
    assert verificador.chamadas_ficticias == 0


def test_senha_com_128_caracteres_e_aceita(cliente):
    resposta = cliente.post(URL, json={"identificador": "julia", "senha": "x" * 128})
    assert resposta.status_code == 401


def test_corpo_que_nao_e_json(cliente):
    resposta = cliente.post(URL, content=b"identificador=julia", headers={"Content-Type": "text/plain"})

    assert resposta.status_code == 415
    assert resposta.json()["detail"] == "Envie o corpo em JSON."


def test_metodo_nao_permitido(cliente):
    resposta = cliente.get(URL)

    assert resposta.status_code == 405
    assert "POST" in resposta.headers["allow"]
    assert resposta.headers["content-type"] == "application/problem+json"


def test_banco_indisponivel(cliente, repositorio):
    def falhar(_):
        raise RepositorioIndisponivel()

    repositorio.buscar_por_login = falhar
    resposta = cliente.post(URL, json={"identificador": "julia", "senha": SENHA_JULIA})

    assert resposta.status_code == 503
    assert resposta.headers["retry-after"] == "30"
