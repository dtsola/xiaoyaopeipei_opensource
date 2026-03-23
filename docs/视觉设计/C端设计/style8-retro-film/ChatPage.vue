<template>
  <div class="retro-chat-container">
    <!-- 胶片噪点纹理 -->
    <div class="film-grain"></div>

    <!-- 暗角效果 -->
    <div class="vignette-overlay"></div>

    <!-- 划痕效果 -->
    <div class="scratch-overlay"></div>

    <!-- 顶部导航 -->
    <header class="retro-header">
      <button class="retro-back" @click="goBack" aria-label="返回">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="retro-brand">
        <div class="brand-frame">
          <span class="brand-title">小遥配配</span>
          <div class="brand-film-stripe"></div>
        </div>
      </div>
      <div class="retro-indicator">
        <div class="indicator-light"></div>
        <span class="indicator-text">REC</span>
      </div>
    </header>

    <!-- 消息区域 -->
    <main class="retro-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['retro-message', msg.role === 'user' ? 'message-user' : 'message-ai']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="retro-avatar ai-avatar">
            <div class="polaroid-frame">
              <div class="polaroid-photo">
                <span class="avatar-text">遥</span>
              </div>
            </div>
          </div>
          <div class="retro-content">
            <div class="retro-bubble ai-bubble">
              <div class="tape-corner tape-tl"></div>
              <div class="tape-corner tape-tr"></div>
              <div class="bubble-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="retro-quick-replies">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="retro-reply-ticket"
                        @click="sendQuickReply(reply)">
                  <span class="ticket-perf"></span>
                  <span>{{ reply }}</span>
                  <span class="ticket-perf"></span>
                </button>
              </div>
              <div class="bubble-footer">
                <span class="film-frame-number">{{ String(index + 1).padStart(3, '0') }}</span>
                <span class="bubble-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="retro-content">
            <div class="retro-bubble user-bubble">
              <div class="bubble-text">{{ msg.content }}</div>
              <div class="bubble-footer">
                <span class="bubble-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>
          <div class="retro-avatar user-avatar">
            <div class="polaroid-frame user-polaroid">
              <div class="polaroid-photo">
                <span class="avatar-text">客</span>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="retro-message message-ai">
        <div class="retro-avatar ai-avatar">
          <div class="polaroid-frame processing">
            <div class="polaroid-photo">
              <span class="avatar-text">遥</span>
            </div>
          </div>
        </div>
        <div class="retro-content">
          <div class="retro-bubble ai-bubble processing-bubble">
            <div class="film-processing">
              <div class="film-sprocket">
                <div class="sprocket-hole" v-for="i in 4" :key="i"></div>
              </div>
              <span class="processing-text">显影中...</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="retro-input-area">
      <div class="input-border-frame">
        <div class="corner-bracket bracket-tl">┌</div>
        <div class="corner-bracket bracket-tr">┐</div>
        <div class="corner-bracket bracket-bl">└</div>
        <div class="corner-bracket bracket-br">┘</div>

        <div class="retro-input-wrapper">
          <button class="retro-action" aria-label="更多">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"/>
              <circle cx="19" cy="12" r="1"/>
              <circle cx="5" cy="12" r="1"/>
            </svg>
          </button>
          <input
            ref="inputRef"
            v-model="inputText"
            type="text"
            class="retro-input"
            placeholder="输入您的需求..."
            @keypress.enter="sendMessage"
          />
          <button
            :class="['retro-send', { active: inputText.trim() }]"
            :disabled="!inputText.trim() || isTyping"
            @click="sendMessage"
            aria-label="发送"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M22 2L11 13"/>
              <path d="M22 2L15 22L11 13"/>
              <path d="M22 2L2 9L11 13"/>
            </svg>
          </button>
        </div>
      </div>
      <div class="retro-footer-mark">
        <span class="mark-text">★ 回忆珍藏 ★</span>
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
    content: '您好！我是小遥，很高兴为您服务。\n\n请问您的预算大概是多少呢？',
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
/* ==================== 复古棕胶片怀旧风格 ==================== */
:root {
  --retro-sepia: #8B7355;
  --retro-sepia-dark: #6B5544;
  --retro-sepia-light: #A89070;
  --retro-cream: #E8DCC8;
  --retro-ivory: #F5F1E8;
  --retro-brown: #4A3728;
  --retro-dark: #3D2E22;
  --retro-gold: #C4A76C;
  --retro-shadow: rgba(74, 55, 40, 0.15);
  --retro-shadow-deep: rgba(74, 55, 40, 0.3);
}

