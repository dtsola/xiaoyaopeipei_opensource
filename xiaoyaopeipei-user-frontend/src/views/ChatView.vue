<template>
  <div class="chat-view">
    <!-- 头部 -->
    <AppHeader :title="shopName || '小遥配配'">
      <template #actions>
        <div class="header-avatar">
          <img src="/logo.png" alt="小遥" />
        </div>
      </template>
    </AppHeader>

    <!-- 店铺信息加载失败提示 -->
    <div v-if="shopError" class="error-banner">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="2"/>
        <path d="M10 7V10M10 13V13.1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <span>{{ shopError }}</span>
    </div>

    <!-- 聊天区域 -->
    <div ref="chatContainer" class="chat-container">
      <div class="chat-messages">
        <!-- 聊天消息列表 -->
        <MessageBubble
          v-for="msg in messages"
          :key="msg.id"
          :message="msg"
          @quick-reply="handleQuickReply"
        />

        <!-- AI 思考中 -->
        <div v-if="isLoading" class="typing-indicator">
          <div class="avatar avatar-assistant">
            <img src="/logo.png" alt="小遥" />
          </div>
          <div class="typing-content">
            <div class="typing-text">AI思考中...</div>
            <LoadingDots />
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-container">
      <div class="input-wrapper">
        <input
          ref="inputRef"
          v-model="inputText"
          type="text"
          class="message-input"
          placeholder="输入您的需求..."
          :disabled="!hasShopId"
          @keypress.enter="handleSend"
          @focus="handleInputFocus"
        />
        <button
          class="send-button"
          :disabled="!inputText.trim() || isLoading || !hasShopId"
          @click="handleSend"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M3 10L17 10M17 10L11 4M17 10L11 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { AppHeader, MessageBubble, LoadingDots } from '@/components'
import { sendMessage, getRecommendations, getPriceRanges } from '@/api'
import { useShop } from '@/composables/useShop'
import { sessionManager } from '@/utils/request'
import type { ChatMessage, UserNeeds } from '@/types'

const router = useRouter()

// 店铺管理
const { initShop, shopName, hasShopInfo, isLoading: shopLoading, error: shopError } = useShop()

// 状态管理
const messages = ref<ChatMessage[]>([])
const inputText = ref('')
const isLoading = ref(false)
const sessionId = ref('')
const chatContainer = ref<HTMLElement>()
const inputRef = ref<HTMLInputElement>()

// 获取shop_id的辅助函数
const getShopId = () => sessionManager.getShopId() || ''

// 响应式的shop_id状态（用于模板绑定）
const hasShopId = ref(false)

// 动态预算区间（默认值，接口加载后会更新）
const priceRanges = ref<string[]>(['3000-5000元', '5000-8000元', '8000-12000元', '12000元以上'])

// 欢迎消息（使用动态预算区间）
const welcomeMessage = computed<ChatMessage>(() => ({
  id: 'welcome',
  role: 'assistant',
  content: '您好！我是小遥，我来帮您选一台合适的电脑～请问您的预算大概是多少呢？',
  timestamp: Date.now(),
  quickReplies: priceRanges.value,
}))

// 用户需求信息
const userNeeds = reactive<Partial<UserNeeds>>({})

// 生成消息ID
const generateId = () => Date.now().toString(36) + Math.random().toString(36).substr(2)

// 滚动到底部
const scrollToBottom = (smooth = true) => {
  nextTick(() => {
    if (chatContainer.value) {
      const scrollOptions: ScrollToOptions = {
        top: chatContainer.value.scrollHeight,
        behavior: smooth ? 'smooth' : 'instant',
      }
      chatContainer.value.scrollTo(scrollOptions)
    }
  })
}

