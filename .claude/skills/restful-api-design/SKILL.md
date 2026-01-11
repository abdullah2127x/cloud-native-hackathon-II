---
name: restful-api-design
description: |
  This skill should be used when designing REST API endpoints, defining HTTP methods, or structuring API responses.
  Use for API architecture decisions and following RESTful principles.
---

# RESTful API Design Skill

Auto-invoke when designing REST API endpoints, defining HTTP methods, or structuring API responses. Use for API architecture decisions and following RESTful principles.

## Resource Naming Conventions (Plural Nouns)

### ✅ DO: Use Plural Nouns for Resource Names
```http
# Good: Plural nouns for collections
GET /users          # Get all users
POST /users         # Create a new user
GET /users/123      # Get user with ID 123
PUT /users/123      # Update user with ID 123
DELETE /users/123   # Delete user with ID 123

# Good: Nested resources
GET /users/123/posts        # Get all posts for user 123
POST /users/123/posts       # Create a post for user 123
GET /users/123/posts/456    # Get post 456 for user 123
```

### ❌ AVOID: Singular Nouns for Collections
```http
# Avoid: Singular nouns (confusing for collections)
GET /user           # Confusing - is this a single user or all users?
POST /user          # Should be /users for creating a user
GET /user/123       # Better: /users/123
```

### ✅ DO: Use Descriptive Resource Names
```http
# Good: Clear, descriptive resource names
GET /products
GET /orders
GET /customers
GET /categories
GET /reviews
```

### ✅ DO: Use Nested Resources for Relationships
```http
# Good: Nested resources for related entities
GET /users/123/orders           # All orders for user 123
GET /users/123/orders/456       # Specific order for user 123
GET /users/123/orders/456/items # Items in specific order
GET /posts/123/comments         # Comments for post 123
```

## HTTP Method Usage

### GET - Retrieve Resources
```http
# Retrieve all resources
GET /users

# Retrieve specific resource
GET /users/123

# Retrieve with query parameters
GET /users?status=active&limit=10&offset=0

# Retrieve nested resources
GET /users/123/orders
```

### POST - Create Resources
```http
# Create a new resource
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}

# Create nested resource
POST /users/123/orders
Content-Type: application/json

{
  "product_id": 456,
  "quantity": 2
}
```

### PUT - Update Entire Resource
```http
# Update entire resource (full replacement)
PUT /users/123
Content-Type: application/json

{
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "status": "active"
}
```

### PATCH - Partial Updates
```http
# Update specific fields only
PATCH /users/123
Content-Type: application/json

{
  "name": "John Smith"
}
```

### DELETE - Remove Resources
```http
# Delete specific resource
DELETE /users/123

# Delete nested resource
DELETE /users/123/orders/456
```

## Status Code Meanings

### 2xx Success Codes
```http
# 200 OK - Successful GET, PUT, PATCH
GET /users/123 → 200 OK
PUT /users/123 → 200 OK (when updating)
PATCH /users/123 → 200 OK (when updating)

# 201 Created - Successful POST
POST /users → 201 Created

# 204 No Content - Successful DELETE or empty response
DELETE /users/123 → 204 No Content
```

### 4xx Client Error Codes
```http
# 400 Bad Request - Invalid request data
POST /users → 400 Bad Request (when request body is invalid)

# 401 Unauthorized - Authentication required
GET /protected → 401 Unauthorized

# 403 Forbidden - Authenticated but not authorized
GET /admin → 403 Forbidden

# 404 Not Found - Resource doesn't exist
GET /users/999 → 404 Not Found

# 409 Conflict - Resource already exists
POST /users → 409 Conflict (when email already exists)

# 422 Unprocessable Entity - Validation errors
POST /users → 422 Unprocessable Entity (validation errors)
```

### 5xx Server Error Codes
```http
# 500 Internal Server Error - Unexpected server error
GET /users → 500 Internal Server Error

# 503 Service Unavailable - Server temporarily unavailable
GET /users → 503 Service Unavailable
```

## Response Format Structure

### Success Response Format
```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "message": "User retrieved successfully"
}
```

