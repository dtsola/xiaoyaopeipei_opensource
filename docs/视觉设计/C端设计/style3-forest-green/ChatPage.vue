<template>
  <div class="natural-chat-container">
    <!-- 纸质纹理背景 -->
    <div class="paper-texture"></div>

    <!-- 顶部导航 -->
    <header class="natural-header">
      <button class="natural-back" @click="goBack" aria-label="返回">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="natural-brand">
        <span class="brand-leaf">🌿</span>
        <span class="brand-name">小遥配配</span>
      </div>
      <div class="natural-status">
        <span class="status-dot"></span>
        <span class="status-text">在线</span>
      </div>
    </header>

    <!-- 消息区域 -->
    <main class="natural-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['natural-msg-row', msg.role === 'user' ? 'msg-right' : 'msg-left']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="natural-avatar ai-avatar">
            <div class="avatar-leaf">🍃</div>
          </div>
          <div class="natural-msg-content">
            <div class="natural-bubble ai-bubble">
              <div class="bubble-corner"></div>
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>

              <!-- 快捷回复 - 自然风格 -->
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="natural-quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="natural-reply-btn"
                        @click="sendQuickReply(reply)">
                  <span class="reply-seed"></span>
                  <span>{{ reply }}</span>
                </button>
              </div>

              <div class="bubble-meta">
                <span class="bubble-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="natural-msg-content">
            <div class="natural-bubble user-bubble">
              <div class="bubble-text">{{ msg.content }}</div>
              <div class="bubble-meta">
                <span class="bubble-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>
          <div class="natural-avatar user-avatar">
            <span class="avatar-initial">你</span>
          </div>
        </template>
      </div>

      <!-- AI思考状态 - 自然风格 -->
      <div v-if="isTyping" class="natural-msg-row msg-left">
        <div class="natural-avatar ai-avatar thinking">
          <div class="avatar-leaf pulse">🍃</div>
        </div>
        <div class="natural-msg-content">
          <div class="natural-bubble ai-bubble thinking-bubble">
            <div class="natural-thinking">
              <span class="thinking-leaf">🍃</span>
              <span>正在思考...</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="natural-input-area">
      <div class="natural-input-wrapper">
        <button class="natural-attach" aria-label="添加附件">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
          </svg>
        </button>

        <div class="natural-input-container">
          <input
            ref="inputRef"
            v-model="inputText"
            type="text"
            class="natural-input"
            placeholder="想找什么样的电脑呢..."
            @keypress.enter="sendMessage"
            @focus="handleInputFocus"
          />
          <div class="input-underline"></div>
        </div>

        <button
          :class="['natural-send', { active: inputText.trim() }]"
          :disabled="!inputText.trim() || isTyping"
          @click="sendMessage"
          aria-label="发送"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>

      <!-- 温馨提示 -->
      <div class="natural-hint">
        <span class="hint-icon">💡</span>
        <span class="hint-text">小遥会根据你的需求，帮你找到最合适的电脑配置</span>
      </div>
    </footer>

    <!-- 植物装饰元素 -->
    <div class="plant-decoration plant-left"></div>
    <div class="plant-decoration plant-right"></div>
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
    content: '你好，我是小遥。🌿\n\n很高兴能帮你选电脑。我们会聊一聊你的需求，然后我帮你找到最合适的配置。\n\n首先，你的预算大概在什么范围？',
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
      content: `收到了。${userMessage.content}，记下了。\n\n还有一个问题，你需要经常带出门使用吗？`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['需要经常带出门', '主要在家用', '不确定']
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
  console.log('返回')
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* ==================== 森系绿风格样式 ==================== */
:root {
  --forest-green: #5D8A66;
  --forest-light: #8FB996;
  --forest-pale: #B8D4BF;
  --warm-brown: #D4A574;
  --warm-beige: #F5E6D3;
  --cream-white: #FAF9F6;
  --terracotta: #E8B4A0;
  --text-dark: #3A3A3A;
  --text-muted: #6B6B6B;
  --text-light: #9A9A9A;
  --shadow-subtle: 0 3px 12px rgba(93, 138, 102, 0.12);
  --shadow-soft: 0 6px 20px rgba(93, 138, 102, 0.15);
  --shadow-medium: 0 8px 28px rgba(93, 138, 102, 0.18);
  --border-soft: rgba(93, 138, 102, 0.15);
}

