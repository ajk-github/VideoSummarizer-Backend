import os
import time
import requests
from app.config import settings

def upload_to_assemblyai(audio_path: str) -> str:
    headers = {'authorization': settings.assemblyai_api_key}
    with open(audio_path, 'rb') as f:
        response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, files={'file': f})
    response.raise_for_status()
    return response.json()['upload_url']

def transcribe_with_assemblyai(audio_url: str) -> list:
    endpoint = "https://api.assemblyai.com/v2/transcript"
    headers = {
        "authorization": settings.assemblyai_api_key,
        "content-type": "application/json"
    }
    payload = {"audio_url": audio_url}
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    transcript_id = response.json()['id']

    polling_url = f"{endpoint}/{transcript_id}"
    while True:
        poll = requests.get(polling_url, headers=headers)
        data = poll.json()
        if data["status"] == "completed":
            return data["words"]
        elif data["status"] == "error":
            raise Exception(f"Transcription failed: {data['error']}")
        time.sleep(3)

def transcribe_with_markers(audio_path: str) -> str:
    try:
        audio_url = upload_to_assemblyai(audio_path)
        words = transcribe_with_assemblyai(audio_url)

        lines = []
        current_min = -1
        for word in words:
            minute = int(word['start'] // 60000)  # ms to minutes
            if minute != current_min:
                current_min = minute
                lines.append(f"[{current_min:02d}:00]")
            lines.append(word['text'])
        return "\n".join(lines)
    
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
