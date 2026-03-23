<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div>
        <h1 class="page-title font-display">数据概览</h1>
        <p class="page-subtitle">今日 {{ currentDate }}</p>
      </div>
      <a-button type="primary" @click="refreshData">
        <template #icon><ReloadOutlined :spin="isRefreshing" /></template>
        刷新数据
      </a-button>
    </div>

    <!-- 数据统计卡片 -->
    <div class="stats-grid">
      <div
        v-for="(stat, index) in stats"
        :key="stat.key"
        class="data-card"
        :class="stat.colorClass"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="stat-header">
          <span class="stat-label">{{ stat.label }}</span>
          <component :is="stat.icon" class="stat-icon" />
        </div>
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-trend" :class="stat.trend > 0 ? 'up' : stat.trend < 0 ? 'down' : 'flat'">
          <CaretUpOutlined v-if="stat.trend > 0" />
          <CaretDownOutlined v-else-if="stat.trend < 0" />
          <MinusOutlined v-else />
          <span>{{ Math.abs(stat.trend) }}%</span>
          <span class="trend-text">较昨日</span>
        </div>
      </div>
    </div>

    <!-- 快捷入口 -->
    <div class="card quick-access-card">
      <h2 class="card-title font-display">快捷入口</h2>
      <div class="quick-access-grid">
        <router-link
          v-for="item in quickAccessItems"
          :key="item.key"
          :to="{ name: item.route }"
          class="quick-access-item"
        >
          <div class="quick-icon" :style="{ background: item.color }">
            <component :is="item.icon" />
          </div>
          <span class="quick-label">{{ item.label }}</span>
        </router-link>
      </div>
    </div>

    <!-- 双列布局 -->
    <div class="dashboard-grid">
      <!-- 最新线索 -->
      <div class="card leads-section">
        <div class="card-header">
          <h2 class="card-title font-display">最新线索（待跟进）</h2>
          <router-link to="/leads" class="view-all-link">
            查看全部 <ArrowRightOutlined />
          </router-link>
        </div>

        <div v-if="recentLeads.length > 0" class="leads-list">
          <div
            v-for="lead in recentLeads"
            :key="lead.id"
            class="lead-item"
            @click="router.push(`/leads/${lead.id}`)"
          >
            <div class="lead-avatar">
              <UserOutlined />
            </div>
            <div class="lead-content">
              <div class="lead-name">客户{{ lead.id.slice(-4) }}</div>
              <div class="lead-needs">
                <span class="need-tag">预算：{{ lead.budget }}</span>
                <span class="need-tag">{{ lead.device_type }} | {{ lead.usage }}</span>
              </div>
              <div class="lead-sku">选择：{{ lead.selected_sku?.name }}</div>
            </div>
            <div class="lead-actions">
              <span class="lead-time">{{ formatTime(lead.created_at) }}</span>
              <a-button type="primary" size="small">查看详情</a-button>
            </div>
          </div>
        </div>

        <a-empty v-else description="暂无新线索" :image="Empty.PRESENTED_IMAGE_SIMPLE" />
      </div>

      <!-- 热门配置 -->
      <div class="card hot-skus-section">
        <div class="card-header">
          <h2 class="card-title font-display">热门配置（本周）</h2>
          <router-link to="/sku" class="view-all-link">
            查看全部 <ArrowRightOutlined />
          </router-link>
        </div>

        <div v-if="hotSKUs.length > 0" class="hot-skus-list">
          <div
            v-for="(sku, index) in hotSKUs"
            :key="sku.id"
            class="hot-sku-item"
            @click="router.push(`/sku/edit/${sku.id}`)"
          >
            <div class="sku-rank" :class="`rank-${index + 1}`">{{ index + 1 }}</div>
            <img :src="sku.image" :alt="sku.name" class="sku-image" />
            <div class="sku-info">
              <div class="sku-name text-ellipsis">{{ sku.name }}</div>
              <div class="sku-stats">被选 {{ sku.select_count }} 次</div>
            </div>
            <div class="sku-device">
              <a-tag :color="getDeviceColor(sku.device_type)">{{ sku.device_type }}</a-tag>
            </div>
          </div>
        </div>

        <a-empty v-else description="暂无数据" :image="Empty.PRESENTED_IMAGE_SIMPLE" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { Empty, message } from 'ant-design-vue'
