"""
Token Refresh Service

Handles token refresh with automatic rotation and blacklisting
"""

from sqlalchemy.orm import Session
from src.users.core.jwt_token import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token
)
from src.users.services.token_blacklist_service import blacklist_token
from fastapi import HTTPException

def refresh_access_token(refresh_token: str, db: Session) -> dict:
    """
    Refresh access token using refresh token
    
    Process:
    1. Verify refresh_token is valid
    2. Blacklist old refresh_token (rotation)
    3. Generate new access_token
    4. Generate new refresh_token
    5. Return both tokens
    
    Args:
        refresh_token: Current refresh token
        db: Database session
        
    Returns:
        Dictionary with new access_token and refresh_token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    
    # Step 1: Verify refresh token
    payload = verify_token(refresh_token, db)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )
    
    # Check if it's actually a refresh token (has type field)
    token_type = payload.get("type")
    if token_type != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type. Expected refresh token."
        )
    
    # Get user_id from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )
    
    # Step 2: Blacklist old refresh token (rotation)
    try:
        blacklist_token(refresh_token, db)
    except Exception as e:
        print(f"Warning: Could not blacklist old refresh token: {str(e)}")
        # Don't fail the refresh, just log the warning
    
    # Step 3: Generate new access token
    new_access_token = create_access_token({"sub": user_id})
    
    # Step 4: Generate new refresh token
    new_refresh_token = create_refresh_token({"sub": user_id})
    
    # Step 5: Return both tokens
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
