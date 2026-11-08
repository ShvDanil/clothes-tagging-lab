import os
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.schema import CreateSchema, DropSchema

from app.db import Database
from app.models import ItemAnnotation

pytestmark = pytest.mark.integration


@pytest.fixture
def database():
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.fail("Set TEST_DATABASE_URL or use: docker compose --profile test run --rm tests")
    # Isolated schema; no application tables or other tests are dropped.
    schema = "lab_test_" + uuid4().hex
    admin_engine = create_engine(url)
    with admin_engine.begin() as connection:
        connection.execute(CreateSchema(schema))
    database = Database(url)
    database.close()
    database.engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    database.session_factory.configure(bind=database.engine)
    try:
        database.initialize()
        database.initialize()  # Startup must also work with existing tables.
        yield database
    finally:
        database.close()
        with admin_engine.begin() as connection:
            connection.execute(DropSchema(schema, cascade=True))
        admin_engine.dispose()


def test_bootstrap_and_jsonb_roundtrip(database):
    database.check()
    with database.session_factory.begin() as session:
        # Storage fixture only: this is not an example of a model annotation.
        row = ItemAnnotation(
            payload={"storage_test": "проверка JSONB"},
            provenance={"test": True},
        )
        session.add(row)
        session.flush()
        row_id = row.id
    with Session(database.engine) as session:
        stored = session.get(ItemAnnotation, row_id)
        assert stored.payload["storage_test"] == "проверка JSONB"
        assert stored.created_at.tzinfo is not None
        assert (
            session.scalar(text("SELECT pg_typeof(payload)::text FROM item_annotations")) == "jsonb"
        )


def test_transaction_rollback_and_unique_request_key(database):
    with database.session_factory.begin() as session:
        session.add(ItemAnnotation(request_key="same-key", payload={}, provenance={}))
    with pytest.raises(IntegrityError), database.session_factory.begin() as session:
        session.add(ItemAnnotation(request_key="same-key", payload={}, provenance={}))
        session.flush()
    with database.session_factory() as session:
        assert session.scalar(select(func.count()).select_from(ItemAnnotation)) == 1
    # The constraint is infrastructure; request-level idempotency is still a task.
