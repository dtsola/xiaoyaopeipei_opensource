<template>
  <div class="cyber-chat-container">
    <!-- CRT扫描线效果 -->
    <div class="crt-overlay"></div>
    <div class="scanlines"></div>

    <!-- 网格背景 -->
    <div class="cyber-grid"></div>

    <!-- 顶部导航 -->
    <header class="cyber-header">
      <button class="cyber-back" @click="goBack">
        <span class="cyber-arrow">◄</span>
      </button>
      <div class="cyber-brand">
        <span class="brand-glitch">XIAOYAO</span>
        <span class="brand-sub">SYSTEM ONLINE</span>
      </div>
      <div class="cyber-status">
        <span class="status-light"></span>
      </div>
    </header>

    <!-- 消息区域 -->
    <main class="cyber-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['cyber-msg-row', msg.role === 'user' ? 'msg-right' : 'msg-left']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="cyber-avatar ai-avatar">
            <div class="avatar-core">
              <span class="core-icon">◈</span>
            </div>
          </div>
          <div class="cyber-msg-content">
            <div class="cyber-bubble ai-bubble">
              <div class="bubble-header">
                <span class="sender-name">AI_ASSISTANT</span>
                <span class="msg-id">#{{ String(index + 1).padStart(4, '0') }}</span>
              </div>
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="cyber-quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="cyber-reply-btn"
                        @click="sendQuickReply(reply)">
                  <span class="reply-prefix">></span>
                  <span>{{ reply }}</span>
                </button>
              </div>
              <span class="bubble-time">{{ msg.time }}</span>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="cyber-msg-content">
            <div class="cyber-bubble user-bubble">
              <div class="bubble-header">
                <span class="sender-name">USER</span>
                <span class="msg-id">#{{ String(index + 1).padStart(4, '0') }}</span>
              </div>
              <div class="bubble-text">{{ msg.content }}</div>
              <span class="bubble-time">{{ msg.time }}</span>
            </div>
          </div>
          <div class="cyber-avatar user-avatar">
            <span class="user-initial">U</span>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="cyber-msg-row msg-left">
        <div class="cyber-avatar ai-avatar">
          <div class="avatar-core processing">
            <span class="core-icon">◈</span>
          </div>
        </div>
        <div class="cyber-msg-content">
          <div class="cyber-bubble ai-bubble typing-bubble">
            <div class="cyber-typing">
              <span class="typing-text">PROCESSING</span>
              <span class="typing-dots">
                <span>.</span><span>.</span><span>.</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="cyber-input-area">
      <div class="input-frame">
        <div class="input-deco-left"></div>
        <div class="input-deco-right"></div>
        <div class="cyber-input-wrapper">
          <span class="input-prompt">></span>
          <input
            ref="inputRef"
            v-model="inputText"
            type="text"
            class="cyber-input"
            placeholder="ENTER COMMAND..."
            @keypress.enter="sendMessage"
          />
          <button
            :class="['cyber-send', { active: inputText.trim() }]"
            :disabled="!inputText.trim() || isTyping"
            @click="sendMessage"
          >
            <span class="send-text">SEND</span>
            <span class="send-icon">►</span>
          </button>
        </div>
      </div>
      <div class="input-footer">
        <span class="footer-line">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>
        <span class="footer-text">XIAOYAO AI SYSTEM v2.077 // NEURAL INTERFACE ACTIVE</span>
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
    content: '>> SYSTEM INITIALIZED\n>> AI ASSISTANT READY\n\nWelcome to Xiaoyao System. Please specify your budget range.',
    time: '14:30',
    quickReplies: ['3000-5000', '5000-8000', '8000-12000', '12000+']
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
      content: `>> INPUT RECEIVED: "${userMessage.content}"\n>> PROCESSING COMPLETE\n\nQuery: Portability requirement detected. Please confirm.`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['Portable required', 'Desktop only', 'Both acceptable']
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
  console.log('Return')
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* ==================== 赛博朋克暗夜风格 ==================== */
:root {
  --neon-purple: #9D4EDD;
  --neon-purple-light: #E0AAFF;
  --neon-cyan: #00D9FF;
  --neon-pink: #FF006E;
  --neon-green: #39FF14;
  --dark-bg: #10002B;
  --dark-secondary: #1A0A3E;
  --dark-tertiary: #240046;
  --text-primary: #E0AAFF;
  --text-secondary: #9D4EDD;
  --text-dim: #7B2CBF;
  --border-glow: rgba(157, 78, 221, 0.5);
  --shadow-neon: 0 0 20px rgba(157, 78, 221, 0.5);
  --shadow-neon-cyan: 0 0 20px rgba(0, 217, 255, 0.5);
}

