import os
from kink import inject
from langchain_fireworks import ChatFireworks
from pydantic import SecretStr
from dotenv import load_dotenv
from rag_api.infrastructure.ports import LLMPort

load_dotenv()

class FireworksLLMAdapter(LLMPort):
    def __init__(self):
        self.model = ChatFireworks(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            max_tokens=None,
            temperature=0,
            api_key=SecretStr(os.environ.get("FIREWORKS_API_KEY"))
        )

    def get_response(self, prompt: str) -> str:
        response = self.model(prompt)
        return response
