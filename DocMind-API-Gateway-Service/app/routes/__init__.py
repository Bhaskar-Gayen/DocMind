from fastapi import APIRouter
from app.routes.auth import  router as auth_router
from .documents import router as documents_router
from .rag import router as rag_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(documents_router)
router.include_router(rag_router)
