<template>
  <div class="tech-white-container">
    <!-- 顶部导航 -->
    <header class="tech-white-header">
      <button class="back-btn" @click="goBack" aria-label="返回">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="brand">
        <div class="brand-dot"></div>
        <span class="brand-name">小遥配配</span>
      </div>
      <div class="header-spacer"></div>
    </header>

    <!-- 消息区域 -->
    <main class="messages-container" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['message-row', msg.role === 'user' ? 'user-row' : 'ai-row']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="message-avatar ai-avatar">
            <div class="avatar-gradient"></div>
            <span class="avatar-text">遥</span>
          </div>
          <div class="message-content">
            <div class="message-bubble ai-bubble">
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="reply-chip"
                        @click="sendQuickReply(reply)">
                  {{ reply }}
                </button>
              </div>
            </div>
            <span class="message-time">{{ msg.time }}</span>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="message-content user-content">
            <div class="message-bubble user-bubble">
              <div class="bubble-text">{{ msg.content }}</div>
            </div>
            <span class="message-time">{{ msg.time }}</span>
          </div>
          <div class="message-avatar user-avatar">
            <span class="avatar-text">客</span>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="message-row ai-row">
        <div class="message-avatar ai-avatar">
          <div class="avatar-gradient"></div>
          <span class="avatar-text">遥</span>
        </div>
        <div class="message-content">
          <div class="message-bubble ai-bubble typing-bubble">
            <div class="typing-indicator">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="input-area">
      <div class="input-container">
        <div class="input-wrapper">
          <input
            ref="inputRef"
            v-model="inputText"
            type="text"
            class="message-input"
            placeholder="输入您的需求..."
            @keypress.enter="sendMessage"
          />
          <button
            :class="['send-btn', { active: inputText.trim() }]"
            :disabled="!inputText.trim() || isTyping"
            @click="sendMessage"
            aria-label="发送"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 2L11 13"/>
              <path d="M22 2L15 22L11 13"/>
              <path d="M22 2L2 9L11 13"/>
            </svg>
          </button>
        </div>
        <div class="input-hint">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v6l4 2"/>
          </svg>
          <span>AI实时回复</span>
        </div>
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
    content: '您好！我是小遥，您的AI电脑导购助手。\n\n请问您的预算大概是多少呢？',
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
      content: `收到您的预算「${userMessage.content}」。\n\n请问您是需要经常携带外出，还是主要在固定场所使用呢？`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['经常携带', '主要固定场所', '两者都有']
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
/* ==================== 科技白风格 - Modern Tech White ==================== */
:root {
  --tech-white: #FFFFFF;
  --tech-gray-bg: #F7F7F8;
  --tech-gray-light: #E8E8EA;
  --tech-gray-medium: #D1D1D6;
  --tech-brand: #FF6B35;
  --tech-brand-light: #FF8C5A;
  --tech-brand-dark: #E55A2B;
  --tech-text-primary: #1A1A1A;
  --tech-text-secondary: #6B7280;
  --tech-text-tertiary: #9CA3AF;
  --tech-border: rgba(0, 0, 0, 0.08);
  --tech-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
  --tech-shadow-md: 0 2px 8px rgba(0, 0, 0, 0.06);
  --tech-shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.08);
}

/* ==================== 容器 ==================== */
.tech-white-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 680px;
  margin: 0 auto;
  background: var(--tech-white);
  font-family: 'Inter', system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  overflow: hidden;
}

/* ==================== 顶部导航 ==================== */
.tech-white-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: var(--tech-white);
  border-bottom: 1px solid var(--tech-border);
  position: relative;
  z-index: 10;
}

.back-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--tech-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: var(--tech-gray-bg);
  color: var(--tech-text-primary);
}

.back-btn:active {
  transform: scale(0.95);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-dot {
  width: 8px;
  height: 8px;
  background: var(--tech-brand);
  border-radius: 50%;
  animation: brandPulse 2s ease-in-out infinite;
}

@keyframes brandPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.brand-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--tech-text-primary);
  letter-spacing: -0.3px;
}

.header-spacer {
  width: 36px;
}

/* ==================== 消息区域 ==================== */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px 20px;
  background: var(--tech-white);
}

.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.messages-container::-webkit-scrollbar-thumb {
  background: var(--tech-gray-medium);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: var(--tech-text-secondary);
}

