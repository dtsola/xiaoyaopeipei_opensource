<template>
  <div class="chat-container">
    <!-- 顶部导航栏 -->
    <header class="chat-header">
      <button class="back-btn" @click="goBack">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="header-title">
        <span class="logo-icon">小遥</span>
        <span class="shop-name">配配</span>
      </div>
      <button class="menu-btn">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="1"/>
          <circle cx="12" cy="5" r="1"/>
          <circle cx="12" cy="19" r="1"/>
        </svg>
      </button>
    </header>

    <!-- 对话消息区域 -->
    <main class="chat-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['message-row', msg.role === 'user' ? 'user-row' : 'ai-row']"
           :style="{ animationDelay: `${index * 0.1}s` }">
        <div v-if="msg.role === 'assistant'" class="avatar ai-avatar">
          <div class="avatar-ring">
            <span class="avatar-text">小遥</span>
          </div>
        </div>
        <div :class="['message-bubble', msg.role === 'user' ? 'user-bubble' : 'ai-bubble']">
          <div class="message-content" v-html="formatMessage(msg.content)"></div>
          <div v-if="msg.quickReplies && msg.quickReplies.length" class="quick-replies">
            <button v-for="(reply, i) in msg.quickReplies" :key="i"
                    class="quick-reply-btn"
                    @click="sendQuickReply(reply)">
              {{ reply }}
            </button>
          </div>
          <span class="message-time">{{ msg.time }}</span>
        </div>
        <div v-if="msg.role === 'user'" class="avatar user-avatar">
          <span class="user-avatar-icon">👤</span>
        </div>
      </div>

      <!-- AI思考中状态 -->
      <div v-if="isTyping" class="message-row ai-row typing-indicator">
        <div class="avatar ai-avatar">
          <div class="avatar-ring">
            <span class="avatar-text">小遥</span>
          </div>
        </div>
        <div class="message-bubble ai-bubble">
          <div class="typing-dots">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </main>

    <!-- 底部输入栏 -->
    <footer class="chat-input-area">
      <div class="input-container">
        <button class="attach-btn" title="添加图片">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
        </button>
        <input
          ref="inputRef"
          v-model="inputText"
          type="text"
          class="message-input"
          placeholder="输入您的需求..."
          @keypress.enter="sendMessage"
          @focus="handleInputFocus"
        />
        <button
          :class="['send-btn', { active: inputText.trim() }]"
          :disabled="!inputText.trim() || isTyping"
          @click="sendMessage"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
          </svg>
        </button>
      </div>
      <div class="input-hint">小遥会根据您的需求推荐合适的电脑配置</div>
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
    content: '您好！我是小遥，我来帮您选一台合适的电脑～\n请问您的预算大概是多少呢？',
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

  // 模拟AI回复
  isTyping.value = true
  await scrollToBottom()

  setTimeout(() => {
    isTyping.value = false
    const aiResponse: Message = {
      role: 'assistant',
      content: '明白了！' + userMessage.content + '～\n您需要经常携带吗？还是主要在家用？',
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['经常携带', '主要在家用', '不确定']
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

const handleInputFocus = () => {
  setTimeout(() => scrollToBottom(), 300)
}

const goBack = () => {
  console.log('返回上一页')
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* ==================== 全局样式变量 ==================== */
:root {
  --primary-blue: #4A90E2;
  --primary-blue-dark: #357ABD;
  --primary-blue-light: #6BAEE8;
  --success-green: #50C878;
  --warning-yellow: #FFB84D;
  --bg-color: #F5F7FA;
  --card-bg: #FFFFFF;
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  --border-color: #E1E8ED;
  --shadow-sm: 0 4px 12px rgba(74, 144, 226, 0.1);
  --shadow-md: 0 6px 20px rgba(74, 144, 226, 0.15);
  --shadow-lg: 0 10px 30px rgba(74, 144, 226, 0.2);
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 18px;
  --radius-full: 50%;
}

/* ==================== 容器布局 ==================== */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: linear-gradient(180deg, var(--bg-color) 0%, #EEF2F7 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  overflow: hidden;
  position: relative;
}

/* 背景网格装饰 */
.chat-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    linear-gradient(var(--border-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--border-color) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: 0.3;
  pointer-events: none;
}

/* ==================== 顶部导航栏 ==================== */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  position: relative;
  z-index: 10;
}

.back-btn, .menu-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--bg-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.back-btn:hover, .menu-btn:hover {
  background: var(--primary-blue);
  color: white;
  transform: scale(1.05);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.shop-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0.5px;
}

/* ==================== 消息区域 ==================== */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 16px;
  position: relative;
  z-index: 1;
  scroll-behavior: smooth;
}

.chat-messages::-webkit-scrollbar {
  width: 4px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--primary-blue-light);
  border-radius: 4px;
}

.message-row {
  display: flex;
  margin-bottom: 20px;
  animation: messageSlideIn 0.4s ease-out;
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
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
.avatar {
  width: 42px;
  height: 42px;
  flex-shrink: 0;
}

.ai-avatar .avatar-ring {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.35);
}

.ai-avatar .avatar-ring::before {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary-blue), var(--success-green));
  z-index: -1;
  opacity: 0.6;
}

