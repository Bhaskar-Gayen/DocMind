from fastapi import APIRouter, Depends
from ..config import settings
from ..dependencies import verify_token
from ..utils.http import forward_request

router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(user: dict = Depends(verify_token)):
    return await forward_request(
        f"{settings.DOCUMENT_SERVICE_URL}/upload",
        method="POST",
        headers={"X-User-ID": user["id"]}
    )


@router.get("/")
async def list_documents(
    page: int = 1,
    limit: int = 10,
    user: dict = Depends(verify_token)
):
    return await forward_request(
        f"{settings.DOCUMENT_SERVICE_URL}/documents",
        params={"page": page, "limit": limit, "user_id": user["id"]}
    )
