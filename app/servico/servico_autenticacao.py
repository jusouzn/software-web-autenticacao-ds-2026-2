from app.servico.modelos import FalhaAutenticacao, IdentidadeUsuario
from app.servico.portas import RepositorioUsuario, VerificadorSenha


class ServicoAutenticacao:
    def __init__(self, repositorio: RepositorioUsuario, verificador: VerificadorSenha):
        self._repositorio = repositorio
        self._verificador = verificador

    @staticmethod
    def normalizar(identificador: str) -> str:
        # RN02: só o identificador é normalizado, a senha não
        return identificador.strip().lower()

    def autenticar(self, identificador: str, senha: str) -> IdentidadeUsuario:
        identificador = self.normalizar(identificador)

        # RN01
        if "@" in identificador:
            usuario = self._repositorio.buscar_por_email(identificador)
        else:
            usuario = self._repositorio.buscar_por_login(identificador)

        if usuario is None:
            # RNF04: sem isso a resposta para usuário inexistente sairia bem mais rápida
            self._verificador.verificar_ficticio(senha)
            raise FalhaAutenticacao()

        if not self._verificador.verificar(senha, usuario.hash_senha):
            raise FalhaAutenticacao()

        return usuario.identidade()
