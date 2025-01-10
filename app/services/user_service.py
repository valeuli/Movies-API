from typing import Type

from sqlalchemy.orm import Session

from app.models.user import User
from app.services.crud_service import CRUDService


class UserService(CRUDService[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_user_by_email(self, user_email: str) -> Type[User] | None:
        """
        Retrieves a user given an email.
        """
        return self.db.query(User).filter_by(email=user_email).first()
