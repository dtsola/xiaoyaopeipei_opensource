/**
 * 环境变量类型定义
 */

/**
 * 导出环境变量配置接口
 */
export interface ImportMetaEnv {
  /** 环境模式 */
  readonly NODE_ENV: string
  /** API基础路径 */
  readonly VITE_API_BASE_URL: string
  /** 是否启用调试模式 */
  readonly VITE_DEBUG: string
  /** 请求超时时间（毫秒） */
  readonly VITE_REQUEST_TIMEOUT: string
  /** Token存储键名 */
  readonly VITE_TOKEN_KEY: string
}

/**
 * 导出元数据接口
 */
export interface ImportMeta {
  readonly env: ImportMetaEnv
}