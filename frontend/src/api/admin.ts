import request from './request'
import type { ApiResponse, SensitiveWordCreatePayload, SensitiveWordDto, SensitiveWordListDto } from '@/types/api'

export async function listSensitiveWords(keyword?: string): Promise<SensitiveWordListDto> {
  const response = await request.get<ApiResponse<SensitiveWordListDto>>('/admin/sensitive-words', {
    params: { keyword },
  })
  return response.data.data
}

export async function createSensitiveWord(payload: SensitiveWordCreatePayload): Promise<SensitiveWordDto> {
  const response = await request.post<ApiResponse<SensitiveWordDto>>('/admin/sensitive-words', payload)
  return response.data.data
}

export async function deleteSensitiveWord(wordId: number): Promise<{ deleted: boolean; word_id: number }> {
  const response = await request.delete<ApiResponse<{ deleted: boolean; word_id: number }>>(`/admin/sensitive-words/${wordId}`)
  return response.data.data
}
