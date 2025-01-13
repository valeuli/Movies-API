import os

from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# SQLalchemy
engine = create_engine(os.environ.get("SQL_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB
MONGO_URI = os.getenv("MONGO_DATABASE_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "mongo_database")
mongo_client = MongoClient(f"{MONGO_URI}/{MONGO_DB_NAME}")