import {
  ReloadOutlined,
  ArrowRightOutlined,
  UserOutlined,
  TeamOutlined,
  BarChartOutlined,
  QrcodeOutlined,
  CaretUpOutlined,
  CaretDownOutlined,
  MinusOutlined,
  PlusOutlined
} from '@ant-design/icons-vue'
import * as dashboardApi from '@/api/dashboard'
import * as leadApi from '@/api/lead'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const router = useRouter()

// 是否正在刷新
const isRefreshing = ref(false)

// 从API获取的数据
const dashboardData = ref<any>(null)
const hotSKUsData = ref<any[]>([])
const recentLeadsData = ref<any[]>([])

// 当前日期
const currentDate = computed(() => {
  return dayjs().format('YYYY年MM月DD日')
})

// 统计数据
const stats = computed(() => {
  const todayStats = dashboardData.value?.today_stats || {}
  return [
    {
      key: 'consult',
      label: '咨询数',
      value: todayStats.consult_count ?? 0,
      trend: todayStats.consult_trend ?? 0,
      colorClass: '',
      icon: TeamOutlined
    },
    {
      key: 'leads',
      label: '线索数',
      value: todayStats.lead_count ?? 0,
      trend: todayStats.lead_trend ?? 0,
      colorClass: 'success',
      icon: UserOutlined
    },
    {
      key: 'conversion',
      label: '转化率',
      value: ((todayStats.conversion_rate ?? 0) * 100).toFixed(1) + '%',
      trend: todayStats.conversion_trend ?? 0,
      colorClass: 'warning',
      icon: BarChartOutlined
    }
  ]
})

// 快捷入口
const quickAccessItems = [
  { key: 'add', label: '添加配置', route: 'SKUAdd', icon: PlusOutlined, color: 'linear-gradient(135deg, #3b82f6, #2563eb)' },
  { key: 'leads', label: '查看线索', route: 'LeadList', icon: TeamOutlined, color: 'linear-gradient(135deg, #10b981, #059669)' },
  { key: 'share', label: '分享管理', route: 'Share', icon: QrcodeOutlined, color: 'linear-gradient(135deg, #8b5cf6, #7c3aed)' }
]

// 最新线索（取待跟进的前3条）
const recentLeads = computed(() => {
  return recentLeadsData.value
    .filter(l => l.status === 'pending')
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 3)
})

// 热门配置
const hotSKUs = computed(() => {
  // 确保数据是数组
  if (!Array.isArray(hotSKUsData.value)) {
    console.warn('hotSKUsData.value 不是数组:', hotSKUsData.value)
    return []
  }

  const unsplashImages = [
    'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=120&h=120&fit=crop',
    'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=120&h=120&fit=crop',
    'https://images.unsplash.com/photo-1593062096033-9a26b09da705?w=120&h=120&fit=crop'
  ]
  return hotSKUsData.value.map((sku, index) => ({
    ...sku,
    image: sku.images?.[0] || unsplashImages[index] || unsplashImages[0]
  }))
})

// 格式化时间
function formatTime(time: string) {
  return dayjs(time).fromNow()
}

// 获取设备类型颜色
function getDeviceColor(type: string) {
  const colors: Record<string, string> = {
    '笔记本': 'blue',
    '台式机': 'green',
    '一体机': 'orange'
  }
  return colors[type] || 'default'
}

// 刷新数据
async function refreshData() {
  isRefreshing.value = true
  try {
    await fetchData()
    message.success('数据已更新')
  } catch (error) {
    console.error('刷新数据失败:', error)
  } finally {
    isRefreshing.value = false
  }
}

