from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    # whisper_model: str = "base"
    assemblyai_api_key: str
    download_dir: str = "downloads"
    audio_format: str = "mp3"
    google_credentials_b64: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
