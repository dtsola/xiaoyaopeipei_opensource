/**
 * 认证模块 API
 */

import { get, post, put, tokenManager } from '@/utils/request'
import type { LoginRequest, RegisterRequest, AuthResponse, MerchantUser } from '@/types'

/**
 * 商家注册
 */
export function register(data: RegisterRequest) {
  return post<AuthResponse>('/auth/register', data)
}

/**
 * 商家登录
 */
export function login(data: LoginRequest) {
  return post<AuthResponse>('/auth/login', data)
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser() {
  return get<MerchantUser>('/auth/me')
}

/**
 * 更新用户信息
 */
export function updateCurrentUser(data: Partial<MerchantUser>) {
  return put<MerchantUser>('/auth/me', data)
}

/**
 * 修改密码
 */
export function updatePassword(data: { old_password: string; new_password: string }) {
  return put('/auth/password', data)
}

/**
 * 登出
 */
export function logout() {
  tokenManager.removeToken()
  return post('/auth/logout')
}

/**
 * 会员续期
 */
export function renewMembership(data: { days: number }) {
  return post<{ membership_expiry: string }>('/auth/membership/renew', data)
}
