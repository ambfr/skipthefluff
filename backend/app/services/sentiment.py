import httpx
import json
from app.config import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

POSITIVE_SIGNALS = [
    "Clear explanation",
    "Great examples",
    "Easy to understand",
    "Best video on this topic",
    "Very helpful",
    "Well structured",
    "Concise",
    "Beginner friendly",
]

NEGATIVE_SIGNALS = [
    "Outdated content",
    "Poor audio quality",
    "Misleading title",
    "Too slow",
    "Too much padding",
    "Hard to follow",
    "Too basic",
]


async def analyze_sentiment(comments: list[str]) -> dict:
    """
    Send comments to Groq and extract positive/negative quality signals.
    Returns: { positive: [...], negative: [...], sentiment_score: float }
    """
    if not comments or not settings.groq_api_key:
        return {"positive": [], "negative": [], "sentiment_score": 50.0}

    # Join top 30 comments to stay within token limits
    comment_block = "\n".join(f"- {c}" for c in comments[:30])

    prompt = f"""You are analyzing YouTube comments to assess video quality.

Here are comments from a YouTube video:
{comment_block}

Based on these comments, identify quality signals.

Positive signals to detect (only include if clearly supported by comments):
{", ".join(POSITIVE_SIGNALS)}

Negative signals to detect (only include if clearly supported by comments):
{", ".join(NEGATIVE_SIGNALS)}

Also give a sentiment_score from 0-100 (100 = overwhelmingly positive comments).

Respond ONLY as JSON with this exact structure, no markdown, no extra text:
{{
  "positive": ["signal1", "signal2"],
  "negative": ["signal1"],
  "sentiment_score": 75.0
}}"""

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
                    "temperature": 0.2,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"].strip()

            # Strip markdown fences if present
            text = text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(text)

            return {
                "positive": parsed.get("positive", [])[:4],
                "negative": parsed.get("negative", [])[:3],
                "sentiment_score": float(parsed.get("sentiment_score", 50.0)),
            }

    except Exception:
        return {"positive": [], "negative": [], "sentiment_score": 50.0}
