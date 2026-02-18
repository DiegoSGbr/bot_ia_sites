"""Modelos e integração com LangChain / Groq."""

from typing import List
import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import requests
from bs4 import BeautifulSoup

from .config import load_config


class BotModel:
    def __init__(self, model_name: str | None = None):
        cfg = load_config()
        model = model_name or cfg.get("MODEL")
        self.chat = ChatGroq(model=model)

    def resposta_bot(self, mensagens: List[tuple], documento: str) -> str:
        mensagem_system = (
            """
# PERSONA
Você é um atendente virtual de alta performance, caracterizado por ser extremamente cortês, prestativo e empático. Seu objetivo é guiar o usuário através das informações contidas na nossa base de conhecimento oficial.

# DIRETRIZES DE ESTILO E TOM DE VOZ
1. Inicie TODAS as primeiras interações rigorosamente com a frase: "Olá, que bom ter você aqui! Em que podemos te ajudar sobre nosso conteúdo?"
2. Mantenha um tom profissional, porém acolhedor.
3. Seja direto e preciso, evitando rodeios, mas sem perder a cortesia.
4. Se não encontrar a resposta no conteúdo fornecido, admita educadamente que não possui essa informação específica no momento e se coloque à disposição para outras dúvidas baseadas no site.

# CONTEXTO DE CONHECIMENTO (RAG)
Sua única fonte de verdade para responder perguntas técnicas ou informativas é o conteúdo abaixo, extraído do site oficial:
---
{informacoes}
---

# REGRAS DE EXECUÇÃO
- Utilize apenas as informações presentes no bloco "CONTEXTO DE CONHECIMENTO" para formular suas respostas.
- Não invente fatos, links ou funcionalidades que não estejam explicitamente descritos no contexto.
- Se a pergunta do usuário for uma saudação inicial, você deve obrigatoriamente usar a frase de abertura padrão mencionada na diretriz 1.
"""
        )

        mensagens_modelo = [("system", mensagem_system)]
        mensagens_modelo += mensagens
        template = ChatPromptTemplate.from_messages(mensagens_modelo)
        chain = template | self.chat
        result = chain.invoke({"informacoes": documento})
        return getattr(result, "content", str(result))


def carrega_site(url: str | None = None) -> str:
    cfg = load_config()
    url = url or cfg.get("BASE_URL")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text

        # Detect simple client-side obfuscation (site serving JS that decrypts content)
        obf_markers = ["aes.js", "toNumbers(", "toHex("]
        if any(m in html for m in obf_markers):
            # Try to render the page with Playwright (if available) to execute JS
            try:
                from playwright.sync_api import sync_playwright

                with sync_playwright() as pw:
                    browser = pw.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.set_extra_http_headers({"User-Agent": headers["User-Agent"]})
                    page.goto(url, timeout=30000)
                    rendered = page.content()
                    soup = BeautifulSoup(rendered, "html.parser")
            except Exception:
                # Playwright not available or failed — fall back to raw HTML
                soup = BeautifulSoup(html, "html.parser")
        else:
            soup = BeautifulSoup(html, "html.parser")

        # Remove scripts/styles
        for s in soup(["script", "style", "noscript"]):
            s.decompose()
        # Get visible text
        texts = soup.stripped_strings
        documento = "\n".join(texts)
        # Limit size to a reasonable length to avoid sending huge payloads
        return documento[:200_000]
    except Exception:
        return ""
