# RESTful API Design - Additional Examples

## Complete API Design Example: E-commerce System

### API Structure
```
/api/v1/
├── auth/
│   ├── POST /login
│   ├── POST /register
│   ├── POST /logout
│   └── GET /me
├── users/
│   ├── GET /users
│   ├── POST /users
│   ├── GET /users/{id}
│   ├── PUT /users/{id}
│   ├── PATCH /users/{id}
│   └── DELETE /users/{id}
├── products/
│   ├── GET /products
│   ├── POST /products
│   ├── GET /products/{id}
│   ├── PUT /products/{id}
│   ├── PATCH /products/{id}
│   └── DELETE /products/{id}
├── categories/
│   ├── GET /categories
│   ├── POST /categories
│   ├── GET /categories/{id}
│   ├── PUT /categories/{id}
│   ├── PATCH /categories/{id}
│   └── DELETE /categories/{id}
├── orders/
│   ├── GET /orders
│   ├── POST /orders
│   ├── GET /orders/{id}
│   ├── PUT /orders/{id}
│   ├── PATCH /orders/{id}
│   └── DELETE /orders/{id}
├── orders/{orderId}/items/
│   ├── GET /orders/{orderId}/items
│   ├── POST /orders/{orderId}/items
│   ├── GET /orders/{orderId}/items/{itemId}
│   ├── PUT /orders/{orderId}/items/{itemId}
│   ├── PATCH /orders/{orderId}/items/{itemId}
│   └── DELETE /orders/{orderId}/items/{itemId}
└── reviews/
    ├── GET /reviews
    ├── POST /reviews
    ├── GET /reviews/{id}
    ├── PUT /reviews/{id}
    ├── PATCH /reviews/{id}
    └── DELETE /reviews/{id}
```

### Complete User Resource Implementation

#### User Model Definition
```typescript
// models/user.ts
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  role: 'admin' | 'moderator' | 'user';
  status: 'active' | 'inactive' | 'suspended';
  createdAt: string;
  updatedAt: string;
  lastLoginAt?: string;
}
```

#### User API Endpoints Implementation

**Create User**
```http
POST /api/v1/users
Content-Type: application/json

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
    "status": "active",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z"
  },
  "message": "User created successfully"
}
```

**Get All Users with Filtering**
```http
GET /api/v1/users?status=active&role=user&page=1&limit=10&sort=name&order=asc
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": [
    {
      "id": 123,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "age": 28,
      "role": "user",
      "status": "active",
      "createdAt": "2024-01-01T10:00:00Z",
      "updatedAt": "2024-01-01T10:00:00Z"
    },
    {
      "id": 124,
      "name": "Bob Smith",
      "email": "bob@example.com",
      "age": 35,
      "role": "user",
      "status": "active",
      "createdAt": "2024-01-01T11:00:00Z",
      "updatedAt": "2024-01-01T11:00:00Z"
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

**Get Single User**
```http
GET /api/v1/users/123
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
    "status": "active",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z",
    "lastLoginAt": "2024-01-01T13:00:00Z"
  },
  "message": "User retrieved successfully"
}
```

**Update User (Full Update)**
```http
PUT /api/v1/users/123
Content-Type: application/json

{
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "age": 31,
  "role": "moderator",
  "status": "active"
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
    "role": "moderator",
    "status": "active",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T14:00:00Z"
  },
  "message": "User updated successfully"
}
```

**Partial Update User**
```http
PATCH /api/v1/users/123
Content-Type: application/json

{
  "name": "John Updated",
  "age": 32
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Updated",
    "email": "johnsmith@example.com",
    "age": 32,
    "role": "moderator",
    "status": "active",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T15:00:00Z"
  },
  "message": "User updated successfully"
}
```

**Delete User**
```http
DELETE /api/v1/users/123
```

```http
HTTP/1.1 204 No Content
```

### Complete Product Resource Implementation

#### Product Model Definition
```typescript
// models/product.ts
interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  stock: number;
  status: 'active' | 'inactive' | 'discontinued';
  createdAt: string;
  updatedAt: string;
  images: string[];
  specifications?: Record<string, any>;
}
```

#### Product API Endpoints

**Create Product**
```http
POST /api/v1/products
Content-Type: application/json

{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "category": "electronics",
  "stock": 50,
  "images": ["https://example.com/image1.jpg"],
  "specifications": {
    "processor": "Intel i7",
    "memory": "16GB",
    "storage": "512GB SSD"
  }
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 456,
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "category": "electronics",
    "stock": 50,
    "status": "active",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z",
    "images": ["https://example.com/image1.jpg"],
    "specifications": {
      "processor": "Intel i7",
      "memory": "16GB",
      "storage": "512GB SSD"
    }
  },
  "message": "Product created successfully"
}
```

**Get Products with Filtering and Search**
```http
GET /api/v1/products?category=electronics&minPrice=500&maxPrice=1500&search=laptop&page=1&limit=10
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": [
    {
      "id": 456,
      "name": "Laptop",
      "description": "High-performance laptop",
      "price": 999.99,
      "category": "electronics",
      "stock": 50,
      "status": "active",
      "createdAt": "2024-01-01T12:00:00Z",
      "updatedAt": "2024-01-01T12:00:00Z",
      "images": ["https://example.com/image1.jpg"]
    }
  ],
  "message": "Products retrieved successfully",
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1,
    "hasNext": false,
    "hasPrev": false
  }
}
```

### Order Resource Implementation

#### Order Model Definition
```typescript
// models/order.ts
interface Order {
  id: number;
  userId: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  totalAmount: number;
  items: OrderItem[];
  shippingAddress: Address;
  billingAddress: Address;
  createdAt: string;
  updatedAt: string;
  paymentMethod: string;
  paymentStatus: 'pending' | 'completed' | 'failed';
}

