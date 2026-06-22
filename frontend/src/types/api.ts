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
  nickname: string
  email: string
  avatar_url: string | null
  role: string
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
  email_code: string
}

export interface EmailCodePayload {
  email: string
}

export interface EmailCodeDto {
  sent: boolean
  code?: string
}

export interface UpdatePasswordPayload {
  old_password: string
  new_password: string
}

export interface UpdateProfilePayload {
  nickname: string
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
  category: string
  author_id: number
  author_nickname: string
  topic_id: number | null
  topic_name: string | null
  allow_comments: boolean
  view_count: number
  comment_count: number
  like_count: number
  liked_by_current_user: boolean
  created_at: string
  updated_at: string
}

export interface CreatePostPayload {
  title: string
  content: string
  category: string
  topic_name?: string | null
  allow_comments: boolean
}

export interface TopicDto {
  id: number
  name: string
  post_count: number
  created_at: string
  updated_at: string
}

export interface TopicListDto {
  items: TopicDto[]
}

export interface CommentDto {
  id: number
  content: string
  author_id: number
  author_nickname: string | null
  post_id: number
  post_title: string | null
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
  view_count: number
  latest_post_at: string | null
  latest_comment_at: string | null
}

export interface UserActivityDto {
  date: string
  post_count: number
  comment_count: number
  like_count: number
  score: number
}

export interface UserActivityListDto {
  items: UserActivityDto[]
}

export interface SensitiveWordDto {
  id: number
  word: string
  created_at: string
}

export interface SensitiveWordListDto {
  items: SensitiveWordDto[]
  total: number
}

export interface SensitiveWordCreatePayload {
  word: string
}
