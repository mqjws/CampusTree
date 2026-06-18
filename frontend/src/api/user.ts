import request from './request'
import type {
  ApiResponse,
  UpdatePasswordPayload,
  UserCommentListDto,
  UserPostListDto,
  UserStatsDto,
  UserDto,
} from '@/types/api'

export async function getCurrentUser(): Promise<UserDto> {
  const response = await request.get<ApiResponse<UserDto>>('/users/me')
  return response.data.data
}

export async function getMyPosts(): Promise<UserPostListDto> {
  const response = await request.get<ApiResponse<UserPostListDto>>('/users/me/posts')
  return response.data.data
}

export async function getMyComments(): Promise<UserCommentListDto> {
  const response = await request.get<ApiResponse<UserCommentListDto>>('/users/me/comments')
  return response.data.data
}

export async function getMyStats(): Promise<UserStatsDto> {
  const response = await request.get<ApiResponse<UserStatsDto>>('/users/me/stats')
  return response.data.data
}

export async function updateMyPassword(
  payload: UpdatePasswordPayload,
): Promise<{ updated: boolean }> {
  const response = await request.put<ApiResponse<{ updated: boolean }>>(
    '/users/me/password',
    payload,
  )
  return response.data.data
}
