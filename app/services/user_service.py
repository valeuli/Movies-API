from typing import Type

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import User as UserSchema
from app.repositories.get_repository import get_repository


class UserService:
    def __init__(self, db: Session):
        self.repository = get_repository(db, User)

    def get_user_by_email(self, user_email: str) -> Type[User] | None:
        """
        Retrieves a user given an email.
        """
        user = self.repository.get_objects_by_filters({"email": user_email}, limit=1)
        if not user:
            return None

        user_schema = self.repository.to_schema(user, UserSchema)
        return user_schema[0]
