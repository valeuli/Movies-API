import os
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

from app.repositories.get_repository import get_repository
from app.repositories.mongo_repository import MongoDBRepository
from app.repositories.sql_repository import SQLRepository


class FakeModel:
    """SQLAlchemy or MongoDB model."""

    __tablename__ = "fake_model"


@pytest.fixture
def mock_sql_session():
    """Mock of SQLAlchemy Session."""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_mongo_client():
    """Mock of MongoDB client."""
    return MagicMock()


@pytest.fixture
def mock_env_sqlite():
    """Conf REPOSITORY_TYPE for 'sqlite'."""
    with patch.dict(os.environ, {"REPOSITORY_TYPE": "sqlite"}):
        yield


@pytest.fixture
def mock_env_mongodb():
    """Conf for REPOSITORY_TYPE for 'mongodb'."""
    with patch.dict(os.environ, {"REPOSITORY_TYPE": "mongodb"}):
        yield


def test_get_repository_sqlite(mock_sql_session, mock_env_sqlite):
    """
    Test to verify get_repository returns SQLRepository.
    """
    repo = get_repository(db=mock_sql_session, model=FakeModel)
    assert isinstance(repo, SQLRepository)
    assert repo.model == FakeModel
    assert repo.db == mock_sql_session


@patch("app.database_settings.mongo_client", new_callable=MagicMock)
def test_get_repository_mongodb(mock_mongo_client, mock_env_mongodb):
    """
    Test to verify it returns MongoDBRepository.
    """
    repository = get_repository(db=None, model=FakeModel)
    assert isinstance(repository, MongoDBRepository)
    assert repository.db.name == "mongo_database"
    assert repository.collection.name == "fake_model"


def test_get_repository_invalid_type(mock_sql_session):
    """
    Test to verify that it raises ValueError.
    """
    with patch.dict(os.environ, {"REPOSITORY_TYPE": "invalid"}):
        with pytest.raises(ValueError, match="Unsupported repository type"):
            get_repository(db=mock_sql_session, model=FakeModel)
