/**
 * 小遥配配 B端 - 用户状态管理
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { MerchantUser, LoginRequest, RegisterRequest } from '@/types'
import * as authApi from '@/api/auth'
import { tokenManager } from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string | null>(tokenManager.getToken())
  const user = ref<MerchantUser | null>(null)
  const isLoading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const shopName = computed(() => user.value?.shop_name || '')
  const userName = computed(() => user.value?.username || '')

  // 登录
  async function login(credentials: LoginRequest) {
    isLoading.value = true
    try {
      const res = await authApi.login(credentials)

      // 保存Token（res.data 是 ApiResponse，res.data.data 才是 AuthResponse）
      token.value = res.data.data.token
      tokenManager.setToken(res.data.data.token)

      // 保存用户信息
      user.value = res.data.data.user as MerchantUser
      localStorage.setItem('user', JSON.stringify(user.value))

      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || '登录失败'
      }
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  async function register(data: RegisterRequest) {
    isLoading.value = true
    try {
      const res = await authApi.register(data)

      // 注册成功后自动登录（res.data 是 ApiResponse，res.data.data 才是 AuthResponse）
      token.value = res.data.data.token
      tokenManager.setToken(res.data.data.token)
      user.value = res.data.data.user as MerchantUser
      localStorage.setItem('user', JSON.stringify(user.value))

      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || '注册失败'
      }
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户信息
  async function fetchUserInfo() {
    if (!token.value) return

    isLoading.value = true
    try {
      const res = await authApi.getCurrentUser()
      user.value = res.data.data as MerchantUser
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch (error) {
      console.error('获取用户信息失败', error)
    } finally {
      isLoading.value = false
    }
  }

  // 退出登录
  function logout() {
    token.value = null
    user.value = null
    tokenManager.removeToken()
    localStorage.removeItem('user')
  }

  // 初始化：从localStorage恢复用户信息
  function init() {
    const savedToken = tokenManager.getToken()
    const savedUser = localStorage.getItem('user')
    if (savedToken && savedUser) {
      token.value = savedToken
      try {
        user.value = JSON.parse(savedUser)
      } catch {
        user.value = null
      }
    }
  }

  // 初始化
  init()

  return {
    // 状态
    token,
    user,
    isLoading,
    // 计算属性
    isLoggedIn,
    shopName,
    userName,
    // 方法
    login,
    register,
    fetchUserInfo,
    logout
  }
})
