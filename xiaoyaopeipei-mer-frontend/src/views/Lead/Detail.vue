<template>
  <div class="lead-detail-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <a-button @click="router.back()" class="back-btn">
          <LeftOutlined />
        </a-button>
        <div>
          <h1 class="page-title font-display">线索详情</h1>
          <p class="page-subtitle">查看客户详细信息和跟进记录</p>
        </div>
      </div>
      <div class="header-actions">
        <a-button @click="handleCall">
          <template #icon><PhoneOutlined /></template>
          联系客户
        </a-button>
        <a-button @click="handleCopyWechat">
          <template #icon><WechatOutlined /></template>
          发送微信
        </a-button>
      </div>
    </div>

    <div v-if="leadDetail" class="detail-content">
      <!-- 客户信息卡片 -->
      <div class="card customer-card">
        <div class="card-header">
          <h2 class="card-title font-display">客户信息</h2>
          <a-dropdown :trigger="['click']">
            <a-button class="status-btn" :class="`status-${leadDetail.status}`">
              <a-badge :status="getStatusBadge(leadDetail.status)" :text="getStatusText(leadDetail.status)" />
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu @click="handleStatusChange">
                <a-menu-item key="pending">
                  <a-badge status="warning" text="待跟进" />
                </a-menu-item>
                <a-menu-item key="contacted">
                  <a-badge status="processing" text="已联系" />
                </a-menu-item>
                <a-menu-item key="closed">
                  <a-badge status="success" text="已成交" />
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="abandoned">
                  <a-badge status="default" text="已放弃" />
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>

        <div class="customer-info-grid">
          <div class="info-item">
            <span class="info-label">客户ID</span>
            <span class="info-value">{{ leadDetail.id.slice(-6) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">手机号</span>
            <div class="info-value-with-action">
              <span>{{ maskPhone(leadDetail.phone) }}</span>
              <a-button type="link" size="small" @click="copyText(leadDetail.phone)">
                <CopyOutlined />
              </a-button>
            </div>
          </div>
          <div class="info-item" v-if="leadDetail.wechat">
            <span class="info-label">微信号</span>
            <div class="info-value-with-action">
              <span>{{ leadDetail.wechat }}</span>
              <a-button type="link" size="small" @click="copyText(leadDetail.wechat!)">
                <CopyOutlined />
              </a-button>
            </div>
          </div>
          <div class="info-item">
            <span class="info-label">咨询时间</span>
            <span class="info-value">{{ formatDateTime(leadDetail.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- 双列布局 -->
      <div class="detail-grid">
        <!-- 左列 -->
        <div class="detail-column">
          <!-- 需求画像 -->
          <div class="card needs-card">
            <h2 class="card-title font-display">
              <AimOutlined class="title-icon" />
              需求画像（AI提取）
            </h2>
            <div class="needs-content">
              <div class="need-item">
                <DollarOutlined class="need-icon" />
                <div class="need-detail">
                  <span class="need-label">预算</span>
                  <span class="need-value">{{ leadDetail.budget }}</span>
                </div>
              </div>
              <div class="need-item">
                <LaptopOutlined class="need-icon" />
                <div class="need-detail">
                  <span class="need-label">设备类型</span>
                  <span class="need-value">{{ leadDetail.device_type }}</span>
                </div>
              </div>
              <div class="need-item">
                <ControlOutlined class="need-icon" />
                <div class="need-detail">
                  <span class="need-label">用途</span>
                  <span class="need-value">{{ leadDetail.usage }}</span>
                </div>
              </div>
              <div v-if="leadDetail.requirements" class="need-item">
                <FileTextOutlined class="need-icon" />
                <div class="need-detail">
                  <span class="need-label">具体需求</span>
                  <span class="need-value">{{ leadDetail.requirements }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 完整对话记录 -->
          <div v-if="conversationMessages.length > 0" class="card conversation-card">
            <h2 class="card-title font-display">完整对话记录</h2>

            <div class="conversation-messages">
              <div
                v-for="message in displayMessages"
                :key="message.id"
                class="message-item"
                :class="`message-${message.role}`"
              >
                <div class="message-header">
                  <span class="message-sender">
                    {{ message.role === 'assistant' ? '小遥' : '客户' }}
                  </span>
                  <span class="message-time">{{ formatMessageTime(message.created_at) }}</span>
                </div>
                <div class="message-content">{{ message.content }}</div>
              </div>

              <!-- 展开按钮 -->
              <div v-if="conversationMessages.length > 3 && !showAllMessages" class="expand-button">
                <a-button type="link" @click="showAllMessages = true">
                  展开完整对话
                  <DownOutlined />
                </a-button>
              </div>
              <div v-if="showAllMessages" class="expand-button">
                <a-button type="link" @click="showAllMessages = false">
                  收起对话
                  <UpOutlined />
                </a-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 右列 -->
        <div class="detail-column">
          <!-- 选中方案 -->
          <div v-if="leadDetail.selected_sku" class="card sku-card">
            <h2 class="card-title font-display">选中方案</h2>
            <div class="sku-display" @click="handleViewSkuDetail" @click.middle="handleViewSkuDetailNewTab">
              <div class="sku-image-wrapper">
                <img v-if="skuDisplayImage" :src="skuDisplayImage" alt="SKU" class="sku-image" />
                <div v-else class="sku-image-placeholder">
                  <span>无图片</span>
                </div>
              </div>
              <div class="sku-info">
                <h3 class="sku-name">{{ leadDetail.selected_sku.name }}</h3>
                <div class="sku-reason">
                  <span class="reason-label">AI推荐理由：</span>
                  这款配置搭载强劲显卡，性能出色，性价比很高！
                </div>
                <div class="sku-price">
                  <span class="price-symbol">¥</span>
                  <span class="price-value">{{ leadDetail.selected_sku.price?.toLocaleString() }}</span>
                </div>
                <div class="sku-action">
                  <a-button size="small" type="link">
                    查看详情
                    <template #icon><RightOutlined /></template>
                  </a-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 跟进记录 -->
          <div class="card notes-card">
            <h2 class="card-title font-display">跟进记录</h2>

            <!-- 添加备注 -->
            <div class="add-note-section">
              <a-textarea
                v-model:value="newNote"
                placeholder="添加跟进备注..."
                :rows="3"
                :maxlength="500"
                show-count
              />
              <div class="note-actions">
                <span class="note-tip">按 Enter 换行，Shift+Enter 快速提交</span>
                <a-button type="primary" @click="handleAddNote">
                  <template #icon><PlusOutlined /></template>
                  添加备注
                </a-button>
              </div>
            </div>

            <!-- 历史备注 -->
            <div v-if="leadDetail.notes && leadDetail.notes.length > 0" class="notes-list">
              <div
                v-for="(note, index) in leadDetail.notes"
                :key="index"
                class="note-item"
              >
                <div class="note-avatar">M</div>
                <div class="note-content">
                  <div class="note-header">
                    <span class="note-author">商家</span>
                    <span class="note-time">{{ formatDateTime(note.created_at) }}</span>
                  </div>
                  <div class="note-text">{{ note.content }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 联系客户弹窗 -->
    <a-modal
      v-model:open="callModalVisible"
      title="联系客户"
      centered
      @ok="handleCallConfirm"
    >
      <p class="call-info">
        手机号：<strong>{{ leadDetail?.phone ? maskPhone(leadDetail.phone) : '' }}</strong>
      </p>
      <p v-if="leadDetail?.wechat" class="call-wechat">
        微信号：{{ leadDetail.wechat }}
      </p>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onActivated, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  LeftOutlined,
  PhoneOutlined,
  WechatOutlined,
  CopyOutlined,
  DownOutlined,
  UpOutlined,
  RightOutlined,
  StarFilled,
  PlusOutlined,
  AimOutlined,
  DollarOutlined,
  LaptopOutlined,
  ControlOutlined,
  FileTextOutlined
} from '@ant-design/icons-vue'
import { useLeadStore } from '@/stores/lead'
import { useSkuStore } from '@/stores/sku'
import type { LeadDetail as LeadDetailType, LeadStatus, ConversationMessage, SKU } from '@/types'
import { getLeadMessages } from '@/api/lead'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()
const leadStore = useLeadStore()
const skuStore = useSkuStore()

// 线索详情
const leadDetail = ref<LeadDetailType | null>(null)

// 完整的SKU详情（用于显示图片）
const fullSkuDetail = ref<SKU | null>(null)

// 新备注
const newNote = ref('')

// 拨打电话弹窗
const callModalVisible = ref(false)

// 对话消息
const conversationMessages = ref<ConversationMessage[]>([])
const showAllMessages = ref(false)

// 显示的消息（默认只显示前3条）
const displayMessages = computed(() => {
  if (showAllMessages.value) {
    return conversationMessages.value
  }
  return conversationMessages.value.slice(0, 3)
})

// 获取SKU显示图片（优先使用完整SKU详情的图片，否则为空）
const skuDisplayImage = computed(() => {
  return fullSkuDetail.value?.images?.[0] || ''
})

// 获取状态徽标类型
function getStatusBadge(status: LeadStatus): 'success' | 'processing' | 'default' | 'warning' {
  const statusMap: Record<LeadStatus, 'success' | 'processing' | 'default' | 'warning'> = {
    pending: 'warning',
    contacted: 'processing',
    closed: 'success',
    abandoned: 'default'
  }
  return statusMap[status]
}

// 获取状态文本
function getStatusText(status: LeadStatus): string {
  const textMap: Record<LeadStatus, string> = {
    pending: '待跟进',
    contacted: '已联系',
    closed: '已成交',
    abandoned: '已放弃'
  }
  return textMap[status]
}

// 格式化日期时间
function formatDateTime(time: string): string {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

// 格式化消息时间（只显示时分秒）
function formatMessageTime(time: string): string {
  return dayjs(time).format('HH:mm:ss')
}

// 手机号脱敏
function maskPhone(phone: string): string {
  if (phone && phone.length === 11) {
    return `${phone.slice(0, 3)}****${phone.slice(7)}`
  }
  return phone
}

// 复制文本
function copyText(text: string) {
  navigator.clipboard.writeText(text)
  message.success('已复制到剪贴板')
}

// 复制微信号
function handleCopyWechat() {
  if (leadDetail.value?.wechat) {
    copyText(leadDetail.value.wechat)
    message.success('微信号已复制，请打开微信添加好友')
  } else {
    message.warning('该客户未留下微信号')
  }
}

// 联系客户
function handleCall() {
  if (leadDetail.value?.phone) {
    navigator.clipboard.writeText(leadDetail.value.phone)
    message.success('电话号码已复制')
  } else {
    message.warning('电话号码不可用')
  }
}

// 查看SKU详情（新标签页打开）
function handleViewSkuDetail() {
  handleViewSkuDetailNewTab()
}

// 在新标签页打开SKU编辑页
function handleViewSkuDetailNewTab() {
  if (leadDetail.value?.selected_sku?.id) {
    const url = router.resolve(`/sku/edit/${leadDetail.value.selected_sku.id}`).href
    window.open(url, '_blank')
  } else {
    message.warning('该线索未选择配置方案')
  }
}

// 状态变更
async function handleStatusChange({ key }: { key: string }) {
  const newStatus = key as LeadStatus
  try {
    await leadStore.updateStatus(route.params.id as string, newStatus)
    message.success(`状态已更新为：${getStatusText(newStatus)}`)
    await fetchLeadDetail()
  } catch (error) {
    console.error('更新状态失败', error)
  }
}

// 添加备注
async function handleAddNote() {
  if (!newNote.value.trim()) {
    message.warning('请输入备注内容')
    return
  }

  try {
    await leadStore.addNote(route.params.id as string, newNote.value)
    newNote.value = ''
    message.success('备注添加成功')
    await fetchLeadDetail()
  } catch (error) {
    console.error('添加备注失败', error)
  }
}

// 获取线索详情
async function fetchLeadDetail() {
  try {
    const data = await leadStore.fetchDetail(route.params.id as string)
    leadDetail.value = data as LeadDetailType

    // 如果有选中的SKU，获取完整的SKU详情（包含图片）
    if (data.selected_sku?.id) {
      try {
        console.log('线索ID:', route.params.id)
        console.log('selected_sku:', data.selected_sku)
        console.log('即将获取SKU详情，ID:', data.selected_sku.id)
        fullSkuDetail.value = await skuStore.fetchDetail(data.selected_sku.id)
      } catch (error) {
        console.error('获取SKU详情失败', error)
        fullSkuDetail.value = null
      }
    } else {
      fullSkuDetail.value = null
    }

    // 获取对话消息
    await fetchConversationMessages()
  } catch (error) {
    console.error('获取线索详情失败', error)
    message.error('获取线索详情失败')
  }
}

// 获取对话消息
async function fetchConversationMessages() {
  try {
    const res = await getLeadMessages(route.params.id as string)
    conversationMessages.value = res.data.data.items
  } catch (error) {
    console.error('获取对话消息失败', error)
  }
}

// 初始化
onMounted(() => {
  fetchLeadDetail()
})

// 监听路由参数变化（修复KeepAlive缓存时数据不更新的问题）
watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      // 重置数据
      leadDetail.value = null
      fullSkuDetail.value = null
      conversationMessages.value = []
      newNote.value = ''
      // 重新获取数据
      fetchLeadDetail()
    }
  }
)

// 页面激活时刷新数据
onActivated(() => {
  fetchLeadDetail()
})
</script>

<style scoped>
.lead-detail-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
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

.header-actions {
  display: flex;
  gap: 12px;
}

/* ========== 客户信息卡片 ========== */
.customer-card {
  padding: 24px;
}

.customer-info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 13px;
  color: var(--text-tertiary);
  font-weight: 500;
}

.info-value {
  font-size: 15px;
  color: var(--text-primary);
  font-weight: 500;
}

.info-value-with-action {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-btn {
  padding: 6px 16px;
  border-radius: var(--radius-full);
}

/* ========== 双列布局 ========== */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.detail-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========== 卡片通用样式 ========== */
.card {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
  padding: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color-light);
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 22px;
}

/* ========== 需求画像 ========== */
.needs-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.need-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.need-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.need-detail {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.need-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

.need-value {
  font-size: 15px;
  color: var(--text-primary);
  font-weight: 500;
}

.confidence-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, var(--warning-lighter), var(--warning-light));
  border-radius: var(--radius-md);
  border: 1px solid var(--warning-color);
}

.confidence-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--warning-color);
}

