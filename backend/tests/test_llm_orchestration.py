import pytest
from backend.services import llm_orchestration


@pytest.mark.asyncio
async def test_chat_returns_string(monkeypatch):

    # Mock llm.invoke to avoid real LLM call
    class MockResponse:
        content = "Mocked response"

    def mock_invoke(self, prompt):
        return MockResponse()


    monkeypatch.setattr(type(llm_orchestration.llm), "invoke", mock_invoke)

    result = await llm_orchestration.chat(
        message="Hello",
        history=[]
    )

    assert result == "Mocked response"


@pytest.mark.asyncio
async def test_translate_returns_structured_json(monkeypatch):

    class MockResponse:
        content = '{"translated_code": "mock code", "explanation": "mock explanation"}'

    def mock_invoke(self, prompt):
        return MockResponse()


    monkeypatch.setattr(type(llm_orchestration.llm), "invoke", mock_invoke)


    result = await llm_orchestration.translate(
        code="pipeline",
        source="jenkins",
        target="github_actions",
        history=[]
    )

    assert result["translated_code"] == "mock code"
    assert result["explanation"] == "mock explanation"
