from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


def fetch_transcript(video_id: str, max_chars: int = 4000) -> str:
    """
    Fetch a video's transcript and return as a single text block,
    capped to max_chars to control Groq token usage.
    Returns empty string if no transcript is available.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join(entry["text"] for entry in transcript_list)
        return full_text[:max_chars]
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return ""
    except Exception:
        return ""
