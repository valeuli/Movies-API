import pytest
from sqlalchemy.orm import Session

from app.database_settings import SessionLocal
from app.main import app
from app.models.user import User
from app.services.crud_service import CRUDService
from app.services.user_service import UserService
from tests.testing_helper import SetupHelper


class TestCRUDService:
    """
    Unit tests for CRUDService.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db: Session):
        """
        Initial configuration for every test.
        """
        app.dependency_overrides[SessionLocal] = lambda: test_db
        self.db = test_db
        self.CRUD_service = CRUDService[User](db=self.db, model=User)
        self.user_service = UserService(db=self.db)
        self.user_email = "johnsnow@example.com"
        self.password = "securepassword"
        self.created_object = SetupHelper.create_test_user(
            self.user_service, self.user_email, self.password
        )

    def test_create_object(self):
        """
        Test to create an object.
        """
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "PaSSWORD123",
        }
        created_object = self.CRUD_service.create_object(user_data)
        assert created_object is not None
        assert created_object.first_name == "Jane"

    def test_get_object(self):
        """
        Test to get an object by id.
        """
        fetched_object = self.CRUD_service.get_object(self.created_object.id)

        assert fetched_object is not None
        assert fetched_object.id == self.created_object.id
        assert fetched_object.first_name == self.created_object.first_name

    def test_get_all_objects(self):
        """
        Test: Obtener todos los usuarios.
        """
        user2 = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@example.com",
            "password": "securepassword2",
        }
        self.CRUD_service.create_object(user2)

        users = self.CRUD_service.get_all_objects()
        actual_emails = {user.email for user in users}

        assert len(users) > 1
        assert "johnsnow@example.com" in actual_emails
        assert "janedoe@example.com" in actual_emails

    def test_update_object(self):
        """
        Test to update an object.
        """
        updated_data = {"first_name": "Maria", "last_name": "Smith"}
        updated_user = self.CRUD_service.update_object(
            self.created_object.id, updated_data
        )

        assert updated_user is not None
        assert updated_user.first_name == "Maria"
        assert updated_user.last_name == "Smith"

    def test_delete_object(self):
        """
        Test to delete an object.
        """
        user_id = self.created_object.id
        deleted_user = self.CRUD_service.delete_object(user_id)

        assert deleted_user is not None
        assert deleted_user.id == user_id
        assert self.CRUD_service.get_object(user_id) is None
