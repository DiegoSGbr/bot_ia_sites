"""Views HTTP (API) usando FastAPI.

Exposição de endpoints públicos para configuração do bot e widget de chat embutível em sites.
"""

from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.controllers.api_controller import configurar_bot
from app.services import resposta_chat
from app.services.config_service import ConfigInput


app = FastAPI(title="Bot IA Sites API")

# CORS: o widget é carregado de outro domínio; o navegador envia OPTIONS (preflight) antes do POST /chat.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho do template do widget (app/static/widget.js)
WIDGET_JS_PATH = Path(__file__).resolve().parent.parent / "static" / "widget.js"


class ConfigRequest(BaseModel):
    """Payload recebido no endpoint de configuração."""

    GROQ_API_KEY: str
    BASE_URL: str


class ConfigResponse(BaseModel):
    """Resposta básica de configuração.

    Futuramente este modelo pode ser estendido para incluir o código do widget
    que será embutido no site do cliente.
    """

    success: bool
    message: str
    config: Dict[str, Any]


@app.post("/config", response_model=ConfigResponse)
def configurar_config_bot(payload: ConfigRequest, request: Request) -> ConfigResponse:
    """Endpoint de configuração inicial do bot.

    Recebe `GROQ_API_KEY` e `BASE_URL`, aplica no processo e retorna um snapshot
    da configuração atual. Use `widget_script_url` para embutir o chat no site.
    """
    input_validado = ConfigInput(**payload.model_dump())
    cfg = configurar_bot(input_validado)
    base = str(request.base_url).rstrip("/")
    cfg["widget_script_url"] = f"{base}/widget.js"
    return ConfigResponse(
        success=True,
        message="Configuração aplicada com sucesso. Embaixe o chat com: <script src=\"" + base + "/widget.js\"></script>",
        config=cfg,
    )


class ChatMessage(BaseModel):
    """Uma mensagem do histórico (user ou assistant)."""
    role: str  # "user" | "assistant"
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


@app.get("/widget.js")
def widget_js(request: Request) -> Response:
    """Retorna o script do widget com a URL base da API injetada (para chamadas ao /chat)."""
    content = WIDGET_JS_PATH.read_text(encoding="utf-8")
    base = str(request.base_url).rstrip("/")
    body = content.replace("__API_BASE_URL__", base)
    return Response(content=body, media_type="application/javascript")

