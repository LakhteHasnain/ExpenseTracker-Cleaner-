from fastapi import APIRouter, Depends, status, Header, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
import json
from src.config.db import get_db
from src.transactions.transaction_model import Transaction
from src.transactions.transaction_schema import TransactionCreate, TransactionResponse
from src.transactions.transaction_controller import TransactionController
from src.users.core.jwt_token import verify_token
from src.images.image_controller import ImageController

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
async def create_transaction(
    name: str = Form(...),
    amount: int = Form(...),
    category: str = Form(...),
    items: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[]),
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction with optional image files
    
    - **name**: Transaction name (required)
    - **amount**: Transaction amount (required)
    - **category**: Transaction category (required)
    - **items**: JSON array of transaction items (optional)
    - **files**: Image files to attach (optional)
    """
    transaction_items = []
    if items:
        try:
            transaction_items = json.loads(items)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid items JSON format"
            )
    
    transaction_data = TransactionCreate(
        name=name,
        amount=amount,
        category=category,
        user_id=user_id,
        items=transaction_items
    )
    
    transaction = TransactionController.create_transaction(transaction_data, db)
    
    if files:
        for file in files:
            if file.content_type and file.content_type.startswith('image/'):
                try:
                    image_data = await file.read()
                    ImageController.upload_image(
                        image_data=image_data,
                        name=file.filename,
                        transaction_id=transaction.transaction_id,
                        db=db
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Failed to upload image {file.filename}: {str(e)}"
                    )
    
    db.refresh(transaction)
    return transaction

@router.get("/", response_model=List[TransactionResponse], status_code=status.HTTP_200_OK)
async def get_transactions(user_id: UUID = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all transactions for authenticated user"""
    return TransactionController.get_transactions(user_id, db)
