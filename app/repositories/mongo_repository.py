from datetime import datetime, timezone
from bson import ObjectId
from typing import List, Dict, Any, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from app.repositories.base_repository import BaseRepository
from app.utils.enum_utils import serialize_enums


class MongoDBRepository(BaseRepository[Dict]):
    def __init__(self, db_name: str, collection_name: str, client: MongoClient):
        """
        Initializes a synchronous MongoDB repository.
        """
        self.db = client[db_name]
        self.collection: Collection = self.db[collection_name]

    def get_object(self, object_id: str) -> Optional[Dict]:
        """
        Get an object by id.
        """
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_all_objects(self) -> List[Dict]:
        """
        Return all objects in the collection.
        """
        return list(self.collection.find())

    def get_objects_by_filters(
        self, filters: Dict[str, Any], offset: int = 0, limit: int = None
    ) -> List[Dict]:
        """
        Retrieves objects that match the given filters with optional pagination.
        """
        query = self.collection.find(filters).skip(offset)
        if limit:
            query = query.limit(limit)
        return list(query)

    def create_object(self, object_data: Dict) -> Dict:
        """
        Creates a new object with the given data.
        """
        serialized_object = serialize_enums(object_data)
        if "created_at" not in object_data:
            serialized_object["created_at"] = datetime.now(timezone.utc)
            serialized_object["updated_at"] = datetime.now(timezone.utc)

        result = self.collection.insert_one(serialized_object)
        serialized_object["id"] = str(result.inserted_id)
        return serialized_object

    def update_object(self, object_id: str, object_data: Dict) -> Optional[Dict]:
        """
        Updates an object with the given id.
        """
        self.collection.update_one({"_id": ObjectId(object_id)}, {"$set": object_data})
        return self.get_object(object_id)

    def delete_object(self, object_id: str) -> Optional[Dict]:
        """
        Deletes an object with the given id.
        """
        return self.collection.find_one_and_delete({"_id": ObjectId(object_id)})

    @staticmethod
    def to_schema(data, schema):
        """
        Transform doc to schema.
        """
        if not data:
            return None

        if isinstance(data, list):
            result = []
            for doc in data:
                if "_id" in doc:
                    doc["id"] = str(doc.pop("_id"))
                result.append(schema(**doc))
            return result

        elif "_id" in data:
            data["id"] = str(data.pop("_id"))

        return schema(**data)
