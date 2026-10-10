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

def test_safety_fire_smoke():
    payload = {
        "request_id": "REQ-FIRE-1",
        "channel": "email",
        "product_family": "Room Heater",
        "warranty_status": "in_warranty",
        "request_text": "it catch fire today and there is smoke everywhere",
        "source": "crm"
    }
    response = client.post("/api/route", json=payload)
    data = response.json()
    assert data["is_safety_incident"] is True
    assert data["needs_review"] is True
    assert "fire" in data["safety_triggers"] or "smoke" in data["safety_triggers"]

def test_safety_electric_shock():
    payload = {
        "request_id": "REQ-SHOCK-1",
        "channel": "email",
        "product_family": "Water Purifier",
        "warranty_status": "in_warranty",
        "request_text": "I got an electric shock from the plug",
        "source": "crm"
    }
    response = client.post("/api/route", json=payload)
    data = response.json()
    assert data["is_safety_incident"] is True
    assert "electric shock" in data["safety_triggers"]

def test_safety_negated_context():
    payload = {
        "request_id": "REQ-NEG-1",
        "channel": "email",
        "product_family": "Air Fryer",
        "warranty_status": "in_warranty",
        "request_text": "Thank god it did not catch fire, but it's broken",
        "source": "crm"
    }
    response = client.post("/api/route", json=payload)
    data = response.json()
    # "not catch fire" should be negated
    assert data["is_safety_incident"] is False
    assert len(data["safety_triggers"]) == 0

def test_ordinary_repair():
    payload = {
        "request_id": "REQ-REP-1",
        "channel": "email",
        "product_family": "Robot Vacuum",
        "warranty_status": "out_of_warranty",
        "request_text": "Making a loud noise and spinning in circles",
        "source": "crm"
    }
    response = client.post("/api/route", json=payload)
    data = response.json()
    assert data["is_safety_incident"] is False
    
def test_normal_exchange():
    payload = {
        "request_id": "REQ-EXC-1",
        "channel": "email",
        "product_family": "Ceiling Fan",
        "warranty_status": "in_warranty",
        "request_text": "Wrong color delivered, I want an exchange",
        "source": "crm"
    }
    response = client.post("/api/route", json=payload)
    data = response.json()
    assert data["is_safety_incident"] is False
