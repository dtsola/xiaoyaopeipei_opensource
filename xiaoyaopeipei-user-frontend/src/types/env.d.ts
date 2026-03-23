/**
 * 环境变量类型定义 - C端
 */

/**
 * 导出环境变量配置接口
 */
export interface ImportMetaEnv {
  /** 环境模式 */
  readonly NODE_ENV: string
  /** 应用标题 */
  readonly VITE_APP_TITLE: string
  /** API基础路径（C端） */
  readonly VITE_API_BASE_URL: string
  /** 商户端后台地址 */
  readonly VITE_MER_BACKEND_URL: string
  /** OSS访问域名 */
  readonly VITE_OSS_DOMAIN: string
  /** 是否启用Mock数据 */
  readonly VITE_USE_MOCK: string
  /** 是否启用调试模式 */
  readonly VITE_DEBUG: string
  /** 请求超时时间（毫秒） */
  readonly VITE_REQUEST_TIMEOUT: string
  /** 会话存储键名 */
  readonly VITE_SESSION_KEY: string
  /** 最大推荐结果数量 */
  readonly VITE_MAX_RECOMMEND_COUNT: string
}

/**
 * 导出元数据接口
 */
export interface ImportMeta {
  readonly env: ImportMetaEnv
}
