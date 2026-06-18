export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  size: number
}

export interface UserDto {
  id: number
  username: string
  email: string
  avatar_url: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginPayload {
  account: string
  password: string
}

export interface RegisterPayload {
  username: string
  email: string
  password: string
}

export interface LoginDto {
  access_token: string
  token_type: string
  user: UserDto
}

export interface PostDto {
  id: number
  title: string
  content: string
  author_id: number
  created_at: string
  updated_at: string
}

export interface CreatePostPayload {
  title: string
  content: string
}

export interface CommentDto {
  id: number
  content: string
  author_id: number
  post_id: number
  created_at: string
  updated_at: string
}

export interface CreateCommentPayload {
  content: string
}

export interface LikePostDto {
  id: number
  user_id: number
  post_id: number
  created_at: string
}

export interface UnlikePostDto {
  deleted: boolean
  post_id: number
}

export interface UserPostListDto {
  items: PostDto[]
}

export interface UserCommentListDto {
  items: CommentDto[]
}

export interface UserStatsDto {
  post_count: number
  comment_count: number
  like_count: number
}
