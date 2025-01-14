from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.dependencies import get_db, get_current_user
from app.services.document_service import DocumentService
from app.models.schemas import DocumentResponse

router = APIRouter(
    responses={404:{"description":"Not Found"}}
)

@router.get("/foo")
async def foo():
    return JSONResponse({"message": "inside doc route"})

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    document_service = DocumentService(db)
    document = await document_service.upload_document(file, current_user_id)
    return document

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    document_service = DocumentService(db)
    return await document_service.get_document(document_id, current_user_id)

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    document_service = DocumentService(db)
    await document_service.delete_document(document_id, current_user_id)
    return {"message": "Document deleted successfully"}