.message-row {
  display: flex;
  margin-bottom: 28px;
  animation: messageSlide 0.4s ease-out;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ai-row {
  justify-content: flex-start;
}

.user-row {
  justify-content: flex-end;
}

/* ==================== 头像 ==================== */
.message-avatar {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  position: relative;
}

.ai-avatar {
  margin-right: 12px;
}

.user-avatar {
  margin-left: 12px;
}

.ai-avatar {
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--tech-brand) 0%, var(--tech-brand-light) 100%);
  border-radius: 10px;
}

.avatar-text {
  position: relative;
  font-size: 14px;
  font-weight: 600;
  color: white;
  z-index: 1;
}

.user-avatar {
  background: var(--tech-gray-bg);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar .avatar-text {
  color: var(--tech-text-secondary);
  font-size: 14px;
  font-weight: 500;
}

/* ==================== 消息内容 ==================== */
.message-content {
  max-width: 75%;
  display: flex;
  flex-direction: column;
}

.user-content {
  align-items: flex-end;
}

.message-bubble {
  padding: 14px 16px;
  border-radius: 14px;
  position: relative;
}

.ai-bubble {
  background: var(--tech-gray-bg);
  border-bottom-left-radius: 4px;
}

.user-bubble {
  background: var(--tech-brand);
  border-bottom-right-radius: 4px;
}

.bubble-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--tech-text-primary);
  white-space: pre-wrap;
  word-wrap: break-word;
}

.user-bubble .bubble-text {
  color: white;
}

.message-time {
  font-size: 11px;
  color: var(--tech-text-tertiary);
  margin-top: 6px;
  padding: 0 4px;
}

.user-content .message-time {
  text-align: right;
}

/* ==================== 快捷回复 ==================== */
.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.reply-chip {
  padding: 8px 14px;
  background: var(--tech-white);
  border: 1px solid var(--tech-gray-light);
  border-radius: 18px;
  color: var(--tech-text-secondary);
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reply-chip:hover {
  background: var(--tech-brand);
  border-color: var(--tech-brand);
  color: white;
  transform: translateY(-1px);
  box-shadow: var(--tech-shadow-sm);
}

.reply-chip:active {
  transform: translateY(0);
}

/* ==================== 思考状态 ==================== */
.typing-bubble {
  padding: 12px 16px;
  min-width: 60px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
}

.typing-dot {
  width: 8px;
  height: 8px;
  background: var(--tech-text-tertiary);
  border-radius: 50%;
  animation: typingBounce 1.2s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.15s; }
.typing-dot:nth-child(3) { animation-delay: 0.3s; }

@keyframes typingBounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-6px);
  }
}

/* ==================== 输入区域 ==================== */
.input-area {
  background: var(--tech-white);
  border-top: 1px solid var(--tech-border);
  padding: 16px 20px 20px;
}

.input-container {
  max-width: 100%;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: var(--tech-gray-bg);
  border-radius: 20px;
  padding: 8px 8px 8px 16px;
  transition: all 0.2s ease;
  border: 1.5px solid transparent;
}

.input-wrapper:focus-within {
  background: var(--tech-white);
  border-color: var(--tech-gray-light);
  box-shadow: var(--tech-shadow-md);
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 15px;
  font-family: inherit;
  color: var(--tech-text-primary);
  outline: none;
  padding: 8px 4px;
  max-height: 120px;
  resize: none;
  line-height: 1.5;
}

.message-input::placeholder {
  color: var(--tech-text-tertiary);
}

.send-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: var(--tech-gray-medium);
  color: var(--tech-white);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.send-btn.active {
  background: var(--tech-brand);
}

.send-btn.active:hover {
  background: var(--tech-brand-dark);
  transform: scale(1.05);
}

.send-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.send-btn:active {
  transform: scale(0.95);
}

.input-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 10px;
  color: var(--tech-text-tertiary);
  font-size: 11px;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .messages-container {
    padding: 20px 16px;
  }

  .message-content {
    max-width: 82%;
  }

  .tech-white-header {
    padding: 14px 16px;
  }

  .input-area {
    padding: 14px 16px 18px;
  }
}

/* ==================== 深色模式支持（可选） ==================== */
@media (prefers-color-scheme: dark) {
  :root {
    --tech-white: #1A1A1A;
    --tech-gray-bg: #2A2A2A;
    --tech-gray-light: #3A3A3A;
    --tech-text-primary: #FFFFFF;
    --tech-text-secondary: #A0A0A0;
    --tech-text-tertiary: #6B7280;
    --tech-border: rgba(255, 255, 255, 0.1);
  }
}
</style>
