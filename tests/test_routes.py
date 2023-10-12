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


def test_login_wrong_password():
    response = client.post(
        "auth/login",
        data={
            "username": "testUser",
            "password": "wrongPassword",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_wrong_username():
    response = client.post(
        "auth/login",
        data={
            "username": "wrongUsername",
            "password": "test",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Incorrect username or password"}


def test_profile():
    response = client.get("auth/profile", headers={"Authorization": "Bearer testUser"})
    assert response.status_code == 200


def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"username": "testUser", "id": 1, "events": []}

def test_create_event():
    response = client.post(
        "/events/",
        json={
            "title": "testEvent",
            "description": "testDescription",
            "date_time": "2021-06-30T15:00:00",
            "location": "testLocation",
            "total_tickets": 100,
            "price": 10.0,
        },
        headers={"Authorization": "Bearer testUser"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "testEvent",
        "description": "testDescription",
        "date_time": "2021-06-30T15:00:00",
        "location": "testLocation",
        "total_tickets": 100,
        "price": 10.0,
        "id": 1,
        "organizer": 1,
        "available_tickets": 100,
    }

def test_create_event_no_token():
    response = client.post(
        "/events/",
        json={
            "title": "testEvent",
            "description": "testDescription",
            "date_time": "2021-06-30T15:00:00",
            "location": "testLocation",
            "total_tickets": 100,
            "price": 10.0,
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_create_event_incomplete_details():
    response = client.post(
        "/events/",
        json={
            "title": "testEvent",
            "description": "testDescription",
            "date_time": "2021-06-30T15:00:00",
            "location": "testLocation",
            "total_tickets": 100,
        },
        headers={"Authorization": "Bearer testUser"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "price"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

def test_get_events():
    response = client.get("/events/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_event():
    response = client.get("/events/1")
    assert response.status_code == 200
    assert response.json() == {
        "title": "testEvent",
        "description": "testDescription",
        "date_time": "2021-06-30T15:00:00",
        "location": "testLocation",
        "total_tickets": 100,
        "price": 10.0,
        "id": 1,
        "organizer": 1,
        "available_tickets": 100,
    }

def test_get_event_not_found():
    response = client.get("/events/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_get_event_organizer():
    response = client.get("/events/1/organizer")
    assert response.status_code == 200
    assert response.json().get("username") == "testUser"

def test_get_event_organizer_not_found():
    response = client.get("/events/2/organizer")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_update_event():
    response = client.patch(
        "/events/1",
        json={
            "title": "testEventUpdated",
            "description": "testDescriptionUpdated",
        },
        headers={"Authorization": "Bearer testUser"},
    )
    assert response.status_code == 200
    assert response.json().get("title") == "testEventUpdated"
    assert response.json().get("description") == "testDescriptionUpdated"