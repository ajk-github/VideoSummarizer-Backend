from pydantic import BaseModel, HttpUrl

class ProcessRequest(BaseModel):
    video_url: HttpUrl

class ProcessResponse(BaseModel):
    transcript: str
    summary: str

class LoginRequest(BaseModel):
    id_token: str