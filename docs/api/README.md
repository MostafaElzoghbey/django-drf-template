# API Documentation

This document provides an overview of the API endpoints available in the Django DRF Template.

## Authentication

The API uses JWT (JSON Web Token) authentication. To authenticate, you need to obtain a token by sending your credentials to the login endpoint.

### Obtaining a Token

**Endpoint:** `POST /api/v1/auth/login/`

**Request Body:**
```json
{
  "email": "your.email@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "refresh": "your_refresh_token",
    "access": "your_access_token",
    "user": {
      "id": "user_id",
      "email": "your.email@example.com",
      "first_name": "Your",
      "last_name": "Name"
    }
  },
  "message": "Login successful"
}
```

### Using the Token

Include the access token in the Authorization header of your requests:

```
Authorization: Bearer your_access_token
```

### Refreshing a Token

**Endpoint:** `POST /api/v1/auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "access": "new_access_token"
  },
  "message": "Token refreshed successfully"
}
```

### Logging Out

**Endpoint:** `POST /api/v1/auth/logout/`

**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Logout successful"
}
```

## Users

### List Users

**Endpoint:** `GET /api/v1/users/`

**Authentication:** Required

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": "user_id",
        "email": "user@example.com",
        "first_name": "User",
        "last_name": "Name",
        "bio": "",
        "profile_picture": null,
        "phone_number": "",
        "date_joined": "2023-01-01T00:00:00Z",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
      }
    ],
    "total_pages": 1,
    "current_page": 1
  }
}
```

### Get Current User

**Endpoint:** `GET /api/v1/users/me/`

**Authentication:** Required

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": "user_id",
    "email": "user@example.com",
    "first_name": "User",
    "last_name": "Name",
    "bio": "",
    "profile_picture": null,
    "phone_number": "",
    "date_joined": "2023-01-01T00:00:00Z",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

### Create User

**Endpoint:** `POST /api/v1/users/`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "new.user@example.com",
  "password": "password",
  "password_confirm": "password",
  "first_name": "New",
  "last_name": "User"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 201,
  "data": {
    "id": "user_id",
    "email": "new.user@example.com",
    "first_name": "New",
    "last_name": "User"
  },
  "message": "Resource created successfully"
}
```

### Update User

**Endpoint:** `PATCH /api/v1/users/{user_id}/`

**Authentication:** Required

**Request Body:**
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "bio": "This is my bio",
  "phone_number": "1234567890"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": "user_id",
    "email": "user@example.com",
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "This is my bio",
    "profile_picture": null,
    "phone_number": "1234567890",
    "date_joined": "2023-01-01T00:00:00Z",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  },
  "message": "Resource updated successfully"
}
```

### Change Password

**Endpoint:** `POST /api/v1/users/change_password/`

**Authentication:** Required

**Request Body:**
```json
{
  "old_password": "current_password",
  "new_password": "new_password",
  "new_password_confirm": "new_password"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Password changed successfully."
}
```

## Password Reset

### Request Password Reset

**Endpoint:** `POST /api/v1/auth/password/reset/`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Password reset email sent"
}
```

### Confirm Password Reset

**Endpoint:** `POST /api/v1/auth/password/reset/confirm/`

**Authentication:** Not required

**Request Body:**
```json
{
  "uid": "uid_from_email",
  "token": "token_from_email",
  "new_password": "new_password",
  "new_password_confirm": "new_password"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Password reset successful"
}
```

## Email Verification

**Endpoint:** `POST /api/v1/auth/email/verify/`

**Authentication:** Not required

**Request Body:**
```json
{
  "uid": "uid_from_email",
  "token": "token_from_email"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Email verified successfully"
}
```
