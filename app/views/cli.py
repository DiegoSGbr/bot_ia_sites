"""Views de linha de comando (CLI): exibição e entrada do usuário."""


def print_welcome() -> None:
    """Exibe mensagem de boas-vindas no início da aplicação."""
    print("Bem-vindo ao Bot Site (CLI) - Pergunte sobre o conteúdo do site ou digite 'x' para encerrar.")


def print_bot(resposta: str) -> None:
    """Exibe a resposta do bot para o usuário."""
    print(f"Bot: {resposta}")


def get_user_input(prompt: str = "Pergunte sobre o site: ") -> str:
    """Solicita e retorna a entrada do usuário."""
    return input(prompt)
