<template>
  <div class="expired-container">
    <div class="expired-card">
      <div class="expired-icon">
        <CloseCircleOutlined />
      </div>
      <h1 class="expired-title">会员已过期</h1>
      <p class="expired-message">
        您的会员已于 {{ expiryDate }} 到期，系统功能已暂停使用。
      </p>
      <p class="expired-tip">请扫码或添加客服微信进行续费，续费后即可正常使用。</p>

      <!-- 二维码展示区域 -->
      <div class="qrcode-section">
        <div class="qrcode-wrapper">
          <img
            src="https://file.xiaoyaosai.com/peipei/kefu/dtsola.png"
            alt="客服微信二维码"
            class="qrcode-image"
          />
        </div>
        <p class="qrcode-label">扫码添加客服微信</p>
      </div>

      <div class="contact-card">
        <div class="contact-info">
          <div class="contact-label">客服微信</div>
          <div class="contact-value">dtsola</div>
        </div>
        <div class="contact-info">
          <div class="contact-label">客服名称</div>
          <div class="contact-value">小遥配配客服</div>
        </div>
      </div>

      <div class="expired-actions">
        <a-button type="primary" size="large" @click="handleCopyWeChat">
          <template #icon><CopyOutlined /></template>
          复制微信号
        </a-button>
        <a-button size="large" @click="handleRefresh">
          <template #icon><ReloadOutlined /></template>
          刷新状态
        </a-button>
      </div>

      <p class="expired-note">
        续费成功后，点击"刷新状态"按钮即可继续使用
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  CloseCircleOutlined,
  CopyOutlined,
  ReloadOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'

const router = useRouter()
const userStore = useUserStore()

const expiryDate = computed(() => {
  if (userStore.user?.membership_expiry) {
    return dayjs(userStore.user.membership_expiry).format('YYYY-MM-DD')
  }
  return '-'
})

// 复制微信号
function handleCopyWeChat() {
  navigator.clipboard.writeText('dtsola').then(() => {
    message.success('微信号已复制到剪贴板')
  }).catch(() => {
    message.error('复制失败，请手动复制：dtsola')
  })
}

// 刷新状态
async function handleRefresh() {
  await userStore.fetchUserInfo()
  if (!userStore.user?.is_membership_expired) {
    message.success('会员状态已更新，即将跳转...')
    setTimeout(() => {
      router.push('/dashboard')
    }, 1000)
  } else {
    message.warning('会员状态仍为过期，请先完成续费')
  }
}

onMounted(async () => {
  // 获取最新的用户信息
  await userStore.fetchUserInfo()
})
</script>

<style scoped>
.expired-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
  box-sizing: border-box;
}

.expired-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 32px 24px;
  max-width: 480px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  text-align: center;
  box-sizing: border-box;
}

.expired-icon {
  font-size: 64px;
  color: #ff4d4f;
  margin-bottom: 16px;
}

.expired-title {
  font-size: 26px;
  font-weight: 700;
  color: #1a1d23;
  margin: 0 0 12px;
}

.expired-message {
  font-size: 15px;
  color: #5a6370;
  margin: 0 0 6px;
}

.expired-tip {
  font-size: 13px;
  color: #8a94a5;
  margin: 0 0 20px;
}

/* 二维码展示区域 */
.qrcode-section {
  margin-bottom: 20px;
}

.qrcode-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}

.qrcode-image {
  width: 160px;
  height: 160px;
  border-radius: 12px;
  border: 2px solid #e8eaed;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.qrcode-label {
  font-size: 13px;
  color: #2563eb;
  font-weight: 500;
  margin: 0;
}

.contact-card {
  background: #fafbfc;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  text-align: left;
}

.contact-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e8eaed;
}

.contact-info:last-child {
  border-bottom: none;
}

.contact-label {
  font-size: 13px;
  color: #8a94a5;
}

.contact-value {
  font-size: 14px;
  font-weight: 600;
  color: #2563eb;
  font-family: 'Courier New', monospace;
}

.expired-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.expired-actions .ant-btn {
  flex: 1;
  height: 42px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
}

.expired-note {
  font-size: 12px;
  color: #8a94a5;
  margin: 0;
}

/* 响应式 */
@media (max-width: 576px) {
  .expired-container {
    padding: 16px;
  }

  .expired-card {
    padding: 24px 20px;
    max-height: calc(100vh - 32px);
  }

  .expired-title {
    font-size: 22px;
  }

  .expired-icon {
    font-size: 56px;
  }

  .qrcode-image {
    width: 140px;
    height: 140px;
  }

  .expired-actions {
    flex-direction: column;
  }
}

/* 滚动条美化 */
.expired-card::-webkit-scrollbar {
  width: 6px;
}

.expired-card::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.expired-card::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.expired-card::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
