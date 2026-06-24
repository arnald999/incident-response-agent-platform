import os

from langfuse.langchain import CallbackHandler

from backend.core.config import settings


def get_langfuse_handler():
    if not settings.langfuse_public_key or not settings.langfuse_secret_key:
        return None

    os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
    os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
    os.environ["LANGFUSE_HOST"] = settings.langfuse_base_url

    return CallbackHandler()