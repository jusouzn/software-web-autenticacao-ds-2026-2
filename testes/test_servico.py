import pytest

from app.servico.modelos import FalhaAutenticacao
from conftest import JULIA, SENHA_JULIA


def test_cv01_email_e_senha_corretos_retorna_identidade(servico):
    identidade = servico.autenticar("julia@exemplo.com.br", SENHA_JULIA)

    assert identidade == JULIA.identidade()
    assert not hasattr(identidade, "hash_senha")


def test_login_e_senha_corretos_retorna_identidade(servico):
    assert servico.autenticar("julia", SENHA_JULIA).login == "julia"


def test_cv02_identificador_e_normalizado(servico):
    assert servico.autenticar("  JULIA ", SENHA_JULIA).login == "julia"
    assert servico.autenticar(" Julia@Exemplo.com.BR", SENHA_JULIA).login == "julia"


def test_cv03_usuario_inexistente_faz_verificacao_ficticia(servico, verificador):
    with pytest.raises(FalhaAutenticacao):
        servico.autenticar("ninguem", SENHA_JULIA)

    assert verificador.chamadas_ficticias == 1
    assert verificador.chamadas == 0


def test_cv04_senha_incorreta(servico):
    with pytest.raises(FalhaAutenticacao):
        servico.autenticar("julia", "senha-errada")


def test_cv05_senha_nao_e_normalizada(servico):
    with pytest.raises(FalhaAutenticacao):
        servico.autenticar("julia", SENHA_JULIA.upper())


def test_rn01_login_nao_e_procurado_como_email(servico):
    # "julia" é login; sem @ o serviço não deve procurar na coluna de e-mail, e vice-versa
    with pytest.raises(FalhaAutenticacao):
        servico.autenticar("julia@", SENHA_JULIA)
