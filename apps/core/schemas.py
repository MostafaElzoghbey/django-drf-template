"""
Custom schema generator for drf-spectacular.
"""

from drf_spectacular.generators import SchemaGenerator


class CustomSchemaGenerator(SchemaGenerator):
    """
    Custom schema generator that wraps all responses in the standard format.
    """

    def get_response_for_code(self, response_code, response, direction="response"):
        """
        Wrap the response in the standard format.
        """
        # Get the original response
        original_response = super().get_response_for_code(
            response_code, response, direction
        )

        # Skip if this is an error response (4xx, 5xx)
        if str(response_code).startswith(("4", "5")):
            # For error responses, we'll use a different format
            return self._get_error_response(response_code, original_response)

        # Skip if this is a 204 No Content response
        if response_code == "204":
            return original_response

        # Get the original schema
        original_schema = (
            original_response.get("content", {})
            .get("application/json", {})
            .get("schema", {})
        )

        # Create the wrapped schema
        wrapped_schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["success"],
                    "description": "The status of the response",
                },
                "code": {
                    "type": "integer",
                    "example": int(response_code),
                    "description": "The HTTP status code",
                },
                "data": original_schema,
                "message": {
                    "type": "string",
                    "description": "A message describing the response",
                },
            },
            "required": ["status", "code"],
        }

        # Update the response with the wrapped schema
        if (
            "content" in original_response
            and "application/json" in original_response["content"]
        ):
            original_response["content"]["application/json"]["schema"] = wrapped_schema

        return original_response

    def _get_error_response(self, response_code, original_response):
        """
        Create an error response in the standard format.
        """
        # Create the error schema
        error_schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["error"],
                    "description": "The status of the response",
                },
                "code": {
                    "type": "integer",
                    "example": int(response_code),
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

        # Update the response with the error schema
        if (
            "content" in original_response
            and "application/json" in original_response["content"]
        ):
            original_response["content"]["application/json"]["schema"] = error_schema

        return original_response


class CustomResponseAutoSchema:
    """
    Mixin for automatically wrapping responses in the standard format.
    """

    def get_response_bodies(self):
        """
        Wrap all response bodies in the standard format.
        """
        responses = super().get_response_bodies()

        # Process each response
        for response_code, response in responses.items():
            # Skip if this is an error response (4xx, 5xx)
            if str(response_code).startswith(("4", "5")):
                # For error responses, we'll use a different format
                responses[response_code] = self._get_error_response(
                    response_code, response
                )
                continue

            # Skip if this is a 204 No Content response
            if response_code == "204":
                continue

            # Get the original schema
            if "content" in response and "application/json" in response["content"]:
                original_schema = response["content"]["application/json"]["schema"]

                # Create the wrapped schema
                wrapped_schema = {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["success"],
                            "description": "The status of the response",
                        },
                        "code": {
                            "type": "integer",
                            "example": int(response_code),
                            "description": "The HTTP status code",
                        },
                        "data": original_schema,
                        "message": {
                            "type": "string",
                            "description": "A message describing the response",
                        },
                    },
                    "required": ["status", "code"],
                }

                # Update the response with the wrapped schema
                response["content"]["application/json"]["schema"] = wrapped_schema

        return responses

    def _get_error_response(self, response_code, response):
        """
        Create an error response in the standard format.
        """
        # Create the error schema
        error_schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["error"],
                    "description": "The status of the response",
                },
                "code": {
                    "type": "integer",
                    "example": int(response_code),
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

        # Update the response with the error schema
        if "content" in response and "application/json" in response["content"]:
            response["content"]["application/json"]["schema"] = error_schema

        return response


from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiExample


class CustomAutoSchema(CustomResponseAutoSchema, AutoSchema):
    """
    Custom auto schema that wraps all responses in the standard format.
    """

    pass


def custom_extend_schema(
    summary=None,
    description=None,
    responses=None,
    examples=None,
    request=None,
    tags=None,
    **kwargs,
):
    """
    Custom extend_schema decorator that automatically adds examples.

    This decorator wraps drf-spectacular's extend_schema decorator and adds
    standard examples for success and error responses.
    """
    # Default examples as a list, not a dict
    default_examples = [
        # 200 Success
        OpenApiExample(
            name="success_response",
            value={
                "status": "success",
                "code": 200,
                "data": {"example": "data"},
                "message": "Operation successful",
            },
            description="Standard success response",
            response_only=True,
            status_codes=["200"],
        ),
        # 201 Created
        OpenApiExample(
            name="created_response",
            value={
                "status": "success",
                "code": 201,
                "data": {"id": "example_id"},
                "message": "Resource created successfully",
            },
            description="Resource created successfully",
            response_only=True,
            status_codes=["201"],
        ),
        # 400 Bad Request
        OpenApiExample(
            name="error_response",
            value={
                "status": "error",
                "code": 400,
                "message": "Invalid data",
                "errors": {"field": ["Error details"]},
            },
            description="Error response",
            response_only=True,
            status_codes=["400"],
        ),
        # 401 Unauthorized
        OpenApiExample(
            name="unauthorized_response",
            value={
                "status": "error",
                "code": 401,
                "message": "Authentication credentials were not provided.",
            },
            description="Unauthorized response",
            response_only=True,
            status_codes=["401"],
        ),
        # 403 Forbidden
        OpenApiExample(
            name="forbidden_response",
            value={
                "status": "error",
                "code": 403,
                "message": "You do not have permission to perform this action.",
            },
            description="Forbidden response",
            response_only=True,
            status_codes=["403"],
        ),
        # 404 Not Found
        OpenApiExample(
            name="not_found_response",
            value={
                "status": "error",
                "code": 404,
                "message": "Resource not found",
            },
            description="Not found response",
            response_only=True,
            status_codes=["404"],
        ),
    ]

    # Merge provided examples with default examples
    if examples:
        # If examples is a list, just extend
        if isinstance(examples, list):
            default_examples.extend(examples)
        # If examples is a dict, convert to list and extend
        elif isinstance(examples, dict):
            for status_code, example_list in examples.items():
                for example in example_list:
                    if not hasattr(example, "status_codes"):
                        example.status_codes = [str(status_code)]
                    default_examples.append(example)

    # Create responses dict if not provided
    if responses is None:
        responses = {}

    # Add default responses for common status codes if not already provided
    for status_code in ["200", "201", "400", "401", "403", "404"]:
        if status_code not in responses:
            if status_code in ["200", "201"]:
                responses[status_code] = {
                    "description": f"Success - Status code {status_code}"
                }
            else:
                responses[status_code] = {
                    "description": f"Error - Status code {status_code}"
                }

    # Call the original extend_schema decorator
    return extend_schema(
        summary=summary,
        description=description,
        responses=responses,
        examples=default_examples,
        request=request,
        tags=tags,
        **kwargs,
    )
