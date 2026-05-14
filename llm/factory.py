from .groq_provider import GroqProvider


def get_llm():
    return GroqProvider()