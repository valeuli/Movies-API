from datetime import datetime, timezone

import pytest
from bson import ObjectId
from mongomock import MongoClient
from pydantic import BaseModel

from app.repositories.mongo_repository import MongoDBRepository


class ExampleSchema(BaseModel):
    id: str
    name: str
    value: int
    created_at: datetime


class TestMongoDBRepository:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        """
        Initial configuration of MongoDB repository
        """
        client = MongoClient()
        self.db_name = "test_db"
        self.collection_name = "test_collection"
        self.repository = MongoDBRepository(self.db_name, self.collection_name, client)
        self.sample_data = {
            "name": "Test Object",
            "value": 42,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        self.document = self.repository.create_object(self.sample_data)

    def teardown_method(self):
        self.repository.collection.delete_many({})

    def test_create_object(self):
        """
        Test to verify object creation.
        """
        data = {
            "name": self.sample_data["name"],
            "value": 40,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = self.repository.create_object(data)

        assert "id" in result
        assert result["name"] == self.sample_data["name"]
        assert result["value"] == 40

    def test_get_object_correctly(self):
        """
        Test to verify object retrieval.
        """
        retrieved_object = self.repository.get_object(self.document["id"])

        assert retrieved_object is not None
        assert retrieved_object["name"] == self.sample_data["name"]

    def test_get_object_failed(self):
        """
        Test to verify object retrieval.
        """
        retrieved_object = self.repository.get_object("67844c2a7c100713fc7f89ef")

        assert retrieved_object is None

    def test_get_all_objects(self):
        """
        Test to verify all objects retrieved.
        """
        self.repository.create_object({"name": "Another Object", "value": 45})
        all_objects = self.repository.get_all_objects()

        assert len(all_objects) == 2

    def test_get_objects_by_filters(self):
        """
        Test to verify objects retrieved by filters.
        """
        self.repository.create_object({"name": "Another Object", "value": 98})
        self.repository.create_object({"name": "Another Object 2", "value": 98})
        filtered_objects = self.repository.get_objects_by_filters(
            {"value": 98}, limit=1
        )
        assert len(filtered_objects) == 1
        assert filtered_objects[0]["name"] == "Another Object"

        filtered_objects = self.repository.get_objects_by_filters({"value": 98})
        assert len(filtered_objects) == 2

    def test_update_object(self):
        """
        Test to verify object updates correctly.
        """
        updated_data = {"name": "Updated Object", "value": 84}
        updated_object = self.repository.update_object(
            self.document["id"], updated_data
        )

        assert updated_object is not None
        assert updated_object["name"] == "Updated Object"
        assert updated_object["value"] == 84

    def test_update_object_failed(self):
        """
        Test to verify object updates correctly.
        """
        updated_data = {"name": "Updated Object", "value": 84}
        updated_object = self.repository.update_object(
            "67844c2a7c100711fc7f89ef", updated_data
        )

        assert updated_object is None

    def test_delete_object(self):
        """
        Test to verify object deletion correctly.
        """
        deleted_object = self.repository.delete_object(self.document["id"])
        remaining_objects = self.repository.get_all_objects()

        assert deleted_object is not None
        assert deleted_object["name"] == self.sample_data["name"]
        assert len(remaining_objects) == 0

    def test_to_schema_single_document(self):
        """
        Test to verify single document transformation to schema.
        """
        data = {
            "_id": ObjectId(),
            "name": "Test Object",
            "value": 42,
            "created_at": datetime.now(timezone.utc),
        }

        result = self.repository.to_schema(data, ExampleSchema)

        assert result is not None
        assert result.id == str(data["id"])
        assert result.name == data["name"]
        assert result.value == data["value"]
        assert result.created_at == data["created_at"]

    def test_to_schema_list_of_documents(self):
        """
        Test to verify list of documents transformation to schema.
        """
        data_list = [
            {
                "_id": ObjectId(),
                "name": "Test Object 1",
                "value": 42,
                "created_at": datetime.now(timezone.utc),
            },
            {
                "_id": ObjectId(),
                "name": "Test Object 2",
                "value": 84,
                "created_at": datetime.now(timezone.utc),
            },
        ]

        result = self.repository.to_schema(data_list, ExampleSchema)

        assert len(result) == len(data_list)

        for idx, item in enumerate(result):
            assert item.id == str(data_list[idx]["id"])
            assert item.name == data_list[idx]["name"]
            assert item.value == data_list[idx]["value"]
            assert item.created_at == data_list[idx]["created_at"]

    def test_to_schema_empty_data(self):
        """
        Test to verify None or empty list handling in to_schema.
        """
        result = self.repository.to_schema(None, ExampleSchema)
        assert result is None
