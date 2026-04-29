"""Serviço de chat: orquestra BotModel e carrega_site para responder ao usuário via API."""

from typing import List


def resposta_chat(message: str, history: List[dict]) -> str:
    """
    Gera resposta do bot para uma mensagem do usuário, usando o histórico e o contexto do site.

    - history: lista de {"role": "user" | "assistant", "content": "..."}
    - message: nova mensagem do usuário
    - Usa a configuração atual (GROK_API_KEY, BASE_URL) e o documento do site (RAG).
    """
    from app.models import BotModel
    from app.services import carrega_site

    documento = carrega_site()
    model = BotModel()

    mensagens: List[tuple] = []
    for h in history:
        role = "user" if h.get("role") == "user" else "assistant"
        content = h.get("content") or ""
        mensagens.append((role, content))
    mensagens.append(("user", message))

    return model.resposta_bot(mensagens, documento)
