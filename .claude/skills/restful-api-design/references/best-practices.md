# RESTful API Design - Best Practices and Common Patterns

## Resource Naming Best Practices

### ✅ DO: Use Plural Nouns for Collections
```http
# Good: Plural nouns for resource collections
GET /users          # All users
GET /products       # All products
GET /orders         # All orders
GET /categories     # All categories

# Good: Nested resources
GET /users/123/orders     # All orders for user 123
GET /products/456/reviews # All reviews for product 456
GET /orders/789/items     # All items in order 789
```

### ❌ AVOID: Inconsistent Naming
```http
# Avoid: Mixing singular and plural
GET /user           # Inconsistent with other resources
GET /products       # Should be consistent
GET /category/123   # Should be /categories/123

# Avoid: Non-descriptive names
GET /data/123       # Not descriptive enough
GET /item/456       # Too generic
```

### ✅ DO: Use Descriptive and Consistent Names
```http
# Good: Clear, descriptive names
GET /users
GET /products
GET /orders
GET /customers
GET /reviews
GET /categories
GET /tags
GET /comments

# Good: Consistent naming across the API
GET /api/v1/users
GET /api/v1/products
GET /api/v1/orders
# All follow the same pattern
```

## HTTP Method Usage Best Practices

### ✅ DO: Use HTTP Methods Correctly
```http
# GET: Retrieve resources (safe, idempotent)
GET /users          # Get all users
GET /users/123      # Get specific user
GET /users/123/orders # Get user's orders

# POST: Create resources or trigger actions
POST /users         # Create new user
POST /users/123/orders # Create order for user
POST /users/123/password-reset # Trigger password reset

# PUT: Update entire resource (idempotent)
PUT /users/123      # Replace entire user resource
Content-Type: application/json

{
  "name": "New Name",
  "email": "new@example.com",
  "status": "active"
}

# PATCH: Partial updates (idempotent)
PATCH /users/123    # Update specific fields only
Content-Type: application/json

{
  "name": "Updated Name"
}

# DELETE: Remove resources (idempotent)
DELETE /users/123   # Delete specific user
```

### ✅ DO: Follow Idempotent Principles
```http
# Idempotent methods (safe to retry)
GET /users/123      # Always returns the same result
PUT /users/123      # Same request always produces same result
DELETE /users/123   # Same request always produces same result

# Non-idempotent methods (results may vary)
POST /users         # May create different resources each time
```

## Status Code Best Practices

### ✅ DO: Use Appropriate Status Codes
```http
# 2xx Success
200 OK: GET, PUT, PATCH (when returning updated resource)
201 Created: POST (when resource is created)
204 No Content: DELETE, PUT, PATCH (when not returning resource)
202 Accepted: Long-running operations (async processing)

# 4xx Client Errors
400 Bad Request: Invalid request format, validation errors
401 Unauthorized: Authentication required/failed
403 Forbidden: Authenticated but not authorized
404 Not Found: Resource doesn't exist
405 Method Not Allowed: Wrong HTTP method
409 Conflict: Resource already exists, version conflicts
422 Unprocessable Entity: Valid request but semantic errors
429 Too Many Requests: Rate limiting

# 5xx Server Errors
500 Internal Server Error: Unexpected server error
502 Bad Gateway: Upstream server error
503 Service Unavailable: Server temporarily unavailable
504 Gateway Timeout: Upstream server timeout
```

### ✅ DO: Be Specific with Error Responses
```http
# Good: Specific error response
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Invalid email format"
      }
    ]
  }
}

# Good: Resource not found
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "resource": "user",
    "id": "123"
  }
}
```

## Response Format Best Practices

### ✅ DO: Use Consistent Response Structure
```json
// Success response with data
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "message": "User retrieved successfully"
}

// Success response for list
{
  "success": true,
  "data": [
    {
      "id": 123,
      "name": "John Doe",
      "email": "john@example.com"
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

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      }
    ]
  }
}
```

### ✅ DO: Handle Empty Lists Properly
```json
// Good: Empty list response
{
  "success": true,
  "data": [],
  "message": "Users retrieved successfully",
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 0,
    "totalPages": 0
  }
}
```

## Query Parameter Best Practices

