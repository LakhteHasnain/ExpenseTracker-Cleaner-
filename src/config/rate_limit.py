"""
Rate Limiting Configuration

Protects against brute-force attacks by limiting login attempts
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)

# Custom exception handler for rate limit exceeded
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Handle rate limit exceeded errors
    Returns standardized error response
    """
    return JSONResponse(
        status_code=429,
        content={
            "status": 429,
            "msg": "Too many login attempts. Please try again later."
        }
    )

# Rate limit configurations
SIGNIN_RATE_LIMIT = "5/minute"  # Max 5 signin attempts per minute per IP
SIGNUP_RATE_LIMIT = "3/minute"  # Max 3 signup attempts per minute per IP
