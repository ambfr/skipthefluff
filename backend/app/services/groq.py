import httpx
from app.config import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


async def get_ai_summary(title: str, channel: str, views: int, score: float) -> dict:
    """Get a short AI summary and category reasoning for a video."""
    if not settings.groq_api_key:
        return {"summary": "", "reasoning": ""}

    prompt = f"""You are analyzing a YouTube video for a smart video discovery app.

Video: "{title}"
Channel: {channel}
Views: {views:,}
Quality Score: {score}/100

Write a 1-2 sentence summary of what this video likely covers and why it ranked well.
Then give a 3-5 word tag that describes its strength (e.g. "Clear step-by-step teaching", "Concise and dense", "Deep technical dive").

Respond ONLY as JSON with keys: "summary" and "tag". No markdown, no extra text."""

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150,
                    "temperature": 0.4,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"].strip()

            import json
            parsed = json.loads(text)
            return parsed
    except Exception:
        return {"summary": "", "tag": ""}
