"""
Custom exception handling for the project.
"""

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class ApplicationError(APIException):
    """
    Base exception for application-specific errors.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "A server error occurred."
    default_code = "error"


class BadRequestError(ApplicationError):
    """
    Exception for bad request errors.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."
    default_code = "bad_request"


class NotFoundError(ApplicationError):
    """
    Exception for not found errors.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found."
    default_code = "not_found"


class ConflictError(ApplicationError):
    """
    Exception for conflict errors.
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Resource conflict."
    default_code = "conflict"


def custom_exception_handler(exc, context):
    """
    Custom exception handler for the API.
    
    This handler provides a consistent error response format across the API.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, it's an unhandled exception
    if response is None:
        if isinstance(exc, ValidationError):
            data = {
                "status": "error",
                "code": "validation_error",
                "message": "Validation error",
                "errors": exc.message_dict if hasattr(exc, "message_dict") else {"detail": exc.messages},
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if isinstance(exc, Http404):
            data = {
                "status": "error",
                "code": "not_found",
                "message": str(exc) if str(exc) else "Resource not found",
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        
        if isinstance(exc, PermissionDenied):
            data = {
                "status": "error",
                "code": "permission_denied",
                "message": str(exc) if str(exc) else "Permission denied",
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        
        # Unhandled exceptions
        return None
    
    # Format the response to match our standard error format
    error_data = {
        "status": "error",
        "code": response.status_code,
    }
    
    # Extract error message and details
    if isinstance(response.data, dict):
        if "detail" in response.data:
            error_data["message"] = response.data["detail"]
            # Remove detail from the original data
            del response.data["detail"]
            
            # If there are other fields, add them as errors
            if response.data:
                error_data["errors"] = response.data
        else:
            error_data["message"] = "An error occurred"
            error_data["errors"] = response.data
    else:
        error_data["message"] = response.data
    
    response.data = error_data
    return response
