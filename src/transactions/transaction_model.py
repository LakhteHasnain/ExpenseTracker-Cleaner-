from sqlalchemy import Column, String, Integer, UUID, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db import Base
import uuid
class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id=Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    amount= Column(Integer,nullable=False)
    category= Column(String(50),nullable=False)
    user_id= Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    items = relationship("TransactionItem", back_populates="transaction")
    images = relationship("Image", back_populates="transaction")
