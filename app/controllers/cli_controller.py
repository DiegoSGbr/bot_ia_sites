"""Controlador do fluxo CLI: loop de perguntas e respostas com o bot."""

from app.models import BotModel
from app.services import carrega_site
from app.views import print_welcome, print_bot, get_user_input


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
        resposta = model.resposta_bot(mensagens, documento)
        mensagens.append(("assistant", resposta))
        print_bot(resposta)

    print("Encerrando. Obrigado por usar.")
