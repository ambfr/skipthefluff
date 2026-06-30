import httpx
import json
from app.config import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


async def analyze_transcript(title: str, transcript: str) -> dict:
    """
    Analyze video transcript to classify content type and assess explanation quality.
    Returns: {
        content_type: "instructional" | "commentary" | "review" | "entertainment" | "unclear",
        explanation_quality: float (0-100),
        topic_match: bool,
        reasoning: str
    }
    """
    if not transcript or not settings.groq_api_key:
        return {
            "content_type": "unclear",
            "explanation_quality": 50.0,
            "topic_match": True,
            "reasoning": "",
        }

    prompt = f"""You are analyzing a YouTube video transcript to assess educational quality.

Video title: "{title}"

Transcript excerpt:
{transcript}

Classify this video and respond ONLY as JSON with this exact structure:
{{
  "content_type": one of ["instructional", "commentary", "review", "entertainment", "unclear"],
  "explanation_quality": a number 0-100 representing how clearly concepts are taught (0 if not educational at all),
  "topic_match": true or false — does the actual content teach/cover what the title claims, or is it just discussing/reacting to the topic without teaching it,
  "reasoning": a 1-sentence explanation of your classification
}}

Important: if this is a reaction video, opinion piece, or commentary ABOUT a course/topic rather than actually teaching it, set content_type to "commentary" and topic_match to false, even if the title sounds educational.

No markdown, no extra text, just the JSON."""

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 200,
                    "temperature": 0.1,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"].strip()
            text = text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(text)

            return {
                "content_type": parsed.get("content_type", "unclear"),
                "explanation_quality": float(parsed.get("explanation_quality", 50.0)),
                "topic_match": bool(parsed.get("topic_match", True)),
                "reasoning": parsed.get("reasoning", ""),
            }

    except Exception:
        return {
            "content_type": "unclear",
            "explanation_quality": 50.0,
            "topic_match": True,
            "reasoning": "",
        }
