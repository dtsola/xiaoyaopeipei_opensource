<template>
  <div class="minimal-chat-container">
    <!-- 顶部导航 -->
    <header class="minimal-header">
      <button class="minimal-back" @click="goBack" aria-label="返回">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="minimal-brand">
        <span class="brand-name">小遥配配</span>
      </div>
      <div class="header-spacer"></div>
    </header>

    <!-- 消息区域 -->
    <main class="minimal-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['minimal-msg-row', msg.role === 'user' ? 'msg-right' : 'msg-left']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="minimal-avatar ai-avatar">
            <span class="avatar-letter">X</span>
          </div>
          <div class="minimal-msg-content">
            <div class="minimal-bubble ai-bubble">
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="minimal-quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="minimal-reply-btn"
                        @click="sendQuickReply(reply)">
                  {{ reply }}
                </button>
              </div>
              <span class="bubble-time">{{ msg.time }}</span>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="minimal-msg-content">
            <div class="minimal-bubble user-bubble">
              <div class="bubble-text">{{ msg.content }}</div>
              <span class="bubble-time">{{ msg.time }}</span>
            </div>
          </div>
          <div class="minimal-avatar user-avatar">
            <span class="avatar-letter">U</span>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="minimal-msg-row msg-left">
        <div class="minimal-avatar ai-avatar">
          <span class="avatar-letter">X</span>
        </div>
        <div class="minimal-msg-content">
          <div class="minimal-bubble ai-bubble typing-bubble">
            <div class="minimal-typing">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="minimal-input-area">
      <div class="minimal-input-wrapper">
        <input
          ref="inputRef"
          v-model="inputText"
          type="text"
          class="minimal-input"
          placeholder="输入您的需求..."
          @keypress.enter="sendMessage"
        />
        <button
          :class="['minimal-send', { active: inputText.trim() }]"
          :disabled="!inputText.trim() || isTyping"
          @click="sendMessage"
          aria-label="发送"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 2L11 13"/>
            <path d="M22 2L15 22L11 13"/>
            <path d="M22 2L2 9L11 13"/>
          </svg>
        </button>
      </div>
      <div class="input-hint">
        AI 智能导购助手
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
  time: string
  quickReplies?: string[]
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: '您好，我是小遥。我来帮您选择合适的电脑。\n\n请问您的预算大概在什么范围？',
    time: '14:30',
    quickReplies: ['3000-5000元', '5000-8000元', '8000-12000元', '12000元以上']
  }
])

const inputText = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

const formatMessage = (content: string) => {
  return content.replace(/\n/g, '<br>')
}

const sendQuickReply = (reply: string) => {
  inputText.value = reply
  sendMessage()
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isTyping.value) return

  const userMessage: Message = {
    role: 'user',
    content: inputText.value,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  messages.value.push(userMessage)
  inputText.value = ''
  await scrollToBottom()

  isTyping.value = true
  await scrollToBottom()

  setTimeout(() => {
    isTyping.value = false
    const aiResponse: Message = {
      role: 'assistant',
      content: `收到。${userMessage.content}，已记录。\n\n请问您需要经常携带吗？`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['需要经常携带', '主要在家使用', '不确定']
    }
    messages.value.push(aiResponse)
    scrollToBottom()
  }, 1500)
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const goBack = () => {
  console.log('返回')
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* ==================== 极简灰高级商务风格 ==================== */
:root {
  --charcoal: #2C2C2C;
  --dark-gray: #3A3A3A;
  --mid-gray: #8A8A8A;
  --light-gray: #E8E8E8;
  --pale-gray: #F5F5F5;
  --off-white: #FAFAFA;
  --pure-white: #FFFFFF;
  --shadow-subtle: 0 1px 3px rgba(0, 0, 0, 0.04);
  --shadow-soft: 0 4px 12px rgba(0, 0, 0, 0.06);
  --shadow-medium: 0 8px 24px rgba(0, 0, 0, 0.08);
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 50%;
}

/* ==================== 容器 ==================== */
.minimal-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 580px;
  margin: 0 auto;
  background: var(--off-white);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', 'PingFang SC', sans-serif;
  overflow: hidden;
}

/* ==================== 顶部导航 ==================== */
.minimal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: var(--pure-white);
  border-bottom: 1px solid var(--light-gray);
  position: relative;
  z-index: 10;
}

.minimal-back {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--mid-gray);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.minimal-back:hover {
  background: var(--pale-gray);
  color: var(--charcoal);
}

.minimal-brand {
  flex: 1;
  text-align: center;
}

