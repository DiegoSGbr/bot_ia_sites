"""Serviço de carregamento e extração de texto de páginas web."""

import requests
from bs4 import BeautifulSoup

from app.config import load_config


def carrega_site(url: str | None = None) -> str:
    """
    Baixa a página da URL configurada (ou informada), extrai o texto visível
    e retorna como string para uso como contexto (RAG).
    Se detectar ofuscação por JS, tenta renderizar com Playwright quando disponível.
    """
    cfg = load_config()
    url = url or cfg.get("BASE_URL")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text

        # Detectar ofuscação simples no lado do cliente (site que serve JS que descriptografa o conteúdo)
        obf_markers = ["aes.js", "toNumbers(", "toHex("]
        if any(m in html for m in obf_markers):
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
                soup = BeautifulSoup(html, "html.parser")
        else:
            soup = BeautifulSoup(html, "html.parser")

        # Remove scripts, estilos e noscript
        for s in soup(["script", "style", "noscript"]):
            s.decompose()
        texts = soup.stripped_strings
        documento = "\n".join(texts)
        return documento[:200_000]
    except Exception:
        return ""
