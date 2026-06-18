import request from './request'
import type {
  ApiResponse,
  CreatePostPayload,
  LikePostDto,
  PaginatedData,
  PostDto,
  UnlikePostDto,
} from '@/types/api'

export async function listPosts(page = 1, size = 10): Promise<PaginatedData<PostDto>> {
  const response = await request.get<ApiResponse<PaginatedData<PostDto>>>('/posts', {
    params: { page, size },
  })
  return response.data.data
}

export async function getPostDetail(postId: number): Promise<PostDto> {
  const response = await request.get<ApiResponse<PostDto>>(`/posts/${postId}`)
  return response.data.data
}

export async function createPost(payload: CreatePostPayload): Promise<PostDto> {
  const response = await request.post<ApiResponse<PostDto>>('/posts', payload)
  return response.data.data
}

export async function likePost(postId: number): Promise<LikePostDto> {
  const response = await request.post<ApiResponse<LikePostDto>>(`/posts/${postId}/like`)
  return response.data.data
}

export async function unlikePost(postId: number): Promise<UnlikePostDto> {
  const response = await request.delete<ApiResponse<UnlikePostDto>>(`/posts/${postId}/like`)
  return response.data.data
}
