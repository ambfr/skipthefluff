from fastapi import APIRouter, HTTPException, Query
from app.services.youtube import search_youtube
from app.models.video import SearchResponse

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search(
    query: str = Query(..., min_length=1, description="Search query"),
    filter: str = Query("beginner", description="Intent filter"),
    max_results: int = Query(10, ge=1, le=20),
):
    try:
        results = await search_youtube(query, max_results)
        return SearchResponse(
            query=query,
            results=results,
            total=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
