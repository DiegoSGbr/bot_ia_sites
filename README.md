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
- **app/models/**: Modelos (ex.: `BotModel` para o chat com Grok/LangChain).
- **app/views/**: Views de apresentação (CLI hoje; depois pode ter API/Web).
- **app/controllers/**: Controladores que orquestram models, services e views.
- **app/services/**: Serviços de negócio (ex.: `carrega_site` para extrair conteúdo do site).
- **scripts/**: Scripts auxiliares para simulação e testes.

## Pré-requisitos

- Python 3.8+
- (Opcional) Ambiente virtual recomendado Venv

## Ambiente recomendado (Windows)

Para evitar problemas de instalação (build de dependências nativas) em alguns ambientes,
recomendo usar **Python 3.11** (ou **3.12**) neste projeto.

Em especial, **evite Python 3.13** se você estiver no Windows sem ferramentas de compilação
disponíveis, pois algumas dependências podem tentar compilar `numpy` e falhar.

### Passo a passo (Python 3.11 + venv)

No PowerShell, dentro da pasta do projeto (`d:\projetos\bot_ia_sites`):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

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

### Tempo de resposta do bot

- **Padrão**: o bot usa o modelo `llama-3.1-8b-instant` e **streaming**: a resposta aparece no console aos poucos, reduzindo a sensação de espera.
- **Limites**: contexto do site limitado a 40k caracteres, resposta a 1024 tokens e histórico a 16 mensagens (ajustáveis no `.env`).
- **Mais qualidade (mais lento)**: no `.env` use `MODEL=llama-3.3-70b-versatile`.
- **Ajustes opcionais no `.env`**: `MAX_CONTEXT_CHARS`, `MAX_RESPONSE_TOKENS`, `MAX_HISTORY_MESSAGES`.

## Execução

Para rodar o projeto:

```bash
python main.py
```

Ou, se desejar rodar o script principal do bot:

```bash
python "IA Bot SIte.py"
```

## Rodar API (FastAPI)

Se você quiser disponibilizar as rotas HTTP (por exemplo `POST /config`, `POST /chat` e `GET /widget.js`), rode a API com `uvicorn`:

```powershell
uvicorn app.views.api:app --host 0.0.0.0 --port 8000 --reload
```

Defina **`ADMIN_TOKEN`** no `.env` (ou no ambiente do processo). O endpoint **`POST /config`** exige o header **`X-ADMIN-TOKEN`** com o mesmo valor; caso contrário retorna **401**. **`GET /widget.js`** e **`POST /chat`** continuam sem esse header.

Exemplo local no PowerShell antes do `uvicorn`:

```powershell
$env:ADMIN_TOKEN="seu_secret_aqui"
```

Depois, valide rapidamente no navegador:

- Documentação Swagger: `http://localhost:8000/docs`
- Widget JS: `http://localhost:8000/widget.js`

E a configuração do bot via endpoint:

- `POST http://localhost:8000/config` com header `X-ADMIN-TOKEN: <ADMIN_TOKEN>` e JSON `{ "GROK_API_KEY": "...", "BASE_URL": "https://..." }`

### Docker

Ao subir com o `Dockerfile`, passe o secret no ambiente do container, por exemplo:

`docker run -e ADMIN_TOKEN=seu_secret ...`

### Deploy na AWS (produção)

Checklist passo a passo (ECR, **ECS Modo Expresso** ou App Runner, S3/CloudFront, certificados, custos e validação): [`docs/DEPLOY_AWS.md`](docs/DEPLOY_AWS.md).

### Deploy gratuito ou barato (testes com usuários)

Opções como Cloud Run, Fly.io, Render, painel em Pages/Netlify e critérios para `/chat`: [`docs/DEPLOY_GRATUITO_TESTES_USUARIOS.md`](docs/DEPLOY_GRATUITO_TESTES_USUARIOS.md).

## Scripts Auxiliares

Para simular perguntas:

```bash
python scripts/simulate_questions.py
```

## Contribuição

Pull requests são bem-vindos! Sinta-se à vontade para abrir issues e sugerir melhorias.


