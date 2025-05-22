from typing import Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings
from langfuse.decorators import observe
class AIService:
    def __init__(self, provider: str = "google", default_model: str = "gemini-2.0-flash"):
        self.provider = provider
        self.default_model = default_model

    def _load_llm(self, model: str):
        if self.provider == "google":
            return ChatGoogleGenerativeAI(model=model, api_key=settings.GEMINI_API_KEY)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
    @observe(as_type="generation")
    def invoke(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = "You are a helpful assistant",
        model: Optional[str] = None
    ) -> str:
        selected_model = model or self.default_model
        llm = self._load_llm(selected_model)

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        return llm.invoke(messages).content
