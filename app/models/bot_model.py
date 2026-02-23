"""Modelo do bot: integração com LangChain / Groq para respostas baseadas em contexto (RAG)."""

from typing import List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import load_config


class BotModel:
    """Modelo de chat que utiliza o contexto do site para responder ao usuário."""

    def __init__(self, model_name: str | None = None):
        cfg = load_config()
        model = model_name or cfg.get("MODEL")
        self.chat = ChatGroq(model=model)

    def resposta_bot(self, mensagens: List[tuple], documento: str) -> str:
        """Gera resposta do bot com base nas mensagens e no documento de contexto (RAG)."""
        mensagem_system = (
            """
# PERSONA
Você é um atendente virtual de alta performance, caracterizado por ser extremamente cortês, prestativo e empático. Seu objetivo é guiar o usuário através das informações 
contidas na nossa base de conhecimento oficial.

# DIRETRIZES DE ESTILO E TOM DE VOZ
1. Inicie APENAS a primeira interação rigorosamente com a frase: "Olá, que bom ter você aqui! Em que podemos te ajudar sobre nosso conteúdo?"
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
