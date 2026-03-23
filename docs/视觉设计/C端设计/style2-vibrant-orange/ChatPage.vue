<template>
  <div class="vibrant-chat-container">
    <!-- 装饰性背景元素 -->
    <div class="bg-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- 顶部导航栏 -->
    <header class="vibrant-header">
      <button class="vibrant-back-btn" @click="goBack">
        <span class="arrow-icon">‹</span>
      </button>
      <div class="header-center">
        <div class="brand-badge">
          <span class="badge-emoji">🔥</span>
          <span class="badge-text">小遥配配</span>
        </div>
        <div class="header-tagline">AI电脑导购助手</div>
      </div>
      <button class="vibrant-menu-btn">
        <span class="menu-dot"></span>
        <span class="menu-dot"></span>
        <span class="menu-dot"></span>
      </button>
    </header>

    <!-- 对话消息区域 -->
    <main class="vibrant-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['msg-row', msg.role === 'user' ? 'msg-user' : 'msg-ai']">

        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="msg-avatar ai-avatar-vibrant">
            <div class="avatar-ring-glow"></div>
            <span class="avatar-emoji">🤖</span>
          </div>
          <div class="msg-content-ai">
            <div class="msg-bubble-ai">
              <div class="bubble-deco"></div>
              <div class="msg-text" v-html="formatMessage(msg.content)"></div>
              <div v-if="msg.quickReplies && msg.quickReplies.length" class="quick-chips">
                <button v-for="(reply, i) in msg.quickReplies" :key="i"
                        class="quick-chip"
                        :style="{ '--chip-color': getChipColor(i) }"
                        @click="sendQuickReply(reply)">
                  <span class="chip-emoji">{{ getChipEmoji(i) }}</span>
                  {{ reply }}
                </button>
              </div>
              <span class="msg-time">{{ msg.time }}</span>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="msg-content-user">
            <div class="msg-bubble-user">
              <div class="bubble-sparkle"></div>
              <div class="msg-text">{{ msg.content }}</div>
              <span class="msg-time">{{ msg.time }}</span>
            </div>
          </div>
          <div class="msg-avatar user-avatar-vibrant">
            <span class="avatar-emoji">😊</span>
          </div>
        </template>
      </div>

      <!-- AI思考状态 -->
      <div v-if="isTyping" class="msg-row msg-ai">
        <div class="msg-avatar ai-avatar-vibrant typing">
          <div class="avatar-ring-glow pulse"></div>
          <span class="avatar-emoji">🤖</span>
        </div>
        <div class="msg-content-ai">
          <div class="msg-bubble-ai typing-bubble">
            <div class="typing-waves">
              <span></span><span></span><span></span>
            </div>
            <span class="typing-text">小遥思考中...</span>
          </div>
        </div>
      </div>
    </main>

    <!-- 底部输入区域 -->
    <footer class="vibrant-input-area">
      <div class="input-wrapper">
        <button class="emoji-btn" @click="toggleEmoji">
          <span class="emoji-icon">😊</span>
        </button>
        <div class="input-field-container">
          <input
            ref="inputRef"
            v-model="inputText"
            type="text"
            class="vibrant-input"
            placeholder="告诉我你想要什么样的电脑~"
            @keypress.enter="sendMessage"
            @focus="handleInputFocus"
          />
          <div class="input-deco-line"></div>
        </div>
        <button
          :class="['send-btn-vibrant', { active: inputText.trim() }]"
          :disabled="!inputText.trim() || isTyping"
          @click="sendMessage"
        >
          <span class="send-icon" v-show="!inputText.trim()">✨</span>
          <span class="send-text" v-show="inputText.trim()">发送</span>
        </button>
      </div>
      <div class="input-footer">
        <span class="footer-tag"># 智能推荐</span>
        <span class="footer-tag"># 专业配置</span>
        <span class="footer-tag"># 省心省力</span>
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

const chipEmojis = ['💰', '🎮', '💻', '🏆']
const chipColors = ['#FF6B35', '#00D9A5', '#7B68EE', '#FF3366']

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: '嗨~ 我是AI导购小遥！👋\n\n找我帮你选电脑，保证不踩坑！\n\n首先告诉我，你的预算大概是多少呢？',
    time: '14:30',
    quickReplies: ['3000-5000元', '5000-8000元', '8000-12000元', '12000+']
  }
])

const inputText = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

const getChipEmoji = (index: number) => chipEmojis[index % chipEmojis.length]
const getChipColor = (index: number) => chipColors[index % chipColors.length]

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
      content: `收到！${userMessage.content}的需求已记下~\n\n再问一下，你需要经常带出门吗？还是主要放在家里用？🤔`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['经常带出门', '主要家用', '不确定']
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

const toggleEmoji = () => {
  console.log('Emoji picker')
}

