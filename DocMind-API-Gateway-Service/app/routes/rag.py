from fastapi import APIRouter, Depends
from ..config import settings
from ..dependencies import verify_token
from ..utils.http import forward_request

router = APIRouter(prefix=f"{settings.API_V1_PREFIX}/rag", tags=["rag"])


@router.post("/query")
async def query_documents(query: dict, user: dict = Depends(verify_token)):
    return await forward_request(
        f"{settings.RAG_SERVICE_URL}/query",
        method="POST",
        json={"query": query, "user_id": user["id"]}
    )
