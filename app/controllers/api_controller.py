"""Controlador da API: orquestra serviços de configuração para as rotas HTTP."""

from typing import Any, Dict

from app.services import aplicar_configuracao
from app.services.config_service import ConfigInput


def configurar_bot(config_input: ConfigInput) -> Dict[str, Any]:
    """Recebe os dados de configuração e delega para o serviço."""
    return aplicar_configuracao(config_input)

