from langchain_openai import ChatOpenAI

from backend.core.config import settings


def get_llm():
    return ChatOpenAI(
        model="gpt-4.1",
        temperature=0,
        api_key=settings.openai_api_key,
    )