from fastapi import APIRouter, Depends, status, Header, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from src.config.db import get_db
from src.transactions.transaction_model import Transaction
from src.transactions.transaction_schema import TransactionCreate, TransactionResponse
from src.transactions.transaction_controller import TransactionController
from src.users.core.jwt_token import verify_token

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> UUID:
    """Extract and verify user_id from JWT token"""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format"
        )
    
    payload = verify_token(token, db)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )
    
    return UUID(user_id)

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, user_id: UUID = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new transaction (requires authentication)"""
    transaction_data.user_id = user_id
    return TransactionController.create_transaction(transaction_data, db)

@router.get("/", response_model=List[TransactionResponse], status_code=status.HTTP_200_OK)
async def get_transactions(user_id: UUID = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all transactions for authenticated user"""
    return TransactionController.get_transactions(user_id, db)