/* ==================== 容器 ==================== */
.retro-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: var(--retro-ivory);
  font-family: 'Courier New', 'Special Elite', 'Typewriter', monospace;
  overflow: hidden;
  position: relative;
}

/* 胶片噪点 */
.film-grain {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.04;
  pointer-events: none;
  animation: grainShift 0.5s steps(10) infinite;
}

@keyframes grainShift {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-5%, -10%); }
  20% { transform: translate(-15%, 5%); }
  30% { transform: translate(7%, -25%); }
  40% { transform: translate(-5%, 25%); }
  50% { transform: translate(-15%, 10%); }
  60% { transform: translate(15%, 0%); }
  70% { transform: translate(0%, 15%); }
  80% { transform: translate(3%, 35%); }
  90% { transform: translate(-10%, 10%); }
}

/* 暗角效果 */
.vignette-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at center,
    transparent 0%,
    transparent 50%,
    rgba(61, 46, 34, 0.15) 100%
  );
  pointer-events: none;
}

/* 划痕效果 */
.scratch-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.scratch-overlay::before {
  content: '';
  position: absolute;
  top: 10%;
  left: 15%;
  width: 1px;
  height: 80px;
  background: linear-gradient(180deg,
    transparent,
    rgba(196, 167, 108, 0.3),
    transparent
  );
  transform: rotate(-5deg);
}

.scratch-overlay::after {
  content: '';
  position: absolute;
  top: 40%;
  right: 20%;
  width: 2px;
  height: 120px;
  background: linear-gradient(180deg,
    transparent,
    rgba(196, 167, 108, 0.2),
    transparent
  );
  transform: rotate(3deg);
}

/* ==================== 顶部导航 ==================== */
.retro-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: rgba(232, 220, 200, 0.95);
  border-bottom: 2px solid var(--retro-sepia);
  position: relative;
  z-index: 10;
}

.retro-back {
  width: 36px;
  height: 36px;
  border: 2px solid var(--retro-sepia);
  background: transparent;
  color: var(--retro-brown);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.retro-back:hover {
  background: var(--retro-sepia);
  color: var(--retro-ivory);
}

.retro-brand {
  flex: 1;
  display: flex;
  justify-content: center;
}

.brand-frame {
  position: relative;
  padding: 8px 24px;
  background: var(--retro-sepia);
  border-radius: 2px;
}

.brand-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--retro-ivory);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.brand-film-stripe {
  position: absolute;
  bottom: 2px;
  left: 8px;
  right: 8px;
  height: 4px;
  background: repeating-linear-gradient(
    90deg,
    var(--retro-ivory) 0px,
    var(--retro-ivory) 4px,
    transparent 4px,
    transparent 8px
  );
}

.retro-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
}

.indicator-light {
  width: 8px;
  height: 8px;
  background: #D32F2F;
  border-radius: 50%;
  animation: recBlink 2s ease-in-out infinite;
}

@keyframes recBlink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.indicator-text {
  font-size: 11px;
  color: var(--retro-brown);
  font-weight: 600;
  letter-spacing: 1px;
}

/* ==================== 消息区域 ==================== */
.retro-messages {
  flex: 1;
  overflow-y: auto;
  padding: 32px 24px;
  position: relative;
  z-index: 1;
}

.retro-messages::-webkit-scrollbar {
  width: 8px;
}

.retro-messages::-webkit-scrollbar-track {
  background: rgba(139, 115, 85, 0.1);
}

.retro-messages::-webkit-scrollbar-thumb {
  background: var(--retro-sepia);
  border-radius: 2px;
}

.retro-message {
  display: flex;
  margin-bottom: 36px;
  animation: retroFadeIn 0.6s ease-out;
}

@keyframes retroFadeIn {
  from {
    opacity: 0;
    transform: translateY(12px);
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
.retro-avatar {
  width: 56px;
  height: 56px;
  flex-shrink: 0;
}

.ai-avatar {
  margin-right: 12px;
}

.user-avatar {
  margin-left: 12px;
}

.polaroid-frame {
  width: 100%;
  height: 100%;
  background: white;
  padding: 6px;
  box-shadow: 0 4px 12px var(--retro-shadow-deep);
  position: relative;
}

.polaroid-frame::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 1px solid var(--retro-sepia);
  opacity: 0.3;
}

.polaroid-photo {
  width: 100%;
  height: 100%;
  background: var(--retro-sepia);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.polaroid-photo::before {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.avatar-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--retro-ivory);
  font-family: 'Courier New', monospace;
}

.user-polaroid {
  background: var(--retro-cream);
}

.user-polaroid .polaroid-photo {
  background: var(--retro-sepia-dark);
}

.polaroid-frame.processing {
  animation: polaroidShake 0.5s ease-in-out infinite;
}

@keyframes polaroidShake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-1deg); }
  75% { transform: rotate(1deg); }
}

