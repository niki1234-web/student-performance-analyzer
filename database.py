import hashlib
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import streamlit as st
from bson import ObjectId
from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

DB_NAME = os.getenv("MONGODB_DB_NAME", "student_performance_analyzer")


def _get_mongo_uri() -> str:
    """Read MongoDB URI from environment, Streamlit secrets, or fallback to local MongoDB."""
    uri = os.getenv("MONGODB_URI")
    if uri:
        return uri
    try:
        secret_uri = st.secrets.get("MONGODB_URI")
        if secret_uri:
            return secret_uri
    except Exception:
        pass
    # Local fallback so the app works without manual env configuration
    return "mongodb://localhost:27017/student_performance_analyzer"


@st.cache_resource(show_spinner=False)
def get_client() -> Optional[MongoClient]:
    uri = _get_mongo_uri()
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client
    except (PyMongoError, ServerSelectionTimeoutError):
        return None


def get_db():
    client = get_client()
    if client is None:
        return None
    return client[DB_NAME]


def is_connected() -> bool:
    return get_db() is not None


def show_connection_help():
    st.warning(
        "MongoDB is not connected. Make sure MongoDB Community Server / Service is running locally, "
        "or set the MONGODB_URI environment variable for MongoDB Atlas."
    )


def init_indexes() -> None:
    db = get_db()
    if db is None:
        return
    try:
        db.students.create_index([("username", ASCENDING)], unique=True, sparse=True)
        db.students.create_index([("name", ASCENDING)])
        db.subjects.create_index([("name", ASCENDING)], unique=True)
        db.topics.create_index([("subject", ASCENDING), ("name", ASCENDING)], unique=True)
        db.questions.create_index([("subject", ASCENDING), ("topic", ASCENDING)])
        db.quiz_attempts.create_index([("student_id", ASCENDING), ("submitted_at", ASCENDING)])
        db.answers.create_index([("student_id", ASCENDING), ("topic", ASCENDING)])
    except PyMongoError:
        pass


def serialize_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not doc:
        return doc
    out = dict(doc)
    if "_id" in out:
        out["_id"] = str(out["_id"])
    return out


def _oid(value: str) -> ObjectId:
    return ObjectId(value)


def _hash_password(password: str) -> str:
    """Password security ke liye hash function."""
    return hashlib.sha256(password.encode()).hexdigest()


# --- AUTHENTICATION & STUDENT MANAGEMENT ---

def register_student(username: str, password: str, name: str) -> Optional[str]:
    """Naya student register karta hai."""
    db = get_db()
    if db is None or not username.strip() or not password.strip() or not name.strip():
        return None
    
    clean_username = username.strip().lower()
    if db.students.find_one({"username": clean_username}):
        return None  # Username pehle se exist karta hai

    doc = {
        "username": clean_username,
        "password": _hash_password(password.strip()),
        "name": name.strip(),
        "created_at": datetime.now(timezone.utc)
    }
    result = db.students.insert_one(doc)
    return str(result.inserted_id)


