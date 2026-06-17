# CampusTree API Reference

This document describes the current CampusTree backend API for frontend integration.

Base URL:

```text
http://127.0.0.1:8000/api/v1
```

Swagger:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

## Common Response Format

Success:

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

Business error:

```json
{
  "code": 400,
  "message": "error message",
  "data": null
}
```

Validation errors currently use FastAPI's default `422` response format.

## Authentication

Protected endpoints require a Bearer token:

```http
Authorization: Bearer <access_token>
```

## User APIs

### Register

```http
POST /api/v1/users/register
```

JWT: No

Request body:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "password123"
}
```

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "avatar_url": null,
    "is_active": true,
    "created_at": "2026-06-17T10:00:00Z",
    "updated_at": "2026-06-17T10:00:00Z"
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 400 | `username already exists` |
| 400 | `email already exists` |
| 422 | Validation error |

### Login

```http
POST /api/v1/users/login
```

JWT: No

Request body:

```json
{
  "account": "alice",
  "password": "password123"
}
```

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "<jwt>",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "alice",
      "email": "alice@example.com",
      "avatar_url": null,
      "is_active": true,
      "created_at": "2026-06-17T10:00:00Z",
      "updated_at": "2026-06-17T10:00:00Z"
    }
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 400 | `invalid account or password` |
| 422 | Validation error |

### Current User

```http
GET /api/v1/users/me
```

JWT: Yes

Request body: None

Response body: `UserRead`

Errors:

| Status | Message |
|---:|---|
| 401 | `missing authorization token` |
| 401 | `invalid token` |
| 401 | `token expired` |

## Post APIs

### List Posts

```http
GET /api/v1/posts?page=1&size=10
```

JWT: No

Query:

| Name | Type | Default | Rule |
|---|---|---:|---|
| `page` | number | 1 | `>= 1` |
| `size` | number | 10 | `1..100` |

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "title": "Hello",
        "content": "CampusTree post content",
        "author_id": 1,
        "created_at": "2026-06-17T10:00:00Z",
        "updated_at": "2026-06-17T10:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10
  }
}
```

### Create Post

```http
POST /api/v1/posts
```

JWT: Yes

Request body:

```json
{
  "title": "Hello",
  "content": "CampusTree post content"
}
```

Response body: `PostRead`

Errors:

| Status | Message |
|---:|---|
| 401 | Authentication error |
| 422 | Validation error |

### Post Detail

```http
GET /api/v1/posts/{post_id}
```

JWT: No

Response body: `PostRead`

Errors:

| Status | Message |
|---:|---|
| 404 | `post not found` |

### Update Post

```http
PATCH /api/v1/posts/{post_id}
```

JWT: Yes

Request body:

```json
{
  "title": "Updated title",
  "content": "Updated content"
}
```

Response body: `PostRead`

Errors:

| Status | Message |
|---:|---|
| 401 | Authentication error |
| 403 | `forbidden` |
| 404 | `post not found` |
| 422 | Validation error |

### Delete Post

```http
DELETE /api/v1/posts/{post_id}
```

JWT: Yes

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "deleted": true,
    "post_id": 1
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 401 | Authentication error |
| 403 | `forbidden` |
| 404 | `post not found` |

## Comment APIs

### Create Comment

```http
POST /api/v1/comments/posts/{post_id}/comments
```

JWT: Yes

Request body:

```json
{
  "content": "Nice post"
}
```

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "content": "Nice post",
    "author_id": 1,
    "post_id": 1,
    "created_at": "2026-06-17T10:00:00Z",
    "updated_at": "2026-06-17T10:00:00Z"
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 401 | Authentication error |
| 404 | `post not found` |
| 422 | Validation error |

### List Comments By Post

```http
GET /api/v1/comments/posts/{post_id}/comments?page=1&size=10
```

JWT: No

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [],
    "total": 0,
    "page": 1,
    "size": 10
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 404 | `post not found` |
| 422 | Validation error |

### Comment Detail

```http
GET /api/v1/comments/{comment_id}
```

JWT: No

Response body: `CommentRead`

Errors:

| Status | Message |
|---:|---|
| 404 | `comment not found` |

### Update Comment

```http
PATCH /api/v1/comments/{comment_id}
```

JWT: Yes

Request body:

```json
{
  "content": "Updated comment"
}
```

Response body: `CommentRead`

Errors:

| Status | Message |
|---:|---|
| 401 | Authentication error |
| 403 | `forbidden` |
| 404 | `comment not found` |
| 422 | Validation error |

### Delete Comment

```http
DELETE /api/v1/comments/{comment_id}
```

JWT: Yes

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "deleted": true,
    "comment_id": 1
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 401 | Authentication error |
| 403 | `forbidden` |
| 404 | `comment not found` |

## Like APIs

### Like Post

```http
POST /api/v1/posts/{post_id}/like
```

JWT: Yes

Request body: None

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "post_id": 1,
    "created_at": "2026-06-17T10:00:00Z"
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 400 | `post already liked` |
| 401 | Authentication error |
| 404 | `post not found` |

### Unlike Post

```http
DELETE /api/v1/posts/{post_id}/like
```

JWT: Yes

Request body: None

Response body:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "deleted": true,
    "post_id": 1
  }
}
```

Errors:

| Status | Message |
|---:|---|
| 400 | `post not liked` |
| 401 | Authentication error |
| 404 | `post not found` |

## Frontend Axios Examples

### Axios Client

```ts
import axios from "axios";

export const api = axios.create({
  baseURL: "/api/v1",
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("campustree_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response.data,
  (error) => Promise.reject(error)
);
```

### Login

```ts
export function login(account: string, password: string) {
  return api.post("/users/login", { account, password });
}
```

### List Posts

```ts
export function listPosts(page = 1, size = 10) {
  return api.get("/posts", { params: { page, size } });
}
```

### Create Post

```ts
export function createPost(title: string, content: string) {
  return api.post("/posts", { title, content });
}
```

### Comment

```ts
export function createComment(postId: number, content: string) {
  return api.post(`/comments/posts/${postId}/comments`, { content });
}
```

### Like

```ts
export function likePost(postId: number) {
  return api.post(`/posts/${postId}/like`);
}

export function unlikePost(postId: number) {
  return api.delete(`/posts/${postId}/like`);
}
```
