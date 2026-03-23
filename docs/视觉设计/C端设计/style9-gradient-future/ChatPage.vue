<template>
  <div class="gradient-chat-container">
    <!-- 流体渐变背景 -->
    <div class="gradient-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="gradient-mesh"></div>
    </div>

    <!-- 玻璃态覆盖层 -->
    <div class="glass-overlay"></div>

    <!-- 顶部导航 -->
    <header class="gradient-header">
      <button class="gradient-back" @click="goBack" aria-label="返回">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="gradient-brand">
        <div class="brand-hologram">
          <span class="brand-icon">✦</span>
          <div class="brand-ring ring-1"></div>
          <div class="brand-ring ring-2"></div>
        </div>
        <div class="brand-text">
          <span class="brand-name">小遥配配</span>
          <div class="brand-glow-line"></div>
        </div>
      </div>
      <div class="gradient-status">
        <div class="status-pulse">
          <div class="pulse-ring"></div>
          <div class="pulse-core"></div>
        </div>
      </div>
    </header>

    <!-- 消息区域 -->
    <main class="gradient-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['gradient-message', msg.role === 'user' ? 'message-user' : 'message-ai']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="gradient-avatar ai-avatar">
            <div class="avatar-glass">
              <div class="avatar-gradient ai-gradient">
                <span class="avatar-emoji">🤖</span>
              </div>
              <div class="avatar-glow"></div>
            </div>
          </div>
          <div class="gradient-content">
            <div class="gradient-bubble ai-bubble">
              <div class="bubble-shine"></div>
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="gradient-quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        :class="['gradient-reply-chip', `chip-${i % 4}`]"
                        @click="sendQuickReply(reply)">
                  <span class="chip-icon"></span>
                  <span>{{ reply }}</span>
                </button>
              </div>
              <div class="bubble-meta">
                <span class="meta-dot"></span>
                <span class="meta-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="gradient-content">
            <div class="gradient-bubble user-bubble">
              <div class="bubble-shine"></div>
              <div class="bubble-text">{{ msg.content }}</div>
              <div class="bubble-meta">
                <span class="meta-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>
          <div class="gradient-avatar user-avatar">
            <div class="avatar-glass">
              <div class="avatar-gradient user-gradient">
                <span class="avatar-emoji">😊</span>
              </div>
              <div class="avatar-glow"></div>
            </div>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="gradient-message message-ai">
        <div class="gradient-avatar ai-avatar">
          <div class="avatar-glass thinking">
            <div class="avatar-gradient ai-gradient">
              <span class="avatar-emoji">🤖</span>
            </div>
            <div class="avatar-glow"></div>
          </div>
        </div>
        <div class="gradient-content">
          <div class="gradient-bubble ai-bubble thinking-bubble">
            <div class="future-thinking">
              <div class="thinking-orbs">
                <div class="think-orb orb-1"></div>
                <div class="think-orb orb-2"></div>
                <div class="think-orb orb-3"></div>
              </div>
              <span class="thinking-label">AI思考中...</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="gradient-input-area">
      <div class="input-glass-container">
        <div class="input-border-gradient"></div>
        <div class="gradient-input-wrapper">
          <button class="gradient-action" aria-label="更多">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"/>
              <circle cx="19" cy="12" r="1"/>
              <circle cx="5" cy="12" r="1"/>
            </svg>
          </button>
          <input
            ref="inputRef"
            v-model="inputText"
            type="text"
            class="gradient-input"
            placeholder="告诉我您的需求..."
            @keypress.enter="sendMessage"
          />
          <button
            :class="['gradient-send', { active: inputText.trim() }]"
            :disabled="!inputText.trim() || isTyping"
            @click="sendMessage"
            aria-label="发送"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M22 2L11 13"/>
              <path d="M22 2L15 22L11 13"/>
              <path d="M22 2L2 9L11 13"/>
            </svg>
          </button>
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
    content: '嗨~我是小遥，您的AI电脑导购助手！🤖\n\n请问您的预算大概是多少呢？',
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
      content: `收到您的预算「${userMessage.content}」！✨\n\n请问您需要经常携带电脑外出吗？`,
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
/* ==================== 渐变虹未来科技风格 ==================== */
:root {
  --gradient-pink: #FF0080;
  --gradient-purple: #7928CA;
  --gradient-blue: #00D4FF;
  --gradient-cyan: #00FFF5;
  --gradient-gold: #FFD700;
  --gradient-dark: #1A0033;
  --gradient-dark-light: #2D0A4E;
  --glass-bg: rgba(255, 255, 255, 0.08);
  --glass-border: rgba(255, 255, 255, 0.15);
}

