from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

class TransactionItemCreateInline(BaseModel):
    name: str = Field(...,description="Transaction item name")
    amount: float = Field(...,description="Transaction item amount")
    quantity: int = Field(...,description="Transaction item quantity")

class TransactionCreate(BaseModel):
    name: str = Field(...,description="Transaction name")
    amount: int = Field(...,description="Transaction amount")
    category: str = Field(...,description="Transaction category")
    user_id: Optional[UUID] = Field(None,description="User ID (set from token)")
    items: Optional[List[TransactionItemCreateInline]] = Field(default_factory=list, description="Transaction items")

class TransactionResponse(BaseModel):
    transaction_id: UUID = Field(...,description="Transaction ID")
    name:str = Field(...,description="Transaction name")
    amount:int = Field(...,description="Transaction amount")
    category:str = Field(...,description="Transaction category")
    user_id:UUID = Field(...,description="User ID")
    items: List['TransactionItemResponse'] = Field(default_factory=list, description="Transaction items")
    images: List['ImageResponse'] = Field(default_factory=list, description="Transaction images")

class TransactionUpdate(BaseModel):
   name:Optional[str] = Field(None,description="Transaction name")
   amount:Optional[int] = Field(None,description="Transaction amount")
   category:Optional[str] = Field(None,description="Transaction category")

class TransactionDelete(BaseModel):
    transaction_id:UUID = Field(...,description="Transaction ID")

from src.transaction_items.transaction_items_schema import TransactionItemResponse
from src.images.image_schema import ImageResponse
TransactionResponse.model_rebuild()