.confidence-stars {
  display: flex;
  gap: 4px;
}

.star {
  font-size: 18px;
  color: var(--border-color);
}

.star.active {
  color: #fbbf24;
}

.confidence-value {
  margin-left: auto;
  font-size: 16px;
  font-weight: 700;
  color: var(--warning-color);
}

/* ========== 对话信息 ========== */
.conversation-messages {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  padding: 12px 16px;
  border-radius: var(--radius-md);
  background: var(--bg-hover);
}

.message-item.message-assistant {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-left: 3px solid var(--primary-color);
}

.message-item.message-user {
  background: var(--bg-secondary);
  border-left: 3px solid var(--text-tertiary);
}

.message-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.message-sender {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.message-sender::before {
  content: '[';
  margin-right: 2px;
}

.message-sender::after {
  content: ']';
  margin-left: 2px;
}

.message-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.message-content {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.expand-button {
  display: flex;
  justify-content: center;
  padding: 8px 0;
}

/* ========== 选中方案 ========== */
.sku-display {
  display: flex;
  gap: 20px;
  cursor: pointer;
  transition: all var(--transition-base);
  border-radius: var(--radius-md);
  padding: 8px;
  margin: -8px;
}

.sku-display:hover {
  background: var(--bg-hover);
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
}

.sku-image-wrapper {
  width: 120px;
  height: 120px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  flex-shrink: 0;
}

.sku-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sku-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-hover);
  color: var(--text-tertiary);
  font-size: 13px;
}

