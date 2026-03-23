<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="login-bg">
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-card card">
      <!-- Logo和标题 -->
      <div class="login-header">
        <div class="logo-wrapper">
          <div class="logo-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="4" y="8" width="40" height="32" rx="4" fill="currentColor" fill-opacity="0.2"/>
              <rect x="8" y="12" width="28" height="20" rx="2" fill="currentColor"/>
              <path d="M36 16L44 24V36H36V16Z" fill="currentColor" fill-opacity="0.6"/>
              <circle cx="18" cy="22" r="3" fill="#ffffff"/>
              <path d="M8 32C8 28 13 26 18 26C23 26 28 28 28 32" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1 class="logo-title font-display">小遥配配</h1>
          <p class="logo-subtitle">AI智能导购系统</p>
        </div>
      </div>

      <!-- Tab切换 -->
      <a-tabs
        v-model:activeKey="activeTab"
        centered
        size="large"
        class="login-tabs"
      >
        <a-tab-pane key="login" tab="登录" />
        <a-tab-pane key="register" tab="注册" />
      </a-tabs>

      <!-- 登录表单 -->
      <a-form
        v-if="activeTab === 'login'"
        :model="loginForm"
        :rules="loginRules"
        @finish="handleLogin"
        class="login-form"
        layout="vertical"
      >
        <a-form-item name="username">
          <a-input
            v-model:value="loginForm.username"
            size="large"
            placeholder="用户名"
            :prefix="h(UserOutlined)"
            allow-clear
          />
        </a-form-item>

        <a-form-item name="password">
          <a-input-password
            v-model:value="loginForm.password"
            size="large"
            placeholder="密码"
            :prefix="h(LockOutlined)"
          />
        </a-form-item>

        <div class="form-options">
          <a-checkbox v-model:checked="loginForm.remember">记住密码</a-checkbox>
          <a class="forgot-link">忘记密码？</a>
        </div>

        <a-button
          type="primary"
          html-type="submit"
          size="large"
          :loading="userStore.isLoading"
          block
          class="submit-btn"
        >
          登录
        </a-button>

        <div class="form-footer">
          还没有账号？<a @click="activeTab = 'register'">立即注册</a>
        </div>
      </a-form>

      <!-- 注册表单 -->
      <a-form
        v-else
        :model="registerForm"
        :rules="registerRules"
        @finish="handleRegister"
        class="login-form"
        layout="vertical"
      >
        <a-form-item name="username">
          <a-input
            v-model:value="registerForm.username"
            size="large"
            placeholder="用户名（4-20个字符）"
            :prefix="h(UserOutlined)"
            allow-clear
          />
        </a-form-item>

        <a-form-item name="password">
          <a-input-password
            v-model:value="registerForm.password"
            size="large"
            placeholder="密码（6-20个字符）"
            :prefix="h(LockOutlined)"
            @input="checkPasswordStrength"
          />
          <!-- 密码强度指示 -->
          <div v-if="registerForm.password" class="password-strength">
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

        <a-form-item name="confirmPassword">
          <a-input-password
            v-model:value="registerForm.confirmPassword"
            size="large"
            placeholder="确认密码"
            :prefix="h(LockOutlined)"
          />
        </a-form-item>

        <a-form-item name="shopName">
          <a-input
            v-model:value="registerForm.shopName"
            size="large"
            placeholder="店铺名称"
            :prefix="h(ShopOutlined)"
            allow-clear
          />
        </a-form-item>

        <a-form-item name="phone">
          <a-input
            v-model:value="registerForm.phone"
            size="large"
            placeholder="联系电话"
            :prefix="h(PhoneOutlined)"
            allow-clear
          />
        </a-form-item>

        <a-form-item>
          <a-checkbox v-model:checked="registerForm.agree">
            我已阅读并同意
            <a>《用户协议》</a>
          </a-checkbox>
        </a-form-item>

        <a-button
          type="primary"
          html-type="submit"
          size="large"
          :loading="userStore.isLoading"
          block
          class="submit-btn"
        >
          注册
        </a-button>

        <div class="form-footer">
          已有账号？<a @click="activeTab = 'login'">立即登录</a>
        </div>
      </a-form>
    </div>

    <!-- 底部信息 -->
    <div class="login-footer">
      <p>小遥配配 - 让电脑选购更智能</p>
      <p>© 2025 XiaoyaoPeipei. All rights reserved.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, h } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { UserOutlined, LockOutlined, ShopOutlined, PhoneOutlined } from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 当前Tab
