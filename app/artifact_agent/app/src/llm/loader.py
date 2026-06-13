import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

load_dotenv()


class LLMFactory:
    @staticmethod
    def get_llm(provider=None):
        provider = (
            provider
            or os.getenv("LLM_PROVIDER", "openai")
        ).lower()

        if provider == "openai":
            return ChatOpenAI(
                model=os.getenv(
                    "OPENAI_MODEL",
                    "gpt-4o-mini"
                ),
                temperature=float(
                    os.getenv(
                        "LLM_TEMPERATURE",
                        0
                    )
                ),
                api_key=os.getenv(
                    "OPENAI_API_KEY"
                ),
            )

        if provider == "mistral":
            return ChatMistralAI(
                model=os.getenv(
                    "MISTRAL_MODEL",
                    "mistral-large-latest"
                ),
                temperature=float(
                    os.getenv(
                        "LLM_TEMPERATURE",
                        0
                    )
                ),
                api_key=os.getenv(
                    "MISTRAL_API_KEY"
                ),
            )

        if provider == "ollama":
            return ChatOllama(
                model=os.getenv(
                    "OLLAMA_MODEL",
                    "deepseek-r1:7b"
                ),
                base_url=os.getenv(
                    "OLLAMA_BASE_URL",
                    "http://localhost:11434"
                ),
                temperature=float(
                    os.getenv(
                        "LLM_TEMPERATURE",
                        0
                    )
                ),
            )

        raise ValueError(
            f"Unsupported provider: {provider}"
        )


llm = LLMFactory.get_llm()