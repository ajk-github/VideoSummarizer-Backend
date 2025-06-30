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
    + transcript +
    "\n\nGenerate concise bullet-point summaries for each section. "
    "Each bullet must start on a new line, and must follow this exact format:\n"
    "- **[MM:SS]** summary content\n\n"
    "Do not include any other symbols, styles, or formatting. Only use this bullet format: - **[MM:SS]** summary."
)


    resp = _client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    return resp.text
