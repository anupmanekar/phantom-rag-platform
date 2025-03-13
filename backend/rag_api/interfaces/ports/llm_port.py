from abc import ABC, abstractmethod

class LLMPort(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass
