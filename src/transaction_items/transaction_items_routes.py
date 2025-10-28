from fastapi import APIRouter, Depends, status, Header, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from src.config.db import get_db
from src.transaction_items.transaction_items_model import TransactionItem
from src.transaction_items.transaction_items_schema import TransactionItemCreate, TransactionItemResponse, TransactionItemUpdate, TransactionItemDelete
from src.transaction_items.transaction_items_controller import TransactionItemController
from src.users.core.jwt_token import verify_token



router = APIRouter(prefix="/api/v1/transaction_items", tags=["transaction_items"])

@router.post("/", response_model=TransactionItemResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction_item(transaction_item_data: TransactionItemCreate, db: Session = Depends(get_db)):
   
    return TransactionItemController.create_transaction_item(transaction_item_data, db)

@router.get("/", response_model=List[TransactionItemResponse], status_code=status.HTTP_200_OK)
async def get_transaction_items(transaction_id: UUID, db: Session = Depends(get_db)):
    return TransactionItemController.get_transaction_items(transaction_id, db)

@router.put("/{transaction_item_id}", response_model=TransactionItemResponse, status_code=status.HTTP_200_OK)
async def update_transaction_item(transaction_item_id: UUID, transaction_item_data: TransactionItemUpdate, db: Session = Depends(get_db)):
    item = TransactionItemController.update_transaction_item(transaction_item_id, transaction_item_data, db)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction item not found")
    return item

@router.delete("/{transaction_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction_item(transaction_item_id: UUID, db: Session = Depends(get_db)):
    success = TransactionItemController.delete_transaction_item(transaction_item_id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction item not found")
    return None