/* ==================== 容器 ==================== */
.gradient-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: var(--gradient-dark);
  font-family: 'SF Pro Display', 'Inter', 'Segoe UI', system-ui, sans-serif;
  overflow: hidden;
  position: relative;
}

/* 流体渐变背景 */
.gradient-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: orbFloat 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, var(--gradient-pink), var(--gradient-purple));
  top: -200px;
  right: -150px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, var(--gradient-blue), var(--gradient-cyan));
  bottom: -150px;
  left: -100px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, var(--gradient-gold), var(--gradient-pink));
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.1); }
  50% { transform: translate(-20px, 20px) scale(0.9); }
  75% { transform: translate(20px, 30px) scale(1.05); }
}

.gradient-mesh {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 20% 30%, rgba(255, 0, 128, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(0, 212, 255, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%);
  animation: meshPulse 10s ease-in-out infinite;
}

@keyframes meshPulse {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

/* 玻璃态覆盖 */
.glass-overlay {
  position: absolute;
  inset: 0;
  background: rgba(26, 0, 51, 0.3);
  backdrop-filter: blur(0px);
  pointer-events: none;
}

/* ==================== 顶部导航 ==================== */
.gradient-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: rgba(45, 10, 78, 0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--glass-border);
  position: relative;
  z-index: 10;
}

.gradient-back {
  width: 40px;
  height: 40px;
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.gradient-back:hover {
  background: rgba(255, 0, 128, 0.3);
  border-color: var(--gradient-pink);
  transform: translateX(-2px);
}

.gradient-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-hologram {
  position: relative;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-icon {
  font-size: 24px;
  background: linear-gradient(135deg, var(--gradient-pink), var(--gradient-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  z-index: 2;
}

.brand-ring {
  position: absolute;
  border: 2px solid;
  border-radius: 50%;
  opacity: 0.5;
}

.ring-1 {
  inset: 0;
  border-color: var(--gradient-pink);
  animation: ringPulse 3s ease-in-out infinite;
}

.ring-2 {
  inset: -6px;
  border-color: var(--gradient-cyan);
  opacity: 0.3;
  animation: ringPulse 3s ease-in-out infinite 0.5s;
}

@keyframes ringPulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.2; }
}

.brand-text {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.brand-name {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, white, var(--gradient-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 1px;
}

.brand-glow-line {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--gradient-pink), var(--gradient-cyan), transparent);
  border-radius: 1px;
}

.gradient-status {
  width: 40px;
}

.status-pulse {
  position: relative;
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pulse-ring {
  position: absolute;
  width: 20px;
  height: 20px;
  border: 2px solid var(--gradient-cyan);
  border-radius: 50%;
  animation: pulseExpand 2s ease-out infinite;
}

@keyframes pulseExpand {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(1.5); opacity: 0; }
}

.pulse-core {
  width: 8px;
  height: 8px;
  background: var(--gradient-cyan);
  border-radius: 50%;
  box-shadow: 0 0 12px var(--gradient-cyan);
}

/* ==================== 消息区域 ==================== */
.gradient-messages {
  flex: 1;
  overflow-y: auto;
  padding: 32px 20px;
  position: relative;
  z-index: 1;
}

.gradient-messages::-webkit-scrollbar {
  width: 6px;
}

.gradient-messages::-webkit-scrollbar-track {
  background: transparent;
}

.gradient-messages::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--gradient-pink), var(--gradient-purple));
  border-radius: 3px;
}

.gradient-message {
  display: flex;
  margin-bottom: 32px;
  animation: gradientSlideIn 0.5s ease-out;
}

@keyframes gradientSlideIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-ai {
  justify-content: flex-start;
}

.message-user {
  justify-content: flex-end;
}

/* ==================== 头像 ==================== */
.gradient-avatar {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.ai-avatar {
  margin-right: 12px;
}

.user-avatar {
  margin-left: 12px;
}

.avatar-glass {
  width: 100%;
  height: 100%;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.avatar-gradient {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.ai-gradient {
  background: linear-gradient(135deg, var(--gradient-pink), var(--gradient-purple));
}

.user-gradient {
  background: linear-gradient(135deg, var(--gradient-blue), var(--gradient-cyan));
}

.avatar-emoji {
  font-size: 22px;
  z-index: 2;
}

.avatar-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, var(--gradient-pink), var(--gradient-cyan));
  border-radius: 18px;
  z-index: -1;
  opacity: 0.5;
  filter: blur(8px);
}

.avatar-glass.thinking {
  animation: thinkingPulse 2s ease-in-out infinite;
}

@keyframes thinkingPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0); }
  50% { box-shadow: 0 0 0 8px rgba(0, 212, 255, 0.2); }
}

