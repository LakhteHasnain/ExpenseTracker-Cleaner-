from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class TransactionCreate(BaseModel):
    name: str = Field(...,description="Transaction name")
    amount: int = Field(...,description="Transaction amount")
    category: str = Field(...,description="Transaction category")
    user_id: Optional[UUID] = Field(None,description="User ID (set from token)")

class TransactionResponse(BaseModel):
    transaction_id: UUID = Field(...,description="Transaction ID")
    name:str = Field(...,description="Transaction name")
    amount:int = Field(...,description="Transaction amount")
    category:str = Field(...,description="Transaction category")
    user_id:UUID = Field(...,description="User ID")

class TransactionUpdate(BaseModel):
   name:Optional[str] = Field(None,description="Transaction name")
   amount:Optional[int] = Field(None,description="Transaction amount")
   category:Optional[str] = Field(None,description="Transaction category")

class TransactionDelete(BaseModel):
    transaction_id:UUID = Field(...,description="Transaction ID")