"""
Token Blacklist Model

Stores revoked/blacklisted tokens to prevent their use after logout
"""

from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from src.config.db import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<TokenBlacklist token_id={self.id} expires_at={self.expires_at}>"
