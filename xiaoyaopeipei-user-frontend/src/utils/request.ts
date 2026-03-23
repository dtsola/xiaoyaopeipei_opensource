/**
 * Axios请求封装 - C端
 */

import axios, { AxiosInstance, AxiosError, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { message } from 'ant-design-vue'

/**
 * 统一响应接口
 */
export interface ApiResponse<T = any> {
  /** 响应状态码 */
  code: number
  /** 响应消息 */
  message: string
  /** 响应数据 */
  data: T
  /** 时间戳 */
  timestamp: number
  /** 请求ID */
  request_id: string
}

/**
 * 请求配置接口
 */
export interface RequestConfig extends AxiosRequestConfig {
  /** 是否显示错误提示 */
  showError?: boolean
  /** 是否显示加载提示 */
  showLoading?: boolean
}

/**
 * 会话管理类
 */
class SessionManager {
  private readonly storageKey: string
  private readonly sessionKey = 'session_id'
  private readonly shopKey = 'shop_id'

  constructor() {
    this.storageKey = import.meta.env.VITE_SESSION_KEY
  }

  /** 获取会话ID */
  getSessionId(): string | null {
    const session = sessionStorage.getItem(this.storageKey)
    if (session) {
      try {
        return JSON.parse(session)[this.sessionKey] || null
      } catch {
        return null
      }
    }
    return null
  }

  /** 设置会话ID */
  setSessionId(sessionId: string): void {
    const session = this.getSession() || {}
    session[this.sessionKey] = sessionId
    sessionStorage.setItem(this.storageKey, JSON.stringify(session))
  }

  /** 获取店铺ID */
  getShopId(): string | null {
    const session = sessionStorage.getItem(this.storageKey)
    if (session) {
      try {
        return JSON.parse(session)[this.shopKey] || null
      } catch {
        return null
      }
    }
    return null
  }

  /** 设置店铺ID */
  setShopId(shopId: string): void {
    const session = this.getSession() || {}
    session[this.shopKey] = shopId
    sessionStorage.setItem(this.storageKey, JSON.stringify(session))
  }

  /** 获取完整会话数据 */
  getSession(): Record<string, any> | null {
    const session = sessionStorage.getItem(this.storageKey)
    if (session) {
      try {
        return JSON.parse(session)
      } catch {
        return null
      }
    }
    return null
  }

  /** 设置会话数据 */
  setSession(data: Record<string, any>): void {
    sessionStorage.setItem(this.storageKey, JSON.stringify(data))
  }

  /** 清除会话 */
  clearSession(): void {
    sessionStorage.removeItem(this.storageKey)
  }
}

/** 导出会话管理实例 */
export const sessionManager = new SessionManager()

/**
 * 创建Axios实例
 */
const createAxiosInstance = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: Number(import.meta.env.VITE_REQUEST_TIMEOUT) || 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  return instance
}

/** Axios实例 */
const request = createAxiosInstance()

/**
 * 请求拦截器
 */
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加会话ID
    const sessionId = sessionManager.getSessionId()
    if (sessionId) {
      config.headers['X-Session-ID'] = sessionId
    }

    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now(),
      }
    }

    // 调试模式下打印请求信息
    if (import.meta.env.VITE_DEBUG === 'true') {
      console.log(`[Request] ${config.method?.toUpperCase()} ${config.url}`, {
        params: config.params,
        data: config.data,
        sessionId,
      })
    }

    return config
  },
  (error: AxiosError) => {
    console.error('[Request Error]', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 */
request.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const { data, config } = response

    // 调试模式下打印响应信息
    if (import.meta.env.VITE_DEBUG === 'true') {
      console.log(`[Response] ${config.url}`, data)
    }

    // 业务状态码判断
    if (data.code === 200) {
      return response
    }

    // 其他业务错误
    message.error(data.message || '请求失败')
    return Promise.reject(new Error(data.message || '请求失败'))
  },
  (error: AxiosError<ApiResponse>) => {
    // 调试模式下打印错误信息
    if (import.meta.env.VITE_DEBUG === 'true') {
      console.error('[Response Error]', error)
    }

    // 网络错误
    if (!error.response) {
      message.error('网络连接失败，请检查网络设置')
      return Promise.reject(error)
    }

    // HTTP状态码错误
    const { status } = error.response
    switch (status) {
      case 400:
        message.error('请求参数错误')
        break
      case 404:
        message.error('请求的资源不存在')
        break
      case 500:
        message.error('服务器内部错误')
        break
      case 502:
        message.error('网关错误')
        break
      case 503:
        message.error('服务暂不可用')
        break
      default:
        message.error(`请求失败 (${status})`)
    }

    return Promise.reject(error)
  }
)

/**
 * 封装GET请求
 */
export function get<T = any>(url: string, params?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
  return request.get(url, { params, ...config })
}

/**
 * 封装POST请求
 */
export function post<T = any>(url: string, data?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
  return request.post(url, data, config)
}

/**
 * 封装PUT请求
 */
export function put<T = any>(url: string, data?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
  return request.put(url, data, config)
}

/**
 * 封装DELETE请求
 */
export function del<T = any>(url: string, params?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
  return request.delete(url, { params, ...config })
}

/** 导出Axios实例 */
export default request
