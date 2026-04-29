"""Serviço de configuração dinâmica do bot via API.

Este serviço recebe parâmetros de configuração (como `GROK_API_KEY` e `BASE_URL`)
e aplica no ambiente do processo, permitindo que futuras requisições usem esses
valores sem precisar reescrever o arquivo `.env`.
"""

from typing import Any, Dict

import os

from pydantic import BaseModel, HttpUrl

from app.config import load_config


class ConfigInput(BaseModel):
    """Entrada de configuração recebida pela API."""

    GROK_API_KEY: str
    BASE_URL: HttpUrl


def aplicar_configuracao(data: ConfigInput) -> Dict[str, Any]:
    """Aplica a configuração no processo e retorna o snapshot atual.

    - Atualiza variáveis de ambiente relevantes.
    - Recarrega a configuração via `load_config` para refletir os novos valores.
    """
    os.environ["GROK_API_KEY"] = data.GROK_API_KEY
    os.environ["BASE_URL"] = str(data.BASE_URL)

    cfg = load_config()
    return cfg

