from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from uuid import UUID
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 1))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """
    Decode JWT token without checking blacklist
    Used by token blacklist service to get expiration time
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def verify_token(token: str, db: Session = None) -> Optional[dict]:
    """
    Verify and decode JWT token
    
    Also checks if token is blacklisted (revoked)
    
    Args:
        token: JWT token to verify
        db: Database session (optional, for blacklist check)
        
    Returns:
        Token payload if valid, None if invalid or blacklisted
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token is blacklisted (if db session provided)
        if db is not None:
            from src.users.services.token_blacklist_service import is_token_blacklisted
            if is_token_blacklisted(token, db):
                return None  # Token is blacklisted
        
        return payload
    except JWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[UUID]:
    """Extract user_id from token"""
    payload = verify_token(token)
    if payload is None:
        return None
    return payload.get("sub")