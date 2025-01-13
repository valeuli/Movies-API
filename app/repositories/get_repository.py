import os

from sqlalchemy.orm import Session

from app.database_settings import mongo_client, MONGO_DB_NAME
from app.repositories.mongo_repository import MongoDBRepository
from app.repositories.sql_repository import SQLRepository


def get_repository(db: Session, model: object) -> object:
    db_type = os.getenv("REPOSITORY_TYPE", "sqlite")

    if db_type == "sqlite":
        return SQLRepository(db=db, model=model)
    elif db_type == "mongodb":
        collection_name = model.__tablename__
        return MongoDBRepository(
            db_name=MONGO_DB_NAME, collection_name=collection_name, client=mongo_client
        )
    else:
        raise ValueError(f"Unsupported repository type")
