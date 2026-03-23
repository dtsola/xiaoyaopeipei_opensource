<template>
  <div class="share-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div>
        <h1 class="page-title font-display">分享管理</h1>
        <p class="page-subtitle">管理您的专属推广二维码和分享链接</p>
      </div>
    </div>

    <!-- 二维码卡片 -->
    <div class="card qrcode-card">
      <h2 class="card-title font-display">专属二维码</h2>
      <div class="qrcode-content">
        <div class="qrcode-wrapper" @click="previewQRCode">
          <img :src="qrcodeUrl" alt="专属二维码" class="qrcode-image" />
          <div class="qrcode-overlay">
            <SearchOutlined />
            <span>点击放大</span>
          </div>
        </div>
        <p class="qrcode-tip">扫码即可咨询</p>
        <div class="qrcode-actions">
          <a-button @click="downloadQRCode">
            <DownloadOutlined />
            下载二维码
          </a-button>
        </div>
        <a-alert
          message="建议"
          description="将二维码打印并贴在店铺显眼位置，让更多客户扫码咨询"
          type="info"
          show-icon
          class="qrcode-alert"
        >
          <template #icon>
            <BulbOutlined />
          </template>
        </a-alert>
      </div>
    </div>

    <!-- 专属链接卡片 -->
    <div class="card link-card">
      <h2 class="card-title font-display">专属链接</h2>
      <div class="link-content">
        <div class="link-input-wrapper">
          <a-input
            :value="shareLink"
            readonly
            size="large"
            class="link-input"
          >
            <template #suffix>
              <a-button type="link" @click="copyLink">
                <CopyOutlined />
                复制
              </a-button>
            </template>
          </a-input>
        </div>
        <a-alert
          message="使用建议"
          description="可发朋友圈、微信群、QQ群等社交平台，让更多人了解您的产品"
          type="info"
          show-icon
          class="link-alert"
        >
          <template #icon>
            <BulbOutlined />
          </template>
        </a-alert>
      </div>
    </div>

    <!-- 二维码预览弹窗 -->
    <a-modal
      v-model:open="qrcodePreviewVisible"
      title="专属二维码"
      :footer="null"
      centered
      width="400px"
    >
      <div class="qrcode-preview-modal">
        <img :src="qrcodeUrl" alt="专属二维码" class="preview-image" />
        <div class="preview-actions">
          <a-button type="primary" block @click="downloadQRCode">
            <DownloadOutlined />
            下载二维码
          </a-button>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  DownloadOutlined,
  CopyOutlined,
  BulbOutlined,
  SearchOutlined
} from '@ant-design/icons-vue'
import * as shareApi from '@/api/share'

// 数据
const qrcodeUrl = ref('')
const shareLink = ref('')
const qrcodePreviewVisible = ref(false)

// 刷新二维码
async function refreshQRCode() {
  try {
    const res = await shareApi.refreshQRCode()
    qrcodeUrl.value = res.data.data.qrcode_url
    shareLink.value = res.data.data.share_link
    message.success('二维码已刷新')
  } catch (error) {
    console.error('刷新二维码失败', error)
  }
}

// 获取二维码
async function fetchQRCode() {
  try {
    const res = await shareApi.getQRCode()
    qrcodeUrl.value = res.data.data.qrcode_url
    shareLink.value = res.data.data.share_link
  } catch (error) {
    console.error('获取二维码失败', error)
  }
}

// 预览二维码
function previewQRCode() {
  qrcodePreviewVisible.value = true
}

// 下载二维码
function downloadQRCode() {
  window.open(qrcodeUrl.value, '_blank')
  message.info('图片已在新窗口打开，请右键"图片另存为"保存')
}

// 复制链接
function copyLink() {
  navigator.clipboard.writeText(shareLink.value)
  message.success('链接已复制到剪贴板')
}

// 初始化
onMounted(() => {
  fetchQRCode()
})
</script>

<style scoped>
.share-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 600px;
  margin: 0 auto;
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin-top: 4px;
}

/* ========== 卡片通用样式 ========== */
.card {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
  padding: 24px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color-light);
}

/* ========== 二维码卡片 ========== */
.qrcode-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.qrcode-wrapper {
  position: relative;
  width: 280px;
  height: 280px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: transform var(--transition-base);
}

.qrcode-wrapper:hover {
  transform: scale(1.02);
}

.qrcode-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.qrcode-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  opacity: 0;
  transition: opacity var(--transition-base);
  font-size: 14px;
}

.qrcode-wrapper:hover .qrcode-overlay {
  opacity: 1;
}

.qrcode-tip {
  font-size: 14px;
  color: var(--text-secondary);
}

.qrcode-actions {
  display: flex;
  gap: 12px;
  width: 100%;
}

.qrcode-actions :deep(.ant-btn) {
  flex: 1;
}

.qrcode-alert {
  width: 100%;
}

/* ========== 链接卡片 ========== */
.link-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.link-input-wrapper {
  width: 100%;
}

.link-input :deep(.ant-input) {
  border-radius: var(--radius-md);
}

.link-alert {
  width: 100%;
}

/* ========== 预览弹窗 ========== */
.qrcode-preview-modal {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.preview-image {
  width: 100%;
  max-width: 350px;
  border-radius: var(--radius-md);
}

.preview-actions {
  width: 100%;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .qrcode-wrapper {
    width: 100%;
    max-width: 320px;
  }
}
</style>
