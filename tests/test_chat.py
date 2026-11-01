from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_domains():
    response = client.get("/domains")
    assert response.status_code == 200
    assert "pest_disease" in response.json()["domains"]


def test_chat_demo_mode(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "api_key", None)

    response = client.post(
        "/api/chat",
        data={
            "message": "How should I diagnose yellowing tomato leaves?",
            "domain": "pest_disease",
            "crop": "Tomato",
            "growth_stage": "Flowering",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "demo"
    assert "Initial recommendation" in body["answer"]


def test_chemical_safety_finding(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "api_key", None)

    response = client.post(
        "/api/chat",
        data={
            "message": (
                "Can I mix this herbicide with another pesticide "
                "and apply it tomorrow?"
            ),
            "domain": "pest_disease",
        },
    )

    assert response.status_code == 200
    findings = response.json()["safety_findings"]
    assert any(
        item["category"] == "chemical_safety"
        for item in findings
    )
