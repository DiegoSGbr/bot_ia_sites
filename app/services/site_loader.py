"""Serviço de carregamento e extração de texto de páginas web."""

import logging

import requests
from bs4 import BeautifulSoup

from app.config import load_config

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
OBF_MARKERS = ["aes.js", "toNumbers(", "toHex("]


def _html_para_texto(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return "\n".join(soup.stripped_strings)


def _carrega_com_playwright(url: str) -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_extra_http_headers({"User-Agent": USER_AGENT})
            page.goto(url, timeout=30000, wait_until="networkidle")
            return _html_para_texto(page.content())
        finally:
            browser.close()


def carrega_site(url: str | None = None) -> str:
    """
    Baixa a página da URL configurada (ou informada), extrai o texto visível
    e retorna como string para uso como contexto (RAG).
    Se detectar ofuscação por JS, tenta renderizar com Playwright quando disponível.
    """
    cfg = load_config()
    url = url or cfg.get("BASE_URL")
    if not url:
        logger.warning("carrega_site: BASE_URL não configurada")
        return ""

    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text

        if any(m in html for m in OBF_MARKERS):
            logger.info("Ofuscação JS detectada em %s; tentando Playwright", url)
            try:
                documento = _carrega_com_playwright(url)
                if documento.strip():
                    return documento[:200_000]
            except Exception:
                logger.exception("Playwright falhou para %s; usando HTML bruto", url)

        documento = _html_para_texto(html)
        if len(documento.strip()) < 100:
            logger.warning(
                "Pouco texto extraído de %s (%d chars) após requests",
                url,
                len(documento),
            )
        return documento[:200_000]
    except requests.RequestException as exc:
        logger.exception("Erro HTTP ao carregar %s: %s", url, exc)
        return ""
    except Exception as exc:
        logger.exception("Erro inesperado ao carregar %s: %s", url, exc)
        return ""