/* ==================== 容器 ==================== */
.natural-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 580px;
  margin: 0 auto;
  background: var(--cream-white);
  font-family: 'Noto Serif SC', 'Source Han Serif SC', 'PingFang SC', serif;
  overflow: hidden;
  position: relative;
}

/* 纸质纹理 */
.paper-texture {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(93, 138, 102, 0.02) 2px,
      rgba(93, 138, 102, 0.02) 4px
    );
  pointer-events: none;
  opacity: 0.6;
}

/* ==================== 顶部导航 ==================== */
.natural-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: rgba(250, 249, 246, 0.95);
  border-bottom: 1px solid var(--border-soft);
  position: relative;
  z-index: 10;
}

.natural-back {
  width: 36px;
  height: 36px;
  border: 1px solid var(--border-soft);
  background: transparent;
  border-radius: 8px;
  color: var(--forest-green);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.natural-back:hover {
  background: var(--forest-green);
  color: white;
  border-color: var(--forest-green);
}

.natural-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-leaf {
  font-size: 20px;
  filter: grayscale(20%);
}

.brand-name {
  font-size: 17px;
  font-weight: 500;
  color: var(--text-dark);
  letter-spacing: 0.5px;
}

.natural-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
}

.status-dot {
  width: 6px;
  height: 6px;
  background: var(--forest-green);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ==================== 消息区域 ==================== */
.natural-messages {
  flex: 1;
  overflow-y: auto;
  padding: 32px 24px;
  position: relative;
  z-index: 1;
  scroll-behavior: smooth;
}

.natural-messages::-webkit-scrollbar {
  width: 4px;
}

.natural-messages::-webkit-scrollbar-track {
  background: transparent;
}

.natural-messages::-webkit-scrollbar-thumb {
  background: var(--forest-pale);
  border-radius: 4px;
}

.natural-msg-row {
  display: flex;
  margin-bottom: 32px;
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
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
.natural-avatar {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
}

.ai-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-leaf {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--forest-light), var(--forest-pale));
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: var(--shadow-subtle);
}

.avatar-leaf.pulse {
  animation: leafPulse 2s ease-in-out infinite;
}

@keyframes leafPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.user-avatar {
  background: linear-gradient(135deg, var(--warm-beige), var(--terracotta));
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
  box-shadow: var(--shadow-subtle);
}

.avatar-initial {
  font-size: 15px;
  font-weight: 600;
  color: var(--warm-brown);
}

/* ==================== 消息气泡 ==================== */
.natural-msg-content {
  max-width: 70%;
}

.msg-left .natural-msg-content {
  margin-left: 14px;
}

.msg-right .natural-msg-content {
  margin-right: 14px;
}

.natural-bubble {
  padding: 16px 20px;
  position: relative;
}

.ai-bubble {
  background: white;
  border-radius: 4px 18px 18px 18px;
  border: 1px solid var(--border-soft);
  box-shadow: var(--shadow-subtle);
}

.bubble-corner {
  position: absolute;
  left: -1px;
  top: 16px;
  width: 0;
  height: 0;
  border: 8px solid transparent;
  border-right-color: white;
  border-left: none;
}

.bubble-corner::before {
  content: '';
  position: absolute;
  left: -1px;
  top: -8px;
  border: 8px solid transparent;
  border-right-color: var(--border-soft);
  border-left: none;
}

.user-bubble {
  background: linear-gradient(135deg, var(--forest-green), var(--forest-light));
  border-radius: 18px 4px 18px 18px;
  box-shadow: var(--shadow-soft);
}

.bubble-text {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-dark);
}

.user-bubble .bubble-text {
  color: white;
  font-weight: 400;
}