// 发送消息
const handleSend = async () => {
  const text = inputText.value.trim()
  if (!text || isLoading.value) return

  // 检查shop_id
  const currentShopId = getShopId()
  if (!currentShopId) {
    message.error('店铺信息缺失，请重新进入')
    return
  }

  // 添加用户消息
  const userMessage: ChatMessage = {
    id: generateId(),
    role: 'user',
    content: text,
    timestamp: Date.now(),
  }
  messages.value.push(userMessage)
  inputText.value = ''

  // 滚动到底部
  scrollToBottom()

  // 显示加载状态
  isLoading.value = true

  try {
    // 调用API
    const response = await sendMessage({
      sessionId: sessionId.value,
      shopId: currentShopId,
      message: text,
    })

    // 调试日志
    console.log('API响应:', response)

    // 更新sessionId并保存到sessionManager
    sessionId.value = response.sessionId
    sessionManager.setSessionId(response.sessionId)

    // 更新用户需求
    Object.assign(userNeeds, response.extractedInfo)

    // 模拟延迟后显示AI回复
    await new Promise(resolve => setTimeout(resolve, 800))

    // 检查AI回复内容
    const aiReplyContent = response.aiResponse || '抱歉，我没能理解您的意思，能再说一遍吗？'
    console.log('AI回复内容:', aiReplyContent)

    // 添加AI消息
    const aiMessage: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: aiReplyContent,
      timestamp: Date.now(),
      quickReplies: response.quickReplies || [],
    }
    messages.value.push(aiMessage)

    console.log('当前消息列表:', messages.value)

    // 滚动到底部
    scrollToBottom()

    // 不再自动跳转，等待用户点击"查看推荐"快捷回复
  } catch (error) {
    console.error('发送消息失败:', error)
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

// 快捷回复
const handleQuickReply = async (reply: string) => {
  // 特殊处理"查看推荐"快捷回复
  if (reply === '查看推荐') {
    await goToRecommend()
    return
  }

  // 其他快捷回复正常发送
  inputText.value = reply
  handleSend()
}

// 输入框焦点处理
const handleInputFocus = () => {
  setTimeout(() => scrollToBottom(), 300)
}

// 跳转到推荐页面
const goToRecommend = async () => {
  if (!userNeeds.budget) return

  const currentShopId = getShopId()
  if (!currentShopId) {
    message.error('店铺信息缺失，请重新进入')
    return
  }

  try {
    // 转换前端驼峰命名到后端蛇形命名
    const backendNeeds = {
      budget: userNeeds.budget,
      device_type: userNeeds.deviceType,  // 驼峰 → 蛇形
      usage: userNeeds.usage,
      requirements: userNeeds.requirements,
      brand: userNeeds.brand,
      portable: userNeeds.portable,
    }

    const response = await getRecommendations({
      sessionId: sessionId.value,
      shopId: currentShopId,
      needs: backendNeeds,
    })

    // 保存推荐结果到 sessionStorage
    sessionStorage.setItem('recommendations', JSON.stringify(response.recommendations))
    sessionStorage.setItem('userNeeds', JSON.stringify(userNeeds))

    router.push('/recommend')
  } catch (error) {
    console.error('获取推荐失败:', error)
  }
}

// 初始化
onMounted(async () => {
  // 初始化店铺信息
  const shopReady = await initShop()
  if (!shopReady) {
    console.error('店铺信息加载失败')
  }

  // 从session恢复会话ID
  const savedSessionId = sessionManager.getSessionId()
  if (savedSessionId) {
    sessionId.value = savedSessionId
  }

  // 获取动态预算区间（直接从sessionManager获取，确保有值）
  const currentShopId = sessionManager.getShopId()
  if (currentShopId) {
    hasShopId.value = true
    try {
      const ranges = await getPriceRanges(currentShopId)
      if (ranges.length > 0) {
        priceRanges.value = ranges
        console.log('动态预算区间:', priceRanges.value)
      }
    } catch (error) {
      console.error('获取预算区间失败，使用默认值:', error)
    }
  }

  // 添加欢迎消息到消息列表
  if (!shopError.value) {
    messages.value.push(welcomeMessage.value)
  }

  scrollToBottom(false)
})
</script>

<style lang="less" scoped>
.chat-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg-secondary);
}

.error-banner {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  background: #fee2e2;
  border-bottom: 1px solid #fecaca;
  color: #991b1b;
  font-size: var(--font-size-sm);

  svg {
    flex-shrink: 0;
  }
}

.header-avatar {
  width: 36px;
  height: 36px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 2px;
  }
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 76px var(--spacing-lg) 100px;
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.typing-indicator {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  max-width: 600px;
  margin: 0 auto;
  animation: fadeInUp 0.3s ease-out;
}

.avatar-assistant {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 2px;
  }
}

.typing-content {
  flex: 1;
  background: var(--color-bg-elevated);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.typing-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.input-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-bg-primary);
  padding: var(--spacing-md) var(--spacing-lg);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
  z-index: var(--z-sticky);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  max-width: 600px;
  margin: 0 auto;
}

.message-input {
  flex: 1;
  height: 48px;
  padding: 0 var(--spacing-lg);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-full);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus:not(:disabled) {
    background: var(--color-bg-primary);
    box-shadow: 0 0 0 2px var(--color-primary-light);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.send-button {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: white;
  border-radius: 50%;
  transition: all var(--transition-fast);
  flex-shrink: 0;

  &:hover:not(:disabled) {
    background: var(--color-primary-hover);
    transform: scale(1.05);
  }

  &:active:not(:disabled) {
    transform: scale(0.95);
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

@media (max-width: 768px) {
  .chat-container {
    padding: 70px var(--spacing-md) 90px;
  }

  .input-container {
    padding: var(--spacing-sm) var(--spacing-md);
  }
}
</style>
