from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "model_loaded": True}

def test_get_teams():
    response = client.get("/api/teams")
    assert response.status_code == 200
    teams = response.json()
    assert "Repairs" in teams
    assert len(teams) == 7

def test_predict_route():
    payload = {
        "request_id": "REQ-TEST-123",
        "channel": "email",
        "product_family": "Air Purifier",
        "warranty_status": "in_warranty",
        "request_text": "My purifier is making a loud noise and leaking.",
        "source": "crm"
    }
    response = client.post("/api/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_team" in data
    assert data["predicted_team"] in [
        "Installs & Demo", "Repairs", "Filters & Consumables",
        "Billing", "Returns & Replacement", "Warranty Claims", "Product Advice"
    ]
    assert "confidence" in data
    assert "reasons" in data
    assert "needs_review" in data

def test_predict_invalid_schema():
    payload = {
        "channel": "email",
        "request_text": "Missing request_id"
    }
    response = client.post("/api/route", json=payload)
    assert response.status_code == 422 # Unprocessable Entity
