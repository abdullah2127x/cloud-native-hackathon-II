# RESTful API Design - Best Practices and Common Patterns

## Resource Naming Best Practices

### ✅ DO: Use Plural Nouns for Collections
```http
# Good: Plural nouns for resource collections
GET /users          # All users
GET /products       # All products
GET /orders         # All orders

# Good: Nested resources
GET /users/123/orders     # All orders for user 123
GET /products/456/reviews # All reviews for product 456
```

### ❌ AVOID: Inconsistent Naming
```http
# Avoid: Mixing singular and plural
GET /user           # Inconsistent with other resources
GET /products       # Should be consistent
GET /category/123   # Should be /categories/123
```

### ✅ DO: Use Descriptive and Consistent Names
```http
# Good: Clear, descriptive names
GET /users
GET /products
GET /categories
GET /orders
GET /reviews

# Good: Consistent naming across the API
GET /api/v1/users
GET /api/v1/products
GET /api/v1/categories
# All follow the same pattern
```

### ✅ DO: Use Hyphens for Multi-Word Resources
```http
# Good: Use hyphens for readability
GET /user-profiles
GET /order-items
GET /shopping-carts
GET /api-keys

# Avoid: Underscores or camelCase in URLs
GET /user_profiles  # Not recommended
GET /userProfiles   # Not recommended
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

# PUT: Update entire resource
PUT /users/123      # Replace entire user resource

# PATCH: Partial updates
PATCH /users/123    # Update specific fields only

# DELETE: Remove resources
DELETE /users/123   # Delete specific user
```

### ❌ AVOID: Misusing HTTP Methods
```http
# Avoid: Using GET for modifications
GET /users/123?delete=true  # Should be DELETE /users/123

# Avoid: Using POST for everything
POST /users/123/update      # Should be PUT or PATCH /users/123
POST /users/123/delete      # Should be DELETE /users/123

# Avoid: Using PUT for partial updates
PUT /users/123 {"name": "New Name"}  # PUT should include complete resource
```

## Status Code Best Practices

### ✅ DO: Use Appropriate Status Codes
```http
# 2xx Success
200 OK: GET, PUT, PATCH (when returning updated resource)
201 Created: POST (when resource is created)
204 No Content: DELETE, PUT, PATCH (when not returning resource)

# 4xx Client Errors
400 Bad Request: Invalid request format
401 Unauthorized: Authentication required
403 Forbidden: Authenticated but not authorized
404 Not Found: Resource doesn't exist
409 Conflict: Resource already exists
422 Unprocessable Entity: Validation errors

# 5xx Server Errors
500 Internal Server Error: Unexpected server error
503 Service Unavailable: Server temporarily unavailable
```

### ✅ DO: Handle Status Codes Consistently
```typescript
// Good: Consistent error handling
function handleApiError(status: number, error: any) {
  switch (status) {
    case 400:
      return { code: 'BAD_REQUEST', message: error.message };
    case 401:
      return { code: 'UNAUTHORIZED', message: 'Authentication required' };
    case 403:
      return { code: 'FORBIDDEN', message: 'Access denied' };
    case 404:
      return { code: 'NOT_FOUND', message: 'Resource not found' };
    case 422:
      return { code: 'VALIDATION_ERROR', message: 'Validation failed', details: error.details };
    default:
      return { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' };
  }
}
```

## Response Format Best Practices

### ✅ DO: Use Consistent Response Structure
```json
{
  "success": true,
  "data": {
    // Resource data here
  },
  "message": "Operation completed successfully"
}
```

### ✅ DO: Include Metadata in List Responses
```json
{
  "success": true,
  "data": [
    // Array of resources
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10
  },
  "message": "Resources retrieved successfully"
}
```

### ✅ DO: Format Error Responses Consistently
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
      }
    ]
  }
}
```

## Query Parameter Best Practices

### ✅ DO: Use Standard Query Parameter Names
```http
# Pagination
GET /users?page=1&limit=10

# Sorting
GET /users?sort=name&order=asc

# Filtering
GET /users?status=active&role=user

# Search
GET /users?search=john

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

## Error Handling Best Practices

### ✅ DO: Provide Meaningful Error Messages
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "The requested user does not exist",
    "timestamp": "2024-01-01T12:00:00Z",
    "path": "/users/999"
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
    user: context.userId || 'anonymous'
  });
}
```

## Security Best Practices

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

### ✅ DO: Validate Input Data
```typescript
// Good: Input validation
function validateUserInput(input: any) {
  const errors = [];

  if (!input.email || typeof input.email !== 'string') {
    errors.push({ field: 'email', message: 'Email is required and must be a string' });
  }

  if (!input.name || input.name.length < 2) {
    errors.push({ field: 'name', message: 'Name must be at least 2 characters' });
  }

  return errors;
}
```

### ✅ DO: Sanitize Sensitive Data
```typescript
// Good: Sanitize sensitive data before sending
function sanitizeUserResponse(user: any) {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    createdAt: user.createdAt,
    // Don't include sensitive fields like password, tokens, etc.
  };
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

### ❌ Anti-pattern: Returning Too Much Data
```json
// Avoid: Returning full nested objects when not needed
{
  "user": {
    "id": 123,
    "name": "John",
    "orders": [
      {
        "id": 456,
        "items": [
          {
            "id": 789,
            "product": {
              "id": 101,
              "name": "Product",
              "description": "Full product details...",
              "specifications": { /* lots of data */ }
            }
          }
        ]
      }
    ]
  }
}

// Better: Return references or limited data
{
  "user": {
    "id": 123,
    "name": "John",
    "orderIds": [456]
  }
}
```

## Testing Best Practices

### ✅ DO: Test API Endpoints Thoroughly
```typescript
// Good: Comprehensive API testing
describe('Users API', () => {
  it('should create a user with valid data', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({
        name: 'John Doe',
        email: 'john@example.com'
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.name).toBe('John Doe');
  });

  it('should return 422 for invalid data', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({
        name: '',  // Invalid - empty name
        email: 'invalid-email'  // Invalid email
      });

    expect(response.status).toBe(422);
    expect(response.body.success).toBe(false);
    expect(response.body.error.details).toHaveLength(2);
  });

  it('should return 404 for non-existent user', async () => {
    const response = await request(app)
      .get('/api/v1/users/999999');

    expect(response.status).toBe(404);
    expect(response.body.success).toBe(false);
  });
});
```

### ✅ DO: Test Edge Cases
```typescript
// Good: Test edge cases
describe('Pagination', () => {
  it('should handle page 0', async () => {
    const response = await request(app).get('/api/v1/users?page=0&limit=10');
    // Should either return page 1 or proper error
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

## Documentation Best Practices

### ✅ DO: Maintain API Documentation
```yaml
# Good: OpenAPI specification
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - email
              properties:
                name:
                  type: string
                  minLength: 2
                email:
                  type: string
                  format: email
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    $ref: '#/components/schemas/User'
```

### ✅ DO: Include Example Requests/Responses
```markdown
## Create User

**POST** `/api/v1/users`

### Request
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Response (201 Created)
```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

### Error Response (422 Unprocessable Entity)
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
      }
    ]
  }
}
```