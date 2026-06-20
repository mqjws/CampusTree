import request from './request'
import type {
  ApiResponse,
  EmailCodeDto,
  EmailCodePayload,
  LoginDto,
  LoginPayload,
  RegisterPayload,
  UserDto,
} from '@/types/api'

export async function login(payload: LoginPayload): Promise<LoginDto> {
  const response = await request.post<ApiResponse<LoginDto>>('/users/login', payload)
  return response.data.data
}

export async function register(payload: RegisterPayload): Promise<UserDto> {
  const response = await request.post<ApiResponse<UserDto>>('/users/register', payload)
  return response.data.data
}

export async function sendEmailCode(payload: EmailCodePayload): Promise<EmailCodeDto> {
  const response = await request.post<ApiResponse<EmailCodeDto>>('/users/email-code', payload)
  return response.data.data
}

export async function getCurrentUser(): Promise<UserDto> {
  const response = await request.get<ApiResponse<UserDto>>('/users/me')
  return response.data.data
}
