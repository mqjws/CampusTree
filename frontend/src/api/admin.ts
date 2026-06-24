import request from './request'
import type {
  AdminPostListDto,
  AdminUserListDto,
  ApiResponse,
  DeletePostDto,
  PostReportDto,
  PostReportListDto,
  SensitiveWordCreatePayload,
  SensitiveWordDto,
  SensitiveWordListDto,
  UserDto,
} from '@/types/api'

export async function listUsers(keyword?: string): Promise<AdminUserListDto> {
  const response = await request.get<ApiResponse<AdminUserListDto>>('/admin/users', {
    params: { keyword },
  })
  return response.data.data
}

export async function updateUserStatus(userId: number, isActive: boolean): Promise<UserDto> {
  const response = await request.patch<ApiResponse<UserDto>>(`/admin/users/${userId}/status`, {
    is_active: isActive,
  })
  return response.data.data
}

export async function deleteUser(userId: number): Promise<{ deleted: boolean; user_id: number }> {
  const response = await request.delete<ApiResponse<{ deleted: boolean; user_id: number }>>(
    `/admin/users/${userId}`,
  )
  return response.data.data
}

export async function listPosts(keyword?: string): Promise<AdminPostListDto> {
  const response = await request.get<ApiResponse<AdminPostListDto>>('/admin/posts', {
    params: { keyword },
  })
  return response.data.data
}

export async function deleteAdminPost(postId: number): Promise<DeletePostDto> {
  const response = await request.delete<ApiResponse<DeletePostDto>>(`/admin/posts/${postId}`)
  return response.data.data
}

export async function listReports(status?: string): Promise<PostReportListDto> {
  const response = await request.get<ApiResponse<PostReportListDto>>('/admin/reports', {
    params: { status },
  })
  return response.data.data
}

export async function updateReportStatus(reportId: number, status: string): Promise<PostReportDto> {
  const response = await request.patch<ApiResponse<PostReportDto>>(`/admin/reports/${reportId}`, {
    status,
  })
  return response.data.data
}

export async function listSensitiveWords(keyword?: string): Promise<SensitiveWordListDto> {
  const response = await request.get<ApiResponse<SensitiveWordListDto>>('/admin/sensitive-words', {
    params: { keyword },
  })
  return response.data.data
}

export async function createSensitiveWord(
  payload: SensitiveWordCreatePayload,
): Promise<SensitiveWordDto> {
  const response = await request.post<ApiResponse<SensitiveWordDto>>(
    '/admin/sensitive-words',
    payload,
  )
  return response.data.data
}

export async function deleteSensitiveWord(
  wordId: number,
): Promise<{ deleted: boolean; word_id: number }> {
  const response = await request.delete<ApiResponse<{ deleted: boolean; word_id: number }>>(
    `/admin/sensitive-words/${wordId}`,
  )
  return response.data.data
}
