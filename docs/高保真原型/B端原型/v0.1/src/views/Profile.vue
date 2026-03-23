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
                <span class="detail-value membership-value">{{ formatDate(userStore.user?.membership_expires_at) }}</span>
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
                <div class="usage-value">23</div>
                <div class="usage-label">配置数量</div>
              </div>
            </div>
            <div class="usage-item">
              <div class="usage-icon lead-icon">
                <TeamOutlined />
              </div>
              <div class="usage-info">
                <div class="usage-value">156</div>
                <div class="usage-label">客户线索</div>
              </div>
            </div>
            <div class="usage-item">
              <div class="usage-icon order-icon">
                <CheckCircleOutlined />
              </div>
              <div class="usage-info">
                <div class="usage-value">45</div>
                <div class="usage-label">成交订单</div>
              </div>
            </div>
            <div class="usage-item">
              <div class="usage-icon day-icon">
                <CalendarOutlined />
              </div>
              <div class="usage-info">
                <div class="usage-value">22</div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
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
  CalendarOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'

const router = useRouter()
const userStore = useUserStore()
const passwordFormRef = ref<FormInstance>()

// 退出确认
const logoutVisible = ref(false)

// 保存状态
const savingShop = ref(false)
const changingPassword = ref(false)

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
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    message.success('店铺信息保存成功！')
  } finally {
    savingShop.value = false
  }
}

// 修改密码
async function handleChangePassword() {
  try {
    await passwordFormRef.value?.validate()
    changingPassword.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

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
    console.error('表单验证失败', error)
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
  padding: 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.detail-label {
  font-size: 14px;
  color: var(--text-tertiary);
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
