from fastapi import APIRouter, Body
from app.auth.auth_handler import verify_firebase_token

router = APIRouter()

@router.post("/login")
def login(id_token: str = Body(..., embed=True)):
    user_info = verify_firebase_token(id_token)
    return {
        "message": "Login successful",
        "user": user_info
    }