def authenticate_student(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Username aur password verify karke student document return karta hai."""
    db = get_db()
    if db is None or not username.strip() or not password.strip():
        return None
    
    user = db.students.find_one({
        "username": username.strip().lower(),
        "password": _hash_password(password.strip())
    })
    return serialize_doc(user)


def create_student(name: str) -> Optional[str]:
    db = get_db()
    if db is None or not name.strip():
        return None
    doc = {"name": name.strip(), "created_at": datetime.now(timezone.utc)}
    result = db.students.insert_one(doc)
    return str(result.inserted_id)


def update_student(student_id: str, name: str) -> bool:
    db = get_db()
    if db is None:
        return False
    result = db.students.update_one({"_id": _oid(student_id)}, {"$set": {"name": name.strip()}})
    return result.modified_count > 0


def list_students() -> List[Dict[str, Any]]:
    db = get_db()
    if db is None:
        return []
    return [serialize_doc(d) for d in db.students.find().sort("name", ASCENDING)]


def get_student(student_id: str) -> Optional[Dict[str, Any]]:
    db = get_db()
    if db is None or not student_id:
        return None
    return serialize_doc(db.students.find_one({"_id": _oid(student_id)}))


# --- SUBJECTS & TOPICS ---

def upsert_subject(name: str) -> None:
    db = get_db()
    if db is None:
        return
    db.subjects.update_one({"name": name}, {"$setOnInsert": {"name": name}}, upsert=True)


def list_subjects() -> List[str]:
    db = get_db()
    if db is None:
        return []
    return [d["name"] for d in db.subjects.find().sort("name", ASCENDING)]


def upsert_topic(subject: str, name: str) -> None:
    db = get_db()
    if db is None:
        return
    db.topics.update_one(
        {"subject": subject, "name": name},
        {"$set": {"subject": subject, "name": name}},
        upsert=True,
    )


def list_topics(subject: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_db()
    if db is None:
        return []
    query = {"subject": subject} if subject else {}
    return [serialize_doc(d) for d in db.topics.find(query).sort([("subject", ASCENDING), ("name", ASCENDING)])]


def update_topic(topic_id: str, subject: str, name: str) -> bool:
    db = get_db()
    if db is None:
        return False
    result = db.topics.update_one({"_id": _oid(topic_id)}, {"$set": {"subject": subject, "name": name}})
    return result.modified_count > 0


# --- QUESTIONS & QUIZZES ---

def insert_question(question: Dict[str, Any]) -> Optional[str]:
    db = get_db()
    if db is None:
        return None
    question["created_at"] = datetime.now(timezone.utc)
    result = db.questions.insert_one(question)
    return str(result.inserted_id)


def update_question(question_id: str, data: Dict[str, Any]) -> bool:
    db = get_db()
    if db is None:
        return False
    result = db.questions.update_one({"_id": _oid(question_id)}, {"$set": data})
    return result.modified_count > 0


def list_questions(subject: Optional[str] = None, topic: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_db()
    if db is None:
        return []
    query: Dict[str, Any] = {}
    if subject:
        query["subject"] = subject
    if topic:
        query["topic"] = topic
    return [serialize_doc(d) for d in db.questions.find(query).sort([("subject", ASCENDING), ("topic", ASCENDING)])]


def save_quiz_attempt(student_id: str, subject: str, topic: str, answer_rows: List[Dict[str, Any]]) -> Optional[str]:
    db = get_db()
    if db is None:
        return None

    total = len(answer_rows)
    correct = sum(1 for row in answer_rows if row["is_correct"])
    incorrect = total - correct
    percentage = round((correct / total) * 100, 2) if total else 0
    now = datetime.now(timezone.utc)

    attempt = {
        "student_id": student_id,
        "subject": subject,
        "topic": topic,
        "submitted_at": now,
        "total_questions": total,
        "correct_answers": correct,
        "incorrect_answers": incorrect,
        "score": f"{correct}/{total}",
        "percentage": percentage,
    }
    attempt_id = db.quiz_attempts.insert_one(attempt).inserted_id

    enriched_answers = []
    for row in answer_rows:
        enriched = dict(row)
        enriched.update(
            {
                "attempt_id": str(attempt_id),
                "student_id": student_id,
                "subject": subject,
                "topic": topic,
                "submitted_at": now,
            }
        )
        enriched_answers.append(enriched)

    if enriched_answers:
        db.answers.insert_many(enriched_answers)
    return str(attempt_id)


def get_attempts(student_id: str) -> List[Dict[str, Any]]:
    db = get_db()
    if db is None or not student_id:
        return []
    return [serialize_doc(d) for d in db.quiz_attempts.find({"student_id": student_id}).sort("submitted_at", -1)]


def get_answers(student_id: str, attempt_id: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_db()
    if db is None or not student_id:
        return []
    query: Dict[str, Any] = {"student_id": student_id}
    if attempt_id:
        query["attempt_id"] = attempt_id
    return [serialize_doc(d) for d in db.answers.find(query).sort("submitted_at", -1)]