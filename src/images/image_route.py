from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from src.config.db import get_db
from src.images.image_controller import ImageController
from src.images.image_schema import ImageResponse, ImageUploadRequest
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

router = APIRouter(prefix="/api/v1/images", tags=["images"])

@router.post("/upload", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    expiration: Optional[int] = None,
    transaction_id: Optional[UUID] = None,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload an image file to ImgBB
    
    - **file**: Image file (required)
    - **name**: Optional image name
    - **expiration**: Optional expiration time in seconds (60-15552000)
    - **transaction_id**: Optional transaction ID to associate with image
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    image_data = await file.read()
    
    return ImageController.upload_image(
        image_data=image_data,
        name=name,
        expiration=expiration,
        transaction_id=transaction_id,
        db=db
    )

@router.post("/upload-url", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image_from_url(
    image_url: str,
    name: Optional[str] = None,
    expiration: Optional[int] = None,
    transaction_id: Optional[UUID] = None,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload an image from URL to ImgBB
    
    - **image_url**: URL of the image (required)
    - **name**: Optional image name
    - **expiration**: Optional expiration time in seconds (60-15552000)
    - **transaction_id**: Optional transaction ID to associate with image
    """
    return ImageController.upload_image_from_url(
        image_url=image_url,
        name=name,
        expiration=expiration,
        transaction_id=transaction_id,
        db=db
    )

@router.get("/{image_id}", response_model=ImageResponse, status_code=status.HTTP_200_OK)
async def get_image(
    image_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get image by ID
    """
    return ImageController.get_image(image_id, db)

@router.get("/transaction/{transaction_id}", response_model=List[ImageResponse], status_code=status.HTTP_200_OK)
async def get_images_by_transaction(
    transaction_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all images for a transaction
    """
    return ImageController.get_images_by_transaction(transaction_id, db)

@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
async def delete_image(
    image_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete image by ID
    """
    return ImageController.delete_image(image_id, db)