import os
from datetime import datetime
from uuid import uuid4

from bson import ObjectId
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.config import (
    INPUT_DIR,
    OUTPUT_DIR,
    ALLOWED_AUDIO_EXTENSIONS,
    MAX_AUDIO_FILE_SIZE_BYTES
)
from backend.database import (
    check_database_connection,
    create_indexes,
    generations_collection,
    error_logs_collection
)
from backend.models import FeedbackRequest
from backend.utils import execute_generative_synthesis


app = FastAPI(
    title="SLT Mobitel Voice-to-Image Generation Service Architecture",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    create_indexes()
    print("Backend started.")
    print("MongoDB connected:", check_database_connection())


def serialize_mongo_document(document: dict) -> dict:
    """
    Converts MongoDB ObjectId and datetime values into JSON-safe values.
    """
    document["_id"] = str(document["_id"])

    if "created_at" in document and isinstance(document["created_at"], datetime):
        document["created_at"] = document["created_at"].isoformat()

    if "updated_at" in document and isinstance(document["updated_at"], datetime):
        document["updated_at"] = document["updated_at"].isoformat()

    if document.get("feedback") and isinstance(document["feedback"].get("created_at"), datetime):
        document["feedback"]["created_at"] = document["feedback"]["created_at"].isoformat()

    return document


def validate_audio_file(file: UploadFile):
    """
    Validates uploaded audio file extension.
    """
    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format. Allowed formats: {list(ALLOWED_AUDIO_EXTENSIONS)}"
        )


async def save_uploaded_audio(file: UploadFile) -> str:
    """
    Saves uploaded audio safely into data/inputs folder.
    Also checks file size.
    """
    validate_audio_file(file)

    original_extension = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid4().hex}{original_extension}"
    staged_audio_path = os.path.join(INPUT_DIR, unique_filename)

    total_size = 0

    with open(staged_audio_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)

            if not chunk:
                break

            total_size += len(chunk)

            if total_size > MAX_AUDIO_FILE_SIZE_BYTES:
                buffer.close()

                if os.path.exists(staged_audio_path):
                    os.remove(staged_audio_path)

                raise HTTPException(
                    status_code=413,
                    detail="Audio file is too large."
                )

            buffer.write(chunk)

    return staged_audio_path


def log_error(error_message: str, original_filename: str | None = None):
    """
    Saves backend errors into MongoDB for debugging.
    """
    error_logs_collection.insert_one({
        "original_filename": original_filename,
        "error_message": error_message,
        "created_at": datetime.utcnow()
    })


@app.get("/")
def root():
    return {
        "message": "SLT Mobitel Voice-to-Image Backend is running",
        "database_connected": check_database_connection()
    }


