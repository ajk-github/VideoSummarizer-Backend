from firebase_admin import auth as firebase_auth
from fastapi import Request, HTTPException

async def verify_firebase_token(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    id_token = auth_header.split(" ")[1]
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
