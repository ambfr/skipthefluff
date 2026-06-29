from pydantic import BaseModel
from typing import Optional

class VideoResult(BaseModel):
    video_id: str
    title: str
    channel: str
    views: Optional[int] = None
    likes: Optional[int] = None
    published_at: Optional[str] = None
    duration: Optional[str] = None
    thumbnail_url: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: list[VideoResult]
    total: int