/* ==================== 容器 ==================== */
.cyber-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: var(--dark-bg);
  font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
  overflow: hidden;
  position: relative;
  color: var(--text-primary);
}

/* CRT效果 */
.crt-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
  pointer-events: none;
  z-index: 100;
}

.scanlines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.15) 0px,
    rgba(0, 0, 0, 0.15) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;
  z-index: 99;
}

/* 网格背景 */
.cyber-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(157, 78, 221, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(157, 78, 221, 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
  100% { transform: perspective(500px) rotateX(60deg) translateY(40px); }
}

/* ==================== 顶部导航 ==================== */
.cyber-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(180deg, var(--dark-secondary) 0%, var(--dark-bg) 100%);
  border-bottom: 2px solid var(--neon-purple);
  box-shadow: var(--shadow-neon), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 10;
}

.cyber-back {
  width: 40px;
  height: 40px;
  border: 2px solid var(--neon-cyan);
  background: transparent;
  color: var(--neon-cyan);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-neon-cyan);
}

.cyber-back:hover {
  background: var(--neon-cyan);
  color: var(--dark-bg);
  box-shadow: 0 0 30px rgba(0, 217, 255, 0.8);
}

.cyber-brand {
  text-align: center;
}

.brand-glitch {
  display: block;
  font-size: 16px;
  font-weight: 900;
  color: var(--neon-purple-light);
  text-shadow:
    0 0 10px var(--neon-purple),
    0 0 20px var(--neon-purple),
    0 0 40px var(--neon-purple);
  letter-spacing: 4px;
  animation: glitch 3s infinite;
}

@keyframes glitch {
  0%, 90%, 100% {
    text-shadow:
      0 0 10px var(--neon-purple),
      0 0 20px var(--neon-purple);
  }
  91% {
    text-shadow:
      -2px 0 var(--neon-cyan),
      2px 0 var(--neon-pink);
  }
  92% {
    text-shadow:
      2px 0 var(--neon-cyan),
      -2px 0 var(--neon-pink);
  }
  93% {
    text-shadow:
      0 0 10px var(--neon-purple),
      0 0 20px var(--neon-purple);
  }
}

.brand-sub {
  font-size: 10px;
  color: var(--neon-cyan);
  letter-spacing: 2px;
}

.cyber-status {
  width: 40px;
  display: flex;
  justify-content: center;
}

.status-light {
  width: 12px;
  height: 12px;
  background: var(--neon-green);
  border-radius: 50%;
  box-shadow: 0 0 20px var(--neon-green);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 20px var(--neon-green); }
  50% { opacity: 0.6; box-shadow: 0 0 10px var(--neon-green); }
}

/* ==================== 消息区域 ==================== */
.cyber-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  position: relative;
  z-index: 1;
}

.cyber-messages::-webkit-scrollbar {
  width: 8px;
}

.cyber-messages::-webkit-scrollbar-track {
  background: var(--dark-secondary);
}

.cyber-messages::-webkit-scrollbar-thumb {
  background: var(--neon-purple);
  border-radius: 4px;
  box-shadow: var(--shadow-neon);
}

.cyber-msg-row {
  display: flex;
  margin-bottom: 24px;
  animation: msgAppear 0.3s ease-out;
}

@keyframes msgAppear {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.msg-right {
  flex-direction: row-reverse;
}

.msg-right .cyber-msg-row {
  animation: msgAppearRight 0.3s ease-out;
}

@keyframes msgAppearRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ==================== 头像 ==================== */
.cyber-avatar {
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

.avatar-core {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--neon-purple), var(--dark-tertiary));
  border: 2px solid var(--neon-purple);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: var(--shadow-neon);
  animation: coreRotate 10s linear infinite;
}

.avatar-core.processing {
  animation: coreRotate 1s linear infinite, corePulse 1s ease-in-out infinite;
}

@keyframes coreRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes corePulse {
  0%, 100% { box-shadow: var(--shadow-neon); }
  50% { box-shadow: 0 0 40px rgba(157, 78, 221, 0.8), 0 0 60px rgba(0, 217, 255, 0.5); }
}

.core-icon {
  font-size: 24px;
  color: var(--neon-purple-light);
  animation: iconReverse 10s linear infinite;
}

@keyframes iconReverse {
  from { transform: rotate(0deg); }
  to { transform: rotate(-360deg); }
}

.user-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--dark-tertiary), var(--neon-cyan));
  border: 2px solid var(--neon-cyan);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-neon-cyan);
}