.brand-name {
  font-size: 16px;
  font-weight: 500;
  color: var(--charcoal);
  letter-spacing: 0.5px;
}

.header-spacer {
  width: 36px;
}

/* ==================== 消息区域 ==================== */
.minimal-messages {
  flex: 1;
  overflow-y: auto;
  padding: 32px 24px;
  background: var(--off-white);
}

.minimal-messages::-webkit-scrollbar {
  width: 4px;
}

.minimal-messages::-webkit-scrollbar-track {
  background: transparent;
}

.minimal-messages::-webkit-scrollbar-thumb {
  background: var(--light-gray);
  border-radius: 4px;
}

.minimal-msg-row {
  display: flex;
  margin-bottom: 32px;
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.msg-left {
  justify-content: flex-start;
}

.msg-right {
  justify-content: flex-end;
}

/* ==================== 头像 ==================== */
.minimal-avatar {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.ai-avatar {
  margin-right: 14px;
}

.user-avatar {
  margin-left: 14px;
}

.ai-avatar .avatar-letter {
  width: 100%;
  height: 100%;
  background: var(--charcoal);
  color: var(--pure-white);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.user-avatar .avatar-letter {
  width: 100%;
  height: 100%;
  background: var(--light-gray);
  color: var(--mid-gray);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
}

/* ==================== 消息气泡 ==================== */
.minimal-msg-content {
  max-width: 75%;
}

.ai-bubble {
  background: var(--pure-white);
  padding: 16px 20px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-subtle);
  border: 1px solid var(--light-gray);
}

.user-bubble {
  background: var(--charcoal);
  padding: 16px 20px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
}

.bubble-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--charcoal);
}

.user-bubble .bubble-text {
  color: var(--pure-white);
}

.bubble-time {
  display: block;
  margin-top: 10px;
  font-size: 11px;
  color: var(--light-gray);
}

.user-bubble .bubble-time {
  color: rgba(255, 255, 255, 0.4);
}

/* ==================== 快捷回复 ==================== */
.minimal-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid var(--pale-gray);
}

.minimal-reply-btn {
  padding: 10px 18px;
  background: transparent;
  border: 1px solid var(--light-gray);
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 400;
  color: var(--dark-gray);
  cursor: pointer;
  transition: all 0.2s ease;
}

.minimal-reply-btn:hover {
  background: var(--charcoal);
  border-color: var(--charcoal);
  color: var(--pure-white);
}

.minimal-reply-btn:active {
  transform: scale(0.98);
}

/* ==================== 思考状态 ==================== */
.typing-bubble {
  padding: 16px 20px;
  background: var(--pure-white);
  border: 1px solid var(--light-gray);
  border-radius: var(--radius-md);
}

.minimal-typing {
  display: flex;
  gap: 6px;
  padding: 2px 0;
}

.typing-dot {
  width: 8px;
  height: 8px;
  background: var(--mid-gray);
  border-radius: 50%;
  animation: typingPulse 1.4s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingPulse {
  0%, 60%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  30% {
    opacity: 1;
    transform: scale(1);
  }
}

/* ==================== 输入区域 ==================== */
.minimal-input-area {
  background: var(--pure-white);
  border-top: 1px solid var(--light-gray);
  padding: 20px 24px 28px;
}

.minimal-input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--off-white);
  border: 1px solid var(--light-gray);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  transition: all 0.2s ease;
}

.minimal-input-wrapper:focus-within {
  background: var(--pure-white);
  border-color: var(--mid-gray);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.04);
}

.minimal-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 15px;
  font-family: inherit;
  color: var(--charcoal);
  outline: none;
}

.minimal-input::placeholder {
  color: var(--mid-gray);
  font-weight: 300;
}

.minimal-send {
  width: 36px;
  height: 36px;
  border: none;
  background: var(--light-gray);
  border-radius: var(--radius-sm);
  color: var(--mid-gray);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.minimal-send.active {
  background: var(--charcoal);
  color: var(--pure-white);
}

.minimal-send.active:hover {
  background: var(--dark-gray);
}

.minimal-send:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

.input-hint {
  text-align: center;
  margin-top: 14px;
  font-size: 11px;
  color: var(--light-gray);
  font-weight: 400;
  letter-spacing: 0.5px;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .minimal-messages {
    padding: 24px 16px;
  }

  .minimal-msg-content {
    max-width: 82%;
  }

  .minimal-header {
    padding: 16px 20px;
  }

  .minimal-input-area {
    padding: 16px 20px 24px;
  }
}
</style>
