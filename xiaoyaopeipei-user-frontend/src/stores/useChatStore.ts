/**
 * 对话状态管理
 * 管理对话消息、会话ID、用户需求等状态
 */

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { sessionManager } from '@/utils/request'
import type { ChatMessage, UserNeeds } from '@/types'

export const useChatStore = defineStore('chat', () => {
  // ========== 状态 ==========
  const messages = ref<ChatMessage[]>([])
  const sessionId = ref<string>('')
  const userNeeds = ref<Partial<UserNeeds>>({})
  const isLoading = ref(false)

  // ========== 计算属性 ==========
  const hasMessages = computed(() => messages.value.length > 0)
  const isComplete = computed(() => !!userNeeds.value.budget)

  // ========== 方法 ==========

  /**
   * 添加消息
   */
  const addMessage = (message: ChatMessage) => {
    messages.value.push(message)
  }

  /**
   * 更新会话ID
   */
  const updateSessionId = (newSessionId: string) => {
    sessionId.value = newSessionId
    sessionManager.setSessionId(newSessionId)
  }

  /**
   * 更新用户需求
   */
  const updateUserNeeds = (needs: Partial<UserNeeds>) => {
    Object.assign(userNeeds.value, needs)
    // 持久化到sessionStorage
    sessionStorage.setItem('userNeeds', JSON.stringify(userNeeds.value))
  }

  /**
   * 清空对话历史
   */
  const clearHistory = () => {
    messages.value = []
    userNeeds.value = {}
    sessionId.value = ''
    sessionStorage.removeItem('userNeeds')
    sessionManager.clearSession()
  }

  /**
   * 恢复会话
   */
  const restoreSession = () => {
    // 从sessionStorage恢复会话ID
    const savedSessionId = sessionManager.getSessionId()
    if (savedSessionId) {
      sessionId.value = savedSessionId
    }

    // 从sessionStorage恢复用户需求
    const savedNeeds = sessionStorage.getItem('userNeeds')
    if (savedNeeds) {
      try {
        userNeeds.value = JSON.parse(savedNeeds)
      } catch (error) {
        console.error('恢复用户需求失败:', error)
      }
    }
  }

  return {
    // 状态
    messages,
    sessionId,
    userNeeds,
    isLoading,
    // 计算属性
    hasMessages,
    isComplete,
    // 方法
    addMessage,
    updateSessionId,
    updateUserNeeds,
    clearHistory,
    restoreSession,
  }
})
