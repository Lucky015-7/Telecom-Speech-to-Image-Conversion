from pymongo import MongoClient, DESCENDING
from backend.config import MONGO_URI, MONGO_DB_NAME

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

generations_collection = db["generations"]
error_logs_collection = db["error_logs"]


def check_database_connection() -> bool:
    try:
        client.admin.command("ping")
        return True
    except Exception as error:
        print("MongoDB connection failed:", error)
        return False


def create_indexes():
    """
    Create indexes to improve query performance.
    This is useful when result history grows.
    """
    generations_collection.create_index([("created_at", DESCENDING)])
    generations_collection.create_index("category")
    generations_collection.create_index("status")
    error_logs_collection.create_index([("created_at", DESCENDING)])