### ✅ DO: Use Standard Query Parameter Names
```http
# Pagination
GET /users?page=1&limit=10
GET /users?offset=0&limit=20

# Filtering
GET /users?status=active&role=admin
GET /products?category=electronics&minPrice=100&maxPrice=500

# Searching
GET /users?search=john
GET /products?search=laptop&q=gaming

# Sorting
GET /users?sort=name&order=asc
GET /users?sortBy=createdAt&sortOrder=desc

# Field selection (if supported)
GET /users?fields=id,name,email
```

### ✅ DO: Validate Query Parameters
```typescript
// Good: Validate query parameters
function validateQueryParams(params: any) {
  const errors = [];

  if (params.page && (!Number.isInteger(params.page) || params.page < 1)) {
    errors.push({ field: 'page', message: 'Page must be a positive integer' });
  }

  if (params.limit && (!Number.isInteger(params.limit) || params.limit < 1 || params.limit > 100)) {
    errors.push({ field: 'limit', message: 'Limit must be between 1 and 100' });
  }

  if (params.sort && !['name', 'email', 'createdAt'].includes(params.sort)) {
    errors.push({ field: 'sort', message: 'Invalid sort field' });
  }

  return errors;
}
```

## Pagination Best Practices

### ✅ DO: Implement Proper Pagination
```http
# Good: Standard pagination parameters
GET /users?page=1&limit=10
```

### ✅ DO: Include Pagination Metadata
```json
{
  "data": [
    // ... resources
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10,
    "hasNext": true,
    "hasPrev": false,
    "next": "/users?page=2&limit=10",
    "prev": null
  }
}
```

### ✅ DO: Handle Edge Cases in Pagination
```typescript
// Good: Handle pagination edge cases
function calculatePagination(total: number, page: number, limit: number) {
  const totalPages = Math.ceil(total / limit);
  const currentPage = Math.max(1, Math.min(page, totalPages || 1));
  const offset = (currentPage - 1) * limit;

  return {
    page: currentPage,
    limit,
    total,
    totalPages,
    offset,
    hasNext: currentPage < totalPages,
    hasPrev: currentPage > 1
  };
}
```

## Security Best Practices

### ✅ DO: Implement Proper Authentication
```http
# Good: JWT token in Authorization header
GET /users/123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Good: API Key in header (for service-to-service)
GET /users/123
X-API-Key: your-api-key-here
```

### ✅ DO: Validate Input Properly
```json
// Good: Input validation
{
  "email": "user@example.com",
  "name": "John Doe",
  "age": 30
}

// Good: Validation response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### ✅ DO: Implement Rate Limiting
```http
# Good: Rate limiting headers
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1609459200

# Rate limit exceeded
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

## Error Handling Best Practices

### ✅ DO: Provide Meaningful Error Messages
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "The requested user does not exist",
    "timestamp": "2024-01-01T12:00:00Z",
    "requestId": "req-12345"
  }
}
```

### ✅ DO: Include Validation Error Details
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
        "message": "Email must be a valid email address"
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

### ✅ DO: Log Errors Properly
```typescript
// Good: Log errors with context
function logApiError(error: any, context: any) {
  console.error('API Error:', {
    timestamp: new Date().toISOString(),
    error: error.message,
    stack: error.stack,
    context,
    userId: context.userId || 'anonymous',
    requestId: context.requestId
  });
}
```

## Performance Best Practices

### ✅ DO: Implement Caching Headers
```http
# Good: Caching headers for GET requests
GET /users/123
Cache-Control: max-age=300  # Cache for 5 minutes
ETag: "abc123"
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
```

### ✅ DO: Support Conditional Requests
```http
# Client request with conditional headers
GET /users/123
If-None-Match: "abc123"  # If resource hasn't changed

# Server response
HTTP/1.1 304 Not Modified  # If resource hasn't changed
# Or
HTTP/1.1 200 OK  # If resource has changed
```

### ✅ DO: Implement Field Selection (if needed)
```http
# Good: Allow clients to select specific fields
GET /users/123?fields=id,name,email