.user-initial {
  font-size: 18px;
  font-weight: 700;
  color: var(--neon-cyan);
}

/* ==================== 消息气泡 ==================== */
.cyber-msg-content {
  max-width: 75%;
}

.ai-bubble {
  background: linear-gradient(135deg, rgba(157, 78, 221, 0.1), rgba(26, 10, 62, 0.9));
  border: 1px solid var(--border-glow);
  padding: 14px 16px;
  position: relative;
  backdrop-filter: blur(10px);
}

.ai-bubble::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(135deg, var(--neon-purple), transparent, var(--neon-cyan));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.5;
}

.user-bubble {
  background: linear-gradient(135deg, rgba(0, 217, 255, 0.15), rgba(36, 0, 70, 0.9));
  border: 1px solid rgba(0, 217, 255, 0.5);
  padding: 14px 16px;
  position: relative;
  backdrop-filter: blur(10px);
}

.bubble-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-glow);
}

.sender-name {
  font-size: 11px;
  font-weight: 700;
  color: var(--neon-cyan);
  letter-spacing: 2px;
}

.msg-id {
  font-size: 10px;
  color: var(--text-dim);
  font-family: 'Courier New', monospace;
}

.bubble-text {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-primary);
}

.user-bubble .bubble-text {
  color: var(--neon-cyan);
}

.bubble-time {
  display: block;
  margin-top: 10px;
  font-size: 10px;
  color: var(--text-dim);
  font-family: 'Courier New', monospace;
}

/* ==================== 快捷回复 ==================== */
.cyber-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.cyber-reply-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: transparent;
  border: 1px solid var(--neon-purple);
  color: var(--neon-purple-light);
  font-size: 12px;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.cyber-reply-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--neon-purple);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.cyber-reply-btn:hover {
  color: var(--dark-bg);
  box-shadow: var(--shadow-neon);
}

.cyber-reply-btn:hover::before {
  opacity: 1;
}

.cyber-reply-btn > * {
  position: relative;
  z-index: 1;
}

.reply-prefix {
  color: var(--neon-cyan);
}

/* ==================== 打字状态 ==================== */
.typing-bubble {
  padding: 12px 16px;
}

.cyber-typing {
  display: flex;
  align-items: center;
  gap: 12px;
}

.typing-text {
  font-size: 12px;
  color: var(--neon-cyan);
  letter-spacing: 2px;
  animation: blink 1s step-end infinite;
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  background: var(--neon-purple);
  animation: dotBlink 1.4s infinite;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotBlink {
  0%, 80%, 100% { opacity: 0.3; }
  40% { opacity: 1; box-shadow: 0 0 10px var(--neon-purple); }
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.5; }
}

/* ==================== 输入区域 ==================== */
.cyber-input-area {
  background: linear-gradient(0deg, var(--dark-secondary) 0%, var(--dark-bg) 100%);
  border-top: 2px solid var(--neon-purple);
  padding: 20px;
  position: relative;
  z-index: 10;
  box-shadow: 0 -5px 30px rgba(157, 78, 221, 0.2);
}

.input-frame {
  position: relative;
  padding: 4px;
}

.input-deco-left,
.input-deco-right {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 20px;
  border: 2px solid var(--neon-cyan);
}

.input-deco-left {
  left: 0;
  border-right: none;
}

.input-deco-right {
  right: 0;
  border-left: none;
}

.cyber-input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--dark-bg);
  border: 1px solid var(--border-glow);
  padding: 12px 16px;
  position: relative;
}

.input-prompt {
  font-size: 18px;
  color: var(--neon-green);
  font-weight: 700;
}

.cyber-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  font-family: 'Courier New', monospace;
  color: var(--neon-cyan);
  outline: none;
}

.cyber-input::placeholder {
  color: var(--text-dim);
  letter-spacing: 1px;
}

.cyber-send {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: transparent;
  border: 2px solid var(--neon-purple);
  color: var(--neon-purple);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cyber-send.active {
  background: var(--neon-purple);
  color: var(--dark-bg);
  box-shadow: var(--shadow-neon);
}

.cyber-send:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.send-icon {
  font-size: 14px;
}

.input-footer {
  margin-top: 16px;
  text-align: center;
}

.footer-line {
  display: block;
  color: var(--text-dim);
  font-size: 10px;
  letter-spacing: 4px;
  margin-bottom: 8px;
}

.footer-text {
  font-size: 9px;
  color: var(--text-dim);
  letter-spacing: 2px;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .cyber-msg-content {
    max-width: 85%;
  }

  .cyber-reply-btn {
    padding: 8px 12px;
    font-size: 11px;
  }
}
</style>
