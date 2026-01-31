# API v1 Reference

**Base URL**: `/api/v1`

## Users
### `POST /users/`
Create a new user.

**Request Body (JSON)**:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe", 
  "is_active": true
}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "roles": [] 
}
```

---

### `GET /users/`
List all users.

**Parameters**:
- `skip`: (int, default=0) Number of records to skip.
- `limit`: (int, default=100) Max records to return.

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "roles": [...]
  }
]

---

## Roles
### `GET /roles/`
List all roles.

### `POST /roles/`
Create a new role.
```json
{
  "name": "manager",
  "description": "Store Manager",
  "permissions": ["users.view", "users.edit"]
}
```

### `PUT /roles/{id}`
Update a role (name, description, or permissions).

### `DELETE /roles/{id}`
Delete a role.

---

## User Role Management
### `POST /users/{user_id}/roles/{role_id}`
Assign a role to a user.

### `DELETE /users/{user_id}/roles/{role_id}`
Remove a role from a user.

```
