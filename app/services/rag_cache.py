"""Cache e persistência do documento RAG e da configuração do bot."""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

STATE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "bot_state.json"
MIN_CONTEXT_CHARS = 500

_state: dict[str, Any] = {
    "base_url": "",
    "documento": "",
    "indexed_at": None,
    "grok_api_key": "",
}


def _ensure_data_dir() -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _apply_env_from_state() -> None:
    base_url = _state.get("base_url") or ""
    api_key = _state.get("grok_api_key") or ""
    if base_url:
        os.environ["BASE_URL"] = base_url
    if api_key:
        os.environ["GROK_API_KEY"] = api_key
        os.environ["GROQ_API_KEY"] = api_key


def atualizar_cache(base_url: str, documento: str, grok_api_key: str | None = None) -> None:
    """Atualiza cache em memória e persiste em disco."""
    _state["base_url"] = base_url
    _state["documento"] = documento
    _state["indexed_at"] = time.time()
    if grok_api_key:
        _state["grok_api_key"] = grok_api_key
    _apply_env_from_state()
    salvar_no_disco()


def obter_documento() -> str:
    return _state.get("documento") or ""


def obter_base_url() -> str:
    return _state.get("base_url") or ""


def context_chars() -> int:
    return len(obter_documento().strip())


def index_ok() -> bool:
    return context_chars() >= MIN_CONTEXT_CHARS


def cache_age_seconds() -> float | None:
    indexed_at = _state.get("indexed_at")
    if indexed_at is None:
        return None
    return max(0.0, time.time() - float(indexed_at))


def base_url_host() -> str | None:
    url = obter_base_url()
    if not url:
        return None
    return urlparse(url).netloc or None


def salvar_no_disco() -> None:
    try:
        _ensure_data_dir()
        payload = {
            "base_url": _state.get("base_url", ""),
            "documento": _state.get("documento", ""),
            "indexed_at": _state.get("indexed_at"),
            "grok_api_key": _state.get("grok_api_key", ""),
        }
        STATE_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except Exception:
        logger.exception("Falha ao salvar estado RAG em %s", STATE_PATH)


def carregar_do_disco() -> bool:
    """Carrega estado persistido; retorna True se havia dados válidos."""
    if not STATE_PATH.is_file():
        return False
    try:
        raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        _state["base_url"] = raw.get("base_url") or ""
        _state["documento"] = raw.get("documento") or ""
        _state["indexed_at"] = raw.get("indexed_at")
        _state["grok_api_key"] = raw.get("grok_api_key") or ""
        _apply_env_from_state()
        logger.info(
            "Estado RAG restaurado: host=%s context_chars=%d",
            base_url_host(),
            context_chars(),
        )
        return bool(_state.get("base_url"))
    except Exception:
        logger.exception("Falha ao carregar estado RAG de %s", STATE_PATH)
        return False


def status_rag() -> dict[str, Any]:
    return {
        "base_url_host": base_url_host(),
        "context_chars": context_chars(),
        "index_ok": index_ok(),
        "cache_age_seconds": cache_age_seconds(),
    }
