from pydantic import BaseModel
from typing import Optional
from enum import Enum

class PipelineType(str, Enum):
    jenkins = "jenkins"
    github_actions = "github_actions"
    airflow = "airflow"
    prefect = "prefect"
    gitlab_ci = "gitlab_ci"

class ChatMessage(BaseModel):
    role: str           # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    source_type: Optional[PipelineType] = None
    target_type: Optional[PipelineType] = None
    conversation_history: Optional[list[ChatMessage]] = []

class ChatResponse(BaseModel):
    message: str
    translated_code: Optional[str] = None
    source_type: Optional[str] = None
    target_type: Optional[str] = None
    status: str = "success"

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    detail: Optional[str] = None

# Stub schemas for future features (don't build yet)
class GuidelineRequest(BaseModel):
    guideline_type: Optional[str] = None

class DocumentSourceRequest(BaseModel):
    source: str         # "confluence" | "github" | "upload"
    url: Optional[str] = None
    token: Optional[str] = None