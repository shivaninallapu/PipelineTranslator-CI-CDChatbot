from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_provider": os.getenv("LLM_PROVIDER"),
        "version": "0.1.0"
    }