"""
Middleware for handling request and response processing.
"""

import json
import logging
import time
import uuid
from typing import Any, Callable, Dict, Optional

from django.http import HttpRequest, HttpResponse, JsonResponse

logger = logging.getLogger(__name__)


class RequestResponseMiddleware:
    """
    Middleware for processing requests and responses.
    
    This middleware:
    1. Adds a request ID to each request
    2. Logs request and response details
    3. Handles response formatting
    """
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        
        # Add request ID to response headers
        start_time = time.time()
        
        # Process the request
        self._log_request(request)
        response = self.get_response(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Add headers to response
        response["X-Request-ID"] = request_id
        response["X-Request-Duration"] = str(int(duration * 1000))  # in milliseconds
        
        # Log the response
        self._log_response(request, response, duration)
        
        # Format JSON responses if needed
        if (
            isinstance(response, JsonResponse)
            and not request.path.startswith("/admin/")
            and not request.path.startswith("/api/docs/")
        ):
            self._format_json_response(response)
        
        return response
    
    def _log_request(self, request: HttpRequest) -> None:
        """
        Log request details.
        """
        logger.info(
            f"Request: {request.method} {request.path} "
            f"[ID: {getattr(request, 'request_id', 'N/A')}]"
        )
    
    def _log_response(
        self, request: HttpRequest, response: HttpResponse, duration: float
    ) -> None:
        """
        Log response details.
        """
        logger.info(
            f"Response: {request.method} {request.path} "
            f"[ID: {getattr(request, 'request_id', 'N/A')}] "
            f"Status: {response.status_code} "
            f"Duration: {int(duration * 1000)}ms"
        )
    
    def _format_json_response(self, response: JsonResponse) -> None:
        """
        Format JSON responses to follow a consistent structure.
        
        If the response is already formatted, it won't be modified.
        """
        # Skip formatting if response is empty
        if not response.content:
            return
        
        try:
            data = json.loads(response.content.decode("utf-8"))
            
            # Skip if the response is already formatted
            if isinstance(data, dict) and "status" in data:
                return
            
            # Format the response
            formatted_data = self._create_formatted_response(data, response.status_code)
            
            # Replace the response content
            response.content = json.dumps(formatted_data).encode("utf-8")
        except json.JSONDecodeError:
            # Not a JSON response, skip formatting
            pass
    
    def _create_formatted_response(
        self, data: Any, status_code: int
    ) -> Dict[str, Any]:
        """
        Create a formatted response following the standard structure.
        """
        # Determine the status based on the status code
        status = "success" if 200 <= status_code < 300 else "error"
        
        # Create the formatted response
        formatted_response = {
            "status": status,
            "code": status_code,
        }
        
        # Add data or error message
        if status == "success":
            formatted_response["data"] = data
        else:
            formatted_response["message"] = (
                data.get("detail", "An error occurred")
                if isinstance(data, dict) and "detail" in data
                else "An error occurred"
            )
            
            # Add errors if available
            if isinstance(data, dict) and "errors" in data:
                formatted_response["errors"] = data["errors"]
        
        return formatted_response
