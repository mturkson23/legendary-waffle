from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from app import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}

def test_register():
    response = client.post(
        "auth/register",
        json={
            "username": "testUser",
            "password": "test",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"access_token": "testUser", "token_type": "bearer"}

def test_register_existing_user():
    response = client.post(
        "auth/register",
        json={
            "username": "testUser",
            "password": "test",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_login():
    response = client.post(
        "auth/login",
        data={
            "username": "testUser",
            "password": "test",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"access_token": "testUser", "token_type": "bearer"}

def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1