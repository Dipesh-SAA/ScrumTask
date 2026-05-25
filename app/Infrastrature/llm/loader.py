from dotenv import load_dotenv
import os
from langchain_mistralai import ChatMistralAI
from langchain_ollama import ChatOllama
load_dotenv()




llm= ChatMistralAI(
        model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
        temperature=0,
        api_key=os.getenv("MISTRAL_API_KEY"),
    )



# llm = ChatOllama(
#     model=os.getenv("OLLAMA_MODEL", "mistral:7b"),
#     temperature=0.5,
# )


# llm = ChatOllama(
#     model=os.getenv("OLLAMA_MODEL", "deepseek-r1:latest"),
#     temperature=0,
# )

# llm = ChatOllama(
#     model=os.getenv("OLLAMA_MODEL"," qwen2.5-coder:7b"),
#     temperature=0,
# )
