import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Configuracao:
    url_banco: str
    desenvolvimento: bool

    @classmethod
    def do_ambiente(cls) -> "Configuracao":
        return cls(
            url_banco=os.environ.get("BANCO_URL", "postgresql://app_autenticacao@db:5432/autenticacao"),
            desenvolvimento=os.environ.get("AMBIENTE", "producao") == "desenvolvimento",
        )
