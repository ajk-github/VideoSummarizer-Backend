from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from typing import Optional
from datetime import datetime
import traceback

from app.schemas import ProcessRequest, ProcessResponse
from app.routes.history import router as history_router
from app.routes.login import router as login_router

from app.services.downloader import download_audio
from app.services.transcriber import transcribe_with_markers
from app.services.summarizer import summarize
from app.models.user_history import get_safe_doc_id
from app.auth.auth_handler import verify_firebase_token
from app.auth import firebase
from firebase_admin import firestore, initialize_app

# ✅ Initialize Firebase only once
try:
    initialize_app()
except ValueError:
    pass

app = FastAPI(title="EduSummarize API")
app.include_router(login_router)
app.include_router(history_router)

# ✅ Extract UID from Firebase token if available
async def get_optional_uid(request: Request) -> Optional[str]:
    try:
        return await verify_firebase_token(request)
    except Exception:
        return None

# ✅ Background pipeline to download, transcribe, summarize, and update Firestore
def process_pipeline(video_url: str, uid: Optional[str]):
    try:
        print(f"DEBUG ▶ uid: {uid}")
        print(f"DEBUG ▶ video_url: {video_url}")

        db = firestore.client()
        doc_id = get_safe_doc_id(video_url)

        if uid:
            doc_ref = db.collection("users").document(uid).collection("history").document(doc_id)

            # ✅ Immediately store "processing" entry
            try:
                doc_ref.set({
                    "video_url": video_url,
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "processing"
                }, merge=True)
                print("DEBUG ▶ Initial Firestore doc created.")
            except Exception:
                print("ERROR ▶ Failed to write initial doc to Firestore:")
                print(traceback.format_exc())

        # ✅ Core processing pipeline
        audio_path = download_audio(video_url)
        print(f"DEBUG ▶ audio_path: {audio_path}")

        transcript = transcribe_with_markers(audio_path)
        print(f"DEBUG ▶ transcript (type): {type(transcript)}")

        summary = summarize(transcript)
        print(f"DEBUG ▶ summary (type): {type(summary)}")

        # ✅ Update Firestore with final results
        if uid:
            doc_ref = db.collection("users").document(uid).collection("history").document(doc_id)
            doc_ref.update({
                "transcript": transcript,
                "summary": summary,
                "status": "complete"
            })
            print("DEBUG ▶ Firestore doc updated with summary and transcript.")

    except Exception:
        print("Background processing error:")
        print(traceback.format_exc())

# ✅ Main API route to trigger background processing
@app.post("/process", response_model=ProcessResponse)
async def process_video(
    req: ProcessRequest,
    background_tasks: BackgroundTasks,
    uid: Optional[str] = Depends(get_optional_uid)
):
    url = str(req.video_url)

    # ✅ Kick off background task
    background_tasks.add_task(process_pipeline, url, uid)

    return ProcessResponse(
        transcript="Processing in background...",
        summary="Processing in background..."
    )
