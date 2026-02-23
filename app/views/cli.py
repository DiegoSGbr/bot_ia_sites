"""Views de linha de comando (CLI): exibição e entrada do usuário."""

import sys


def print_welcome() -> None:
    """Exibe mensagem de boas-vindas no início da aplicação."""
    print("Bem-vindo ao Bot Site (CLI) - Pergunte sobre o conteúdo do site ou digite 'x' para encerrar.")


def print_bot(resposta: str) -> None:
    """Exibe a resposta do bot para o usuário."""
    print(f"Bot: {resposta}")


def print_bot_stream(chunks, prefix: str = "Bot: ") -> str:
    """Exibe a resposta do bot em streaming e retorna o texto completo."""
    sys.stdout.write(prefix)
    full: list[str] = []
    for chunk in chunks:
        sys.stdout.write(chunk)
        sys.stdout.flush()
        full.append(chunk)
    print()
    return "".join(full)


def get_user_input(prompt: str = "Pergunte sobre o site: ") -> str:
    """Solicita e retorna a entrada do usuário."""
    return input(prompt)
