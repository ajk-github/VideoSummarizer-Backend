from fastapi import FastAPI, HTTPException, Depends, Request
from typing import Optional

from app.schemas import ProcessRequest, ProcessResponse
from app.routes.history import router as history_router
from app.routes.login import router as login_router

from app.services.downloader import download_audio
from app.services.transcriber import transcribe_with_markers
from app.services.summarizer import summarize
from app.models.user_history import save_video_history
from app.auth.auth_handler import verify_firebase_token

from app.auth import firebase 
import traceback

app = FastAPI(title="EduSummarize API")

app.include_router(login_router)
app.include_router(history_router)


# ✅ Optional token logic wrapper
async def get_optional_uid(request: Request) -> Optional[str]:
    try:
        return await verify_firebase_token(request)
    except Exception:
        return None


@app.post("/process", response_model=ProcessResponse)
async def process_video(req: ProcessRequest, uid: Optional[str] = Depends(get_optional_uid)):
    try:
        print("DEBUG ▶ uid:", uid)
        
        url = str(req.video_url)
        print("DEBUG ▶ video_url:", url)

        audio_path = download_audio(url)
        print("DEBUG ▶ audio_path:", audio_path)

        transcript = transcribe_with_markers(audio_path)
        print("DEBUG ▶ transcript (type):", type(transcript))

        summary = summarize(transcript)
        print("DEBUG ▶ summary (type):", type(summary))

        # ✅ Save only if user is logged in
        if uid:
            save_video_history(uid, url, transcript, summary)

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

    return ProcessResponse(transcript=transcript, summary=summary)
