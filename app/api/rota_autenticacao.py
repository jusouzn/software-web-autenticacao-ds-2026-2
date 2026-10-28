from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.api.dtos import ProblemaHTTP, RequisicaoAutenticacao, RespostaAutenticacao, UsuarioResposta
from app.servico.servico_autenticacao import ServicoAutenticacao

roteador = APIRouter(prefix="/api/v1")


def exigir_json(request: Request) -> None:
    tipo = request.headers.get("content-type", "").split(";")[0].strip().lower()
    if tipo != "application/json":
        raise HTTPException(415, "Envie o corpo em JSON.")


def obter_servico(request: Request) -> ServicoAutenticacao:
    return request.app.state.servico


ERROS_DOCUMENTADOS = {
    codigo: {"model": ProblemaHTTP, "content": {"application/problem+json": {}}}
    for codigo in (400, 401, 415, 429, 500, 503)
}


# def (e não async def): o Argon2 e o psycopg bloqueiam, então o FastAPI roda a função numa thread separada
@roteador.post(
    "/autenticacao",
    response_model=RespostaAutenticacao,
    dependencies=[Depends(exigir_json)],
    responses=ERROS_DOCUMENTADOS,
)
def autenticar(
    dados: RequisicaoAutenticacao,
    response: Response,
    servico: ServicoAutenticacao = Depends(obter_servico),
) -> RespostaAutenticacao:
    identidade = servico.autenticar(dados.identificador, dados.senha.get_secret_value())

    response.headers["Cache-Control"] = "no-store"
    return RespostaAutenticacao(
        usuario=UsuarioResposta(
            id=identidade.id,
            login=identidade.login,
            email=identidade.email,
            nome=identidade.nome,
        )
    )
