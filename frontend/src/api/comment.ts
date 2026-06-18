import request from './request'
import type { ApiResponse, CommentDto, CreateCommentPayload, PaginatedData } from '@/types/api'

export async function listCommentsByPost(
  postId: number,
  page = 1,
  size = 10,
): Promise<PaginatedData<CommentDto>> {
  const response = await request.get<ApiResponse<PaginatedData<CommentDto>>>(
    `/comments/posts/${postId}/comments`,
    {
      params: { page, size },
    },
  )
  return response.data.data
}

export async function createComment(
  postId: number,
  payload: CreateCommentPayload,
): Promise<CommentDto> {
  const response = await request.post<ApiResponse<CommentDto>>(
    `/comments/posts/${postId}/comments`,
    payload,
  )
  return response.data.data
}
