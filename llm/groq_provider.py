from langchain_groq import ChatGroq
from .base import BaseLLM
import os


class GroqProvider(BaseLLM):
    def __init__(self, model="llama-3.1-8b-instant"):
        self.llm = ChatGroq(
            model=model,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content