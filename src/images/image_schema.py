from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ImageUploadRequest(BaseModel):
    name: Optional[str] = Field(None, description="Optional image name")
    expiration: Optional[int] = Field(None, description="Optional expiration time in seconds (60-15552000)")
    transaction_id: Optional[UUID] = Field(None, description="Optional transaction ID")

class ImageResponse(BaseModel):
    id: UUID = Field(..., description="Image UUID")
    image_id: str = Field(..., description="ImgBB image ID")
    url: str = Field(..., description="Image URL")
    transaction_id: Optional[UUID] = Field(None, description="Transaction ID")
    
    class Config:
        from_attributes = True



