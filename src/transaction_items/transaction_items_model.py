from sqlalchemy import Column, String, Integer, UUID, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.config.db import Base
import uuid 

class TransactionItem(Base):
    __tablename__="transaction_items"

    transaction_item_id=Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name=Column(String(100),nullable=False)
    amount=Column(Float,nullable=False)
    quantity=Column(Integer,nullable=False)
    transaction_id=Column(UUID(as_uuid=True), ForeignKey("transactions.transaction_id"), nullable=False)
    transaction = relationship("Transaction", back_populates="items")