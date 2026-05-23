"""Serviço de configuração dinâmica do bot via API.

Este serviço recebe parâmetros de configuração (como `GROK_API_KEY` e `BASE_URL`)
e aplica no ambiente do processo, permitindo que futuras requisições usem esses
valores sem precisar reescrever o arquivo `.env`.
"""

from typing import Any, Dict

import os

from pydantic import BaseModel, HttpUrl

from app.config import load_config
from app.services.rag_cache import atualizar_cache, context_chars, index_ok
from app.services.site_loader import carrega_site


class ConfigInput(BaseModel):
    """Entrada de configuração recebida pela API."""

    GROK_API_KEY: str
    BASE_URL: HttpUrl


def aplicar_configuracao(data: ConfigInput) -> Dict[str, Any]:
    """Aplica a configuração no processo, indexa o site para RAG e persiste o cache."""
    base_url = str(data.BASE_URL)
    os.environ["GROK_API_KEY"] = data.GROK_API_KEY
    os.environ["GROQ_API_KEY"] = data.GROK_API_KEY
    os.environ["BASE_URL"] = base_url

    documento = carrega_site(base_url)
    atualizar_cache(base_url, documento, data.GROK_API_KEY)

    cfg = load_config()
    cfg["context_chars"] = context_chars()
    cfg["index_ok"] = index_ok()
    return cfg
