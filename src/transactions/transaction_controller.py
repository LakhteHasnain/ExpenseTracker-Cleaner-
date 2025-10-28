from sqlalchemy.orm import Session
from src.config.db import get_db
from src.transactions.transaction_model import Transaction
from src.transaction_items.transaction_items_model import TransactionItem
from src.transactions.transaction_schema import TransactionCreate, TransactionResponse
from fastapi import Depends
import uuid
from uuid import UUID
from typing import List

class TransactionController:
    @staticmethod
    def create_transaction(transaction_data:TransactionCreate,db:Session  = Depends(get_db))->TransactionResponse:
        """Create a new transaction with items"""
        db_transaction = Transaction(
            transaction_id=uuid.uuid4(),
            name=transaction_data.name,
            amount=transaction_data.amount,
            category=transaction_data.category,
            user_id=transaction_data.user_id
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        db_transaction.items = []
        if transaction_data.items:
            for item_data in transaction_data.items:
                db_item = TransactionItem(
                    transaction_item_id=uuid.uuid4(),
                    name=item_data.name,
                    amount=item_data.amount,
                    quantity=item_data.quantity,
                    transaction_id=db_transaction.transaction_id
                )
                db.add(db_item)
                db_transaction.items.append(db_item)
            db.commit()
        
        return db_transaction

    @staticmethod
    def get_transactions(user_id:UUID,db:Session = Depends(get_db))->List[TransactionResponse]:
        """Get all transactions for a user with items"""
        return db.query(Transaction).filter(Transaction.user_id == user_id).all()