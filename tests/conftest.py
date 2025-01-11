import os

import pytest
from app.database_settings import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker

from app.main import app

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Setup test database and create tables.
    """
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "5"
    os.environ["SECRET_TOKEN"] = "secret_token"
    os.environ["ALGORITHM"] = "HS256"
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="class")
def test_db(setup_test_db):
    """
    Get a clean session for testing.
    """
    app.dependency_overrides[SessionLocal] = lambda: test_db
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
