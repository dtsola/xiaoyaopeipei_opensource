<template>
  <div class="profile-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div>
        <h1 class="page-title font-display">个人中心</h1>
        <p class="page-subtitle">管理您的账号信息和店铺设置</p>
      </div>
      <a-button danger @click="logoutVisible = true">
        <template #icon><LogoutOutlined /></template>
        退出登录
      </a-button>
    </div>

    <div class="profile-grid">
      <!-- 左列：店铺信息 -->
      <div class="profile-left">
        <!-- 账号信息 -->
        <div class="card account-card">
          <h2 class="card-title font-display">账号信息</h2>
          <div class="account-content">
            <div class="account-avatar-wrapper">
              <div class="account-avatar">
                {{ userStore.userName?.charAt(0)?.toUpperCase() || 'U' }}
              </div>
              <div class="account-badge">商家</div>
            </div>
            <div class="account-details">
              <div class="detail-item">
                <span class="detail-label">用户名</span>
                <span class="detail-value">{{ userStore.userName }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">注册时间</span>
                <span class="detail-value">{{ formatDate(userStore.user?.created_at) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">会员到期时间</span>
                <span class="detail-value membership-value">{{ formatDate(userStore.user?.membership_expiry) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">客服微信</span>
                <div class="detail-value-actions">
                  <span class="detail-value wechat-value">dtsola</span>
                  <a-button type="link" size="small" @click="qrcodeVisible = true">
                    <template #icon><CustomerServiceOutlined /></template>
                    充值/续期 联系客服
                  </a-button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 店铺信息 -->
        <div class="card shop-card">
          <h2 class="card-title font-display">店铺信息</h2>
          <a-form
            :model="shopForm"
            layout="vertical"
            class="shop-form"
          >
            <a-form-item label="店铺名称">
              <a-input
                v-model:value="shopForm.shopName"
                size="large"
                placeholder="请输入店铺名称"
                allow-clear
              />
            </a-form-item>

            <a-form-item label="联系电话">
              <a-input
                v-model:value="shopForm.phone"
                size="large"
                placeholder="请输入联系电话"
                allow-clear
              />
            </a-form-item>

            <a-form-item label="店铺地址">
              <a-input
                v-model:value="shopForm.address"
                size="large"
                placeholder="请输入店铺地址"
                allow-clear
              />
            </a-form-item>

            <a-form-item label="营业时间">
              <a-input
                v-model:value="shopForm.businessHours"
                size="large"
                placeholder="如：9:00 - 21:00"
                allow-clear
              />
            </a-form-item>

            <a-form-item>
              <a-button
                type="primary"
                :loading="savingShop"
                @click="handleSaveShop"
                block
                size="large"
              >
                <template #icon><SaveOutlined /></template>
                保存修改
              </a-button>
            </a-form-item>
          </a-form>
        </div>
      </div>

      <!-- 右列：密码修改和使用统计 -->
      <div class="profile-right">
        <!-- 修改密码 -->
        <div class="card password-card">
          <h2 class="card-title font-display">修改密码</h2>
          <a-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            layout="vertical"
            class="password-form"
          >
            <a-form-item name="oldPassword" label="旧密码">
              <a-input-password
                v-model:value="passwordForm.oldPassword"
                size="large"
                placeholder="请输入旧密码"
                @input="checkNewPasswordStrength"
              />
            </a-form-item>

            <a-form-item name="newPassword" label="新密码">
              <a-input-password
                v-model:value="passwordForm.newPassword"
                size="large"
                placeholder="请输入新密码（6-20个字符）"
                @input="checkNewPasswordStrength"
              />
              <!-- 密码强度指示 -->
              <div v-if="passwordForm.newPassword" class="password-strength">
                <div class="strength-bar">
                  <div
                    class="strength-fill"
                    :class="strengthClass"
                    :style="{ width: strengthWidth }"
                  ></div>
                </div>
                <span class="strength-text" :class="strengthClass">{{ strengthText }}</span>
              </div>
            </a-form-item>

            <a-form-item name="confirmPassword" label="确认新密码">
              <a-input-password
                v-model:value="passwordForm.confirmPassword"
                size="large"
                placeholder="请再次输入新密码"
              />
            </a-form-item>

            <a-form-item>
              <a-button
                type="primary"
                :loading="changingPassword"
                @click="handleChangePassword"
                block
                size="large"
              >
                <template #icon><LockOutlined /></template>
                修改密码
              </a-button>
            </a-form-item>
          </a-form>
        </div>

        <!-- 使用统计 -->
        <div class="card stats-card">
          <h2 class="card-title font-display">使用统计</h2>
          <div class="usage-stats">
            <div class="usage-item">
              <div class="usage-icon config-icon">
                <ShoppingOutlined />
              </div>
              <div class="usage-info">
                <div class="usage-value">{{ summaryData.sku_count }}</div>
                <div class="usage-label">配置数量</div>
              </div>
            </div>
            <div class="usage-item">
              <div class="usage-icon lead-icon">
                <TeamOutlined />
              </div>
              <div class="usage-info">
                <div class="usage-value">{{ summaryData.lead_count }}</div>
                <div class="usage-label">客户线索</div>
              </div>
            </div>
            <div class="usage-item">
              <div class="usage-icon order-icon">
                <CheckCircleOutlined />
              </div>
              <div class="usage-info">
                <div class="usage-value">{{ summaryData.closed_count }}</div>
                <div class="usage-label">成交订单</div>
              </div>
            </div>
            <div class="usage-item">
              <div class="usage-icon day-icon">
                <CalendarOutlined />
              </div>
              <div class="usage-info">
                <div class="usage-value">{{ summaryData.days_since_registration }}</div>
                <div class="usage-label">使用天数</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 退出确认弹窗 -->
    <a-modal
      v-model:open="logoutVisible"
      title="确认退出"
      content="确定要退出登录吗？"
      centered
      @ok="handleLogout"
    >
      <template #footer>
        <a-button @click="logoutVisible = false">取消</a-button>
        <a-button type="primary" danger @click="handleLogout">确定退出</a-button>
      </template>
    </a-modal>

    <!-- 会员续期弹窗 -->
    <a-modal
      v-model:open="renewVisible"
      title="会员续期"
      :width="400"
      centered
      @ok="handleRenewMembership"
      :confirm-loading="renewing"
    >
      <div class="renew-content">
        <p class="renew-tip">当前会员到期时间：{{ formatDate(userStore.user?.membership_expiry) }}</p>
        <a-form-item label="续期天数" :style="{ marginBottom: 0 }">
          <a-input-number
            v-model:value="renewDays"
            :min="1"
            :max="365"
            style="width: 100%"
            size="large"
          />
        </a-form-item>
      </div>
    </a-modal>

    <!-- 会员到期提醒弹窗 -->
    <a-modal
      v-model:open="expiryWarningVisible"
      :title="isExpired ? '会员已过期' : '会员即将到期'"
      :width="400"
      centered
      @ok="expiryWarningVisible = false"
      :closable="!isExpired"
      :maskClosable="!isExpired"
    >
      <template #icon>
        <WarningOutlined :style="`color: ${isExpired ? '#ff4d4f' : '#faad14'}; font-size: 22px;`" />
      </template>
      <div class="warning-content">
        <p v-if="isExpired">您的会员已过期，请添加客服微信进行续费。</p>
        <p v-else>您的会员即将到期，为避免影响使用，请及时续期。</p>
        <p v-if="isExpired">到期时间：{{ formatDate(userStore.user?.membership_expiry) }}</p>
        <p v-else>到期时间：{{ formatDate(userStore.user?.membership_expiry) }}</p>
        <p v-if="isExpired" class="contact-wechat">客服微信：dtsola</p>
      </div>
      <template #footer>
        <a-button v-if="!isExpired" @click="expiryWarningVisible = false">稍后提醒</a-button>
        <a-button v-if="isExpired" type="primary" @click="handleCopyWeChat">
          <template #icon><CopyOutlined /></template>
          复制微信号
        </a-button>
        <a-button v-if="!isExpired" type="primary" @click="handleImmediateRenew">
          <template #icon><CrownOutlined /></template>
          立即续期
        </a-button>
        <a-button v-if="isExpired" @click="expiryWarningVisible = false">关闭</a-button>
      </template>
    </a-modal>

    <!-- 客服微信二维码弹窗 -->
    <a-modal
      v-model:open="qrcodeVisible"
      title="扫码联系客服续费"
      :width="360"
      :footer="null"
      centered
    >
      <div class="qrcode-content">
        <p class="qrcode-tip">请使用微信扫描下方二维码，联系客服进行续费</p>
        <div class="qrcode-image-wrapper">
          <img
            src="https://file.xiaoyaosai.com/peipei/kefu/dtsola.png"
            alt="客服微信二维码"
            class="qrcode-image"
          />
        </div>
        <p class="qrcode-wechat">客服微信号：dtsola</p>
        <a-button type="primary" block @click="handleCopyWeChat">
          <template #icon><CopyOutlined /></template>
          复制微信号
        </a-button>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import type { FormInstance } from 'ant-design-vue'
import {
  LogoutOutlined,
  SaveOutlined,
  LockOutlined,
  ShoppingOutlined,
  TeamOutlined,
  CheckCircleOutlined,
  CalendarOutlined,
  WarningOutlined,
  CrownOutlined,
  CopyOutlined,
  CustomerServiceOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/user'
import * as authApi from '@/api/auth'
import * as dashboardApi from '@/api/dashboard'
import dayjs from 'dayjs'

const router = useRouter()
const userStore = useUserStore()
const passwordFormRef = ref<FormInstance>()

// 弹窗状态
const logoutVisible = ref(false)
const renewVisible = ref(false)
const expiryWarningVisible = ref(false)
const qrcodeVisible = ref(false)

// 保存状态
const savingShop = ref(false)
const changingPassword = ref(false)
const renewing = ref(false)

// 续期天数
const renewDays = ref(7)

// 使用统计数据
const summaryData = reactive({
  sku_count: 0,
  lead_count: 0,
  closed_count: 0,
  days_since_registration: 0
})
const summaryLoading = ref(false)

// 店铺表单
const shopForm = reactive({
  shopName: userStore.user?.shop_name || '',
  phone: userStore.user?.phone || '',
  address: userStore.user?.address || '',
  businessHours: userStore.user?.business_hours || ''
})

// 密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 密码强度
const passwordStrength = ref(0)

// 密码强度计算
const strengthWidth = computed(() => {
  return (passwordStrength.value / 3) * 100 + '%'
})

const strengthClass = computed(() => {
  if (passwordStrength.value <= 1) return 'weak'
  if (passwordStrength.value === 2) return 'medium'
  return 'strong'
})

const strengthText = computed(() => {
  if (passwordStrength.value <= 1) return '弱'
  if (passwordStrength.value === 2) return '中'
  return '强'
})

// 会员是否已过期
const isExpired = computed(() => {
  return userStore.user?.is_membership_expired || false
})

// 密码验证规则
const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入旧密码' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码' },
    { min: 6, max: 20, message: '密码长度为6-20个字符' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码' },
    {
      validator: (_rule: any, value: string) => {
        if (value !== passwordForm.newPassword) {
          return Promise.reject('两次输入的密码不一致')
        }
        return Promise.resolve()
      }
    }
  ]
}

// 格式化日期
function formatDate(dateStr?: string): string {
  if (!dateStr) return '-'
  return dayjs(dateStr).format('YYYY-MM-DD')
}

// 检查密码强度
function checkNewPasswordStrength() {
  const password = passwordForm.newPassword
  let strength = 0

  if (password.length >= 8) strength++
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
  if (/\d/.test(password)) strength++
  if (/[!@#$%^&*]/.test(password)) strength++

  passwordStrength.value = Math.min(strength, 3)
}

// 保存店铺信息
async function handleSaveShop() {
  savingShop.value = true
  try {
    await authApi.updateCurrentUser({
      shop_name: shopForm.shopName,
      phone: shopForm.phone,
      address: shopForm.address,
      business_hours: shopForm.businessHours
    })
    // 更新store中的用户信息
    await userStore.fetchUserInfo()
    message.success('店铺信息保存成功！')
  } catch (error) {
    console.error('保存失败', error)
  } finally {
    savingShop.value = false
  }
}

// 修改密码
async function handleChangePassword() {
  try {
    await passwordFormRef.value?.validate()
    changingPassword.value = true

    await authApi.updatePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })

    message.success('密码修改成功！请重新登录')
    // 清空表单
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    passwordStrength.value = 0

    // 延迟后退出登录
    setTimeout(() => {
      handleLogout()
    }, 1500)
  } catch (error) {
    console.error('修改密码失败', error)
  } finally {
    changingPassword.value = false
  }
}

// 退出登录
function handleLogout() {
  userStore.logout()
  logoutVisible.value = false
  router.push('/login')
}

// 会员续期
async function handleRenewMembership() {
  renewing.value = true
  try {
    const res = await authApi.renewMembership({ days: renewDays.value })
    // 更新用户信息
    await userStore.fetchUserInfo()
    renewVisible.value = false
    renewDays.value = 7
    message.success(`续期成功，新的到期时间：${formatDate(res.data.data.membership_expiry)}`)
  } catch (error) {
    console.error('续期失败', error)
    message.error('续期失败，请重试')
  } finally {
    renewing.value = false
  }
}

// 立即续期（从警告弹窗）- 显示客服二维码
function handleImmediateRenew() {
  expiryWarningVisible.value = false
  qrcodeVisible.value = true
}

// 复制微信号
function handleCopyWeChat() {
  navigator.clipboard.writeText('dtsola').then(() => {
    message.success('微信号已复制到剪贴板')
  }).catch(() => {
    message.error('复制失败，请手动复制：dtsola')
  })
}

// 检查是否需要显示到期提醒
function checkExpiryWarning() {
  if (userStore.user?.show_expiry_warning) {
    expiryWarningVisible.value = true
  }
}

// 获取使用统计数据
async function fetchSummaryData() {
  summaryLoading.value = true
  try {
    const res = await dashboardApi.getSummary()
    // res.data 是 ApiResponse 类型，需要再取 res.data.data 获取实际数据
    Object.assign(summaryData, res.data.data)
  } catch (error) {
    console.error('获取统计数据失败', error)
  } finally {
    summaryLoading.value = false
  }
}

// 监听用户信息变化，检查是否需要显示提醒
watch(() => userStore.user?.show_expiry_warning, (show) => {
  if (show) {
    checkExpiryWarning()
  }
}, { immediate: true })

// 页面挂载时检查
onMounted(() => {
  checkExpiryWarning()
  fetchSummaryData()
})
</script>

<style scoped>
.profile-container {
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

/* ========== 双列布局 ========== */
.profile-grid {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 20px;
}

.profile-left,
.profile-right {
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

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color-light);
}

/* ========== 账号信息卡片 ========== */
.account-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.account-avatar-wrapper {
  position: relative;
}

.account-avatar {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 600;
}

.account-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background: var(--success-color);
  color: #ffffff;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: var(--radius-full);
  font-weight: 500;
}

.account-details {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.detail-label {
  font-size: 14px;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.membership-value {
  color: var(--primary-color);
  font-weight: 600;
}

.wechat-value {
  color: #2563eb;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.membership-item {
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.detail-value-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 8px;
}

/* 续期弹窗 */
.renew-content {
  padding: 8px 0;
}

.renew-tip {
  margin-bottom: 16px;
  color: var(--text-secondary);
}

/* 到期警告 */
.warning-content p {
  margin-bottom: 8px;
}

.warning-content p:last-child {
  margin-bottom: 0;
  color: var(--primary-color);
  font-weight: 500;
}

.warning-content .contact-wechat {
  color: #2563eb;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

/* 二维码弹窗 */
.qrcode-content {
  text-align: center;
  padding: 16px 0;
}

.qrcode-tip {
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.qrcode-image-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.qrcode-image {
  width: 240px;
  height: 240px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.qrcode-wechat {
  color: var(--primary-color);
  font-weight: 600;
  font-family: 'Courier New', monospace;
  margin-bottom: 16px;
}

/* ========== 表单样式 ========== */
:deep(.ant-form-item) {
  margin-bottom: 20px;
}

:deep(.ant-input),
:deep(.ant-input-password) {
  border-radius: var(--radius-md);
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: var(--text-secondary);
}

/* ========== 密码强度 ========== */
.password-strength {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: var(--border-color-light);
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all var(--transition-base);
}

.strength-fill.weak {
  background: var(--danger-color);
}

.strength-fill.medium {
  background: var(--warning-color);
}

.strength-fill.strong {
  background: var(--success-color);
}

.strength-text {
  font-size: 12px;
  font-weight: 600;
  min-width: 24px;
}

.strength-text.weak {
  color: var(--danger-color);
}

.strength-text.medium {
  color: var(--warning-color);
}

.strength-text.strong {
  color: var(--success-color);
}

/* ========== 使用统计 ========== */
.usage-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.usage-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.usage-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #ffffff;
}

.config-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.lead-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.order-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.day-icon {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.usage-info {
  flex: 1;
}

.usage-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.usage-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }

  .profile-left {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .usage-stats {
    grid-template-columns: 1fr;
  }
}
</style>