const goBack = () => {
  console.log('返回')
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* ==================== 活力橙风格样式变量 ==================== */
:root {
  --vibrant-orange: #FF6B35;
  --vibrant-orange-light: #FF8C42;
  --vibrant-orange-dark: #E55A2B;
  --mint-green: #00D9A5;
  --purple-blue: #7B68EE;
  --hot-pink: #FF3366;
  --cream-bg: #FFF8F3;
  --white: #FFFFFF;
  --text-dark: #2D2D2D;
  --text-gray: #666666;
  --text-light: #999999;
}

/* ==================== 容器 ==================== */
.vibrant-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: linear-gradient(180deg, #FFF8F3 0%, #FFE8D6 50%, #FFD8C2 100%);
  font-family: 'Nunito', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  overflow: hidden;
  position: relative;
}

/* ==================== 背景装饰 ==================== */
.bg-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.5;
  animation: blobFloat 20s ease-in-out infinite;
}

.blob-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, var(--vibrant-orange), var(--hot-pink));
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.blob-2 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, var(--mint-green), var(--purple-blue));
  bottom: 20%;
  left: -80px;
  animation-delay: -7s;
}

.blob-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, var(--purple-blue), var(--vibrant-orange-light));
  bottom: -50px;
  right: 20%;
  animation-delay: -14s;
}

@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.1); }
  50% { transform: translate(-20px, 20px) scale(0.9); }
  75% { transform: translate(-30px, -20px) scale(1.05); }
}

/* ==================== 顶部导航 ==================== */
.vibrant-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 10;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.1);
}

