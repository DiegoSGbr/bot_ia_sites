"""Configuração e carregamento de variáveis de ambiente."""

import os
from dotenv import load_dotenv

BASE_URL = "https://dsmidias.rf.gd"
# Padrão: modelo rápido para menor tempo de resposta. Para mais qualidade: "llama-3.3-70b-versatile"
DEFAULT_MODEL = "llama-3.1-8b-instant"
MAX_CONTEXT_CHARS = 40_000  # Limite de caracteres do documento no prompt (reduz tokens = resposta mais rápida)
MAX_RESPONSE_TOKENS = 1024  # Limita tamanho da resposta para reduzir tempo de geração
MAX_HISTORY_MESSAGES = 16   # Máximo de mensagens (user+assistant) no histórico enviado ao modelo


def load_config(env_path: str | None = None) -> dict:
    """Carrega `.env` e retorna dicionário com configuração relevante.

    Se `GROQ_API_KEY` estiver definida no `.env` ou no ambiente, garante que
    `os.environ['GROQ_API_KEY']` esteja disponível para bibliotecas.
    """
    load_dotenv(env_path)
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    def _int(key: str, default: int) -> int:
        val = os.getenv(key)
        return int(val) if val is not None and val.isdigit() else default

    return {
        "GROQ_API_KEY": api_key,
        "BASE_URL": os.getenv("BASE_URL", BASE_URL),
        "MODEL": os.getenv("MODEL", DEFAULT_MODEL),
        "HF_TOKEN": os.getenv("HF_TOKEN"),
        "MAX_CONTEXT_CHARS": _int("MAX_CONTEXT_CHARS", MAX_CONTEXT_CHARS),
        "MAX_RESPONSE_TOKENS": _int("MAX_RESPONSE_TOKENS", MAX_RESPONSE_TOKENS),
        "MAX_HISTORY_MESSAGES": _int("MAX_HISTORY_MESSAGES", MAX_HISTORY_MESSAGES),
    }
