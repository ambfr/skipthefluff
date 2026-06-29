import httpx
from app.config import settings

YOUTUBE_COMMENTS_URL = "https://www.googleapis.com/youtube/v3/commentThreads"


async def fetch_comments(video_id: str, max_results: int = 50) -> list[str]:
    """Fetch top comments for a video. Returns list of comment text strings."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(YOUTUBE_COMMENTS_URL, params={
                "part": "snippet",
                "videoId": video_id,
                "maxResults": max_results,
                "order": "relevance",
                "key": settings.youtube_api_key,
            })

            # Comments may be disabled — handle gracefully
            if resp.status_code == 403:
                return []

            resp.raise_for_status()
            data = resp.json()

            comments = []
            for item in data.get("items", []):
                text = (
                    item.get("snippet", {})
                    .get("topLevelComment", {})
                    .get("snippet", {})
                    .get("textDisplay", "")
                )
                if text:
                    comments.append(text[:300])  # cap length per comment

            return comments

    except Exception:
        return []
