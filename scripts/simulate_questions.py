from app.models import BotModel, carrega_site


def simulate():
    model = BotModel()
    documento = carrega_site()
    perguntas = [
        "Qual é o objetivo do site?",
        "Que serviços esse site oferece?",
        "O que é um tour virtual oferecido pela empresa?",
        "Como a empresa trabalha com Google Maps?",
    ]
    mensagens = []
    for p in perguntas:
        mensagens.append(("user", p))
        resposta = model.resposta_bot(mensagens, documento)
        mensagens.append(("assistant", resposta))
        print("Pergunta:", p)
        print("Resposta:\n", resposta)
        print("-" * 60)


if __name__ == '__main__':
    simulate()
