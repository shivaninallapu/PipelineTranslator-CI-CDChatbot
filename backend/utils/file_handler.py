import os
import uuid
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", 5)) * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".groovy",    # Jenkinsfile
    ".yml",       # GitHub Actions, Airflow
    ".yaml",
    ".py",        # Airflow DAGs, Prefect
    ".json",
    ".xml",
    ".txt"
}

async def save_uploaded_file(file: UploadFile) -> dict:
    """Save uploaded file and return its content and metadata"""
    
    # Check file extension
    _, ext = os.path.splitext(file.filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {ext} not supported. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {os.getenv('MAX_FILE_SIZE_MB')}MB"
        )
    
    # Save file with unique name
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Decode content for LLM
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File encoding not supported. Please use UTF-8 encoded files."
        )
    
    return {
        "filename": file.filename,
        "file_path": file_path,
        "content": decoded_content,
        "size_bytes": len(content)
    }

def cleanup_file(file_path: str):
    """Delete temp file after processing"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not delete temp file {file_path}: {e}")