.vibrant-back-btn {
  width: 44px;
  height: 44px;
  border: none;
  background: linear-gradient(135deg, var(--vibrant-orange), var(--vibrant-orange-light));
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

.vibrant-back-btn:hover {
  transform: scale(1.1) rotate(-10deg);
}

.vibrant-back-btn .arrow-icon {
  font-size: 28px;
  color: white;
  font-weight: 300;
  margin-left: -4px;
}

.header-center {
  text-align: center;
  flex: 1;
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, var(--vibrant-orange), var(--hot-pink));
  padding: 8px 20px;
  border-radius: 30px;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

.badge-emoji {
  font-size: 20px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.badge-text {
  font-size: 18px;
  font-weight: 800;
  color: white;
  letter-spacing: 1px;
}

.header-tagline {
  margin-top: 6px;
  font-size: 12px;
  color: var(--text-gray);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.vibrant-menu-btn {
  width: 44px;
  height: 44px;
  border: none;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.vibrant-menu-btn:hover {
  transform: rotate(90deg);
}

.menu-dot {
  width: 6px;
  height: 6px;
  background: var(--vibrant-orange);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.vibrant-menu-btn:hover .menu-dot:nth-child(1) { background: var(--vibrant-orange); }
.vibrant-menu-btn:hover .menu-dot:nth-child(2) { background: var(--mint-green); }
.vibrant-menu-btn:hover .menu-dot:nth-child(3) { background: var(--hot-pink); }

/* ==================== 消息区域 ==================== */
.vibrant-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 16px;
  position: relative;
  z-index: 1;
  scroll-behavior: smooth;
}

.vibrant-messages::-webkit-scrollbar {
  width: 0;
}

.msg-row {
  display: flex;
  margin-bottom: 24px;
  animation: msgPopIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes msgPopIn {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.msg-ai {
  justify-content: flex-start;
}

.msg-user {
  justify-content: flex-end;
}

/* ==================== 头像 ==================== */
.msg-avatar {
  width: 50px;
  height: 50px;
  flex-shrink: 0;
  position: relative;
}

.ai-avatar-vibrant {
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-ring-glow {
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, var(--vibrant-orange), var(--mint-green), var(--purple-blue), var(--hot-pink), var(--vibrant-orange));
  animation: ringSpin 3s linear infinite;
}

.avatar-ring-glow::before {
  content: '';
  position: absolute;
  inset: 3px;
  background: #FFE8D6;
  border-radius: 50%;
}

@keyframes ringSpin {
  to { transform: rotate(360deg); }
}

.avatar-ring-glow.pulse {
  animation: ringSpin 3s linear infinite, ringPulse 1.5s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% { transform: rotate(0deg) scale(1); opacity: 0.8; }
  50% { transform: rotate(180deg) scale(1.1); opacity: 1; }
}

.ai-avatar-vibrant .avatar-emoji {
  font-size: 26px;
  position: relative;
  z-index: 1;
}

.user-avatar-vibrant {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, var(--purple-blue), var(--mint-green));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 8px;
  box-shadow: 0 4px 15px rgba(123, 104, 238, 0.3);
}

.user-avatar-vibrant .avatar-emoji {
  font-size: 22px;
}

/* ==================== AI消息气泡 ==================== */
.msg-content-ai {
  max-width: 75%;
  margin-left: 12px;
}

.msg-bubble-ai {
  background: white;
  border-radius: 24px 24px 24px 8px;
  padding: 16px 20px;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.12);
  position: relative;
  border: 3px solid transparent;
  background-clip: padding-box;
}

.msg-bubble-ai::before {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 24px 24px 24px 8px;
  background: linear-gradient(135deg, var(--vibrant-orange), var(--mint-green));
  z-index: -1;
  opacity: 0.1;
}

.bubble-deco {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, var(--vibrant-orange), var(--hot-pink));
  border-radius: 50%;
  opacity: 0.8;
}

.msg-bubble-ai .msg-text {
  font-size: 15px;
  line-height: 1.7;
  color: var(--text-dark);
  font-weight: 500;
}

/* ==================== 快捷回复芯片 ==================== */
.quick-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.quick-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: white;
  border: 2px solid var(--chip-color, var(--vibrant-orange));
  border-radius: 50px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-dark);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.quick-chip:hover {
  background: var(--chip-color, var(--vibrant-orange));
  color: white;
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.chip-emoji {
  font-size: 16px;
}

/* ==================== 用户消息气泡 ==================== */
.msg-content-user {
  max-width: 75%;
  margin-right: 12px;
}

.msg-bubble-user {
  background: linear-gradient(135deg, var(--vibrant-orange), var(--vibrant-orange-light));
  border-radius: 24px 24px 8px 24px;
  padding: 16px 20px;
  box-shadow: 0 6px 25px rgba(255, 107, 53, 0.35);
  position: relative;
  overflow: hidden;
}

.bubble-sparkle {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='20' cy='20' r='2' fill='white' opacity='0.3'/%3E%3Ccircle cx='80' cy='40' r='1.5' fill='white' opacity='0.3'/%3E%3Ccircle cx='40' cy='70' r='2.5' fill='white' opacity='0.3'/%3E%3C/svg%3E");
  animation: sparkle 3s linear infinite;
}

@keyframes sparkle {
  to { background-position: 100px 100px; }
}

.msg-bubble-user .msg-text {
  font-size: 15px;
  line-height: 1.6;
  color: white;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

/* ==================== 消息时间 ==================== */
.msg-time {
  display: block;
  font-size: 11px;
  color: var(--text-light);
  margin-top: 8px;
  opacity: 0.7;
}

.msg-bubble-user .msg-time {
  color: rgba(255, 255, 255, 0.8);
}

/* ==================== 打字动画 ==================== */
.typing-bubble {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
}

.typing-waves {
  display: flex;
  gap: 6px;
}

.typing-waves span {
  width: 10px;
  height: 10px;
  background: linear-gradient(135deg, var(--vibrant-orange), var(--hot-pink));
  border-radius: 50%;
  animation: wave 1.4s ease-in-out infinite;
}

.typing-waves span:nth-child(1) { animation-delay: 0s; }
.typing-waves span:nth-child(2) { animation-delay: 0.2s; }
.typing-waves span:nth-child(3) { animation-delay: 0.4s; }

@keyframes wave {
  0%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translateY(-12px) scale(1.2);
    opacity: 1;
  }
}

.typing-text {
  font-size: 13px;
  color: var(--text-gray);
  font-weight: 600;
}

/* ==================== 输入区域 ==================== */
.vibrant-input-area {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 16px 20px 24px;
  position: relative;
  z-index: 10;
  border-top: 1px solid rgba(255, 107, 53, 0.1);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border-radius: 30px;
  padding: 8px 8px 8px 16px;
  box-shadow: 0 8px 30px rgba(255, 107, 53, 0.15);
  border: 3px solid transparent;
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: var(--vibrant-orange);
  box-shadow: 0 8px 40px rgba(255, 107, 53, 0.25);
}

.emoji-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: linear-gradient(135deg, var(--mint-green), #00E5B8);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 4px 12px rgba(0, 217, 165, 0.3);
}

.emoji-btn:hover {
  transform: scale(1.15) rotate(-10deg);
}

.emoji-icon {
  font-size: 22px;
}

.input-field-container {
  flex: 1;
  position: relative;
}

.vibrant-input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 15px;
  color: var(--text-dark);
  font-weight: 500;
  padding: 10px 0;
  outline: none;
}

.vibrant-input::placeholder {
  color: var(--text-light);
  font-weight: 400;
}

.input-deco-line {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 0;
  background: linear-gradient(90deg, var(--vibrant-orange), var(--hot-pink));
  transition: width 0.3s ease;
}

.vibrant-input:focus + .input-deco-line {
  width: 100%;
}

.send-btn-vibrant {
  width: 50px;
  height: 50px;
  border: none;
  background: linear-gradient(135deg, var(--text-light), var(--text-gray));
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.send-btn-vibrant.active {
  background: linear-gradient(135deg, var(--vibrant-orange), var(--hot-pink));
  box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
}

.send-btn-vibrant.active:hover {
  transform: scale(1.1);
}

.send-btn-vibrant:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.send-icon {
  font-size: 20px;
  animation: sparkle 2s ease-in-out infinite;
}

.send-text {
  font-size: 14px;
  font-weight: 700;
  color: white;
}

/* ==================== 底部标签 ==================== */
.input-footer {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 12px;
}

.footer-tag {
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.1), rgba(255, 51, 102, 0.1));
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  color: var(--vibrant-orange);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* ==================== 响应式 ==================== */
@media (max-width: 480px) {
  .msg-bubble-ai, .msg-bubble-user {
    padding: 14px 16px;
  }

  .quick-chip {
    padding: 8px 14px;
    font-size: 12px;
  }
}
</style>