.sku-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sku-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.sku-specs {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.spec-row {
  display: flex;
  gap: 8px;
  font-size: 13px;
}

.spec-label {
  color: var(--text-tertiary);
  min-width: 40px;
}

.spec-value {
  color: var(--text-primary);
  font-weight: 500;
}

.sku-reason {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  padding: 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.reason-label {
  font-weight: 600;
  color: var(--text-primary);
}

.sku-price {
  display: flex;
  align-items: baseline;
  margin-top: auto;
}

.price-symbol {
  font-size: 16px;
  color: var(--danger-color);
  font-weight: 600;
}

.price-value {
  font-size: 24px;
  color: var(--danger-color);
  font-weight: 700;
}

.sku-action {
  margin-top: 8px;
}

.sku-action :deep(.ant-btn-link) {
  padding: 0;
  height: auto;
  font-size: 13px;
}

/* ========== 跟进记录 ========== */
.add-note-section {
  margin-bottom: 20px;
}

.note-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}

.note-tip {
  font-size: 12px;
  color: var(--text-tertiary);
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.note-item {
  display: flex;
  gap: 12px;
}

.note-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--success-color), #10b981);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.note-content {
  flex: 1;
  padding: 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.note-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.note-author {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.note-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.note-text {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.6;
}

/* ========== 拨打电话弹窗 ========== */
.call-info {
  font-size: 16px;
  margin-bottom: 8px;
}

.call-wechat {
  font-size: 14px;
  color: var(--text-secondary);
}

/* ========== 响应式 ========== */
@media (max-width: 1200px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .header-actions {
    justify-content: stretch;
  }

  .header-actions :deep(.ant-btn) {
    flex: 1;
  }

  .customer-info-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .sku-display {
    flex-direction: column;
  }

  .sku-image-wrapper {
    width: 100%;
    height: 200px;
  }
}

:deep(.ant-btn-link) .rotate {
  transform: rotate(180deg);
}
</style>
