"""Configuração e carregamento de variáveis de ambiente."""

import os
from dotenv import load_dotenv

BASE_URL = "https://dsmidias.rf.gd"
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def load_config(env_path: str | None = None) -> dict:
    """Carrega `.env` e retorna dicionário com configuração relevante.

    Se `GROQ_API_KEY` estiver definida no `.env` ou no ambiente, garante que
    `os.environ['GROQ_API_KEY']` esteja disponível para bibliotecas.
    """
    load_dotenv(env_path)
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    return {
        "GROQ_API_KEY": api_key,
        "BASE_URL": os.getenv("BASE_URL", BASE_URL),
        "MODEL": os.getenv("MODEL", DEFAULT_MODEL),
    }
