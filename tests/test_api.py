import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import AnalysisResult


def fake_analyze(_: str) -> tuple[AnalysisResult, str]:
    return (
        AnalysisResult(
            summary="Bản tóm tắt kiểm thử.",
            sentiment="positive",
            keywords=["kiểm thử", "FastAPI", "AI"],
        ),
        "fake-model",
    )


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_and_save(monkeypatch) -> None:
    monkeypatch.setattr("app.api.routes.analyze_with_ai", fake_analyze)
    with TestClient(app) as client:
        response = client.post("/analyze", json={"text": "FastAPI rất dễ học."})

    assert response.status_code == 201
    body = response.json()
    assert body["sentiment"] == "positive"
    assert body["model"] == "fake-model"

