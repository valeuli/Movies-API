from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List, Dict, Any

T = TypeVar("T")


class CRUDService(Generic[T]):
    """
    Generic CRUD service for models.
    """

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_object(self, object_id: int) -> T:
        """
        Get an object by id.
        """
        return self.db.query(self.model).filter(self.model.id == object_id).first()

    def get_all_objects(self) -> List[T]:
        """
        Return all objects of a table in the database.
        """
        return self.db.query(self.model).all()

    def get_objects_by_filters(
        self, filters: Dict[str, Any], offset: int = 0, limit: int = None
    ) -> List[T]:
        """
        Retrieves objects that match the given filters with optional pagination.
        """
        query = self.db.query(self.model)
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        return query.all()

    def create_object(self, object_data: dict) -> T:
        """
        Creates a new object with the given data.
        """
        new_object = self.model(**object_data)
        self.db.add(new_object)
        self.db.commit()
        self.db.refresh(new_object)
        return new_object

    def update_object(self, object_id: int, object_data: dict) -> T | None:
        """
        Updates an object with the given id.
        """
        obj = self.get_object(object_id)
        if not obj:
            return None
        for key, value in object_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_object(self, object_id: int) -> T | None:
        """
        Deletes an object with the given id.
        """
        obj = self.get_object(object_id)
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return obj
