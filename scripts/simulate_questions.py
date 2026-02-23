import time

from app.models import BotModel
from app.services import carrega_site


def simulate():
    model = BotModel()
    documento = carrega_site()
    perguntas = [
        "Qual é o objetivo do site?",
        "Que serviços esse site oferece?",
    ]
    mensagens = []
    for p in perguntas:
        mensagens.append(("user", p))
        t0 = time.perf_counter()
        resposta = model.resposta_bot(mensagens, documento)
        elapsed = time.perf_counter() - t0
        mensagens.append(("assistant", resposta))
        print("Pergunta:", p)
        print(f"Tempo: {elapsed:.1f}s")
        print("Resposta:\n", resposta[:500] + ("..." if len(resposta) > 500 else ""))
        print("-" * 60)


if __name__ == "__main__":
    simulate()
