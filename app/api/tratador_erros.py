import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.api.dtos import ProblemaHTTP
from app.servico.modelos import FalhaAutenticacao, RepositorioIndisponivel

log = logging.getLogger(__name__)

TITULOS = {
    400: "Requisição inválida",
    401: "Falha de autenticação",
    404: "Recurso não encontrado",
    405: "Método não permitido",
    415: "Tipo de conteúdo não suportado",
    500: "Erro interno",
    503: "Serviço indisponível",
}


def resposta_problema(status: int, detalhe: str, cabecalhos: dict | None = None) -> JSONResponse:
    problema = ProblemaHTTP(title=TITULOS.get(status, "Erro"), status=status, detail=detalhe)
    return JSONResponse(
        problema.model_dump(),
        status_code=status,
        media_type="application/problem+json",
        headers={"Cache-Control": "no-store", **(cabecalhos or {})},
    )


def registrar_tratadores(app: FastAPI) -> None:
    @app.exception_handler(FalhaAutenticacao)
    async def falha_autenticacao(request: Request, erro: FalhaAutenticacao):
        # mesma resposta para usuário inexistente e senha errada (RN04)
        return resposta_problema(
            401,
            "Login, e-mail ou senha inválidos.",
            {"WWW-Authenticate": 'Formulario realm="autenticacao"'},
        )

    @app.exception_handler(RequestValidationError)
    async def requisicao_invalida(request: Request, erro: RequestValidationError):
        # o FastAPI responderia 422; o contrato (Seção 2.5) usa 400 para qualquer entrada mal formada
        return resposta_problema(400, "Requisição inválida: informe identificador e senha.")

    @app.exception_handler(HTTPException)
    async def erro_http(request: Request, erro: HTTPException):
        # cobre 404, 405 (o Starlette já manda o cabeçalho Allow) e o 415 da rota
        return resposta_problema(erro.status_code, str(erro.detail), erro.headers)

    @app.exception_handler(RepositorioIndisponivel)
    async def banco_indisponivel(request: Request, erro: RepositorioIndisponivel):
        log.error("Banco de dados indisponível", exc_info=erro)
        return resposta_problema(503, "Serviço temporariamente indisponível.", {"Retry-After": "30"})

    @app.exception_handler(Exception)
    async def erro_inesperado(request: Request, erro: Exception):
        log.exception("Erro inesperado em %s %s", request.method, request.url.path)
        return resposta_problema(500, "Erro interno.")
