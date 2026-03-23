/**
 * 小遥配配 B端 - 用户状态管理
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { MerchantUser, LoginRequest, RegisterRequest } from '@/types'
import { mockUser, delay } from '@/utils/mockData'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem('token'))
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
      await delay(800)

      // Mock验证
      if (credentials.username === 'test' && credentials.password === '123456') {
        token.value = 'mock_token_' + Date.now()
        user.value = mockUser
        localStorage.setItem('token', token.value)
        localStorage.setItem('user', JSON.stringify(user.value))
        return { success: true }
      }

      // 允许任意用户名密码登录（原型模式）
      token.value = 'mock_token_' + Date.now()
      user.value = { ...mockUser, username: credentials.username }
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return { success: true }
    } catch (error) {
      return { success: false, message: '登录失败，请稍后重试' }
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  async function register(data: RegisterRequest) {
    isLoading.value = true
    try {
      await delay(1000)
      // 模拟注册成功后自动登录
      token.value = 'mock_token_' + Date.now()
      user.value = {
        ...mockUser,
        username: data.username,
        shop_name: data.shop_name,
        phone: data.phone
      }
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return { success: true }
    } catch (error) {
      return { success: false, message: '注册失败，请稍后重试' }
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户信息
  async function fetchUserInfo() {
    if (!token.value) return

    isLoading.value = true
    try {
      await delay(500)
      user.value = mockUser
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
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 初始化：从localStorage恢复用户信息
  function init() {
    const savedToken = localStorage.getItem('token')
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
