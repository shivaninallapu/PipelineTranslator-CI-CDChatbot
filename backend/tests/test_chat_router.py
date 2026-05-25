from fastapi.testclient import TestClient
from backend.main import app
import backend.routers.chat as chat_router
import io

client = TestClient(app)

BASE = "/api"  # <-- change this to match your app.include_router(prefix=...)

def test_chat_text_endpoint(monkeypatch):

    async def mock_chat(*args, **kwargs):
        return "Mocked chat response"

    monkeypatch.setattr(
        chat_router.langchain_service,
        "chat",
        mock_chat
    )

    response = client.post(
        "/api/chat/text",
        json={
            "message": "Hello",
            "source_type": None,
            "target_type": None,
            "conversation_history": []
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Mocked chat response"


def test_chat_file_upload_translation(monkeypatch):
    async def mock_translate_pipeline(**kwargs):
        return {"translated_code": "mock code", "explanation": "mock explanation"}

    async def mock_save_uploaded_file(file):
        # Simulate what your real helper returns
        return {"content": "pipeline code", "file_path": "/tmp/fake.txt"}

    def mock_cleanup_file(path):
        return None

    monkeypatch.setattr(chat_router.langchain_service, "translate_pipeline", mock_translate_pipeline)
    monkeypatch.setattr(chat_router, "save_uploaded_file", mock_save_uploaded_file)
    monkeypatch.setattr(chat_router, "cleanup_file", mock_cleanup_file)

    file_bytes = io.BytesIO(b"pipeline code")
    response = client.post(
        f"{BASE}/chat",
        data={
            "message": "translate this",
            "source_type": "jenkins",
            "target_type": "github_actions",
            "conversation_history": "[]",
        },
        files={"file": ("sample.txt", file_bytes, "text/plain")}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["translated_code"] == "mock code"
    assert body["message"] == "mock explanation"