@app.post("/api/v1/process-audio")
async def process_audio_endpoint(file: UploadFile = File(...)):
    """
    Receives audio file, runs AI generation pipeline,
    saves result metadata to MongoDB, and returns the result.
    """
    staged_audio_path = None
    result_id = None

    try:
        staged_audio_path = await save_uploaded_audio(file)

        generation_doc = {
            "original_filename": file.filename,
            "stored_audio_path": staged_audio_path,
            "output_image_path": None,
            "transcript": None,
            "metrics": {},
            "category": None,
            "prompt": None,
            "status": "processing",
            "feedback": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        inserted_result = generations_collection.insert_one(generation_doc)
        result_id = inserted_result.inserted_id

        transcript, metrics, category, prompt, image_object = execute_generative_synthesis(
            staged_audio_path
        )

        output_filename = f"prod_{result_id}.png"
        staged_image_path = os.path.join(OUTPUT_DIR, output_filename)
        image_object.save(staged_image_path)

        generations_collection.update_one(
            {"_id": result_id},
            {
                "$set": {
                    "transcript": transcript,
                    "metrics": metrics,
                    "category": category,
                    "prompt": prompt,
                    "output_image_path": staged_image_path,
                    "status": "completed",
                    "updated_at": datetime.utcnow()
                }
            }
        )

        updated_doc = generations_collection.find_one({"_id": result_id})

        return {
            "status": "success",
            "message": "Audio processed and image generated successfully.",
            "result": serialize_mongo_document(updated_doc)
        }

    except HTTPException:
        raise

    except Exception as error:
        error_message = str(error)

        log_error(
            error_message=error_message,
            original_filename=file.filename if file else None
        )

        if result_id:
            generations_collection.update_one(
                {"_id": result_id},
                {
                    "$set": {
                        "status": "failed",
                        "error_message": error_message,
                        "updated_at": datetime.utcnow()
                    }
                }
            )

        raise HTTPException(status_code=500, detail=error_message)


@app.get("/api/v1/results")
def get_all_results(limit: int = 20):
    """
    Returns generated result history.
    """
    limit = min(limit, 100)

    results = list(
        generations_collection
        .find()
        .sort("created_at", -1)
        .limit(limit)
    )

    return {
        "count": len(results),
        "results": [serialize_mongo_document(doc) for doc in results]
    }


@app.get("/api/v1/results/{result_id}")
def get_result_by_id(result_id: str):
    """
    Returns one generated result by MongoDB ID.
    """
    if not ObjectId.is_valid(result_id):
        raise HTTPException(status_code=400, detail="Invalid result ID.")

    result = generations_collection.find_one({"_id": ObjectId(result_id)})

    if not result:
        raise HTTPException(status_code=404, detail="Result not found.")

    return serialize_mongo_document(result)


@app.delete("/api/v1/results/{result_id}")
def delete_result(result_id: str):
    """
    Deletes one result from MongoDB and removes related files.
    """
    if not ObjectId.is_valid(result_id):
        raise HTTPException(status_code=400, detail="Invalid result ID.")

    result = generations_collection.find_one({"_id": ObjectId(result_id)})

    if not result:
        raise HTTPException(status_code=404, detail="Result not found.")

    stored_audio_path = result.get("stored_audio_path")
    output_image_path = result.get("output_image_path")

    for path in [stored_audio_path, output_image_path]:
        if path and os.path.exists(path):
            os.remove(path)

    generations_collection.delete_one({"_id": ObjectId(result_id)})

    return {
        "status": "success",
        "message": "Result deleted successfully."
    }


@app.post("/api/v1/results/{result_id}/feedback")
def add_feedback(result_id: str, feedback: FeedbackRequest):
    """
    Adds user feedback/rating for a generated image result.
    """
    if not ObjectId.is_valid(result_id):
        raise HTTPException(status_code=400, detail="Invalid result ID.")

    feedback_doc = {
        "rating": feedback.rating,
        "comment": feedback.comment,
        "created_at": datetime.utcnow()
    }

    update_result = generations_collection.update_one(
        {"_id": ObjectId(result_id)},
        {
            "$set": {
                "feedback": feedback_doc,
                "updated_at": datetime.utcnow()
            }
        }
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Result not found.")

    return {
        "status": "success",
        "message": "Feedback saved successfully.",
        "feedback": {
            "rating": feedback.rating,
            "comment": feedback.comment
        }
    }


@app.get("/api/v1/analytics/categories")
def get_category_analytics():
    """
    Returns count of generated results grouped by telecom category.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    analytics = list(generations_collection.aggregate(pipeline))

    return {
        "status": "success",
        "analytics": [
            {
                "category": item["_id"] or "unknown",
                "count": item["count"]
            }
            for item in analytics
        ]
    }


@app.get("/api/v1/analytics/status")
def get_status_analytics():
    """
    Returns count of generated results grouped by processing status.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    analytics = list(generations_collection.aggregate(pipeline))

    return {
        "status": "success",
        "analytics": [
            {
                "status": item["_id"] or "unknown",
                "count": item["count"]
            }
            for item in analytics
        ]
    }


@app.get("/api/v1/fetch-image/{result_id}")
def fetch_image_by_result_id(result_id: str):
    """
    Safely retrieves generated image by result ID.
    This is safer than accepting a full file path from the user.
    """
    if not ObjectId.is_valid(result_id):
        raise HTTPException(status_code=400, detail="Invalid result ID.")

    result = generations_collection.find_one({"_id": ObjectId(result_id)})

    if not result:
        raise HTTPException(status_code=404, detail="Result not found.")

    image_path = result.get("output_image_path")

    if not image_path or not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Generated image not found.")

    return FileResponse(image_path, media_type="image/png")


@app.get("/api/v1/errors")
def get_error_logs(limit: int = 20):
    """
    Returns latest backend errors.
    Useful during development.
    """
    limit = min(limit, 100)

    errors = list(
        error_logs_collection
        .find()
        .sort("created_at", -1)
        .limit(limit)
    )

    return {
        "count": len(errors),
        "errors": [serialize_mongo_document(error) for error in errors]
    }