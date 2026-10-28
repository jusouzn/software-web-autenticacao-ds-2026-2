import re
from pathlib import Path

from app.infraestrutura.verificador_argon2 import VerificadorSenhaArgon2

verificador = VerificadorSenhaArgon2()


def test_cv10_parametros_do_hash():
    hash_senha = verificador.gerar_hash("qualquer")
    assert hash_senha.startswith("$argon2id$v=19$m=19456,t=2,p=1$")


def test_verifica_senha_correta_e_incorreta():
    hash_senha = verificador.gerar_hash("S3nh@-de-teste")

    assert verificador.verificar("S3nh@-de-teste", hash_senha)
    assert not verificador.verificar("s3nh@-de-teste", hash_senha)


def test_hash_invalido_nao_quebra():
    assert not verificador.verificar("qualquer", "isso nao e um hash")


def test_hashes_da_carga_de_teste_conferem():
    sql = (Path(__file__).parent.parent / "db" / "02-carga-teste.sql").read_text(encoding="utf-8")
    hashes = re.findall(r"\$argon2id\$[^']+", sql)
    senhas = ["S3nh@-de-teste", "Kesley#2026", "Veronica!2026"]

    assert len(hashes) == len(senhas)
    for senha, hash_senha in zip(senhas, hashes):
        assert verificador.verificar(senha, hash_senha)
