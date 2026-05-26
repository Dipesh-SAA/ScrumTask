from dotenv import load_dotenv
import os
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI


def get_int_env(name, default):
    value = os.getenv(name)
    return int(value) if value else default


llm = ChatOpenAI(
       model=os.getenv("OPENAI_MODEL", "gpt-4"),
    temperature=0,
       api_key=os.getenv("OPENAI_API_KEY"),
       max_tokens=get_int_env("OPENAI_MAX_COMPLETION_TOKENS", 3500)

)

# llm=ChatMistralAI(
#       model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
#        temperature=0,
#         api_key=os.getenv("MISTRAL_API_KEY"),
#   )



# def _openai_llm():
#     from langchain_openai import ChatOpenAI

#     return ChatOpenAI(
#         model=os.getenv("OPENAI_MODEL", "gpt-4"),
#         temperature=0,
#         api_key=os.getenv("OPENAI_API_KEY"),
#     )


# def _mistral_llm():
#     from langchain_mistralai import ChatMistralAI

#     return ChatMistralAI(
#         model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
#         temperature=0,
#         api_key=os.getenv("MISTRAL_API_KEY"),
#     )


# def _ollama_llm():
#     from langchain_ollama import ChatOllama

#     return ChatOllama(
#         model=os.getenv("OLLAMA_MODEL", "deepseek-r1:latest"),
#         temperature=0,
#     )


# def _load_llm():
#     provider = os.getenv("LLM_PROVIDER", "auto").lower()

#     if provider == "openai":
#         return _openai_llm()

#     if provider == "mistral":
#         return _mistral_llm()

#     if provider == "ollama":
#         return _ollama_llm()

#     if os.getenv("OPENAI_API_KEY"):
#         try:
#             return _openai_llm()
#         except ModuleNotFoundError:
#             pass

#     if os.getenv("MISTRAL_API_KEY"):
#         try:
#             return _mistral_llm()
#         except ModuleNotFoundError:
#             pass

#     return _ollama_llm()


# llm = _load_llm()
