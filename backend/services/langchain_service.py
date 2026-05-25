import os
from dotenv import load_dotenv
from fastapi import HTTPException
import asyncio

load_dotenv()

class LangChainService:
    def __init__(self):
        self.llm_provider = os.getenv("LLM_PROVIDER", "ollama")
        
        try:
            import backend.services.llm_orchestration as llm_orchestration
            self.langchain = llm_orchestration
            print("✅ LangChain module loaded successfully")
        except Exception as exc:
            print(f"⚠️ LangChain module unavailable, using stub responses: {exc}")
            self.langchain = None
        
        print(f"🔗 LangChain service initialized with provider: {self.llm_provider}")

    async def translate_pipeline(self, pipeline_code, source_type, target_type, conversation_history):
        if self.langchain is None:
            return {
                "translated_code": "# stub translation",
                "explanation": "Stub: llm_orchestration.py not found",
                "status": "success"
            }
        
        try:
            return await asyncio.wait_for(
                self.langchain.translate(
                    code=pipeline_code,
                    source=source_type,
                    target=target_type,
                    history=conversation_history
                ),
                timeout=120.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="LLM took too long to respond. Try a smaller pipeline."
            )

    async def chat(self, message, history):
        if self.langchain is None:
            return f"[Stub] Received: {message}"
        
        try:
            return await asyncio.wait_for(
                self.langchain.chat(
                    message=message,
                    history=history
                ),
                timeout=60.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="LLM took too long to respond. Please try again."
            )


# Singleton — instantiated once when server boots
langchain_service = LangChainService()
