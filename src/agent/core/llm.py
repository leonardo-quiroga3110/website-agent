from langchain_openai import ChatOpenAI
from agent.core.config import get_settings

def get_llm(model_name: str = "gpt-4o") -> ChatOpenAI:
    """
    Returns a configured instance of the OpenAI Chat model.
    """
    settings = get_settings()
    return ChatOpenAI(
        model=model_name,
        openai_api_key=settings.OPENAI_API_KEY,
        temperature=0,
        max_retries=3
    )
