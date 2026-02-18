"""Funções de apresentação (CLI) do projeto."""

def print_welcome() -> None:
    print("Bem-vindo ao Bot Site (CLI)")


def print_bot(resposta: str) -> None:
    print(f"Bot: {resposta}")


def get_user_input(prompt: str = 'Pergunte sobre o site: ') -> str:
    return input(prompt)
