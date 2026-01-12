# RESTful API Design - Examples and Patterns

## Complete Example: User Management API

### API Specification
```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: API for managing user accounts and profiles
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
    description: Production server
paths:
  /users:
    get:
      tags:
        - Users
      summary: List all users
      description: Retrieve a list of all users with optional filtering and pagination
      parameters:
        - name: page
          in: query
          description: Page number for pagination
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 10
        - name: status
          in: query
          description: Filter users by status
          required: false
          schema:
            type: string
            enum: [active, inactive, suspended]
      responses:
        '200':
          description: List of users retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
    post:
      tags:
        - Users
      summary: Create a new user
      description: Create a new user account
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
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    $ref: '#/components/schemas/User'
                  message:
                    type: string
                    example: "User created successfully"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'
  /users/{id}:
    get:
      tags:
        - Users
      summary: Get user by ID
      description: Retrieve details of a specific user
      parameters:
        - name: id
          in: path
          required: true
          description: User ID
          schema:
            type: integer
      responses:
        '200':
          description: User retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'
    put:
      tags:
        - Users
      summary: Update user by ID
      description: Update all fields of a specific user
      parameters:
        - name: id
          in: path
          required: true
          description: User ID
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    $ref: '#/components/schemas/User'
                  message:
                    type: string
                    example: "User updated successfully"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'
    delete:
      tags:
        - Users
      summary: Delete user by ID
      description: Delete a specific user
      parameters:
        - name: id
          in: path
          required: true
          description: User ID
          schema:
            type: integer
      responses:
        '200':
          description: User deleted successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  message:
                    type: string
                    example: "User deleted successfully"
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
        - createdAt
      properties:
        id:
          type: integer
          example: 123
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          example: "John Doe"
        status:
          type: string
          enum: [active, inactive, suspended]
          example: "active"
        createdAt:
          type: string
          format: date-time
          example: "2024-01-01T00:00:00Z"
        updatedAt:
          type: string
          format: date-time
          example: "2024-01-01T00:00:00Z"
    CreateUserRequest:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          example: "John Doe"
        password:
          type: string
          format: password
          example: "securePassword123"
        status:
          type: string
          enum: [active, inactive]
          default: "active"
    UpdateUserRequest:
      type: object
      properties:
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          example: "John Doe"
        status:
          type: string
          enum: [active, inactive, suspended]
          example: "active"
    Pagination:
      type: object
      properties:
        page:
          type: integer
          example: 1
        limit:
          type: integer
          example: 10
        total:
          type: integer
          example: 100
        totalPages:
          type: integer
          example: 10
        hasNext:
          type: boolean
          example: true
        hasPrev:
          type: boolean
          example: false
    Error:
      type: object
      properties:
        success:
          type: boolean
          example: false
        error:
          type: object
          properties:
            code:
              type: string
              example: "VALIDATION_ERROR"
            message:
              type: string
              example: "Invalid input data"
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                    example: "email"
                  message:
                    type: string
                    example: "Email is required"
  responses:
    Unauthorized:
      description: Unauthorized - Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            success: false
            error:
              code: "UNAUTHORIZED"
              message: "Authentication required"
    Forbidden:
      description: Forbidden - Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            success: false
            error:
              code: "FORBIDDEN"
              message: "Insufficient permissions"
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            success: false
            error:
              code: "NOT_FOUND"
              message: "Resource not found"
    BadRequest:
      description: Bad request - Invalid input data
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            success: false
            error:
              code: "VALIDATION_ERROR"
              message: "Invalid input data"
              details:
                - field: "email"
                  message: "Email is required"
    Conflict:
      description: Conflict - Resource already exists
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            success: false
            error:
              code: "CONFLICT"
              message: "Resource already exists"