// 获取数据
async function fetchData() {
  try {
    // 获取首页看板数据
    const dashboardRes = await dashboardApi.getDashboardData()
    dashboardData.value = dashboardRes.data.data

    // 获取热门配置
    const hotSkuRes = await dashboardApi.getTopSKUs(10)
    hotSKUsData.value = hotSkuRes.data.data.top_skus || []

    // 获取最新线索（待跟进）
    const leadRes = await leadApi.getLeadList({ status: 'pending', page: 1, limit: 10 })
    recentLeadsData.value = leadRes.data.data.items
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

onMounted(() => {
  fetchData()
})

// 页面激活时刷新数据（解决路由切换后空白问题）
onActivated(() => {
  fetchData()
})
</script>

<style scoped>
.dashboard-container {
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

/* ========== 统计卡片 ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.data-card {
  background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-hover) 100%);
  border-radius: var(--radius-lg);
  padding: 24px;
  position: relative;
  overflow: hidden;
  border: 1px solid var(--border-color);
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.data-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-hover));
}

.data-card.success::before {
  background: linear-gradient(90deg, var(--success-color), #10b981);
}

.data-card.warning::before {
  background: linear-gradient(90deg, var(--warning-color), #f59e0b);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-icon {
  font-size: 24px;
  color: var(--primary-color);
  opacity: 0.5;
}

.stat-value {
  font-size: 40px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
  font-family: var(--font-body);
}

.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.stat-trend.up {
  color: var(--success-color);
  background: var(--success-lighter);
}

.stat-trend.down {
  color: var(--danger-color);
  background: var(--danger-lighter);
}

.stat-trend.flat {
  color: var(--text-secondary);
  background: var(--bg-gray);
}

.trend-text {
  font-weight: 400;
  opacity: 0.8;
  margin-left: 2px;
}

/* ========== 快捷入口 ========== */
.quick-access-card {
  padding: 24px;
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.quick-access-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border-radius: var(--radius-lg);
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all var(--transition-base);
  text-decoration: none;
}

.quick-access-item:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.quick-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 24px;
}

.quick-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

/* ========== 双列布局 ========== */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

/* ========== 线索列表 ========== */
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
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--primary-color);
  font-size: 14px;
  text-decoration: none;
}

.view-all-link:hover {
  color: var(--primary-hover);
}

.leads-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.lead-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: var(--radius-md);
  background: var(--bg-hover);
  border: 1px solid var(--border-color-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.lead-item:hover {
  background: var(--primary-lighter);
  border-color: var(--primary-color);
}

.lead-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.lead-content {
  flex: 1;
  min-width: 0;
}

.lead-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.lead-needs {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 6px;
}

.need-tag {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 2px 8px;
  background: var(--bg-active);
  border-radius: 4px;
}

.lead-sku {
  font-size: 13px;
  color: var(--primary-color);
}

.lead-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.lead-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* ========== 热门配置 ========== */
.hot-skus-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hot-sku-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: var(--radius-md);
  background: var(--bg-hover);
  border: 1px solid var(--border-color-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.hot-sku-item:hover {
  background: var(--bg-active);
  border-color: var(--primary-color);
}

.sku-rank {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.rank-1 {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #ffffff;
}

.rank-2 {
  background: linear-gradient(135deg, #94a3b8, #64748b);
  color: #ffffff;
}

.rank-3 {
  background: linear-gradient(135deg, #cd7f32, #b87333);
  color: #ffffff;
}

.sku-image {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  object-fit: cover;
  flex-shrink: 0;
}

.sku-info {
  flex: 1;
  min-width: 0;
}

.sku-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.sku-stats {
  font-size: 12px;
  color: var(--text-tertiary);
}

.sku-device {
  flex-shrink: 0;
}

/* ========== 响应式 ========== */
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .dashboard-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .quick-access-grid {
    grid-template-columns: 1fr;
  }
}
</style>
