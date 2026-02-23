# IA Bot Site

Projeto inicial de teste para um bot Atendimento de sites com IA. 
Desenvolvido em Python, recebe como Rag principal uma url de Site e uma chave da Grok AI e se torna uma atendente especialista das informações desse site.

O objetivo é servir como base teste para experimentos e futuras melhorias(api, end point, crud para recebimento de parametros, receber outros modelos de ia, controle de usuarios, integração com site passado como parametro dentre outras melhorias).

## Estrutura do Projeto (MVC)

O projeto segue o padrão **MVC** (Model-View-Controller), com uma pasta **services/** para lógica de negócio e integrações, facilitando a inclusão de novos serviços, views e controllers no futuro.

```
IA Bot SIte.py
main.py
requirements.txt
app/
    __init__.py
    config.py              # Configuração e variáveis de ambiente
    models/                 # Modelos (entidades, integração LLM)
        __init__.py
        bot_model.py
    views/                  # Apresentação (CLI; futuramente API/Web)
        __init__.py
        cli.py
    controllers/            # Controladores (orquestração)
        __init__.py
        cli_controller.py
    services/               # Serviços (carregamento de sites, APIs, etc.)
        __init__.py
        site_loader.py
scripts/
    __init__.py
    simulate_questions.py
```

- **main.py**: Ponto de entrada da aplicação.
- **IA Bot SIte.py**: Launcher que delega para `main.py`.
- **requirements.txt**: Lista de dependências do projeto.
- **app/models/**: Modelos (ex.: `BotModel` para o chat com Groq/LangChain).
- **app/views/**: Views de apresentação (CLI hoje; depois pode ter API/Web).
- **app/controllers/**: Controladores que orquestram models, services e views.
- **app/services/**: Serviços de negócio (ex.: `carrega_site` para extrair conteúdo do site).
- **scripts/**: Scripts auxiliares para simulação e testes.

## Pré-requisitos

- Python 3.8+
- (Opcional) Ambiente virtual recomendado Venv

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ia-bot-site.git
   cd ia-bot-site
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   # Ative no Windows:
   venv\Scripts\activate
   # Ou no Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. Renomeie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme necessário.
2. Configure os parâmetros em `app/config.py` se necessário.

## Execução

Para rodar o projeto:

```bash
python main.py
```

Ou, se desejar rodar o script principal do bot:

```bash
python "IA Bot SIte.py"
```

## Scripts Auxiliares

Para simular perguntas:

```bash
python scripts/simulate_questions.py
```

## Contribuição

Pull requests são bem-vindos! Sinta-se à vontade para abrir issues e sugerir melhorias.


