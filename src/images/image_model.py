from sqlalchemy import Column, String, ForeignKey, UUID,Integer
from sqlalchemy.orm import relationship
from src.config.db import Base
import uuid

class Image(Base):
    __tablename__ = "images"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    image_id = Column(String, index=True)
    url = Column(String, index=True)
    display_url = Column(String, nullable=True)
    delete_url = Column(String, nullable=True)
    filename = Column(String, nullable=True)
    mime = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    expiration = Column(String, nullable=True)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.transaction_id"), nullable=True)
    transaction = relationship("Transaction", back_populates="images")