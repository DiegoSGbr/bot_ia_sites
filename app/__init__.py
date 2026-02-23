"""
Pacote principal do projeto (arquitetura MVC).

Estrutura:
- models/   : modelos (entidades, integração LLM)
- views/    : apresentação (CLI, futuramente API/Web)
- controllers/ : orquestração da aplicação
- services/ : serviços de negócio (carregamento de sites, APIs, etc.)
"""

from app.config import load_config
from app.models import BotModel
from app.services import carrega_site
from app.views import print_welcome, print_bot, get_user_input
from app.controllers import run_cli

__all__ = [
    "load_config",
    "BotModel",
    "carrega_site",
    "print_welcome",
    "print_bot",
    "get_user_input",
    "run_cli",
]
