from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
import boto3
from elasticsearch import Elasticsearch
import redis

from app.models.document import Document, DocumentCreate
from app.core.config import settings
from app.services.storage_service import S3StorageService
from app.services.search_service import ElasticsearchService
from app.utils.file_processor import process_document


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.s3 = S3StorageService()
        self.es = ElasticsearchService()
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    async def upload_document(self, file: UploadFile, user_id: int) -> Document:
        try:
            # Process document using unstructured.io
            processed_content = await process_document(file)

            # Upload to S3
            s3_key = await self.s3.upload_file(file)

            # Create document record
            doc = DocumentCreate(
                filename=file.filename,
                file_type=file.content_type,
                file_size=file.size,
                user_id=user_id
            )

            db_document = Document(**doc.dict(), s3_key=s3_key)
            self.db.add(db_document)
            self.db.commit()
            self.db.refresh(db_document)

            # Index in Elasticsearch
            await self.es.index_document(db_document.id, processed_content)

            return db_document

        except Exception as e:
            # Rollback in case of failure
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def get_document(self, document_id: int, user_id: int) -> Document:
        document = self.db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user_id
        ).first()

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        return document

    async def delete_document(self, document_id: int, user_id: int):
        document = await self.get_document(document_id, user_id)

        # Delete from S3
        await self.s3.delete_file(document.s3_key)

        # Delete from Elasticsearch
        await self.es.delete_document(document_id)

        # Delete from database
        self.db.delete(document)
        self.db.commit()