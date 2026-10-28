from contextlib import asynccontextmanager

from fastapi import FastAPI
from psycopg_pool import ConnectionPool

from app.api.rota_autenticacao import roteador
from app.api.tratador_erros import registrar_tratadores
from app.infraestrutura.configuracao import Configuracao
from app.infraestrutura.repositorio_postgres import RepositorioUsuarioPostgres
from app.infraestrutura.verificador_argon2 import VerificadorSenhaArgon2
from app.servico.servico_autenticacao import ServicoAutenticacao


def criar_app(servico: ServicoAutenticacao | None = None) -> FastAPI:
    """Monta a aplicação. Os testes passam um serviço pronto; em produção ele é criado aqui."""
    configuracao = Configuracao.do_ambiente()

    @asynccontextmanager
    async def ciclo_de_vida(app: FastAPI):
        if servico is not None:
            app.state.servico = servico
            yield
            return

        # único ponto que conhece todas as camadas: liga as implementações concretas às portas do serviço
        with ConnectionPool(configuracao.url_banco, min_size=1, max_size=4, timeout=3, open=False) as pool:
            app.state.servico = ServicoAutenticacao(
                RepositorioUsuarioPostgres(pool),
                VerificadorSenhaArgon2(),
            )
            yield

    # a documentação OpenAPI só fica disponível em desenvolvimento
    docs = "/api/docs" if configuracao.desenvolvimento else None
    openapi = "/api/openapi.json" if configuracao.desenvolvimento else None

    app = FastAPI(
        title="Autenticação de usuários",
        version="1.0.0",
        lifespan=ciclo_de_vida,
        docs_url=docs,
        redoc_url=None,
        openapi_url=openapi,
    )
    registrar_tratadores(app)
    app.include_router(roteador)
    return app


app = criar_app()
