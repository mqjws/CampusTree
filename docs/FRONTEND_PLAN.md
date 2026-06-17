# CampusTree Frontend Plan

This document defines the Vue3 frontend implementation plan for the current CampusTree backend.

## Tech Stack

- Vue3
- Vite
- Element Plus
- Pinia
- Axios
- Vue Router
- TypeScript is recommended for API types and store contracts.

## Frontend Directory Structure

```text
frontend/
  src/
    api/
      request.ts
      user.ts
      post.ts
      comment.ts
      like.ts
      types.ts
    assets/
    components/
      AppHeader.vue
      PostCard.vue
      CommentList.vue
      CommentForm.vue
      EmptyState.vue
      LoadingState.vue
    layouts/
      MainLayout.vue
      AuthLayout.vue
    router/
      index.ts
    stores/
      auth.ts
      post.ts
      comment.ts
    styles/
      index.css
    views/
      Login.vue
      Register.vue
      Home.vue
      PostDetail.vue
      CreatePost.vue
      UserCenter.vue
    App.vue
    main.ts
```

## Page Plan

### Login

Purpose:

- User login.
- Persist JWT token.
- Load current user after login.

Main UI:

- Account input.
- Password input.
- Login button.
- Link to Register.

API:

- `POST /api/v1/users/login`
- `GET /api/v1/users/me`

### Register

Purpose:

- Create a new user account.

Main UI:

- Username input.
- Email input.
- Password input.
- Register button.
- Link to Login.

API:

- `POST /api/v1/users/register`

### Home

Purpose:

- Main post feed.

Main UI:

- Header with login state.
- Post list.
- Pagination.
- Create post entry for authenticated users.

API:

- `GET /api/v1/posts`
- `POST /api/v1/posts/{post_id}/like`
- `DELETE /api/v1/posts/{post_id}/like`

Note:

- The current backend does not return like count or whether the current user liked each post. MVP can show like action feedback only after user interaction.

### PostDetail

Purpose:

- Show one post and its comments.

Main UI:

- Post title/content.
- Author id.
- Created/updated time.
- Like/unlike button.
- Comment list.
- Comment form for authenticated users.
- Edit/delete actions for owner where applicable.

API:

- `GET /api/v1/posts/{post_id}`
- `PATCH /api/v1/posts/{post_id}`
- `DELETE /api/v1/posts/{post_id}`
- `GET /api/v1/comments/posts/{post_id}/comments`
- `POST /api/v1/comments/posts/{post_id}/comments`
- `PATCH /api/v1/comments/{comment_id}`
- `DELETE /api/v1/comments/{comment_id}`
- `POST /api/v1/posts/{post_id}/like`
- `DELETE /api/v1/posts/{post_id}/like`

### CreatePost

Purpose:

- Create a new post.

Main UI:

- Title input.
- Content textarea.
- Submit button.
- Cancel/back button.

API:

- `POST /api/v1/posts`

Route guard:

- Requires authenticated user.

### UserCenter

Purpose:

- Display current user information.

Main UI:

- Username.
- Email.
- Avatar placeholder.
- Account status.
- Logout button.

API:

- `GET /api/v1/users/me`

## Pinia Store Design

### `stores/auth.ts`

State:

```ts
interface AuthState {
  token: string | null;
  user: UserRead | null;
  initialized: boolean;
}
```

Actions:

- `login(account, password)`
- `register(payload)`
- `fetchCurrentUser()`
- `logout()`
- `restoreToken()`

Responsibilities:

- Persist token.
- Clear token on logout or `401`.
- Provide `isAuthenticated` getter.

### `stores/post.ts`

State:

```ts
interface PostState {
  items: PostRead[];
  current: PostRead | null;
  total: number;
  page: number;
  size: number;
  loading: boolean;
}
```

Actions:

- `fetchPosts(page, size)`
- `fetchPost(id)`
- `createPost(payload)`
- `updatePost(id, payload)`
- `deletePost(id)`
- `likePost(id)`
- `unlikePost(id)`

### `stores/comment.ts`

State:

```ts
interface CommentState {
  items: CommentRead[];
  total: number;
  page: number;
  size: number;
  loading: boolean;
}
```

Actions:

- `fetchComments(postId, page, size)`
- `createComment(postId, content)`
- `updateComment(commentId, content)`
- `deleteComment(commentId)`

## Axios Wrapper Design

File:

```text
src/api/request.ts
```

Design:

- Base URL: `/api/v1` in development proxy, or environment variable `VITE_API_BASE_URL`.
- Request interceptor attaches `Authorization: Bearer <token>`.
- Response interceptor unwraps backend format.
- `401` clears auth store and redirects to Login.
- Business errors display `message` from backend.
- `422` displays validation summary.

Recommended response type:

```ts
export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}
```

Example:

```ts
import axios from "axios";

export const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  timeout: 10000,
});

request.interceptors.request.use((config) => {
  const token = localStorage.getItem("campustree_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## Token Persistence

Storage:

```text
localStorage key: campustree_token
```

Flow:

1. Login succeeds.
2. Save `access_token` to localStorage.
3. Save user info to Pinia.
4. On app startup, read token from localStorage.
5. If token exists, call `/users/me`.
6. If `/users/me` returns `401`, clear token and redirect to Login.

Logout:

1. Clear localStorage token.
2. Clear Pinia user state.
3. Redirect to Login or Home.

## Page Development Order

1. Project setup: Vite, Vue Router, Pinia, Element Plus, Axios.
2. API types and Axios wrapper.
3. Auth store, Login, Register.
4. Main layout and route guards.
5. Home post list with pagination.
6. PostDetail page.
7. CreatePost page.
8. Comment list and comment form.
9. Like/unlike interactions.
10. UserCenter and logout.
11. Error states, loading states, empty states.

## MVP UI Design

Style direction:

- Quiet, practical, content-first campus community UI.
- Use Element Plus components consistently.
- Avoid decorative landing page patterns.
- Prioritize readable post lists and fast navigation.

Layout:

- Top navigation bar with app name, Home, Create Post, User Center, Login/Logout.
- Main content max width around `960px`.
- Feed uses clean post rows or compact cards.
- Post detail uses a single-column reading layout.
- Comments sit below post content.

Core components:

- `AppHeader.vue`
- `PostCard.vue`
- `CommentList.vue`
- `CommentForm.vue`
- `EmptyState.vue`
- `LoadingState.vue`

Element Plus components:

- `ElForm`, `ElInput`, `ElButton` for auth and post forms.
- `ElCard` or simple bordered containers for post items.
- `ElPagination` for post/comment pagination.
- `ElMessage` for success/error feedback.
- `ElDialog` for delete confirmation.

MVP interaction rules:

- Anonymous users can view posts and comments.
- Anonymous users are redirected to Login when creating posts, commenting, liking, editing, or deleting.
- Only owner actions should be shown for post/comment edit and delete when `author_id === currentUser.id`.
- API `403` should show a permission error.
- API `404` should show a not-found state.

## Current Backend Notes For Frontend

- Comment routes currently use `/comments/posts/{post_id}/comments`, not `/posts/{post_id}/comments`.
- Like routes use `/posts/{post_id}/like`.
- The backend does not currently expose like counts, comment counts, author profile details, or current user's liked status in post list responses.
- Swagger response schemas are incomplete because backend routes do not declare `response_model`; use this document and source schemas as the integration reference.
