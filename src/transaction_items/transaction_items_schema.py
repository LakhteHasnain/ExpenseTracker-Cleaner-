from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class TransactionItemCreate(BaseModel):
    name: str = Field(...,description="Transaction item name")
    amount: float = Field(...,description="Transaction item amount")
    quantity: int = Field(...,description="Transaction item quantity")
    transaction_id: Optional[UUID] = Field(None,description="Transaction ID")

class TransactionItemResponse(BaseModel):
    transaction_item_id: UUID = Field(...,description="Transaction item ID")
    name:str = Field(...,description="Transaction item name")
    amount:float = Field(...,description="Transaction item amount")
    quantity:int = Field(...,description="Transaction item quantity")
    transaction_id:UUID = Field(...,description="Transaction ID")

class TransactionItemUpdate(BaseModel):
    name: Optional[str] = Field(None,description="Transaction item name")
    amount: Optional[float] = Field(None,description="Transaction item amount")
    quantity: Optional[int] = Field(None,description="Transaction item quantity")

class TransactionItemDelete(BaseModel):
    transaction_item_id: UUID = Field(...,description="Transaction item ID")