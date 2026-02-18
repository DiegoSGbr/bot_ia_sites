"""Controladores: lógica de aplicação (CLI loop)."""

from .models import BotModel, carrega_site
from .views import print_welcome, print_bot, get_user_input


def run_cli() -> None:
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
