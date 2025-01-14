from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    filename: str
    file_type: str
    file_size: int

class DocumentCreate(DocumentBase):
    user_id: int

class DocumentResponse(DocumentBase):
    id: int
    s3_key: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True