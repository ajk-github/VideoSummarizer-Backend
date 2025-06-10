from app.auth.firebase import db
from datetime import datetime
import hashlib

def get_safe_doc_id(video_url: str) -> str:
    # Firebase doesn't allow slashes or some characters in doc IDs
    return hashlib.sha256(video_url.encode()).hexdigest()

def save_video_history(uid: str, url: str, transcript: str, summary: str):
    doc_id = get_safe_doc_id(url)  # use hashed video_url as doc ID
    ref = db.collection("users").document(uid).collection("history").document(doc_id)
    ref.set({
        "video_url": url,
        "transcript": transcript,
        "summary": summary,
        "timestamp": datetime.utcnow()
    })

def get_user_history(uid: str):
    ref = db.collection("users").document(uid).collection("history").order_by("timestamp", direction="DESCENDING")
    docs = ref.stream()
    return [{doc.id: doc.to_dict()} for doc in docs]

def get_video_summary_by_id(uid: str, video_url: str):
    doc_id = get_safe_doc_id(video_url)
    doc_ref = db.collection("users").document(uid).collection("history").document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None
