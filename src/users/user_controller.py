from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.config.db import get_db
from src.users.user_model import User
from src.users.user_schema import UserCreate, UserResponse
from src.users.core.user_password_hash import get_password_hash

class UserController:
    @staticmethod
    async def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
        """Create a new user with hashed password"""
        # Check if user with email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            user_id=uuid.uuid4(),
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            age=user_data.age
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> UserResponse:
        """Get a single user by ID"""
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[UserResponse]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    async def update_user(
        user_id: uuid.UUID, 
        user_data: UserCreate, 
        db: Session = Depends(get_db)
    ) -> UserResponse:
        """Update user information"""
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if email is being updated to an existing email
        if user_data.email != user.email:
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
        
        # Update user data
        user.name = user_data.name
        user.email = user_data.email
        if user_data.password:
            user.password = get_password_hash(user_data.password)
        if user_data.age is not None:
            user.age = user_data.age
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    async def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> dict:
        """Delete a user"""
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}