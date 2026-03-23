<template>
  <div class="lead-list-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div>
        <h1 class="page-title font-display">客户线索管理</h1>
        <p class="page-subtitle">跟进您的客户线索，提升转化率</p>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar card">
      <!-- 状态Tab -->
      <div class="status-tabs">
        <div
          v-for="tab in statusTabs"
          :key="tab.key"
          class="status-tab"
          :class="{ active: activeStatus === tab.key }"
          @click="activeStatus = tab.key"
        >
          {{ tab.label }}
          <span v-if="tab.count > 0" class="tab-count">{{ tab.count }}</span>
        </div>
      </div>

      <!-- 筛选控件 -->
      <div class="filter-controls">
        <!-- 设备类型筛选 -->
        <a-checkbox-group v-model:value="selectedDeviceTypes" class="device-filter">
          <a-checkbox value="desktop">台式机</a-checkbox>
          <a-checkbox value="laptop">笔记本</a-checkbox>
          <a-checkbox value="aio">一体机</a-checkbox>
        </a-checkbox-group>

        <!-- 搜索框 -->
        <a-input-search
          v-model:value="searchKeyword"
          placeholder="搜索客户手机号、需求..."
          style="width: 280px"
          allow-clear
          @search="handleSearch"
        >
          <template #prefix>
            <SearchOutlined />
          </template>
        </a-input-search>
      </div>
    </div>

    <!-- 线索列表 -->
    <div v-if="filteredLeads.length > 0" class="leads-content">
      <div
        v-for="lead in paginatedLeads"
        :key="lead.id"
        class="lead-card card"
        :class="[`status-${lead.status}`, { new: isNewLead(lead.created_at) }]"
        @click="router.push(`/leads/${lead.id}`)"
      >
        <!-- 左侧：状态指示条 -->
        <div class="lead-status-bar"></div>

        <!-- 内容区域 -->
        <div class="lead-main">
          <!-- 头部：客户信息 + 状态 -->
          <div class="lead-header-row">
            <div class="lead-info">
              <div class="lead-avatar">
                <UserOutlined />
              </div>
              <div>
                <div class="lead-name">
                  客户{{ lead.id.slice(-4) }}
                  <a-tag v-if="isNewLead(lead.created_at)" color="red" class="new-tag">NEW</a-tag>
                </div>
                <div class="lead-contact">
                  <span class="contact-item">
                    <PhoneOutlined />
                    {{ lead.phone }}
                  </span>
                  <span v-if="lead.wechat" class="contact-item">
                    <WechatOutlined />
                    {{ lead.wechat }}
                  </span>
                </div>
              </div>
            </div>

            <a-dropdown :trigger="['click']" @click.stop>
              <a-button class="status-dropdown-btn">
                <a-badge :status="getStatusBadge(lead.status)" :text="getStatusText(lead.status)" />
                <DownOutlined />
              </a-button>
              <template #overlay>
                <a-menu @click="(e) => handleStatusChange(lead.id, e.key)">
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

          <!-- 需求摘要 -->
          <div class="lead-needs">
            <div class="need-row">
              <span class="need-icon"><span class="icon-dollar"></span></span>
              <span class="need-label">预算：</span>
              <span class="need-value">{{ lead.budget }}</span>
            </div>
            <div class="need-row">
              <span class="need-icon"><span class="icon-device"></span></span>
              <span class="need-label">{{ lead.device_type }} | {{ lead.usage }}</span>
              <span v-if="lead.requirements" class="need-extra"> | {{ lead.requirements }}</span>
            </div>
          </div>

          <!-- 选中的方案 -->
          <div v-if="lead.selected_sku" class="lead-sku">
            <ShoppingOutlined />
            <span class="sku-label">选中方案：</span>
            <span class="sku-name">{{ lead.selected_sku.name }}</span>
            <span class="sku-price">¥{{ lead.selected_sku.price?.toLocaleString() }}</span>
          </div>

          <!-- 底部：时间 + 操作 -->
          <div class="lead-footer">
            <span class="lead-time">
              <ClockCircleOutlined />
              {{ formatTime(lead.created_at) }}
            </span>
            <div class="lead-actions" @click.stop>
              <a-button size="small" @click="handleCall(lead)">
                <PhoneOutlined />
                拨打
              </a-button>
              <a-button type="primary" size="small" @click="router.push(`/leads/${lead.id}`)">
                查看详情
              </a-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <a-empty
      v-else
      description="暂无线索数据"
      :image="Empty.PRESENTED_IMAGE_SIMPLE"
      class="empty-state"
    />

    <!-- 分页 -->
    <div v-if="filteredLeads.length > pageSize" class="pagination-wrapper">
      <a-pagination
        v-model:current="currentPage"
        v-model:page-size="pageSize"
        :total="filteredLeads.length"
        show-size-changer
        show-quick-jumper
        :show-total="(total) => `共 ${total} 条线索`"
        @change="handlePageChange"
      />
    </div>

    <!-- 拨打电话弹窗 -->
    <a-modal
      v-model:open="callModalVisible"
      title="拨打电话"
      centered
      @ok="handleCallConfirm"
    >
      <p class="call-info">
        即将拨打：<strong>{{ currentLead?.phone }}</strong>
      </p>
      <p v-if="currentLead?.wechat" class="call-wechat">
        微信号：{{ currentLead.wechat }}
        <a-button type="link" size="small" @click="copyWechat">
          <CopyOutlined />
          复制
        </a-button>
      </p>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { Empty } from 'ant-design-vue'
