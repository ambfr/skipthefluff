from fastapi import APIRouter, HTTPException, Query
from app.services.youtube import search_youtube
from app.services.scoring import rank_and_categorize
from app.services.groq import get_ai_summary
from app.models.video import RankResponse, RankedVideo

router = APIRouter()

@router.get("/rank", response_model=RankResponse)
async def rank(
    query: str = Query(..., min_length=1),
    intent: str = Query("beginner"),
    max_results: int = Query(10, ge=1, le=20),
):
    try:
        # 1. Fetch raw YouTube results
        videos = await search_youtube(query, max_results)
        if not videos:
            return RankResponse(query=query, intent=intent, results=[], total=0, top_score=0)

        # 2. Score and rank
        ranked = rank_and_categorize(videos, intent)

        # 3. Build response (AI summary only for top 4 to save quota)
        results = []
        for i, item in enumerate(ranked):
            video = item["video"]
            score = item["score"]
            label = item["label"]
            rank = item["rank"]

            ai_summary = ""
            ai_tag = ""
            if i < 4 and score > 0:
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
                rank=rank,
                ai_summary=ai_summary,
                ai_tag=ai_tag,
            ))

        top_score = results[0].score if results else 0

        return RankResponse(
            query=query,
            intent=intent,
            results=results,
            total=len(results),
            top_score=top_score,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
