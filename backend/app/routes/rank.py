from fastapi import APIRouter, HTTPException, Query
from app.services.youtube import search_youtube
from app.services.scoring import rank_and_categorize, compute_score_with_sentiment
from app.services.groq import get_ai_summary
from app.services.comments import fetch_comments
from app.services.sentiment import analyze_sentiment
from app.models.video import RankResponse, RankedVideo

router = APIRouter()

@router.get("/rank", response_model=RankResponse)
async def rank(
    query: str = Query(..., min_length=1),
    intent: str = Query("beginner"),
    max_results: int = Query(8, ge=1, le=15),
):
    try:
        # 1. Fetch raw YouTube results
        videos = await search_youtube(query, max_results)
        if not videos:
            return RankResponse(query=query, intent=intent, results=[], total=0, top_score=0, total_comments_read=0)

        # 2. For top 6 videos, fetch comments and run sentiment
        # (limit to 6 to manage YouTube API quota)
        sentiment_data = {}
        total_comments_read = 0

        for video in videos[:6]:
            comments = await fetch_comments(video.video_id, max_results=40)
            total_comments_read += len(comments)
            if comments:
                sentiment = await analyze_sentiment(comments)
            else:
                sentiment = {"positive": [], "negative": [], "sentiment_score": 50.0}
            sentiment_data[video.video_id] = {
                "sentiment": sentiment,
                "comments_count": len(comments),
            }

        # 3. Score with sentiment blended in, then rank
        scored = []
        for video in videos:
            s = sentiment_data.get(video.video_id, {})
            sentiment_score = s.get("sentiment", {}).get("sentiment_score", 50.0)
            score = compute_score_with_sentiment(video, intent, sentiment_score)
            scored.append((video, score, s))

        scored.sort(key=lambda x: x[1], reverse=True)

        # 4. Assign labels and get AI summaries for top 4
        LABELS = ["Best overall", "Quick learning", "Best for beginners", "Most detailed"]
        results = []

        for i, (video, score, s) in enumerate(scored):
            label = LABELS[i] if i < len(LABELS) else None
            sentiment = s.get("sentiment", {})

            ai_summary = ""
            ai_tag = ""
            if i < 4:
                ai_data = await get_ai_summary(
                    title=video.title,
                    channel=video.channel,
                    views=video.views or 0,
                    score=score,
                )
                ai_summary = ai_data.get("summary", "")
                ai_tag = ai_data.get("tag", "")

            results.append(RankedVideo(
                video_id=video.video_id,
                title=video.title,
                channel=video.channel,
                views=video.views,
                likes=video.likes,
                published_at=video.published_at,
                duration=video.duration,
                thumbnail_url=video.thumbnail_url,
                score=score,
                label=label,
                rank=i,
                ai_summary=ai_summary,
                ai_tag=ai_tag,
                positive_signals=sentiment.get("positive", []),
                negative_signals=sentiment.get("negative", []),
                sentiment_score=sentiment.get("sentiment_score"),
                comments_read=s.get("comments_count", 0),
            ))

        top_score = results[0].score if results else 0

        return RankResponse(
            query=query,
            intent=intent,
            results=results,
            total=len(results),
            top_score=top_score,
            total_comments_read=total_comments_read,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