# Response with selected fields only
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
    // Other fields omitted
  }
}
```

## API Versioning Best Practices

### ✅ DO: Use URL Versioning (Recommended)
```http
# Good: URL versioning
GET /api/v1/users
POST /api/v1/users
GET /api/v2/users  # New version with breaking changes
```

### ✅ DO: Plan for Backward Compatibility
```typescript
// Good: Handle version compatibility
function handleUserResponse(user: any, version: string) {
  if (version === 'v1') {
    return {
      id: user.id,
      name: user.name,
      email: user.email
    };
  } else if (version === 'v2') {
    return {
      id: user.id,
      name: user.name,
      email: user.email,
      createdAt: user.createdAt,
      profile: {
        bio: user.bio,
        avatar: user.avatar
      }
    };
  }
}
```

## Common Anti-Patterns to Avoid

### ❌ Anti-pattern: Inconsistent Status Codes
```http
# Avoid: Inconsistent status codes
POST /users - Returns 200 instead of 201 when creating
DELETE /users/123 - Returns 200 with body instead of 204
GET /users/999 - Returns 200 with null instead of 404
```

### ❌ Anti-pattern: Inconsistent Response Formats
```json
// Avoid: Inconsistent response formats
// Sometimes returning just the data
GET /users/123 → {"id": 123, "name": "John"}

// Sometimes wrapping in data object
GET /users → {"data": [{"id": 123, "name": "John"}]}

// Be consistent: always use the same format
GET /users/123 → {"success": true, "data": {"id": 123, "name": "John"}}
GET /users → {"success": true, "data": [{"id": 123, "name": "John"}]}
```

### ❌ Anti-pattern: Generic Error Messages
```json
// Avoid: Generic error messages
{
  "error": "Something went wrong"  // Not helpful for debugging
}

// Good: Specific error messages
{
  "success": false,
  "error": {
    "code": "INVALID_EMAIL",
    "message": "The email address is invalid",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

### ❌ Anti-pattern: Exposing Internal Details
```json
// Avoid: Exposing internal server details
{
  "success": false,
  "error": {
    "message": "Internal Server Error: TypeError: Cannot read property 'name' of undefined at /path/to/file.js:123:45"
  }
}

// Good: Generic error with internal tracking
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "requestId": "req-12345"  // For internal tracking
  }
}
```

## Testing Best Practices

### ✅ DO: Test API Endpoints Properly
```typescript
// Good: API testing with different scenarios
describe('Users API', () => {
  it('should return 200 and user data when user exists', async () => {
    const response = await request(app)
      .get('/api/v1/users/123')
      .set('Authorization', 'Bearer valid-token');

    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
    expect(response.body.data.id).toBe(123);
  });

  it('should return 404 when user does not exist', async () => {
    const response = await request(app)
      .get('/api/v1/users/999')
      .set('Authorization', 'Bearer valid-token');

    expect(response.status).toBe(404);
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('USER_NOT_FOUND');
  });

  it('should return 401 when no token provided', async () => {
    const response = await request(app)
      .get('/api/v1/users/123');

    expect(response.status).toBe(401);
  });
});
```

### ✅ DO: Test Edge Cases
```typescript
// Good: Test edge cases
describe('Pagination', () => {
  it('should handle page 0', async () => {
    const response = await request(app).get('/api/v1/users?page=0&limit=10');
    // Should either return page 1 or proper validation error
  });

  it('should handle large page numbers', async () => {
    const response = await request(app).get('/api/v1/users?page=999999&limit=10');
    // Should return empty results or last page
  });

  it('should handle invalid limit', async () => {
    const response = await request(app).get('/api/v1/users?limit=0');
    // Should return validation error
  });
});
```

## Performance Optimization Patterns

### ✅ DO: Implement Proper Error Handling
```typescript
// Good: Proper error handling with appropriate status codes
async function getUser(req, res) {
  try {
    const user = await userService.findById(req.params.id);

    if (!user) {
      return res.status(404).json({
        success: false,
        error: {
          code: 'USER_NOT_FOUND',
          message: 'User not found'
        }
      });
    }

    return res.status(200).json({
      success: true,
      data: user,
      message: 'User retrieved successfully'
    });
  } catch (error) {
    // Log the actual error for debugging
    console.error('Error retrieving user:', error);

    // Return generic error to client
    return res.status(500).json({
      success: false,
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      }
    });
  }
}
```

### ✅ DO: Use Proper HTTP Headers
```http
# Good: Proper headers for security and performance
Content-Type: application/json
Content-Length: [length]
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
```