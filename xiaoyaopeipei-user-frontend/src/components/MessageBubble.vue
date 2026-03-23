<template>
  <div class="message-bubble" :class="`message-${message.role}`">
    <div class="message-wrapper">
      <!-- 头像 -->
      <div class="avatar-wrapper">
        <div class="avatar" :class="`avatar-${message.role}`">
          <img v-if="message.role === 'assistant'" src="/logo.png" alt="小遥配配" class="assistant-logo" />
          <svg v-else width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 10C12.7614 10 15 7.76142 15 5C15 2.23858 12.7614 0 10 0C7.23858 0 5 2.23858 5 5C5 7.76142 7.23858 10 10 10Z" fill="currentColor"/>
            <path d="M10 12C6.68629 12 2 13.3431 2 15V16C2 17.1046 2.89543 18 4 18H16C17.1046 18 18 17.1046 18 16V15C18 13.3431 13.3137 12 10 12Z" fill="currentColor"/>
          </svg>
        </div>
      </div>

      <!-- 消息内容 -->
      <div class="message-content">
        <div class="message-text" :class="`message-text-${message.role}`">
          <span class="text-content">{{ message.content }}</span>
        </div>

        <!-- 快捷回复按钮 -->
        <div v-if="message.quickReplies && message.quickReplies.length > 0" class="quick-replies">
          <button
            v-for="(reply, index) in message.quickReplies"
            :key="index"
            class="quick-reply-button"
            @click="$emit('quickReply', reply)"
          >
            <span>{{ reply }}</span>
          </button>
        </div>

        <!-- 时间戳 -->
        <div class="message-time">
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage } from '@/types'

interface Props {
  message: ChatMessage
}

defineProps<Props>()
defineEmits<{
  quickReply: [reply: string]
}>()

const formatTime = (timestamp: number): string => {
  const date = new Date(timestamp)
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}
</script>

<style lang="less" scoped>
.message-bubble {
  padding: var(--spacing-lg) var(--spacing-lg);
  animation: fadeInUp var(--transition-slow) ease-out;

  &.message-assistant {
    .message-wrapper {
      flex-direction: row;
    }

    .avatar {
      background: #ffffff;
      margin-right: var(--spacing-md);
      position: relative;
      z-index: 2;
    }

    .message-text {
      background: var(--gradient-message-ai);
      color: var(--color-text-primary);
      border-radius: 4px 18px 18px 18px;
      border: 1px solid rgba(0, 0, 0, 0.04);
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }
  }

  &.message-user {
    .message-wrapper {
      flex-direction: row-reverse;
    }

    .avatar {
      background: var(--color-bg-secondary);
      color: var(--color-text-secondary);
      margin-left: var(--spacing-md);
    }

    .message-text {
      background: var(--gradient-message-user);
      color: var(--color-text-inverse);
      border-radius: 18px 4px 18px 18px;
      box-shadow: var(--shadow-primary-glow);
    }
  }
}

.message-wrapper {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
}

// AI头像
.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-inverse);

  &.avatar-assistant {
    border: 1px solid rgba(0, 0, 0, 0.08);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }

  &.avatar-user {
    border: 1px solid var(--color-border-light);
  }
}

.assistant-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 2px;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-text {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-base);
  line-height: 1.6;
  word-wrap: break-word;
  white-space: pre-wrap;
  max-width: 75%;
  position: relative;
  overflow: hidden;

  .text-content {
    position: relative;
    z-index: 1;
  }
}

// 快捷回复按钮 - 渐变hover效果
.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
}

.quick-reply-button {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--gradient-primary-subtle);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  padding: 0;
  color: var(--color-primary);

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--gradient-primary);
    opacity: 0;
    transition: opacity 0.3s;
    z-index: 0;
  }

  span {
    position: relative;
    z-index: 1;
    display: block;
    padding: var(--spacing-sm) var(--spacing-lg);
    transition: color 0.3s;
  }

  &:hover {
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: var(--shadow-button);

    &::before {
      opacity: 1;
    }

    span {
      color: var(--color-text-inverse);
    }
  }

  &:active {
    transform: scale(0.95);
  }
}

.message-time {
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

@media (max-width: 768px) {
  .message-text {
    max-width: 80%;
  }

  .quick-replies {
    gap: var(--spacing-xs);
  }

  .quick-reply-button {
    span {
      padding: var(--spacing-xs) var(--spacing-md);
      font-size: var(--font-size-xs);
    }
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
