import os
from kink import inject
from google import genai
from google.genai.types import HttpOptions, Part
from pydantic import SecretStr
from dotenv import load_dotenv
from rag_api.infrastructure.ports import LLMPort
from langchain_google_vertexai import ChatVertexAI


load_dotenv()

class GoogleGenAILLMAdapter(LLMPort):
    def __init__(self):
        self.client = genai.Client(http_options=HttpOptions(api_version="v1"))
        self.model = ChatVertexAI(
            model="gemini-2.0-flash-001",
            temperature=0,
            max_tokens=None,
            max_retries=6,
            stop=None,
        )

    def get_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=[prompt]
        )
        return response
    
    def ask_question_on_image(self, image_loc, image_bytes, question):
        response = self.client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=[
                    "What is shown in this image?",
                    Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                ],
            )
        return response.text