.avatar-text {
  color: white;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.user-avatar {
  background: linear-gradient(135deg, #E8F4FD 0%, #D1E9FC 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 8px;
  box-shadow: 0 3px 12px rgba(74, 144, 226, 0.2);
}

.user-avatar-icon {
  font-size: 22px;
}

/* ==================== 消息气泡 ==================== */
.message-bubble {
  max-width: 72%;
  padding: 14px 18px;
  border-radius: var(--radius-md);
  position: relative;
}

.ai-bubble {
  background: white;
  color: var(--text-primary);
  margin-left: 10px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.ai-bubble::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 16px;
  border: 8px solid transparent;
  border-right-color: white;
  filter: drop-shadow(-2px 0 2px rgba(0, 0, 0, 0.05));
}

.user-bubble {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
  color: white;
  margin-right: 10px;
  box-shadow: 0 5px 18px rgba(74, 144, 226, 0.35);
}

.user-bubble::after {
  content: '';
  position: absolute;
  right: -8px;
  top: 16px;
  border: 8px solid transparent;
  border-left-color: var(--primary-blue);
}

.message-content {
  font-size: 15px;
  line-height: 1.6;
  word-wrap: break-word;
}

.message-time {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 6px;
  display: block;
  opacity: 0.7;
}

.user-bubble .message-time {
  color: rgba(255, 255, 255, 0.7);
}

/* ==================== 快捷回复按钮 ==================== */
.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.quick-reply-btn {
  padding: 8px 16px;
  background: var(--bg-color);
  border: 1px solid var(--primary-blue-light);
  border-radius: 20px;
  color: var(--primary-blue);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.quick-reply-btn:hover {
  background: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.quick-reply-btn:active {
  transform: translateY(0);
}

/* ==================== 打字指示器 ==================== */
.typing-indicator .typing-dots {
  display: flex;
  gap: 6px;
  padding: 8px 0;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  background: var(--primary-blue);
  border-radius: 50%;
  animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: 0s; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* ==================== 底部输入区域 ==================== */
.chat-input-area {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--border-color);
  padding: 12px 16px 20px;
  position: relative;
  z-index: 10;
}

.input-container {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-color);
  border-radius: var(--radius-lg);
  padding: 8px 12px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.input-container:focus-within {
  border-color: var(--primary-blue-light);
  box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.1);
}

.attach-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--text-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all 0.3s ease;
}

.attach-btn:hover {
  background: var(--primary-blue);
  color: white;
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 15px;
  color: var(--text-primary);
  outline: none;
  padding: 8px 0;
}

.message-input::placeholder {
  color: var(--text-tertiary);
}

.send-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--text-tertiary);
  border-radius: var(--radius-sm);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.send-btn.active {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);
}

.send-btn.active:hover {
  transform: scale(1.05);
}

.send-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.input-hint {
  text-align: center;
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 8px;
}

/* ==================== 响应式适配 ==================== */
@media (max-width: 480px) {
  .message-bubble {
    max-width: 80%;
  }

  .quick-replies {
    gap: 6px;
  }

  .quick-reply-btn {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>
