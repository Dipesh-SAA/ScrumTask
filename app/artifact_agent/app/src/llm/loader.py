from app.Infrastrature.llm.loader import _load_llm, llm


class LLMFactory:
    @staticmethod
    def get_llm(provider=None):
        return _load_llm(provider)
