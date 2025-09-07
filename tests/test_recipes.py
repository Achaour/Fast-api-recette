def test_create_and_list_recipe(client):
    # Signup + Login
    client.post("/auth/signup", json={"email": "b@b.com", "password": "secret"})
    login = client.post("/auth/login", data={"username": "b@b.com", "password": "secret"})
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create recipe
    response = client.post(
        "/recipes/",
        headers=headers,
        json={
            "title": "Pasta",
            "ingredients": "pasta, tomato, salt",
            "instructions": "boil water, cook pasta",
            "prep_minutes": 10,
            "difficulty": "easy",
        },
    )
    assert response.status_code == 201

    # List recipes
    response = client.get("/recipes/")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) > 0