.bubble-meta {
  margin-top: 10px;
}

.bubble-time {
  font-size: 11px;
  color: var(--text-light);
}

.user-bubble .bubble-time {
  color: rgba(255, 255, 255, 0.7);
}

/* ==================== 快捷回复 ==================== */
.natural-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed var(--border-soft);
}

.natural-reply-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: white;
  border: 1px solid var(--border-soft);
  border-radius: 24px;
  font-size: 14px;
  font-weight: 400;
  color: var(--text-dark);
  cursor: pointer;
  transition: all 0.25s ease;
}

.natural-reply-btn:hover {
  background: var(--forest-green);
  border-color: var(--forest-green);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-soft);
}

.reply-seed {
  width: 14px;
  height: 14px;
  background: var(--forest-pale);
  border-radius: 50%;
  display: inline-block;
}

.natural-reply-btn:hover .reply-seed {
  background: white;
}

/* ==================== 思考状态 ==================== */
.thinking-bubble {
  padding: 14px 18px;
  background: var(--warm-beige);
  border-color: transparent;
}

.natural-thinking {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: var(--text-muted);
  font-style: italic;
}

.thinking-leaf {
  font-size: 16px;
  animation: sway 2s ease-in-out infinite;
}

@keyframes sway {
  0%, 100% { transform: rotate(-5deg); }
  50% { transform: rotate(5deg); }
}

/* ==================== 输入区域 ==================== */
.natural-input-area {
  background: rgba(250, 249, 246, 0.98);
  padding: 20px 24px 28px;
  border-top: 1px solid var(--border-soft);
  position: relative;
  z-index: 10;
}

.natural-input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: white;
  padding: 12px 16px;
  border-radius: 16px;
  border: 1px solid var(--border-soft);
  box-shadow: var(--shadow-subtle);
  transition: all 0.25s ease;
}

.natural-input-wrapper:focus-within {
  border-color: var(--forest-light);
  box-shadow: var(--shadow-soft);
}

.natural-attach {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.natural-attach:hover {
  background: var(--warm-beige);
  color: var(--forest-green);
}

.natural-input-container {
  flex: 1;
  position: relative;
}

.natural-input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 15px;
  font-family: inherit;
  color: var(--text-dark);
  padding: 8px 0;
  outline: none;
}

.natural-input::placeholder {
  color: var(--text-light);
  font-style: italic;
}

.input-underline {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 1px;
  width: 0;
  background: var(--forest-green);
  transition: width 0.3s ease;
}

.natural-input:focus + .input-underline {
  width: 100%;
}

.natural-send {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border-soft);
  background: transparent;
  border-radius: 10px;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
  flex-shrink: 0;
}

.natural-send.active {
  background: var(--forest-green);
  border-color: var(--forest-green);
  color: white;
}

.natural-send.active:hover {
  background: var(--forest-light);
  border-color: var(--forest-light);
}

.natural-send:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

/* ==================== 温馨提示 ==================== */
.natural-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 14px;
  font-size: 12px;
  color: var(--text-muted);
}

.hint-icon {
  font-size: 14px;
  opacity: 0.7;
}

/* ==================== 植物装饰 ==================== */
.plant-decoration {
  position: absolute;
  bottom: 0;
  width: 120px;
  height: 120px;
  opacity: 0.15;
  pointer-events: none;
  z-index: 0;
}

.plant-left {
  left: 0;
  background: radial-gradient(ellipse at bottom left, var(--forest-green) 0%, transparent 70%);
}

.plant-right {
  right: 0;
  background: radial-gradient(ellipse at bottom right, var(--forest-light) 0%, transparent 70%);
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .natural-messages {
    padding: 24px 16px;
  }

  .natural-msg-content {
    max-width: 80%;
  }

  .natural-bubble {
    padding: 16px 18px;
  }

  .natural-quick-replies {
    gap: 8px;
  }

  .natural-reply-btn {
    padding: 8px 14px;
    font-size: 13px;
  }
}
</style>