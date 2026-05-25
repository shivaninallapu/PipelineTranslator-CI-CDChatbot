from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from backend.routers import chat, health

app = FastAPI(
    title="Pipeline Translation API",
    description="Translates pipeline code between formats using LLM",
    version="0.1.0"
)

# CORS - allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
        "http://localhost:3000",  # fallback
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(chat.router, prefix="/api")

# Stub routers for future features
# app.include_router(confluence.router, prefix="/api")
# app.include_router(github.router, prefix="/api")
# app.include_router(guidelines.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Create upload directory if it doesn't exist
    os.makedirs(os.getenv("UPLOAD_DIR", "./uploads"), exist_ok=True)
    print("✅ Backend started successfully")
    print(f"📡 LLM Provider: {os.getenv('LLM_PROVIDER')}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)