from sqlalchemy.orm import Session
from src.config.db import get_db
from src.transaction_items.transaction_items_model import TransactionItem
from src.transaction_items.transaction_items_schema import TransactionItemCreate, TransactionItemResponse, TransactionItemUpdate, TransactionItemDelete
from fastapi import Depends
import uuid
from uuid import UUID
from typing import List

class TransactionItemController:
    @staticmethod
    def create_transaction_item(transaction_item_data:TransactionItemCreate,db:Session = Depends(get_db))->TransactionItemResponse:
        """Create a new transaction item"""
        db_transaction_item = TransactionItem(
            transaction_item_id=uuid.uuid4(),
            name=transaction_item_data.name,
            amount=transaction_item_data.amount,
            quantity=transaction_item_data.quantity,
            transaction_id=transaction_item_data.transaction_id
        )
        db.add(db_transaction_item)
        db.commit()
        db.refresh(db_transaction_item)
        return db_transaction_item
    
    @staticmethod
    def get_transaction_items(transaction_id:UUID,db:Session = Depends(get_db))->List[TransactionItemResponse]:
        """Get all transaction items for a transaction"""
        return db.query(TransactionItem).filter(TransactionItem.transaction_id == transaction_id).all()
    
    @staticmethod
    def update_transaction_item(transaction_item_id:UUID, transaction_item_data:TransactionItemUpdate, db:Session = Depends(get_db))->TransactionItemResponse:
        """Update a transaction item"""
        db_transaction_item = db.query(TransactionItem).filter(TransactionItem.transaction_item_id == transaction_item_id).first()
        if not db_transaction_item:
            return None
        
        if transaction_item_data.name is not None:
            db_transaction_item.name = transaction_item_data.name
        if transaction_item_data.amount is not None:
            db_transaction_item.amount = transaction_item_data.amount
        if transaction_item_data.quantity is not None:
            db_transaction_item.quantity = transaction_item_data.quantity
        
        db.commit()
        db.refresh(db_transaction_item)
        return db_transaction_item
    
    @staticmethod
    def delete_transaction_item(transaction_item_id:UUID, db:Session = Depends(get_db))->bool:
        """Delete a transaction item"""
        db_transaction_item = db.query(TransactionItem).filter(TransactionItem.transaction_item_id == transaction_item_id).first()
        if not db_transaction_item:
            return False
        
        db.delete(db_transaction_item)
        db.commit()
        return True