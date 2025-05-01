"""
Helper functions for the project.
"""

import random
import string
from typing import Any, Dict, List, Optional, Union

from django.conf import settings
from django.utils import timezone


def generate_random_string(length: int = 10) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of the random string to generate.
        
    Returns:
        A random string.
    """
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def get_client_ip(request) -> str:
    """
    Get the client IP address from the request.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        The client IP address.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def format_response(
    data: Optional[Any] = None,
    status: str = "success",
    code: int = 200,
    message: Optional[str] = None,
    errors: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
) -> Dict[str, Any]:
    """
    Format a response following the standard API response format.
    
    Args:
        data: The data to include in the response.
        status: The status of the response (success or error).
        code: The HTTP status code.
        message: A message to include in the response.
        errors: Any errors to include in the response.
        
    Returns:
        A formatted response dictionary.
    """
    response = {
        "status": status,
        "code": code,
    }
    
    if data is not None:
        response["data"] = data
    
    if message:
        response["message"] = message
    
    if errors:
        response["errors"] = errors
    
    return response


def is_production() -> bool:
    """
    Check if the application is running in production mode.
    
    Returns:
        True if in production, False otherwise.
    """
    return not settings.DEBUG


def get_current_time() -> str:
    """
    Get the current time in ISO format.
    
    Returns:
        Current time in ISO format.
    """
    return timezone.now().isoformat()
