from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List

T = TypeVar("T")


class CRUDService(Generic[T]):
    """
    Generic CRUD service for models.
    """

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_object(self, object_id: int) -> T:
        return self.db.query(self.model).filter(self.model.id == object_id).first()

    def get_all_objects(self) -> List[T]:
        return self.db.query(self.model).all()

    def create_object(self, object_data: dict) -> T:
        new_object = self.model(**object_data)
        self.db.add(new_object)
        self.db.commit()
        self.db.refresh(new_object)
        return new_object

    def update_object(self, object_id: int, object_data: dict) -> T | None:
        obj = self.get_object(object_id)
        if not obj:
            return None
        for key, value in object_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_object(self, object_id: int) -> T | None:
        obj = self.get_object(object_id)
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return obj
