import request from './request'
import type { ApiResponse, TopicListDto } from '@/types/api'

export async function listTopics(keyword?: string, limit = 20): Promise<TopicListDto> {
  const response = await request.get<ApiResponse<TopicListDto>>('/topics', {
    params: { keyword, limit },
  })
  return response.data.data
}

export async function listHotTopics(limit = 8): Promise<TopicListDto> {
  const response = await request.get<ApiResponse<TopicListDto>>('/topics/hot', {
    params: { limit },
  })
  return response.data.data
}
