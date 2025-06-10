from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.user_history import get_user_history, get_video_summary_by_id
from app.auth.auth_handler import verify_firebase_token

router = APIRouter()

@router.get("/history")
def fetch_history(uid: str = Depends(verify_firebase_token)):
    return get_user_history(uid)

@router.get("/history/detail")
def fetch_summary_detail(
    video_url: str = Query(..., alias="video_url"),
    uid: str = Depends(verify_firebase_token)
):
    summary = get_video_summary_by_id(uid, video_url)
    if summary:
        return summary
    raise HTTPException(status_code=404, detail="Summary not found")