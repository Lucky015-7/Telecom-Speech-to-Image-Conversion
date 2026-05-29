import sys
from pymongo import MongoClient, DESCENDING
from backend.config import MONGO_URI, MONGO_DB_NAME

# Try to connect to real MongoDB with a fast 2-second timeout
try:
    print(f"Connecting to MongoDB at {MONGO_URI}...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    # Trigger a quick connection test
    client.admin.command("ping")
    db = client[MONGO_DB_NAME]
    using_mock = False
    print("Successfully connected to real MongoDB instance.")
except Exception as e:
    print("Real MongoDB connection failed. Falling back to in-memory mongomock...")
    try:
        import mongomock
        client = mongomock.MongoClient()
        db = client[MONGO_DB_NAME]
        using_mock = True
        print("Using mongomock in-memory database successfully.")
    except ImportError:
        print("mongomock not installed! Database operations will fail.")
        client = None
        db = None
        using_mock = False

if db is not None:
    generations_collection = db["generations"]
    error_logs_collection = db["error_logs"]
else:
    generations_collection = None
    error_logs_collection = None


def check_database_connection() -> bool:
    if using_mock:
        return True
    if client is None:
        return False
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
    if generations_collection is None or error_logs_collection is None:
        return
    try:
        generations_collection.create_index([("created_at", DESCENDING)])
        generations_collection.create_index("category")
        generations_collection.create_index("status")
        error_logs_collection.create_index([("created_at", DESCENDING)])
    except Exception as error:
        print("Could not create MongoDB indexes:", error)
