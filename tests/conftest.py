
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, SessionLocal


# 🔹 Fixture qui s'exécute une fois par session de tests
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Crée toutes les tables avant les tests
    init_db()
    yield
    # Ici tu pourrais drop la DB si besoin (pour garder propre)


# 🔹 Fixture pour fournir un client HTTP
@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# 🔹 Fixture pour accéder directement à la session DB si besoin
@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
