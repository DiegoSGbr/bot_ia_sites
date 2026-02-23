"""Modelo do bot: integração com LangChain / Groq para respostas baseadas em contexto (RAG)."""

from typing import Iterator, List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import load_config


class BotModel:
    """Modelo de chat que utiliza o contexto do site para responder ao usuário."""

    def __init__(self, model_name: str | None = None):
        cfg = load_config()
        model = model_name or cfg.get("MODEL")
        max_tokens = cfg.get("MAX_RESPONSE_TOKENS", 2048)
        self.chat = ChatGroq(
            model=model,
            temperature=0,
            max_tokens=max_tokens,
        )
        self.max_context_chars = cfg.get("MAX_CONTEXT_CHARS", 80_000)
        self.max_history_messages = cfg.get("MAX_HISTORY_MESSAGES", 20)

    def resposta_bot(self, mensagens: List[tuple], documento: str) -> str:
        """Gera resposta do bot com base nas mensagens e no documento de contexto (RAG)."""
        # Limita o contexto enviado para reduzir tokens e tempo de resposta
        doc = documento[: self.max_context_chars] if len(documento) > self.max_context_chars else documento
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
        # Envia só as últimas N mensagens para não inflar o prompt
        recentes = mensagens[-self.max_history_messages :] if len(mensagens) > self.max_history_messages else mensagens
        mensagens_modelo += recentes
        template = ChatPromptTemplate.from_messages(mensagens_modelo)
        chain = template | self.chat
        result = chain.invoke({"informacoes": doc})
        return getattr(result, "content", str(result))

    def resposta_bot_stream(self, mensagens: List[tuple], documento: str) -> Iterator[str]:
        """Gera a resposta em streaming (chunks) para exibir no console aos poucos."""
        doc = documento[: self.max_context_chars] if len(documento) > self.max_context_chars else documento
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
        recentes = mensagens[-self.max_history_messages :] if len(mensagens) > self.max_history_messages else mensagens
        mensagens_modelo += recentes
        template = ChatPromptTemplate.from_messages(mensagens_modelo)
        chain = template | self.chat
        for chunk in chain.stream({"informacoes": doc}):
            content = getattr(chunk, "content", "") or ""
            if content:
                yield content
