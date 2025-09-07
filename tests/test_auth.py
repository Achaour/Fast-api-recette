from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_and_login():
    r = client.post("/auth/signup", json={"email":"a@a.com","password":"x"})
    assert r.status_code in (201, 400)  # si relancé, 400 (déjà inscrit)
    r = client.post("/auth/login", json={"email":"a@a.com","password":"x"})
    assert r.status_code == 200
    assert "access_token" in r.json()
