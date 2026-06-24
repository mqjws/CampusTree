import request from './request'
import type {
  ApiResponse,
  CreatePostPayload,
  DeletePostDto,
  LikePostDto,
  PaginatedData,
  PostDto,
  PostReportCreatePayload,
  PostReportDto,
  UnlikePostDto,
} from '@/types/api'

export type PostSort = 'latest' | 'hot' | 'views' | 'comments' | 'likes'

export async function listPosts(
  page = 1,
  size = 10,
  sort: PostSort = 'latest',
  category?: string,
  topicId?: number,
  keyword?: string,
): Promise<PaginatedData<PostDto>> {
  const response = await request.get<ApiResponse<PaginatedData<PostDto>>>('/posts', {
    params: { page, size, sort, category, topic_id: topicId, keyword },
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

export async function deletePost(postId: number): Promise<DeletePostDto> {
  const response = await request.delete<ApiResponse<DeletePostDto>>(`/posts/${postId}`)
  return response.data.data
}

export async function reportPost(
  postId: number,
  payload: PostReportCreatePayload,
): Promise<PostReportDto> {
  const response = await request.post<ApiResponse<PostReportDto>>(
    `/posts/${postId}/reports`,
    payload,
  )
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
