import httpx
from app.config import settings
from app.models.video import VideoResult

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

async def search_youtube(query: str, max_results: int = 10) -> list[VideoResult]:
    async with httpx.AsyncClient() as client:
        # Step 1: search for video IDs
        search_resp = await client.get(YOUTUBE_SEARCH_URL, params={
            "part": "snippet",
            "q": query,
            "maxResults": max_results,
            "type": "video",
            "key": settings.youtube_api_key,
        })
        search_resp.raise_for_status()
        search_data = search_resp.json()

        items = search_data.get("items", [])
        if not items:
            return []

        video_ids = [item["id"]["videoId"] for item in items]

        # Step 2: fetch stats + duration for each video
        stats_resp = await client.get(YOUTUBE_VIDEOS_URL, params={
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(video_ids),
            "key": settings.youtube_api_key,
        })
        stats_resp.raise_for_status()
        stats_data = stats_resp.json()

        results = []
        for video in stats_data.get("items", []):
            snippet = video.get("snippet", {})
            stats = video.get("statistics", {})
            content = video.get("contentDetails", {})

            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = (
                thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url")
            )

            results.append(VideoResult(
                video_id=video["id"],
                title=snippet.get("title", ""),
                channel=snippet.get("channelTitle", ""),
                views=int(stats.get("viewCount", 0)) if stats.get("viewCount") else None,
                likes=int(stats.get("likeCount", 0)) if stats.get("likeCount") else None,
                published_at=snippet.get("publishedAt"),
                duration=content.get("duration"),
                thumbnail_url=thumbnail_url,
            ))

        return results
