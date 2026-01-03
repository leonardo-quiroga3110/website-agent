from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings for the Autonomous Agent.
    Loads from .env file and environment variables.
    """
    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(..., description="API key for OpenAI models")
    
    # LangGraph/LangChain Configuration
    LANGCHAIN_TRACING_V2: bool = Field(default=False)
    LANGCHAIN_API_KEY: str | None = Field(default=None, description="API key for LangChain tracing")
    LANGCHAIN_PROJECT: str = Field(default="langgraph-agent")

    # App Settings
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")

    # RAG Configuration
    CHROMA_PATH: str = Field(default="./chroma_db", description="Path to persist ChromaDB")
    COLLECTION_NAME: str = Field(default="monte_azul_docs", description="ChromaDB collection name")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", description="OpenAI embedding model")
    WEBSITE_URL: str = Field(default="https://www.monteazulgroup.com/es", description="Website to scrape")

    # WhatsApp Business API Configuration
    WHATSAPP_PHONE_NUMBER_ID: str | None = Field(default=None)
    WHATSAPP_ACCESS_TOKEN: str | None = Field(default=None)
    WEBHOOK_VERIFY_TOKEN: str | None = Field(default=None)

    # Database Configuration (Supabase/Postgres)
    DATABASE_URL: str | None = Field(default=None, description="PostgreSQL URL for persistent memory")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the settings to avoid redundant disk/env reads.
    """
    return Settings()
