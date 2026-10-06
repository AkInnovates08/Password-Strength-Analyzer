import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app import app

def test_health():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json["status"] == "ok"

def test_analyze_api_does_not_return_password():
    client = app.test_client()
    password = "SyntheticDemo123!"
    r = client.post("/api/analyze", json={"password": password})
    assert r.status_code == 200
    assert password not in r.get_data(as_text=True)

def test_generator_api():
    client = app.test_client()
    r = client.post("/api/generate-password", json={"length": 20})
    assert r.status_code == 200
    assert len(r.json["password"]) == 20

def test_dashboard_has_no_password_field():
    client = app.test_client()
    r = client.get("/api/dashboard/stats")
    assert "password" not in r.get_data(as_text=True).lower()
