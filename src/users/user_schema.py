from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from uuid import UUID
from src.users.core.user_password_hash import is_password_valid

class UserCreate(BaseModel):
    name: str = Field(..., min_length=5, max_length=100, description="User's full name", nullable=False)
    email: EmailStr = Field(..., description="User's email address", nullable=False)
    password: str = Field(..., min_length=8, description="User's password (minimum 8 characters)", nullable=False)
    age: Optional[int] = Field(None, ge=1, le=150, description="User's age (1-150)", nullable=True)
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if not is_password_valid(v):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, and one digit"
            )
        return v
    
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, v) -> Optional[int]:
        """Validate age is reasonable and correct type"""
        if v is None:
            return None
        
        # If it's a string, try to convert to int
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                raise ValueError("Age must be a valid integer")
        
        # Check if it's an integer
        if not isinstance(v, int):
            raise ValueError("Age must be an integer")
        
        # Check range
        if v < 1 or v > 150:
            raise ValueError("Age must be between 1 and 150")
        
        return v

class UserResponse(BaseModel):
    user_id: UUID = Field(..., description="Unique user identifier", nullable=False)
    name: str = Field(..., description="User's full name", nullable=False)
    email: str = Field(..., description="User's email address", nullable=False)
    age: Optional[int] = Field(None, description="User's age", nullable=True)

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., min_length=1, description="User's email address", nullable=False)
    password: str = Field(..., min_length=8, description="User's password (minimum 8 characters)", nullable=False)
    
   

class AuthResponse(BaseModel):
    user: UserResponse = Field(..., description="User information", nullable=False)
    access_token: str = Field(..., description="JWT access token", nullable=False)
    refresh_token: str = Field(..., description="JWT refresh token", nullable=False)
    token_type: str = Field(default="bearer", description="Token type", nullable=False)

class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="New JWT access token", nullable=False)
    refresh_token: str = Field(..., description="New JWT refresh token", nullable=False)
    token_type: str = Field(default="bearer", description="Token type", nullable=False)

class LogoutResponse(BaseModel):
    status: int = Field(..., description="HTTP status code", nullable=False)
    msg: str = Field(..., description="Logout message", nullable=False)

class ErrorResponse(BaseModel):
    status: int = Field(..., description="HTTP status code", nullable=False)
    msg: str = Field(..., description="Error message", nullable=False)