### List Response Format
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "id": 124,
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ],
  "message": "Users retrieved successfully",
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10
  }
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      },
      {
        "field": "name",
        "message": "Name must be at least 2 characters"
      }
    ]
  }
}
```

## Pagination Patterns

### Query Parameters for Pagination
```http
GET /users?page=1&limit=10&sort=name&order=asc
```

### Pagination Response Structure
```json
{
  "success": true,
  "data": [
    // ... user data
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10,
    "hasNext": true,
    "hasPrev": false
  }
}
```

### Alternative Pagination with Offset/Limit
```http
GET /users?offset=0&limit=10
```

### Offset/Limit Response Structure
```json
{
  "success": true,
  "data": [
    // ... user data
  ],
  "pagination": {
    "offset": 0,
    "limit": 10,
    "total": 100,
    "hasNext": true,
    "nextOffset": 10
  }
}
```

## Error Response Format

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found",
    "timestamp": "2024-01-01T12:00:00Z",
    "path": "/users/999"
  }
}
```

### Validation Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "code": "TOO_YOUNG",
        "message": "Age must be at least 18"
      }
    ]
  }
}
```

### Business Logic Error Response
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_FUNDS",
    "message": "Insufficient funds for this transaction",
    "details": {
      "currentBalance": 50.00,
      "requiredAmount": 100.00
    }
  }
}
```

## API Versioning Approach

### URL Path Versioning (Recommended)
```http
# Version in URL path
GET /api/v1/users
POST /api/v1/users
GET /api/v2/users
```

### Header Versioning
```http
# Version in header
GET /users
Accept: application/vnd.myapi.v1+json
```

### Query Parameter Versioning
```http
# Version in query parameter
GET /users?version=1.0
```

### Versioned Response Example
```json
{
  "version": "1.0",
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

## Request/Response Examples

### User Resource Examples

#### Create User (POST)
```http
POST /api/v1/users
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "role": "user"
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "role": "user",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z"
  },
  "message": "User created successfully"
}
```

#### Get User (GET)
```http
GET /api/v1/users/123
Authorization: Bearer <token>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "role": "user",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z"
  },
  "message": "User retrieved successfully"
}
```

#### Update User (PUT)
```http
PUT /api/v1/users/123
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "age": 31
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Smith",
    "email": "johnsmith@example.com",
    "age": 31,
    "role": "user",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T13:00:00Z"
  },
  "message": "User updated successfully"
}
```

#### Get Users with Pagination (GET)
```http
GET /api/v1/users?page=1&limit=10&status=active
Authorization: Bearer <token>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": [
    {
      "id": 123,
      "name": "John Doe",
      "email": "john@example.com",
      "age": 30,
      "role": "user",
      "status": "active"
    },
    {
      "id": 124,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "age": 25,
      "role": "user",
      "status": "active"
    }
  ],
  "message": "Users retrieved successfully",
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10,
    "hasNext": true,
    "hasPrev": false
  }
}
```

#### Error Response Example
```http
POST /api/v1/users
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "",
  "email": "invalid-email",
  "age": 15
}
```

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "name",
        "code": "REQUIRED",
        "message": "Name is required"
      },
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "code": "TOO_YOUNG",
        "message": "Age must be at least 18"
      }
    ]
  }
}
```

## API Design Best Practices

### Consistent Naming Conventions
```http
# Good: Consistent naming
GET /api/v1/users
GET /api/v1/products
GET /api/v1/orders

# Avoid: Inconsistent naming
GET /api/v1/user-list    # Inconsistent with other endpoints
GET /api/v1/getProducts  # Inconsistent verb usage
```

### Use Proper HTTP Methods
```http
# Good: Proper method usage
GET /users     # Retrieve users
POST /users    # Create user
PUT /users/123 # Update user
DELETE /users/123 # Delete user

# Avoid: Misusing methods
GET /users/delete?id=123  # Should use DELETE method
POST /users/123           # Should use PUT/PATCH for updates
```

### Handle Query Parameters Consistently
```http
# Good: Consistent query parameter usage
GET /users?status=active&sort=name&order=asc&limit=10&page=1

# Standard parameters:
# - page/offset: for pagination
# - limit: for pagination
# - sort: for sorting
# - order: for sort direction
# - search: for search queries
# - filter: for filtering
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing API structure, current endpoints, response formats, authentication methods |
| **Conversation** | User's specific requirements for API endpoints, resource relationships, business logic |
| **Skill References** | RESTful API patterns from `references/` (naming, responses, error handling) |
| **User Guidelines** | Project-specific conventions, team standards, security requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).