/* ==================== 消息气泡 ==================== */
.gradient-content {
  max-width: 70%;
}

.gradient-bubble {
  padding: 16px 20px;
  position: relative;
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  overflow: hidden;
}

.ai-bubble {
  background: var(--glass-bg);
  border-radius: 4px 20px 20px 20px;
}

.user-bubble {
  background: linear-gradient(135deg, rgba(255, 0, 128, 0.3), rgba(121, 40, 202, 0.3));
  border-radius: 20px 20px 4px 20px;
}

.bubble-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 70%
  );
  animation: shineMove 3s linear infinite;
}

@keyframes shineMove {
  0% { transform: translateX(-100%) translateY(-100%); }
  100% { transform: translateX(100%) translateY(100%); }
}

.bubble-text {
  font-size: 15px;
  line-height: 1.7;
  color: white;
  position: relative;
  z-index: 1;
}

.bubble-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--glass-border);
  position: relative;
  z-index: 1;
}

.meta-dot {
  width: 4px;
  height: 4px;
  background: var(--gradient-cyan);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--gradient-cyan);
}

.meta-time {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
}

/* ==================== 快捷回复 ==================== */
.gradient-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
  position: relative;
  z-index: 1;
}

.gradient-reply-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: 1px solid var(--glass-border);
  color: white;
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border-radius: 24px;
}

.chip-0 { background: rgba(255, 0, 128, 0.2); }
.chip-1 { background: rgba(121, 40, 202, 0.2); }
.chip-2 { background: rgba(0, 212, 255, 0.2); }
.chip-3 { background: rgba(255, 215, 0, 0.2); }

.gradient-reply-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.chip-0:hover { background: rgba(255, 0, 128, 0.4); border-color: var(--gradient-pink); }
.chip-1:hover { background: rgba(121, 40, 202, 0.4); border-color: var(--gradient-purple); }
.chip-2:hover { background: rgba(0, 212, 255, 0.4); border-color: var(--gradient-blue); }
.chip-3:hover { background: rgba(255, 215, 0, 0.4); border-color: var(--gradient-gold); }

.chip-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.6;
}

/* ==================== 思考状态 ==================== */
.thinking-bubble {
  padding: 14px 18px;
}

.future-thinking {
  display: flex;
  align-items: center;
  gap: 12px;
}

.thinking-orbs {
  display: flex;
  gap: 6px;
}

.think-orb {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: thinkBounce 1.4s ease-in-out infinite;
}

.think-orb:nth-child(1) {
  background: var(--gradient-pink);
  animation-delay: 0s;
}

.think-orb:nth-child(2) {
  background: var(--gradient-purple);
  animation-delay: 0.2s;
}

.think-orb:nth-child(3) {
  background: var(--gradient-cyan);
  animation-delay: 0.4s;
}

@keyframes thinkBounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.thinking-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

/* ==================== 输入区域 ==================== */
.gradient-input-area {
  background: rgba(45, 10, 78, 0.6);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--glass-border);
  padding: 20px 24px;
  position: relative;
  z-index: 10;
}

.input-glass-container {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  overflow: hidden;
}

.input-border-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, var(--gradient-pink), var(--gradient-purple), var(--gradient-cyan), var(--gradient-gold));
  opacity: 0.3;
  z-index: -1;
}

.gradient-input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
}

.gradient-action {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.gradient-action:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.gradient-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 15px;
  font-family: inherit;
  color: white;
  outline: none;
  padding: 10px 8px;
}

.gradient-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.gradient-send {
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.gradient-send.active {
  background: linear-gradient(135deg, var(--gradient-pink), var(--gradient-purple));
  color: white;
  box-shadow: 0 4px 15px rgba(255, 0, 128, 0.4);
}

.gradient-send:disabled {
  cursor: not-allowed;
  opacity: 0.3;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .gradient-messages {
    padding: 24px 16px;
  }

  .gradient-content {
    max-width: 80%;
  }
}
</style>
