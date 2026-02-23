"""Controlador do fluxo CLI: loop de perguntas e respostas com o bot."""

from app.models import BotModel
from app.services import carrega_site
from app.views import print_welcome, print_bot_stream, get_user_input


def run_cli() -> None:
    """Inicia o loop interativo da interface em linha de comando."""
    print_welcome()
    model = BotModel()
    documento = carrega_site()
    mensagens = []

    while True:
        pergunta = get_user_input()
        if pergunta.lower() == "x":
            break
        mensagens.append(("user", pergunta))
        chunks = model.resposta_bot_stream(mensagens, documento)
        resposta = print_bot_stream(chunks)
        mensagens.append(("assistant", resposta))

    print("Encerrando. Obrigado por usar.")