const activeTab = ref('login')

// 登录表单
const loginForm = reactive({
  username: 'test',
  password: '123456',
  remember: true
})

// 注册表单
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  shopName: '',
  phone: '',
  agree: false
})

// 密码强度
const passwordStrength = ref(0)

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名' }
  ],
  password: [
    { required: true, message: '请输入密码' }
  ]
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名' },
    { min: 4, max: 20, message: '用户名长度为4-20个字符' }
  ],
  password: [
    { required: true, message: '请输入密码' },
    { min: 6, max: 20, message: '密码长度为6-20个字符' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码' },
    {
      validator: (_rule: any, value: string) => {
        if (value !== registerForm.password) {
          return Promise.reject('两次输入的密码不一致')
        }
        return Promise.resolve()
      }
    }
  ],
  shopName: [
    { required: true, message: '请输入店铺名称' }
  ],
  phone: [
    { required: true, message: '请输入联系电话' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' }
  ],
  agree: [
    {
      validator: (_rule: any, value: boolean) => {
        if (!value) {
          return Promise.reject('请阅读并同意用户协议')
        }
        return Promise.resolve()
      }
    }
  ]
}

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

function checkPasswordStrength() {
  const password = registerForm.password
  let strength = 0

  if (password.length >= 8) strength++
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
  if (/\d/.test(password)) strength++
  if (/[!@#$%^&*]/.test(password)) strength++

  passwordStrength.value = Math.min(strength, 3)
}

// 处理登录
async function handleLogin() {
  const result = await userStore.login({
    username: loginForm.username,
    password: loginForm.password
  })

  if (result.success) {
    message.success('登录成功！')
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/dashboard')
  } else {
    message.error(result.message || '登录失败')
  }
}

// 处理注册
async function handleRegister() {
  const result = await userStore.register({
    username: registerForm.username,
    password: registerForm.password,
    shop_name: registerForm.shopName,
    phone: registerForm.phone
  })

  if (result.success) {
    message.success('注册成功！')
    router.push('/dashboard')
  } else {
    message.error(result.message || '注册失败')
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 20px;
}

/* 背景装饰 */
.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: -1;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  opacity: 0.08;
  filter: blur(60px);
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  right: -100px;
}

.circle-2 {
  width: 300px;
  height: 300px;
  bottom: -50px;
  left: -50px;
  background: linear-gradient(135deg, var(--success-color), #10b981);
}

.circle-3 {
  width: 200px;
  height: 200px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, var(--warning-color), #f59e0b);
  opacity: 0.05;
}

/* 登录卡片 */
.login-card {
  width: 100%;
  max-width: 440px;
  padding: 48px 40px;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 头部 */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  border-radius: var(--radius-lg);
  color: white;
  margin-bottom: 16px;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
}

.logo-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.logo-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
}

/* Tab样式 */
.login-tabs :deep(.ant-tabs-nav) {
  margin-bottom: 32px;
}

.login-tabs :deep(.ant-tabs-tab) {
  font-size: 16px;
  font-weight: 500;
  padding: 12px 24px;
}

.login-tabs :deep(.ant-tabs-tab-active .ant-tabs-tab-btn) {
  color: var(--primary-color);
  font-weight: 600;
}

.login-tabs :deep(.ant-tabs-ink-bar) {
  background: var(--primary-color);
  height: 3px;
  border-radius: 2px;
}

/* 表单样式 */
.login-form :deep(.ant-form-item) {
  margin-bottom: 20px;
}

.login-form :deep(.ant-input),
.login-form :deep(.ant-input-password) {
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  padding: 10px 16px;
}

.login-form :deep(.ant-input:focus),
.login-form :deep(.ant-input-password .ant-input:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.login-form :deep(.ant-input-prefix) {
  color: var(--text-tertiary);
  margin-right: 8px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.forgot-link {
  color: var(--primary-color);
  font-size: 14px;
}

.submit-btn {
  height: 48px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 16px;
}

.form-footer {
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
}

.form-footer a {
  color: var(--primary-color);
  font-weight: 500;
  cursor: pointer;
}

/* 密码强度 */
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

/* 底部信息 */
.login-footer {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 12px;
}

.login-footer p {
  margin: 4px 0;
}
</style>
