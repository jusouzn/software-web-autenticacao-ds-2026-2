from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator


class RequisicaoAutenticacao(BaseModel):
    # campo a mais no JSON também é requisição inválida
    model_config = ConfigDict(extra="forbid")

    identificador: str = Field(min_length=1, max_length=254)
    senha: SecretStr

    # RN03. A senha é SecretStr para não aparecer em log nem em repr()
    @field_validator("senha")
    @classmethod
    def validar_tamanho_senha(cls, senha: SecretStr) -> SecretStr:
        if not 1 <= len(senha.get_secret_value()) <= 128:
            raise ValueError("a senha deve ter de 1 a 128 caracteres")
        return senha


class UsuarioResposta(BaseModel):
    id: UUID
    login: str
    email: str
    nome: str


class RespostaAutenticacao(BaseModel):
    autenticado: bool = True
    usuario: UsuarioResposta


class ProblemaHTTP(BaseModel):
    """Formato Problem Details (RFC 9457) usado em todas as respostas de erro."""

    type: str = "about:blank"
    title: str
    status: int
    detail: str
