from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import json

from backend.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from backend.services.langchain_service import langchain_service
from backend.utils.file_handler import save_uploaded_file, cleanup_file

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    message: str = Form(...),
    source_type: Optional[str] = Form(None),
    target_type: Optional[str] = Form(None),
    conversation_history: Optional[str] = Form("[]"),  # JSON string
    file: Optional[UploadFile] = File(None)
):
    """
    Main chat endpoint.
    Accepts a message + optional file upload.
    Returns AI response with optional translated code.
    """
    
    file_data = None
    file_path = None
    
    try:
        # Parse conversation history from JSON string
        try:
            history = json.loads(conversation_history)
        except json.JSONDecodeError:
            history = []
        
        # Handle file upload if provided
        pipeline_code = None
        if file and file.filename:
            file_data = await save_uploaded_file(file)
            pipeline_code = file_data["content"]
            file_path = file_data["file_path"]
        
        # Determine if this is a translation request
        is_translation = (
            pipeline_code is not None or 
            (source_type and target_type)
        )
        
        if is_translation and pipeline_code:
            # Translation request
            result = await langchain_service.translate_pipeline(
                pipeline_code=pipeline_code,
                source_type=source_type or "jenkins",
                target_type=target_type or "github_actions",
                conversation_history=history
            )
            
            return ChatResponse(
                message=result.get("explanation", "Translation complete."),
                translated_code=result.get("translated_code"),
                source_type=source_type,
                target_type=target_type,
                status="success"
            )
        
        else:
            # General chat request (no translation)
            response = await langchain_service.chat(
                message=message,
                history=history
            )
            
            return ChatResponse(
                message=response,
                status="success"
            )
    
    except HTTPException:
        raise  # re-raise HTTP exceptions as-is
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )
    
    finally:
        # Always clean up temp files
        if file_path:
            cleanup_file(file_path)


@router.post("/chat/text", response_model=ChatResponse)
async def chat_text(request: ChatRequest):
    """
    Text-only chat endpoint (no file upload).
    Easier for frontend to use when pasting code directly.
    """
    try:
        is_translation = (
            request.source_type and 
            request.target_type and 
            request.message
        )
        
        if is_translation:
            result = await langchain_service.translate_pipeline(
                pipeline_code=request.message,
                source_type=request.source_type,
                target_type=request.target_type,
                conversation_history=[
                    msg.dict() for msg in request.conversation_history
                ]
            )
            return ChatResponse(
                message=result.get("explanation", "Translation complete."),
                translated_code=result.get("translated_code"),
                source_type=request.source_type,
                target_type=request.target_type,
                status="success"
            )
        
        else:
            response = await langchain_service.chat(
                message=request.message,
                history=[
                    msg.dict() for msg in request.conversation_history
                ]
            )
            return ChatResponse(
                message=response,
                status="success"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )


# --- STUB ENDPOINTS (future features, return mock data for now) ---

@router.get("/guidelines")
async def get_guidelines():
    """STUB: Returns available team guidelines. Full implementation in Phase 2."""
    return {
        "status": "stub",
        "message": "Guidelines feature coming in Phase 2",
        "guidelines": [
            {"id": "naming-001", "type": "naming_convention", "title": "Variable Naming"},
            {"id": "security-001", "type": "security", "title": "Secret Management"},
            {"id": "deploy-001", "type": "deployment", "title": "Production Deployment"},
        ]
    }

@router.post("/connect/confluence")
async def connect_confluence():
    """STUB: Confluence integration coming in Phase 2."""
    return {
        "status": "stub",
        "message": "Confluence integration coming in Phase 2"
    }

@router.post("/connect/github")
async def connect_github():
    """STUB: GitHub integration coming in Phase 2."""
    return {
        "status": "stub", 
        "message": "GitHub integration coming in Phase 2"
    }