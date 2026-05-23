"""Views HTTP (API) usando FastAPI.

Exposição de endpoints públicos para configuração do bot e widget de chat embutível em sites.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.controllers.api_controller import configurar_bot
from app.services import resposta_chat
from app.services.admin_auth_service import ErroAutenticacaoAdmin, validar_token_admin
from app.services.config_service import ConfigInput
from app.services.rag_cache import carregar_do_disco, status_rag

logger = logging.getLogger(__name__)

WIDGET_JS_PATH = Path(__file__).resolve().parent.parent / "static" / "widget.js"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if carregar_do_disco():
        logger.info("Configuração e cache RAG restaurados do disco")
    yield


app = FastAPI(title="Bot IA Sites API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _exigir_admin_token(
    x_admin_token: str | None = Header(
        None,
        alias="X-ADMIN-TOKEN",
        description="Token igual ao definido em ADMIN_TOKEN no servidor.",
    ),
) -> None:
    """Dependency: valida o token administrativo antes de aplicar configuração."""
    try:
        validar_token_admin(x_admin_token)
    except ErroAutenticacaoAdmin as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


class ConfigRequest(BaseModel):
    """Payload recebido no endpoint de configuração."""

    GROK_API_KEY: str
    BASE_URL: str


class ConfigResponse(BaseModel):
    """Resposta básica de configuração."""

    success: bool
    message: str
    config: Dict[str, Any]


@app.post("/config", response_model=ConfigResponse)
def configurar_config_bot(
    payload: ConfigRequest,
    request: Request,
    _: None = Depends(_exigir_admin_token),
) -> ConfigResponse:
    """Endpoint de configuração inicial do bot."""
    input_validado = ConfigInput(**payload.model_dump())
    cfg = configurar_bot(input_validado)
    base = str(request.base_url).rstrip("/")
    cfg["widget_script_url"] = f"{base}/widget.js"

    if cfg.get("index_ok"):
        message = (
            f'Configuração aplicada com sucesso ({cfg.get("context_chars", 0)} caracteres indexados). '
            f'Baixe o chat com: <script src="{base}/widget.js"></script>'
        )
    else:
        message = (
            "O site foi configurado, mas quase nenhum texto foi extraído da página. "
            "Verifique a URL informada ou se o site depende de JavaScript para exibir o conteúdo. "
            f'Script do widget: <script src="{base}/widget.js"></script>'
        )

    return ConfigResponse(success=True, message=message, config=cfg)


class ChatMessage(BaseModel):
    """Uma mensagem do histórico (user ou assistant)."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Payload do endpoint de chat."""
    message: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    """Resposta do bot no chat."""
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Recebe a mensagem do usuário e o histórico, retorna a resposta do bot (RAG no site configurado)."""
    history = [h.model_dump() for h in payload.history]
    text = resposta_chat(payload.message, history)
    return ChatResponse(response=text)


@app.get("/health/rag")
def health_rag() -> Dict[str, Any]:
    """Diagnóstico do cache RAG (sem expor secrets)."""
    return status_rag()


@app.get("/widget.js")
def widget_js(request: Request) -> Response:
    """Retorna o script do widget com a URL base da API injetada (para chamadas ao /chat)."""
    content = WIDGET_JS_PATH.read_text(encoding="utf-8")
    base = str(request.base_url).rstrip("/")
    body = content.replace("__API_BASE_URL__", base)
    return Response(content=body, media_type="application/javascript")