/* ==================== 消息气泡 ==================== */
.retro-content {
  max-width: 70%;
}

.ai-bubble {
  background: var(--retro-cream);
  padding: 18px 20px;
  position: relative;
  box-shadow: 4px 4px 0 var(--retro-sepia);
  border: 1px solid var(--retro-sepia);
}

.tape-corner {
  position: absolute;
  width: 30px;
  height: 12px;
  background: rgba(196, 167, 108, 0.4);
  transform: rotate(-45deg);
}

.tape-tl {
  top: -6px;
  left: -10px;
}

.tape-tr {
  top: -6px;
  right: -10px;
  transform: rotate(45deg);
}

.user-bubble {
  background: var(--retro-sepia);
  padding: 18px 20px;
  position: relative;
  box-shadow: 4px 4px 0 var(--retro-brown);
  border: 1px solid var(--retro-dark);
}

.bubble-text {
  font-size: 14px;
  line-height: 1.8;
  color: var(--retro-dark);
}

.user-bubble .bubble-text {
  color: var(--retro-ivory);
}

.bubble-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed var(--retro-sepia-light);
}

.film-frame-number {
  font-size: 11px;
  color: var(--retro-sepia-dark);
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
}

.bubble-time {
  font-size: 11px;
  color: var(--retro-sepia);
  font-family: 'Courier New', monospace;
}

.user-bubble .bubble-time {
  color: rgba(245, 241, 232, 0.7);
}

/* ==================== 快捷回复 ==================== */
.retro-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.retro-reply-ticket {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--retro-sepia);
  color: var(--retro-dark);
  font-size: 12px;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.ticket-perf {
  width: 2px;
  height: 12px;
  background: var(--retro-cream);
}

.retro-reply-ticket:hover {
  background: var(--retro-sepia);
  color: var(--retro-ivory);
}

.retro-reply-ticket:hover .ticket-perf {
  background: var(--retro-sepia-dark);
}

/* ==================== 思考状态 ==================== */
.processing-bubble {
  padding: 14px 18px;
}

.film-processing {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: var(--retro-dark);
}

.film-sprocket {
  display: flex;
  gap: 4px;
}

.sprocket-hole {
  width: 6px;
  height: 10px;
  background: var(--retro-sepia);
  animation: sprocketMove 1s linear infinite;
}

.sprocket-hole:nth-child(2) { animation-delay: 0.1s; }
.sprocket-hole:nth-child(3) { animation-delay: 0.2s; }
.sprocket-hole:nth-child(4) { animation-delay: 0.3s; }

@keyframes sprocketMove {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.processing-text {
  font-style: italic;
}

/* ==================== 输入区域 ==================== */
.retro-input-area {
  background: rgba(232, 220, 200, 0.98);
  border-top: 2px solid var(--retro-sepia);
  padding: 20px 24px 28px;
  position: relative;
  z-index: 10;
}

.input-border-frame {
  position: relative;
  padding: 8px;
  background: var(--retro-ivory);
  box-shadow: 4px 4px 0 var(--retro-sepia);
}

.corner-bracket {
  position: absolute;
  font-size: 16px;
  color: var(--retro-sepia);
  font-family: 'Courier New', monospace;
}

.bracket-tl { top: 4px; left: 4px; }
.bracket-tr { top: 4px; right: 4px; }
.bracket-bl { bottom: 4px; left: 4px; }
.bracket-br { bottom: 4px; right: 4px; }

.retro-input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.retro-action {
  width: 32px;
  height: 32px;
  border: 1px solid var(--retro-sepia);
  background: transparent;
  color: var(--retro-brown);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.retro-action:hover {
  background: var(--retro-sepia);
  color: var(--retro-ivory);
}

.retro-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  font-family: 'Courier New', monospace;
  color: var(--retro-dark);
  outline: none;
  padding: 10px 8px;
}

.retro-input::placeholder {
  color: var(--retro-sepia);
  font-style: italic;
}

.retro-send {
  width: 36px;
  height: 36px;
  border: 2px solid var(--retro-sepia);
  background: transparent;
  color: var(--retro-brown);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.retro-send.active {
  background: var(--retro-sepia);
  color: var(--retro-ivory);
}

.retro-send:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

.retro-footer-mark {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.mark-text {
  font-size: 11px;
  color: var(--retro-sepia);
  letter-spacing: 3px;
  font-family: 'Courier New', monospace;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .retro-messages {
    padding: 24px 16px;
  }

  .retro-content {
    max-width: 80%;
  }
}
</style>
