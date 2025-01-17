import os
from langchain_fireworks import ChatFireworks

class LLMHandler:
    def __init__(self):
        self.model = ChatFireworks(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            max_tokens=None,
            temperature=0,
            api_key=os.environ.get("FIREWORKS_API_KEY")
        )
