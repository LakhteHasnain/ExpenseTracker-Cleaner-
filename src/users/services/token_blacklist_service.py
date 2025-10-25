"""
Token Blacklist Service

Handles token revocation and validation
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.users.token_blacklist_model import TokenBlacklist
from src.users.core.jwt_token import decode_token

def blacklist_token(token: str, db: Session) -> bool:
    """
    Add a token to the blacklist (revoke it)
    
    Args:
        token: JWT token to blacklist
        db: Database session
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Decode token to get expiration time
        payload = decode_token(token)
        if not payload:
            return False
        
        # Get token expiration from payload
        exp = payload.get("exp")
        if not exp:
            return False
        
        expires_at = datetime.fromtimestamp(exp)
        
        # Create blacklist entry
        blacklisted = TokenBlacklist(
            token=token,
            expires_at=expires_at
        )
        
        db.add(blacklisted)
        db.commit()
        
        return True
    except Exception as e:
        print(f"Error blacklisting token: {str(e)}")
        return False

def is_token_blacklisted(token: str, db: Session) -> bool:
    """
    Check if a token is blacklisted
    
    Args:
        token: JWT token to check
        db: Database session
        
    Returns:
        True if token is blacklisted, False otherwise
    """
    try:
        blacklisted = db.query(TokenBlacklist).filter(
            TokenBlacklist.token == token
        ).first()
        
        return blacklisted is not None
    except Exception as e:
        print(f"Error checking token blacklist: {str(e)}")
        return False

def cleanup_expired_tokens(db: Session) -> int:
    """
    Delete expired tokens from blacklist
    
    Removes tokens that have naturally expired
    Helps keep database clean
    
    Args:
        db: Database session
        
    Returns:
        Number of tokens deleted
    """
    try:
        # Delete tokens that have expired
        result = db.query(TokenBlacklist).filter(
            TokenBlacklist.expires_at < datetime.utcnow()
        ).delete()
        
        db.commit()
        
        return result
    except Exception as e:
        print(f"Error cleaning up expired tokens: {str(e)}")
        return 0

def get_blacklist_stats(db: Session) -> dict:
    """
    Get statistics about the token blacklist
    
    Args:
        db: Database session
        
    Returns:
        Dictionary with blacklist statistics
    """
    try:
        total_blacklisted = db.query(TokenBlacklist).count()
        expired = db.query(TokenBlacklist).filter(
            TokenBlacklist.expires_at < datetime.utcnow()
        ).count()
        active = total_blacklisted - expired
        
        return {
            "total_blacklisted": total_blacklisted,
            "active_blacklisted": active,
            "expired": expired
        }
    except Exception as e:
        print(f"Error getting blacklist stats: {str(e)}")
        return {}
