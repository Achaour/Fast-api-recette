from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def auth_header():
    client.post("/auth/signup", json={"email":"b@b.com","password":"x"})
    token = client.post("/auth/login", json={"email":"b@b.com","password":"x"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_and_list_recipe():
    h = auth_header()
    r = client.post("/recipes/", headers=h, json={
        "title":"Pasta", "ingredients":"tomato\npasta", "instructions":"Boil", "prep_minutes":10, "difficulty":"easy"
    })
    assert r.status_code == 201
    r2 = client.get("/recipes?ingredient=tomato")
    assert r2.status_code == 200
    assert any("Pasta" == it["title"] for it in r2.json())
