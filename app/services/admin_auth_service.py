"""Validação do token administrativo para endpoints protegidos (ex.: POST /config)."""

import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class ErroAutenticacaoAdmin(Exception):
    """Falha na validação do token administrativo (mensagem segura para o cliente HTTP)."""

    def __init__(self, detail: str, status_code: int = 401) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


def validar_token_admin(token_recebido: str | None) -> None:
    """Garante que o header `X-ADMIN-TOKEN` coincide com `ADMIN_TOKEN` no ambiente.

    Levanta `ErroAutenticacaoAdmin` se o servidor não tiver token configurado,
    se o header estiver ausente ou se o valor for inválido.
    """
    esperado = (os.getenv("ADMIN_TOKEN") or "").strip()
    if not esperado:
        raise ErroAutenticacaoAdmin(
            "O servidor não definiu ADMIN_TOKEN. Configure a variável de ambiente no backend.",
        )
    if not token_recebido or not str(token_recebido).strip():
        raise ErroAutenticacaoAdmin(
            "Token administrativo ausente. Envie o header X-ADMIN-TOKEN.",
        )
    if not secrets.compare_digest(str(token_recebido).strip(), esperado):
        raise ErroAutenticacaoAdmin(
            "Token administrativo inválido ou incorreto.",
        )
