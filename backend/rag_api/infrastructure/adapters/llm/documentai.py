import os
from kink import inject
import vertexai
from vertexai.preview.vision_models import Image, ImageTextModel
from pydantic import SecretStr
from dotenv import load_dotenv
from rag_api.infrastructure.ports import LLMPort

load_dotenv()

class DocumentAILLMAdapter(LLMPort):
    def __init__(self, gcp_project_id):
        vertexai.init(project=gcp_project_id, location="northamerica-northeast2")
        self.model = ImageTextModel.from_pretrained("gemini-2.0-flash-001")

    def get_response(self, prompt: str) -> str:
        response = self.model(prompt)
        return response
    
    def ask_question_on_image(self, image_loc, image_bytes, question):
        source_img = Image.load_from_file(location=image_loc) if image_loc else Image(image_bytes=image_bytes)
        answers = self.model.ask_question(
                    image=source_img,
                    question=question,
                    number_of_results=1)
        return answers
