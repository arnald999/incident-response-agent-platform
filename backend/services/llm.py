from langchain_openai import ChatOpenAI

from backend.core.config import settings


def get_llm():
    if not settings.openrouter_api_key:
        return None

    return ChatOpenAI(
        model=settings.model_name,
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        temperature=0,
    )