import {
  SearchOutlined,
  UserOutlined,
  PhoneOutlined,
  WechatOutlined,
  ShoppingOutlined,
  ClockCircleOutlined,
  DownOutlined,
  CopyOutlined
} from '@ant-design/icons-vue'
import { mockLeads } from '@/utils/mockData'
import type { Lead, LeadStatus } from '@/types'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const router = useRouter()

// 筛选状态
const activeStatus = ref<LeadStatus | 'all'>('all')
const selectedDeviceTypes = ref<string[]>([])
const searchKeyword = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)

// 拨打电话弹窗
const callModalVisible = ref(false)
const currentLead = ref<Lead | null>(null)

// 状态Tab配置
const statusTabs = computed(() => [
  { key: 'all', label: '全部', count: mockLeads.length },
  { key: 'pending', label: '待跟进', count: mockLeads.filter(l => l.status === 'pending').length },
  { key: 'contacted', label: '已联系', count: mockLeads.filter(l => l.status === 'contacted').length },
  { key: 'closed', label: '已成交', count: mockLeads.filter(l => l.status === 'closed').length },
  { key: 'abandoned', label: '已放弃', count: mockLeads.filter(l => l.status === 'abandoned').length }
])

// 筛选后的线索列表
const filteredLeads = computed(() => {
  let result = [...mockLeads]

  // 状态筛选
  if (activeStatus.value !== 'all') {
    result = result.filter(lead => lead.status === activeStatus.value)
  }

  // 设备类型筛选
  if (selectedDeviceTypes.value.length > 0) {
    result = result.filter(lead => selectedDeviceTypes.value.includes(lead.device_type))
  }

  // 搜索筛选
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(lead =>
      lead.phone.includes(keyword) ||
      lead.wechat?.toLowerCase().includes(keyword) ||
      lead.budget.includes(keyword) ||
      lead.usage.includes(keyword)
    )
  }

  // 按时间倒序
  result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())

  return result
})

// 分页后的线索列表
const paginatedLeads = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredLeads.value.slice(start, end)
})

// 判断是否为新线索（5分钟内）
function isNewLead(time: string): boolean {
  return dayjs().diff(dayjs(time), 'minute') < 5
}

