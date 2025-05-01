"""
API schemas for the API app.
"""

from drf_yasg import openapi

# Standard response schema
standard_response_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["success", "error"],
            "description": "The status of the response",
        },
        "code": {
            "type": "integer",
            "description": "The HTTP status code",
        },
        "data": {
            "type": "object",
            "description": "The response data (for success responses)",
        },
        "message": {
            "type": "string",
            "description": "A message describing the response",
        },
        "errors": {
            "type": "object",
            "description": "Errors that occurred (for error responses)",
        },
    },
    "required": ["status", "code"],
}

# Authentication response schema
auth_response_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["success"],
            "description": "The status of the response",
        },
        "code": {
            "type": "integer",
            "description": "The HTTP status code",
        },
        "data": {
            "type": "object",
            "properties": {
                "refresh": {
                    "type": "string",
                    "description": "The refresh token",
                },
                "access": {
                    "type": "string",
                    "description": "The access token",
                },
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                            "description": "The user ID",
                        },
                        "email": {
                            "type": "string",
                            "format": "email",
                            "description": "The user email",
                        },
                        "first_name": {
                            "type": "string",
                            "description": "The user first name",
                        },
                        "last_name": {
                            "type": "string",
                            "description": "The user last name",
                        },
                    },
                    "required": ["id", "email"],
                },
            },
            "required": ["refresh", "access", "user"],
        },
        "message": {
            "type": "string",
            "description": "A message describing the response",
        },
    },
    "required": ["status", "code", "data"],
}

# Error response schema
error_response_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["error"],
            "description": "The status of the response",
        },
        "code": {
            "type": "integer",
            "description": "The HTTP status code",
        },
        "message": {
            "type": "string",
            "description": "A message describing the error",
        },
        "errors": {
            "type": "object",
            "description": "Errors that occurred",
        },
    },
    "required": ["status", "code", "message"],
}

# Swagger parameter definitions
token_param = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="JWT token in the format: Bearer <token>",
    type=openapi.TYPE_STRING,
    required=True,
)

# Swagger response definitions
standard_success_response = openapi.Response(
    description="Success response",
    schema=openapi.Schema(**standard_response_schema),
)

auth_success_response = openapi.Response(
    description="Authentication success response",
    schema=openapi.Schema(**auth_response_schema),
)

error_response = openapi.Response(
    description="Error response",
    schema=openapi.Schema(**error_response_schema),
)
