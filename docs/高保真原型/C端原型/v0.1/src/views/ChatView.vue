<template>
  <div class="chat-view">
    <!-- 头部 -->
    <AppHeader title="小遥配配">
      <template #actions>
        <div class="header-avatar">小遥</div>
      </template>
    </AppHeader>

    <!-- 聊天区域 -->
    <div ref="chatContainer" class="chat-container">
      <div class="chat-messages">
        <!-- 欢迎消息 -->
        <MessageBubble
          v-if="messages.length === 0"
          :message="welcomeMessage"
          @quick-reply="handleQuickReply"
        />

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
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2C6.68629 2 4 4.68629 4 8V12C4 15.3137 6.68629 18 10 18C13.3137 18 16 15.3137 16 12V8C16 4.68629 13.3137 2 10 2Z" fill="currentColor"/>
            </svg>
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
          @keypress.enter="handleSend"
          @focus="handleInputFocus"
        />
        <button
          class="send-button"
          :disabled="!inputText.trim() || isLoading"
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
import { ref, reactive, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { AppHeader, MessageBubble, LoadingDots } from '@/components'
import { mockApi } from '@/api'
import type { ChatMessage, UserNeeds } from '@/types'

const router = useRouter()

// 状态管理
const messages = ref<ChatMessage[]>([])
const inputText = ref('')
const isLoading = ref(false)
const sessionId = ref('')
const shopId = ref('1234567890123456789')
const chatContainer = ref<HTMLElement>()
const inputRef = ref<HTMLInputElement>()

// 欢迎消息
const welcomeMessage: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content: '您好！我是小遥，我来帮您选一台合适的电脑～请问您的预算大概是多少呢？',
  timestamp: Date.now(),
  quickReplies: ['3000-5000元', '5000-8000元', '8000-12000元', '12000元以上'],
}

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
    const response = await mockApi.sendMessage({
      sessionId: sessionId.value,
      shopId: shopId.value,
      message: text,
    })

    // 更新sessionId
    sessionId.value = response.sessionId

    // 更新用户需求
    Object.assign(userNeeds, response.extractedInfo)

    // 模拟延迟后显示AI回复
    await new Promise(resolve => setTimeout(resolve, 800))

    // 添加AI消息
    const aiMessage: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: response.aiResponse,
      timestamp: Date.now(),
      quickReplies: response.quickReplies,
    }
    messages.value.push(aiMessage)

    // 滚动到底部
    scrollToBottom()

    // 检查是否可以推荐
    if (response.isComplete || response.nextAction === 'recommend') {
      // 延迟后自动跳转到推荐页面
      setTimeout(async () => {
        await goToRecommend()
      }, 1500)
    }
  } catch (error) {
    console.error('发送消息失败:', error)
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

// 快捷回复
const handleQuickReply = (reply: string) => {
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

  try {
    const response = await mockApi.getRecommendations({
      sessionId: sessionId.value,
      shopId: shopId.value,
      needs: userNeeds as UserNeeds,
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
onMounted(() => {
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

.header-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-xs);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);
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
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);
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

  &:focus {
    background: var(--color-bg-primary);
    box-shadow: 0 0 0 2px var(--color-primary-light);
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
