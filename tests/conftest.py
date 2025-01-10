import os

import pytest
from app.database_settings import Base, engine
from sqlalchemy.orm import sessionmaker

# Motor y sesión para pruebas
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Setup test database and create tables.
    """
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="class")
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
