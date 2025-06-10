import whisper
from app.config import settings

# load once at import
_whisper_model = whisper.load_model(settings.whisper_model)

def transcribe_with_markers(audio_path: str) -> str:
    """
    Uses Whisper to transcribe `audio_path` and injects [MM:00] markers
    at each new-minute boundary.
    """
    result = _whisper_model.transcribe(audio_path)
    segments = result["segments"]

    lines = []
    current_min = -1
    for seg in segments:
        minute = int(seg["start"] // 60)
        if minute != current_min:
            current_min = minute
            lines.append(f"[{current_min:02d}:00]")
        lines.append(seg["text"].strip())
    return "\n".join(lines)
