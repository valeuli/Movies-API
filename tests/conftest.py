import os

import pytest

from app.database_settings import (
    Base,
    test_engine,
    TestingSessionLocal,
    get_session_local,
)

from main import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Setup test database and create tables.
    """
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "5"
    os.environ["SECRET_TOKEN"] = "secret_token"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["REPOSITORY_TYPE"] = "sqlite"
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def test_db(setup_test_db):
    """
    Get a clean session for testing.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function", autouse=True)
def override_dependency(test_db):
    """
    Function to override FastAPI's SessionLocal dependency for testing.
    """
    app.dependency_overrides[get_session_local] = lambda: test_db
