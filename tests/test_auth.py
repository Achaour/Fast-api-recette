def test_signup_and_login(client):
    # Signup
    response = client.post("/auth/signup", json={"email": "a@a.com", "password": "secret"})
    assert response.status_code == 201

    # Login (⚠️ ici, login attend form-data)
    response = client.post(
        "/auth/login",
        data={"username": "a@a.com", "password": "secret"}  # pas JSON
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