interface OrderItem {
  id: number;
  productId: number;
  productName: string;
  quantity: number;
  price: number;
  subtotal: number;
}

interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}
```

#### Order API Endpoints

**Create Order**
```http
POST /api/v1/orders
Content-Type: application/json

{
  "userId": 123,
  "items": [
    {
      "productId": 456,
      "quantity": 2
    }
  ],
  "shippingAddress": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipCode": "10001",
    "country": "USA"
  },
  "billingAddress": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipCode": "10001",
    "country": "USA"
  },
  "paymentMethod": "credit_card"
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 789,
    "userId": 123,
    "status": "pending",
    "totalAmount": 1999.98,
    "items": [
      {
        "id": 101,
        "productId": 456,
        "productName": "Laptop",
        "quantity": 2,
        "price": 999.99,
        "subtotal": 1999.98
      }
    ],
    "shippingAddress": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zipCode": "10001",
      "country": "USA"
    },
    "billingAddress": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zipCode": "10001",
      "country": "USA"
    },
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z",
    "paymentMethod": "credit_card",
    "paymentStatus": "pending"
  },
  "message": "Order created successfully"
}
```

## Advanced API Patterns

### Search and Filtering API

#### Advanced Search Endpoint
```http
GET /api/v1/products/search?q=laptop&category=electronics&minPrice=500&maxPrice=1500&inStock=true&sort=price&order=asc&page=1&limit=20
```

#### Complex Filtering Response
```json
{
  "success": true,
  "data": [
    // ... filtered products
  ],
  "message": "Products searched successfully",
  "filters": {
    "query": "laptop",
    "category": "electronics",
    "priceRange": {
      "min": 500,
      "max": 1500
    },
    "inStock": true
  },
  "pagination": {
    // ... pagination data
  },
  "facets": {
    "categories": [
      {"name": "laptops", "count": 15},
      {"name": "desktops", "count": 8}
    ],
    "priceRanges": [
      {"range": "500-800", "count": 5},
      {"range": "800-1200", "count": 7},
      {"range": "1200-1500", "count": 3}
    ]
  }
}
```

### Bulk Operations API

#### Bulk Create Users
```http
POST /api/v1/users/bulk
Content-Type: application/json

{
  "users": [
    {
      "name": "User 1",
      "email": "user1@example.com"
    },
    {
      "name": "User 2",
      "email": "user2@example.com"
    }
  ]
}
```

#### Bulk Operation Response
```json
{
  "success": true,
  "data": {
    "created": [
      {
        "id": 123,
        "name": "User 1",
        "email": "user1@example.com"
      },
      {
        "id": 124,
        "name": "User 2",
        "email": "user2@example.com"
      }
    ],
    "failed": [],
    "summary": {
      "total": 2,
      "successful": 2,
      "failed": 0
    }
  },
  "message": "Bulk operation completed successfully"
}
```

### File Upload API

#### Upload File Endpoint
```http
POST /api/v1/upload
Content-Type: multipart/form-data

# File upload with metadata
```

#### Upload Response
```json
{
  "success": true,
  "data": {
    "fileId": "abc123",
    "filename": "document.pdf",
    "originalName": "my-document.pdf",
    "size": 1024000,
    "mimeType": "application/pdf",
    "url": "https://cdn.example.com/files/abc123.pdf",
    "uploadDate": "2024-01-01T12:00:00Z"
  },
  "message": "File uploaded successfully"
}
```

### Webhook/Event API

#### Webhook Registration
```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "event": "order.created",
  "url": "https://your-app.com/webhook",
  "secret": "webhook-secret",
  "active": true
}
```

#### Event Response
```json
{
  "success": true,
  "data": {
    "id": 456,
    "event": "order.created",
    "url": "https://your-app.com/webhook",
    "active": true,
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z"
  },
  "message": "Webhook registered successfully"
}
```

### API Documentation Example

#### OpenAPI/Swagger Specification
```yaml
openapi: 3.0.0
info:
  title: E-commerce API
  version: 1.0.0
  description: RESTful API for e-commerce platform
servers:
  - url: https://api.example.com/v1
    description: Production server
paths:
  /users:
    get:
      summary: Get all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SuccessResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '422':
          $ref: '#/components/responses/ValidationError'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
        createdAt:
          type: string
          format: date-time
    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer
    SuccessResponse:
      type: object
      properties:
        success:
          type: boolean
          example: true
        data:
          type: object
        message:
          type: string
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ValidationErrorResponse'
```

## Real-World API Design Patterns

### API Gateway Pattern
```http
# API Gateway handles authentication, rate limiting, routing
POST /api/v1/users
Authorization: Bearer <token>
X-Request-ID: <uuid>

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Versioning Strategies

#### URL Versioning (Recommended)
```http
# Version in URL path
GET /api/v1/users
GET /api/v2/users
```

#### Header Versioning
```http
# Version in header
GET /api/users
Accept: application/vnd.myapi.v1+json
```

#### Query Parameter Versioning
```http
# Version in query parameter
GET /api/users?version=v1
```

### Rate Limiting Response
```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1609459200

{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "retryAfter": 60
  }
}
```

### API Health Check
```http
GET /api/v1/health
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "dependencies": {
    "database": "healthy",
    "cache": "healthy",
    "externalService": "degraded"
  }
}
```