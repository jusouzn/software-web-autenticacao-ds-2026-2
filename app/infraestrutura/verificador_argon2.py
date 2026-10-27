from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

# Configuração mínima recomendada pela OWASP: m = 19 MiB, t = 2, p = 1
_hasher = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1)


class VerificadorSenhaArgon2:
    def __init__(self):
        # hash de uma senha qualquer, só para gastar o mesmo tempo quando o usuário não existe
        self._hash_ficticio = _hasher.hash("senha-que-nao-pertence-a-ninguem")

    def verificar(self, senha: str, hash_senha: str) -> bool:
        try:
            return _hasher.verify(hash_senha, senha)
        except (VerificationError, InvalidHashError):
            return False

    def verificar_ficticio(self, senha: str) -> None:
        self.verificar(senha, self._hash_ficticio)

    @staticmethod
    def gerar_hash(senha: str) -> str:
        return _hasher.hash(senha)
