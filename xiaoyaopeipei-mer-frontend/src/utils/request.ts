/**
 * Axios请求封装
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
  /** 是否需要Token */
  needToken?: boolean
}

/**
 * Token管理类
 */
class TokenManager {
  private readonly storageKey: string

  constructor() {
    this.storageKey = import.meta.env.VITE_TOKEN_KEY
  }

  /** 获取Token */
  getToken(): string | null {
    return localStorage.getItem(this.storageKey)
  }

  /** 设置Token */
  setToken(token: string): void {
    localStorage.setItem(this.storageKey, token)
  }

  /** 移除Token */
  removeToken(): void {
    localStorage.removeItem(this.storageKey)
  }
}

/** 导出Token管理实例 */
export const tokenManager = new TokenManager()

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
    // 添加Token
    const token = tokenManager.getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
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
    const { data } = response

    // 调试模式下打印响应信息
    if (import.meta.env.VITE_DEBUG === 'true') {
      console.log(`[Response] ${response.config.url}`, data)
    }

    // 业务状态码判断
    if (data.code === 200) {
      return response
    }

    // Token过期或无效
    if (data.code === 401) {
      tokenManager.removeToken()
      message.error('登录已过期，请重新登录')
      window.location.href = '/login'
      return Promise.reject(new Error(data.message || '登录已过期'))
    }

    // 无权限
    if (data.code === 403) {
      message.error('没有权限访问该资源')
      return Promise.reject(new Error(data.message || '没有权限'))
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
      case 401:
        tokenManager.removeToken()
        message.error('登录已过期，请重新登录')
        window.location.href = '/login'
        break
      case 403:
        message.error('没有权限访问该资源')
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

/**
 * 封装文件上传
 */
export function upload<T = any>(url: string, file: File, onProgress?: (percent: number) => void): Promise<ApiResponse<T>> {
  const formData = new FormData()
  formData.append('file', file)

  return request.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percent)
      }
    },
  })
}

/** 导出Axios实例 */
export default request