// 获取状态徽标类型
function getStatusBadge(status: LeadStatus): 'success' | 'processing' | 'default' | 'error' | 'warning' {
  const statusMap: Record<LeadStatus, 'success' | 'processing' | 'default' | 'error' | 'warning'> = {
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

// 格式化时间
function formatTime(time: string): string {
  return dayjs(time).fromNow()
}

// 搜索处理
function handleSearch() {
  currentPage.value = 1
}

// 分页处理
function handlePageChange(page: number) {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 状态变更
function handleStatusChange(leadId: string, newStatus: string) {
  message.success(`状态已更新为：${getStatusText(newStatus as LeadStatus)}`)
}

// 拨打电话
function handleCall(lead: Lead) {
  currentLead.value = lead
  callModalVisible.value = true
}

// 确认拨打电话
function handleCallConfirm() {
  callModalVisible.value = false
  message.success(`正在拨打：${currentLead.value?.phone}`)
}

// 复制微信号
function copyWechat() {
  if (currentLead.value?.wechat) {
    navigator.clipboard.writeText(currentLead.value.wechat)
    message.success('微信号已复制')
  }
}
</script>

<style scoped>
.lead-list-container {
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

/* ========== 筛选栏 ========== */
.filter-bar {
  padding: 20px;
}

.status-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.status-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.status-tab:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.status-tab.active {
  background: var(--primary-color);
  color: #ffffff;
  border-color: var(--primary-color);
}

.tab-count {
  font-size: 12px;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.filter-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.device-filter {
  display: flex;
  gap: 16px;
}

/* ========== 线索卡片 ========== */
.leads-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.lead-card {
  display: flex;
  padding: 0;
  cursor: pointer;
  transition: all var(--transition-base);
  overflow: hidden;
}

.lead-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateX(4px);
}

.lead-status-bar {
  width: 4px;
  border-radius: var(--radius-md) 0 0 var(--radius-md);
}

.lead-card.status-pending .lead-status-bar {
  background: var(--warning-color);
}

.lead-card.status-contacted .lead-status-bar {
  background: var(--primary-color);
}

.lead-card.status-closed .lead-status-bar {
  background: var(--success-color);
}

.lead-card.status-abandoned {
  opacity: 0.6;
}

.lead-card.status-abandoned .lead-status-bar {
  background: var(--text-tertiary);
}

.lead-card.new {
  border: 1px solid var(--danger-color);
}

.lead-main {
  flex: 1;
  padding: 20px;
}

/* 头部行 */
.lead-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.lead-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.lead-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.lead-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.new-tag {
  font-size: 11px;
  padding: 2px 6px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.lead-contact {
  display: flex;
  gap: 16px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--text-secondary);
}

.status-dropdown-btn {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 需求摘要 */
.lead-needs {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
}

.need-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.need-label {
  color: var(--text-secondary);
  font-weight: 500;
}

.need-value {
  color: var(--text-primary);
  font-weight: 500;
}

.need-extra {
  color: var(--text-tertiary);
}

/* 选中方案 */
.lead-sku {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: var(--primary-lighter);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
}

.sku-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.sku-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--primary-color);
}

.sku-price {
  margin-left: auto;
  font-size: 16px;
  font-weight: 700;
  color: var(--danger-color);
}

/* 底部 */
.lead-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.lead-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.lead-actions {
  display: flex;
  gap: 8px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px;
}

/* 拨打电话弹窗 */
.call-info {
  font-size: 16px;
  margin-bottom: 8px;
}

.call-wechat {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 响应式 */
@media (max-width: 768px) {
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-controls :deep(.ant-input-search) {
    width: 100% !important;
  }

  .device-filter {
    flex-wrap: wrap;
  }

  .lead-header-row {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .lead-contact {
    flex-direction: column;
    gap: 4px;
  }

  .lead-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .lead-actions {
    justify-content: stretch;
  }

  .lead-actions :deep(.ant-btn) {
    flex: 1;
  }
}
</style>
