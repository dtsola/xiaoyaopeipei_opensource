<template>
  <div class="zen-chat-container">
    <!-- 和纸纹理背景 -->
    <div class="washi-texture"></div>

    <!-- 禅意装饰 -->
    <div class="zen-decoration">
      <div class="enso-circle enso-large"></div>
      <div class="enso-circle enso-small"></div>
      <div class="bamboo-stroke"></div>
    </div>

    <!-- 顶部导航 -->
    <header class="zen-header">
      <button class="zen-back-btn" @click="goBack" aria-label="返回">
        <span class="back-arrow">›</span>
      </button>
      <div class="zen-brand">
        <div class="brand-seal">
          <span class="seal-char">小</span>
        </div>
        <div class="brand-text-vertical">
          <span class="brand-char">小</span>
          <span class="brand-char">遥</span>
          <span class="brand-char">配</span>
          <span class="brand-char">配</span>
        </div>
      </div>
      <div class="zen-status">
        <div class="status-dot"></div>
      </div>
    </header>

    <!-- 消息区域 -->
    <main class="zen-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['zen-message', msg.role === 'user' ? 'message-user' : 'message-ai']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="zen-avatar ai-avatar">
            <div class="avatar-sumi">
              <span class="sumi-text">遥</span>
            </div>
          </div>
          <div class="zen-content">
            <div class="zen-bubble ai-bubble">
              <div class="bubble-corner-brush"></div>
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="zen-quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="zen-reply-chip"
                        @click="sendQuickReply(reply)">
                  <span class="chip-seal">{{ i + 1 }}</span>
                  <span>{{ reply }}</span>
                </button>
              </div>
              <div class="bubble-meta">
                <span class="meta-time">{{ msg.time }}</span>
                <div class="meta-seal">
                  <span class="seal-mini">完</span>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="zen-content">
            <div class="zen-bubble user-bubble">
              <div class="bubble-text">{{ msg.content }}</div>
              <div class="bubble-meta">
                <span class="meta-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>
          <div class="zen-avatar user-avatar">
            <div class="avatar-sumi user-sumi">
              <span class="sumi-text">客</span>
            </div>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="zen-message message-ai">
        <div class="zen-avatar ai-avatar">
          <div class="avatar-sumi thinking">
            <span class="sumi-text">遥</span>
          </div>
        </div>
        <div class="zen-content">
          <div class="zen-bubble ai-bubble thinking-bubble">
            <div class="zen-thinking-indicator">
              <div class="thinking-ink"></div>
              <span class="thinking-text">思考中...</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="zen-input-area">
      <div class="zen-input-container">
        <div class="input-frame">
          <div class="frame-corner frame-tl"></div>
          <div class="frame-corner frame-tr"></div>
          <div class="frame-corner frame-bl"></div>
          <div class="frame-corner frame-br"></div>
          <div class="frame-border frame-top"></div>
          <div class="frame-border frame-bottom"></div>
          <div class="frame-border frame-left"></div>
          <div class="frame-border frame-right"></div>

          <div class="input-inner">
            <input
              ref="inputRef"
              v-model="inputText"
              type="text"
              class="zen-input-field"
              placeholder="何でもお聞きください..."
              @keypress.enter="sendMessage"
            />
            <button
              :class="['zen-send-btn', { active: inputText.trim() }]"
              :disabled="!inputText.trim() || isTyping"
              @click="sendMessage"
              aria-label="发送"
            >
              <span class="send-char">送</span>
            </button>
          </div>
        </div>
      </div>
      <div class="zen-footer">
        <div class="footer-line"></div>
        <span class="footer-text">誠意相待 · 用心推薦</span>
        <div class="footer-line"></div>
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
    content: 'はじめまして。小遥と申します。\n\nパソコン選び、お任せください。\n\nまずは、予算はどのくらいでしょうか？',
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
      content: `承知いたしました。予算「${userMessage.content}」ですね。\n\nよく持ち歩く必要はありますか？それとも、主に家で使いますか？`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['よく持ち歩く', '主に家で使う', 'どちらでも']
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
/* ==================== 日式和风禅意风格 ==================== */
:root {
  --zen-red: #C8553D;
  --zen-red-light: #E07A5F;
  --zen-red-dark: #A63C28;
  --zen-cream: #F5F0E8;
  --zen-beige: #E8DFD1;
  --zen-gold: #B8956B;
  --zen-gold-light: #D4B896;
  --zen-brown: #6B5B4F;
  --zen-charcoal: #3D3D3D;
  --zen-ink: #2C2C2C;
  --zen-shadow: rgba(107, 91, 79, 0.1);
  --zen-shadow-deep: rgba(107, 91, 79, 0.2);
}

/* ==================== 容器 ==================== */
.zen-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: var(--zen-cream);
  font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif JP', 'Source Han Serif JP', serif;
  overflow: hidden;
  position: relative;
}

/* 和纸纹理 */
.washi-texture {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(184, 149, 107, 0.03) 2px,
      rgba(184, 149, 107, 0.03) 4px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 2px,
      rgba(184, 149, 107, 0.02) 2px,
      rgba(184, 149, 107, 0.02) 4px
    );
  pointer-events: none;
  opacity: 0.8;
}

/* 禅意装饰 */
.zen-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.enso-circle {
  position: absolute;
  border: 2px solid var(--zen-gold);
  opacity: 0.15;
  border-radius: 50%;
}

.enso-large {
  width: 400px;
  height: 400px;
  top: -150px;
  right: -150px;
  border-width: 1px;
}

.enso-small {
  width: 200px;
  height: 200px;
  bottom: 15%;
  left: -80px;
  border-width: 2px;
}

.bamboo-stroke {
  position: absolute;
  top: 20%;
  right: 8%;
  width: 2px;
  height: 120px;
  background: linear-gradient(180deg,
    transparent 0%,
    var(--zen-gold) 20%,
    var(--zen-gold) 80%,
    transparent 100%
  );
  opacity: 0.2;
}

.bamboo-stroke::before {
  content: '';
  position: absolute;
  top: 30%;
  left: 50%;
  transform: translateX(-50%);
  width: 8px;
  height: 2px;
  background: var(--zen-gold);
  opacity: 0.3;
}

.bamboo-stroke::after {
  content: '';
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 2px;
  background: var(--zen-gold);
  opacity: 0.3;
}

/* ==================== 顶部导航 ==================== */
.zen-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  background: rgba(245, 240, 232, 0.95);
  border-bottom: 1px solid var(--zen-beige);
  position: relative;
  z-index: 10;
}

.zen-back-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--zen-gold);
  background: transparent;
  color: var(--zen-brown);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
}

.zen-back-btn::before {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.zen-back-btn:hover {
  background: var(--zen-red);
  border-color: var(--zen-red);
  color: white;
}

.zen-back-btn:hover::before {
  border-color: white;
}

.back-arrow {
  font-size: 28px;
  line-height: 1;
  margin-right: -4px;
}

.zen-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-seal {
  width: 44px;
  height: 44px;
  background: var(--zen-red);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px var(--zen-shadow);
  position: relative;
}

.brand-seal::before {
  content: '';
  position: absolute;
  inset: 2px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.seal-char {
  font-size: 22px;
  color: white;
  font-weight: 500;
}

.brand-text-vertical {
  display: flex;
  flex-direction: column;
  gap: 2px;
  writing-mode: vertical-rl;
  text-orientation: upright;
}

.brand-char {
  font-size: 18px;
  color: var(--zen-charcoal);
  letter-spacing: 4px;
  font-weight: 500;
}

.zen-status {
  width: 40px;
  display: flex;
  justify-content: center;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--zen-red);
  border-radius: 50%;
  animation: zenPulse 3s ease-in-out infinite;
}

@keyframes zenPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.9); }
}

/* ==================== 消息区域 ==================== */
.zen-messages {
  flex: 1;
  overflow-y: auto;
  padding: 40px 28px;
  position: relative;
  z-index: 1;
}

.zen-messages::-webkit-scrollbar {
  width: 4px;
}

.zen-messages::-webkit-scrollbar-track {
  background: transparent;
}

.zen-messages::-webkit-scrollbar-thumb {
  background: var(--zen-gold);
  border-radius: 2px;
}

.zen-message {
  display: flex;
  margin-bottom: 40px;
  animation: zenFadeIn 0.8s ease-out;
}

@keyframes zenFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
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
.zen-avatar {
  width: 52px;
  height: 52px;
  flex-shrink: 0;
}

.ai-avatar {
  margin-right: 16px;
}

.user-avatar {
  margin-left: 16px;
}

.avatar-sumi {
  width: 100%;
  height: 100%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 4px 12px var(--zen-shadow);
}

.avatar-sumi::before {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px solid var(--zen-gold);
  opacity: 0.5;
}

.avatar-sumi.thinking {
  animation: sumiBreath 2s ease-in-out infinite;
}

@keyframes sumiBreath {
  0%, 100% { box-shadow: 0 4px 12px var(--zen-shadow); }
  50% { box-shadow: 0 4px 20px var(--zen-shadow-deep), 0 0 0 4px rgba(184, 149, 107, 0.1); }
}

.sumi-text {
  font-size: 20px;
  color: var(--zen-red);
  font-weight: 500;
}

.user-sumi {
  background: var(--zen-beige);
}

.user-sumi .sumi-text {
  color: var(--zen-brown);
}

/* ==================== 消息气泡 ==================== */
.zen-content {
  max-width: 70%;
}

.ai-bubble {
  background: white;
  padding: 20px 24px;
  position: relative;
  box-shadow: 0 2px 12px var(--zen-shadow);
}

.ai-bubble::before {
  content: '';
  position: absolute;
  left: -1px;
  top: 24px;
  width: 0;
  height: 0;
  border: 12px solid transparent;
  border-right-color: white;
  border-left: none;
}

.bubble-corner-brush {
  position: absolute;
  left: -1px;
  top: 24px;
  width: 12px;
  height: 24px;
  background: white;
  clip-path: polygon(0 0, 100% 50%, 0 100%);
}

.user-bubble {
  background: var(--zen-red);
  padding: 20px 24px;
  position: relative;
  box-shadow: 0 4px 16px var(--zen-shadow-deep);
}

.user-bubble::before {
  content: '';
  position: absolute;
  right: -1px;
  top: 24px;
  width: 0;
  height: 0;
  border: 12px solid transparent;
  border-left-color: var(--zen-red);
  border-right: none;
}

.bubble-text {
  font-size: 15px;
  line-height: 2;
  color: var(--zen-charcoal);
}

.user-bubble .bubble-text {
  color: white;
}

.bubble-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--zen-beige);
}

.meta-time {
  font-size: 11px;
  color: var(--zen-gold);
  letter-spacing: 1px;
}

.user-bubble .meta-time {
  color: rgba(255, 255, 255, 0.7);
}

.meta-seal {
  width: 24px;
  height: 24px;
  background: var(--zen-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 1px;
}

.seal-mini {
  font-size: 10px;
  color: white;
  font-weight: 500;
}

/* ==================== 快捷回复 ==================== */
.zen-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
}

.zen-reply-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: transparent;
  border: 1px solid var(--zen-gold);
  color: var(--zen-brown);
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.chip-seal {
  width: 18px;
  height: 18px;
  background: var(--zen-gold);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 500;
}

.zen-reply-chip:hover {
  background: var(--zen-red);
  border-color: var(--zen-red);
  color: white;
}

.zen-reply-chip:hover .chip-seal {
  background: white;
  color: var(--zen-red);
}

/* ==================== 思考状态 ==================== */
.thinking-bubble {
  padding: 16px 20px;
  background: white;
}

.zen-thinking-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--zen-brown);
}

.thinking-ink {
  width: 20px;
  height: 20px;
  border: 2px solid var(--zen-gold);
  border-top-color: transparent;
  border-radius: 50%;
  animation: inkSpin 1.2s linear infinite;
}

@keyframes inkSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ==================== 输入区域 ==================== */
.zen-input-area {
  background: rgba(245, 240, 232, 0.98);
  border-top: 1px solid var(--zen-beige);
  padding: 24px 28px 32px;
  position: relative;
  z-index: 10;
}

.zen-input-container {
  max-width: 100%;
}

.input-frame {
  position: relative;
  padding: 8px;
  background: white;
  box-shadow: 0 2px 12px var(--zen-shadow);
}

.frame-corner {
  position: absolute;
  width: 12px;
  height: 12px;
  border: 2px solid var(--zen-gold);
  opacity: 0.6;
}

.frame-tl { top: 4px; left: 4px; border-right: none; border-bottom: none; }
.frame-tr { top: 4px; right: 4px; border-left: none; border-bottom: none; }
.frame-bl { bottom: 4px; left: 4px; border-right: none; border-top: none; }
.frame-br { bottom: 4px; right: 4px; border-left: none; border-top: none; }

.frame-border {
  position: absolute;
  background: var(--zen-gold);
  opacity: 0.3;
}

.frame-top { top: 0; left: 16px; right: 16px; height: 1px; }
.frame-bottom { bottom: 0; left: 16px; right: 16px; height: 1px; }
.frame-left { left: 0; top: 16px; bottom: 16px; width: 1px; }
.frame-right { right: 0; top: 16px; bottom: 16px; width: 1px; }

.input-inner {
  display: flex;
  align-items: center;
  gap: 12px;
}

.zen-input-field {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 15px;
  font-family: inherit;
  color: var(--zen-charcoal);
  outline: none;
  padding: 12px 8px;
}

.zen-input-field::placeholder {
  color: var(--zen-gold);
  opacity: 0.8;
}

.zen-send-btn {
  width: 44px;
  height: 44px;
  border: 1px solid var(--zen-gold);
  background: transparent;
  color: var(--zen-brown);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.zen-send-btn.active {
  background: var(--zen-red);
  border-color: var(--zen-red);
  color: white;
}

.zen-send-btn:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

.send-char {
  font-size: 16px;
  font-weight: 500;
}

/* ==================== 底部装饰 ==================== */
.zen-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.footer-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    var(--zen-gold) 50%,
    transparent 100%
  );
}

.footer-text {
  font-size: 12px;
  color: var(--zen-gold);
  letter-spacing: 4px;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .zen-messages {
    padding: 32px 20px;
  }

  .zen-content {
    max-width: 80%;
  }

  .brand-char {
    font-size: 16px;
    letter-spacing: 2px;
  }
}
</style>
