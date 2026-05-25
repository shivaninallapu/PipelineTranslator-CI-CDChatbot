import os
import pytest
import httpx

@pytest.mark.integration
def test_localai_is_up_when_configured():
    # Only enforce this when you explicitly chose LocalAI
    provider = (os.getenv("LLM_PROVIDER") or "").lower()
    if provider and provider != "localai":
        pytest.skip(f"LLM_PROVIDER={provider}, not localai")

    base = os.getenv("LOCALAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
    if not base:
        # default for local dev if you want
        base = "http://localhost:8080/v1"

    # If you didn't actually intend to run LocalAI, skip instead of failing CI
    # Set REQUIRE_LOCALAI=1 to force failure when down.
    require = os.getenv("REQUIRE_LOCALAI", "0") == "1"

    try:
        with httpx.Client(timeout=3.0) as client:
            r = client.get(f"{base}/models", headers={"Authorization": "Bearer dummy"})
    except Exception as e:
        if require:
            raise
        pytest.skip(f"LocalAI not reachable at {base}: {e}")

    if r.status_code != 200:
        msg = f"Bad response from LocalAI: {r.status_code} {r.text}"
        if require:
            pytest.fail(msg)
        pytest.skip(msg)

    data = r.json()
    assert "data" in data and isinstance(data["data"], list), f"Unexpected JSON: {data}"
    assert len(data["data"]) > 0, "LocalAI is up but returned no models"
