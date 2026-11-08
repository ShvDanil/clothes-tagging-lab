import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.config import Settings
from app.db import Database
from app.main import create_app


@pytest.fixture
def client(monkeypatch):
    # Unit tests do not connect to PostgreSQL or paid model APIs.
    monkeypatch.setattr(Database, "initialize", lambda self: None)
    monkeypatch.setattr(Database, "check", lambda self: None)
    application = create_app(
        Settings(
            database_url="postgresql+psycopg://unused:unused@localhost/unused",
            max_images_per_item=5,
        )
    )
    with TestClient(application) as instance:
        yield instance


def test_liveness_and_readiness(client):
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200


def test_readiness_reports_database_failure(client, monkeypatch):
    def unavailable(self):
        raise OperationalError("SELECT 1", {}, Exception("database offline"))

    monkeypatch.setattr(Database, "check", unavailable)
    response = client.get("/ready")
    assert response.status_code == 503
    assert "offline" not in response.text
    assert client.get("/health").status_code == 200


def test_openapi_exposes_image_upload(client):
    spec = client.get("/openapi.json").json()
    content = spec["paths"]["/annotate"]["post"]["requestBody"]["content"]
    assert "multipart/form-data" in content
    body_name = content["multipart/form-data"]["schema"]["$ref"].rsplit("/", 1)[1]
    images = spec["components"]["schemas"][body_name]["properties"]["images"]
    assert images["type"] == "array"
    assert images["items"]["type"] == "string"
    assert images["items"]["contentMediaType"] == "application/octet-stream"
    assert client.post("/annotate").status_code == 422


@pytest.mark.parametrize("count", [1, 2, 5])
def test_starter_accepts_one_or_many_uploads(client, count):
    # Transport fixtures only; decoding and the model pipeline remain the assignment.
    files = [
        ("images", (f"view-{i}.jpg", b"transport fixture", "image/jpeg")) for i in range(count)
    ]
    assert client.post("/annotate", files=files).status_code == 501


def test_excess_images_are_rejected_before_the_pipeline(client):
    maximum = client.app.state.settings.max_images_per_item
    files = [
        ("images", (f"view-{i}.jpg", b"transport fixture", "image/jpeg"))
        for i in range(maximum + 1)
    ]
    assert client.post("/annotate", files=files).status_code == 422
