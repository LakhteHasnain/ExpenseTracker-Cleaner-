from fastapi import status
from typing import Dict, Any, List, Optional

def format_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    Format error response in standardized format
    
    Args:
        status_code: HTTP status code
        message: Error message
        
    Returns:
        Dictionary with status and msg keys
    """
    return {
        "status": status_code,
        "msg": message
    }

def format_validation_error_response(errors: List[Dict]) -> Dict[str, Any]:
    """
    Format validation errors from Pydantic
    
    Args:
        errors: List of validation errors from Pydantic
        
    Returns:
        Dictionary with status and msg keys
    """
    error_messages = []
    
    for error in errors:
        field = " -> ".join(str(loc) for loc in error.get("loc", [])[1:])
        msg = error.get("msg", "Unknown error")
        error_messages.append(f"{field}: {msg}")
    
    combined_message = "; ".join(error_messages)
    
    return {
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "msg": combined_message
    }

def format_success_response(data: Any, status_code: int = status.HTTP_200_OK) -> Dict[str, Any]:
    """
    Format success response
    
    Args:
        data: Response data
        status_code: HTTP status code
        
    Returns:
        Dictionary with status and data
    """
    return {
        "status": status_code,
        "data": data
    }
