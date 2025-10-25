from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict

from src.users.user_model import User
from src.users.user_schema import UserCreate, UserLogin, UserResponse
from src.users.core.user_password_hash import get_password_hash, verify_password
from src.users.core.jwt_token import create_access_token, create_refresh_token

def sign_up(user_data: UserCreate, db: Session) -> Dict:
    """Create a new user account and return tokens"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        age=user_data.age
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": str(new_user.user_id)})
    refresh_token = create_refresh_token(data={"sub": str(new_user.user_id)})
    
    return {
        "user": {
            "user_id": str(new_user.user_id),
            "name": new_user.name,
            "email": new_user.email,
            "age": new_user.age
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def sign_in(login_data: UserLogin, db: Session) -> Dict:
    """Authenticate user and return tokens"""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.user_id)})
    refresh_token = create_refresh_token(data={"sub": str(user.user_id)})
    
    return {
        "user": {
            "user_id": str(user.user_id),
            "name": user.name,
            "email": user.email,
            "age": user.age
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }