<template>
  <div class="candy-chat-container">
    <!-- 背景装饰 -->
    <div class="candy-bg">
      <div class="floating-star star-1">⭐</div>
      <div class="floating-star star-2">✨</div>
      <div class="floating-star star-3">💫</div>
      <div class="floating-heart heart-1">💖</div>
      <div class="floating-heart heart-2">💕</div>
      <div class="candy-cloud cloud-1">☁️</div>
      <div class="candy-cloud cloud-2">☁️</div>
    </div>

    <!-- 顶部导航 -->
    <header class="candy-header">
      <button class="candy-back" @click="goBack">
        <span class="back-emoji">🌸</span>
      </button>
      <div class="candy-brand">
        <div class="brand-icon">🎀</div>
        <div class="brand-texts">
          <span class="brand-name">小遥配配</span>
          <span class="brand-mood">~ 快乐选电脑 ~</span>
        </div>
      </div>
      <div class="candy-menu">
        <span class="menu-dots">•••</span>
      </div>
    </header>

    <!-- 消息区域 -->
    <main class="candy-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['candy-msg-row', msg.role === 'user' ? 'msg-right' : 'msg-left']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="candy-avatar ai-avatar">
            <div class="avatar-wrapper">
              <span class="avatar-face">🤖</span>
              <div class="avatar-blush"></div>
            </div>
          </div>
          <div class="candy-msg-content">
            <div class="candy-bubble ai-bubble">
              <div class="bubble-ribbon"></div>
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="candy-quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="candy-reply-btn"
                        :style="{ '--btn-color': getCandyColor(i) }"
                        @click="sendQuickReply(reply)">
                  <span class="candy-sparkle">✨</span>
                  <span>{{ reply }}</span>
                </button>
              </div>
              <div class="bubble-time">{{ msg.time }}</div>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="candy-msg-content">
            <div class="candy-bubble user-bubble">
              <div class="bubble-decoration">
                <span class="deco-star">⭐</span>
              </div>
              <div class="bubble-text">{{ msg.content }}</div>
              <div class="bubble-time">{{ msg.time }}</div>
            </div>
          </div>
          <div class="candy-avatar user-avatar">
            <div class="avatar-wrapper">
              <span class="avatar-face">😊</span>
              <div class="avatar-blush"></div>
            </div>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="candy-msg-row msg-left">
        <div class="candy-avatar ai-avatar">
          <div class="avatar-wrapper thinking">
            <span class="avatar-face">🤖</span>
            <div class="avatar-blush"></div>
          </div>
        </div>
        <div class="candy-msg-content">
          <div class="candy-bubble ai-bubble thinking-bubble">
            <div class="candy-thinking">
              <span class="thinking-icon">💭</span>
              <span class="thinking-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="candy-input-area">
      <div class="input-frame">
        <div class="frame-deco-left">🌸</div>
        <div class="candy-input-wrapper">
          <button class="candy-sticker" @click="toggleSticker">
            <span class="sticker-emoji">😄</span>
          </button>
          <input
            ref="inputRef"
            v-model="inputText"
            type="text"
            class="candy-input"
            placeholder="告诉我你想要什么样的电脑吧~ ✨"
            @keypress.enter="sendMessage"
          />
          <button
            :class="['candy-send', { active: inputText.trim() }]"
            :disabled="!inputText.trim() || isTyping"
            @click="sendMessage"
          >
            <span class="send-emoji">🚀</span>
          </button>
        </div>
        <div class="frame-deco-right">🌸</div>
      </div>
      <div class="input-footer">
        <span class="footer-sparkle">✨</span>
        <span class="footer-text">小遥会帮你找到最合适的电脑~ 💖</span>
        <span class="footer-sparkle">✨</span>
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

const candyColors = ['#FFB6D9', '#B8E6FF', '#FFF5BA', '#C8F7DC']

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: '嗨~ 我是AI导购小遥！🎀\n\n超级开心能帮你选电脑！\n\n首先告诉我，你的预算大概有多少呢？💕',
    time: '14:30',
    quickReplies: ['3000-5000元', '5000-8000元', '8000-12000元', '12000元以上']
  }
])

const inputText = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

const getCandyColor = (index: number) => {
  return candyColors[index % candyColors.length]
}

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
      content: `收到啦~ ${userMessage.value}💝\n\n再问一下，你需要经常带出门吗？还是主要放在家里用呢？🤔`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['经常带出门', '主要在家用', '不确定耶~']
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

const toggleSticker = () => {
  console.log('Open sticker picker')
}

const goBack = () => {
  console.log('Go back')
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* ==================== 糖果粉可爱风格 ==================== */
:root {
  --candy-pink: #FFB6D9;
  --candy-pink-light: #FFCDE6;
  --candy-pink-dark: #FF8AB3;
  --sky-blue: #B8E6FF;
  --cream-yellow: #FFF5BA;
  --mint-green: #C8F7DC;
  --bg-pink: #FFF0F7;
  --text-primary: #5A5A5A;
  --text-secondary: #8A8A8A;
  --text-light: #AAAAAA;
  --shadow-soft: 0 4px 20px rgba(255, 182, 217, 0.2);
  --shadow-medium: 0 6px 25px rgba(255, 182, 217, 0.25);
  --radius-lg: 24px;
  --radius-md: 18px;
  --radius-sm: 12px;
  --radius-full: 50%;
}

/* ==================== 容器 ==================== */
.candy-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: var(--bg-pink);
  font-family: 'Nunito', 'Comic Sans MS', 'Muli', 'PingFang SC', sans-serif;
  overflow: hidden;
  position: relative;
}

/* 背景装饰 */
.candy-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.floating-star {
  position: absolute;
  font-size: 24px;
  animation: float 6s ease-in-out infinite;
  opacity: 0.6;
}

.star-1 { top: 10%; left: 10%; animation-delay: 0s; }
.star-2 { top: 25%; right: 15%; animation-delay: 2s; font-size: 20px; }
.star-3 { top: 45%; left: 8%; animation-delay: 4s; font-size: 18px; }

.floating-heart {
  position: absolute;
  font-size: 28px;
  animation: floatHeart 5s ease-in-out infinite;
  opacity: 0.5;
}

.heart-1 { top: 15%; right: 25%; animation-delay: 1s; }
.heart-2 { bottom: 35%; left: 12%; animation-delay: 3s; font-size: 24px; }

.candy-cloud {
  position: absolute;
  font-size: 48px;
  animation: cloudFloat 20s linear infinite;
  opacity: 0.3;
}

.cloud-1 { top: 5%; left: -5%; }
.cloud-2 { top: 60%; right: -10%; animation-delay: 10s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

@keyframes floatHeart {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-15px) scale(1.1); }
}

@keyframes cloudFloat {
  from { transform: translateX(-100px); }
  to { transform: translateX(calc(100vw + 200px)); }
}

/* ==================== 顶部导航 ==================== */
.candy-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 240, 247, 0.9) 100%);
  border-bottom: 3px solid var(--candy-pink);
  position: relative;
  z-index: 10;
}

.candy-back {
  width: 44px;
  height: 44px;
  border: none;
  background: linear-gradient(135deg, var(--candy-pink), var(--candy-pink-light));
  border-radius: var(--radius-full);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-soft);
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.candy-back:hover {
  transform: scale(1.1) rotate(-10deg);
  box-shadow: var(--shadow-medium);
}

.back-emoji {
  font-size: 22px;
}

.candy-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  font-size: 32px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.brand-texts {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.brand-name {
  font-size: 18px;
  font-weight: 800;
  color: var(--candy-pink-dark);
  line-height: 1.2;
}

.brand-mood {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.candy-menu {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--candy-pink);
  font-size: 20px;
  font-weight: 300;
  cursor: pointer;
  border-radius: var(--radius-full);
  transition: all 0.3s ease;
}

.candy-menu:hover {
  background: var(--bg-pink);
}

/* ==================== 消息区域 ==================== */
.candy-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 16px;
  position: relative;
  z-index: 1;
}

.candy-messages::-webkit-scrollbar {
  width: 6px;
}

.candy-messages::-webkit-scrollbar-track {
  background: transparent;
}

.candy-messages::-webkit-scrollbar-thumb {
  background: var(--candy-pink-light);
  border-radius: 10px;
}

.candy-msg-row {
  display: flex;
  margin-bottom: 24px;
  animation: candyPopIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes candyPopIn {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.msg-left {
  justify-content: flex-start;
}

.msg-right {
  justify-content: flex-end;
}

/* ==================== 头像 ==================== */
.candy-avatar {
  width: 50px;
  height: 50px;
  flex-shrink: 0;
}

.ai-avatar {
  margin-right: 10px;
}

.user-avatar {
  margin-left: 10px;
}

.avatar-wrapper {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--candy-pink), var(--sky-blue));
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: var(--shadow-soft);
  border: 3px solid white;
}

.avatar-wrapper.thinking {
  animation: thinkingPulse 1.5s ease-in-out infinite;
}

@keyframes thinkingPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.avatar-face {
  font-size: 26px;
}

.avatar-blush {
  position: absolute;
  bottom: 6px;
  width: 16px;
  height: 8px;
  background: rgba(255, 138, 179, 0.4);
  border-radius: 50%;
  filter: blur(2px);
}

/* ==================== 消息气泡 ==================== */
.candy-msg-content {
  max-width: 75%;
}

.candy-bubble {
  padding: 16px 18px;
  position: relative;
}

.ai-bubble {
  background: white;
  border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) 6px;
  box-shadow: var(--shadow-soft);
  border: 2px solid var(--candy-pink-light);
}

.user-bubble {
  background: linear-gradient(135deg, var(--candy-pink), var(--candy-pink-light));
  border-radius: var(--radius-lg) var(--radius-lg) 6px var(--radius-lg);
  box-shadow: var(--shadow-medium);
}

.bubble-ribbon {
  position: absolute;
  top: -3px;
  right: -3px;
  width: 20px;
  height: 20px;
  background: var(--cream-yellow);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.bubble-decoration {
  position: absolute;
  top: 10px;
  right: 10px;
}

.deco-star {
  font-size: 16px;
  animation: starSpin 3s linear infinite;
}

@keyframes starSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.bubble-text {
  font-size: 15px;
  line-height: 1.7;
  color: var(--text-primary);
}

.user-bubble .bubble-text {
  color: white;
  font-weight: 600;
}

.bubble-time {
  margin-top: 10px;
  font-size: 11px;
  color: var(--text-light);
}

.user-bubble .bubble-time {
  color: rgba(255, 255, 255, 0.8);
}

/* ==================== 快捷回复 ==================== */
.candy-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.candy-reply-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 2px solid var(--btn-color, var(--candy-pink));
  border-radius: 50px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.candy-reply-btn:hover {
  background: var(--btn-color, var(--candy-pink));
  color: white;
  transform: translateY(-4px) scale(1.05);
  box-shadow: var(--shadow-medium);
}

.candy-sparkle {
  font-size: 14px;
}

/* ==================== 思考状态 ==================== */
.thinking-bubble {
  padding: 14px 18px;
  background: white;
}

.candy-thinking {
  display: flex;
  align-items: center;
  gap: 12px;
}

.thinking-icon {
  font-size: 20px;
}

.thinking-dots {
  display: flex;
  gap: 6px;
}

.thinking-dots .dot {
  width: 10px;
  height: 10px;
  background: var(--candy-pink);
  border-radius: 50%;
  animation: dotBounce 1.4s ease-in-out infinite;
}

.thinking-dots .dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots .dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotBounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* ==================== 输入区域 ==================== */
.candy-input-area {
  background: linear-gradient(0deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 240, 247, 0.95) 100%);
  border-top: 3px solid var(--candy-pink);
  padding: 16px 20px 20px;
  position: relative;
  z-index: 10;
}

.input-frame {
  display: flex;
  align-items: center;
  gap: 8px;
}

.frame-deco-left,
.frame-deco-right {
  font-size: 20px;
}

.candy-input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 3px solid var(--candy-pink-light);
  border-radius: var(--radius-lg);
  padding: 8px 16px;
  box-shadow: var(--shadow-soft);
  transition: all 0.3s ease;
}

.candy-input-wrapper:focus-within {
  border-color: var(--candy-pink);
  box-shadow: var(--shadow-medium), 0 0 0 4px rgba(255, 182, 217, 0.1);
}

.candy-sticker {
  width: 36px;
  height: 36px;
  border: none;
  background: linear-gradient(135deg, var(--sky-blue), var(--mint-green));
  border-radius: var(--radius-full);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 3px 10px rgba(184, 230, 255, 0.3);
}

.candy-sticker:hover {
  transform: scale(1.15) rotate(-10deg);
}

.sticker-emoji {
  font-size: 20px;
}

.candy-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  font-family: inherit;
  color: var(--text-primary);
  outline: none;
}

.candy-input::placeholder {
  color: var(--text-light);
  font-weight: 400;
}

.candy-send {
  width: 42px;
  height: 42px;
  border: none;
  background: var(--text-light);
  border-radius: var(--radius-full);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.candy-send.active {
  background: linear-gradient(135deg, var(--candy-pink), var(--candy-pink-dark));
  box-shadow: var(--shadow-medium);
}

.candy-send.active:hover {
  transform: scale(1.1);
}

.candy-send:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.send-emoji {
  font-size: 20px;
}

.input-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 12px;
}

.footer-sparkle {
  font-size: 14px;
}

.footer-text {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .candy-msg-content {
    max-width: 82%;
  }

  .candy-reply-btn {
    padding: 8px 14px;
    font-size: 12px;
  }
}
</style>
