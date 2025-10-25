from fastapi import APIRouter, Depends, status, Request, Header, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.config.db import get_db
from src.users.user_controller import UserController
from src.users.user_schema import UserCreate, UserResponse, UserLogin, AuthResponse, LogoutResponse, RefreshResponse
from src.users.services.user_auth import sign_up, sign_in
from src.users.services.token_blacklist_service import blacklist_token
from src.users.services.token_refresh_service import refresh_access_token
from src.users.constants.use_api_paths import USER_ENDPOINTS
from src.config.rate_limit import limiter, SIGNIN_RATE_LIMIT, SIGNUP_RATE_LIMIT

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(SIGNUP_RATE_LIMIT)
async def signup(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account
    
    Rate Limited: 3 attempts per minute per IP
    """
    return sign_up(user_data, db)

@router.post("/signin", response_model=AuthResponse, status_code=status.HTTP_200_OK)
@limiter.limit(SIGNIN_RATE_LIMIT)
async def signin(request: Request, login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user
    
    Rate Limited: 5 attempts per minute per IP
    Protects against brute-force attacks
    """
    return sign_in(login_data, db)

@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
async def logout(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    Logout user by revoking their token
    
    Requires: Authorization header with Bearer token
    
    Example:
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )
    
    # Extract token from "Bearer <token>" format
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
    
    # Blacklist the token
    success = blacklist_token(token, db)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to logout. Invalid token."
        )
    
    return {
        "status": 200,
        "msg": "Logged out successfully"
    }

@router.post("/refresh", response_model=RefreshResponse, status_code=status.HTTP_200_OK)
async def refresh(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    
    Process:
    1. Verify refresh token is valid
    2. Blacklist old refresh token (rotation)
    3. Generate new access token
    4. Generate new refresh token
    
    Requires: Authorization header with Bearer refresh token
    
    Example:
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    
    Returns:
        New access_token and refresh_token
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )
    
    # Extract token from "Bearer <token>" format
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
    
    # Refresh the token (handles rotation and blacklisting)
    return refresh_access_token(token, db)
