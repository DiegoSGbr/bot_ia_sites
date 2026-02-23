# Camada de views (MVC): apresentação para o usuário (CLI, futuramente API/Web).

from .cli import print_welcome, print_bot, print_bot_stream, get_user_input

__all__ = ["print_welcome", "print_bot", "print_bot_stream", "get_user_input"]
