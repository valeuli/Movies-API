from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Dict, Any, Optional

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    def get_object(self, object_id: Any) -> Optional[T]:
        """
        Retrieve a single object by its ID.
        """
        pass

    @abstractmethod
    def get_all_objects(self) -> List[T]:
        """
        Retrieve all objects.
        """
        pass

    @abstractmethod
    def get_objects_by_filters(self, filters: Dict[str, Any]) -> List[T]:
        """
        Retrieve objects that match specific filters.
        """
        pass

    @abstractmethod
    def create_object(self, object_data: dict) -> T:
        """
        Create a new object with the given data.
        """
        pass

    @abstractmethod
    def update_object(self, object_id: Any, object_data: dict) -> Optional[T]:
        """
        Update an existing object by its ID with new data.
        """
        pass

    @abstractmethod
    def delete_object(self, object_id: Any) -> Optional[T]:
        """
        Delete an object by its ID.
        """
        pass

    @staticmethod
    def to_schema(data: Any, schema: Any) -> Any:
        """
        Default behavior: Return data as is. Override if needed.
        """
        return data
