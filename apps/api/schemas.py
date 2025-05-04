"""
API schemas for the API app.
"""

from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from apps.core.schemas import custom_extend_schema

# Standard response schema examples
standard_success_example = OpenApiExample(
    name="success_response",
    value={
        "status": "success",
        "code": 200,
        "data": {"example": "data"},
        "message": "Operation successful",
    },
    description="Standard success response",
)

auth_success_example = OpenApiExample(
    name="auth_success_response",
    value={
        "status": "success",
        "code": 200,
        "data": {
            "refresh": "refresh_token_example",
            "access": "access_token_example",
            "user": {
                "id": "user_id_example",
                "email": "user@example.com",
                "first_name": "First",
                "last_name": "Last",
            },
        },
        "message": "Login successful",
    },
    description="Authentication success response",
)

error_example = OpenApiExample(
    name="error_response",
    value={
        "status": "error",
        "code": 400,
        "message": "An error occurred",
        "errors": {"field": ["Error details"]},
    },
    description="Error response",
)

# Reusable schema extensions
standard_response = custom_extend_schema(
    examples=[standard_success_example],
)

auth_response = custom_extend_schema(
    examples=[auth_success_example],
)

error_response = custom_extend_schema(
    examples=[error_example],
)

# Reusable responses
standard_success_response = OpenApiResponse(
    description="Success response",
    examples=[standard_success_example],
)

auth_success_response = OpenApiResponse(
    description="Authentication success response",
    examples=[auth_success_example],
)

error_response_400 = OpenApiResponse(
    description="Error response",
    examples=[error_example],
)
