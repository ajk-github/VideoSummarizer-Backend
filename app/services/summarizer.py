from google import genai
from app.config import settings

# initialize once
_client = genai.Client(api_key=settings.gemini_api_key)

def summarize(transcript: str) -> str:
    """
    Calls Gemini to produce bullet-point summaries prefixed with each [MM:00].
    """
    prompt = (
        "You are an AI assistant. Here is a transcript annotated with minute markers:\n\n"
        + transcript
        + "\n\nGenerate concise bullet-point summaries for each section, "
          "prefixing each bullet with its timestamp (e.g. “- [00:00] …”)."
    )

    resp = _client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    return resp.text
