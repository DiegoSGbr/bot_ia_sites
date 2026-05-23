"""Serviço de chat: orquestra BotModel e carrega_site para responder ao usuário via API."""

import os
from typing import List

from app.config import load_config
from app.services.rag_cache import atualizar_cache, obter_base_url, obter_documento
from app.services.site_loader import carrega_site


def resposta_chat(message: str, history: List[dict]) -> str:
    """
    Gera resposta do bot para uma mensagem do usuário, usando o histórico e o contexto do site.

    - history: lista de {"role": "user" | "assistant", "content": "..."}
    - message: nova mensagem do usuário
    - Usa cache RAG indexado em POST /config; fallback para scrape se cache vazio.
    """
    from app.models import BotModel

    documento = obter_documento()
    if not documento.strip():
        cfg = load_config()
        base_url = cfg.get("BASE_URL") or obter_base_url()
        documento = carrega_site(base_url)
        if documento.strip() and base_url:
            grok = os.getenv("GROK_API_KEY") or os.getenv("GROQ_API_KEY")
            atualizar_cache(base_url, documento, grok)

    model = BotModel()

    mensagens: List[tuple] = []
    for h in history:
        role = "user" if h.get("role") == "user" else "assistant"
        content = h.get("content") or ""
        mensagens.append((role, content))
    mensagens.append(("user", message))

    return model.resposta_bot(mensagens, documento)
