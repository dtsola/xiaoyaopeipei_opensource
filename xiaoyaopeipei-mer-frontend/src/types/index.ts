/**
 * 小遥配配 B端 - 类型定义
 */

// ========== 用户/商家相关 ==========
export interface MerchantUser {
  id: string
  username: string
  shop_name: string
  phone: string
  address?: string
  business_hours?: string
  share_link?: string
  membership_expiry?: string
  is_membership_expired?: boolean
  show_expiry_warning?: boolean
  created_at: string
  updated_at?: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
  shop_name: string
  phone: string
  address?: string
  business_hours?: string
}

export interface AuthResponse {
  token: string
  user: MerchantUser
}

// ========== SKU相关 ==========
export type DeviceType = 'desktop' | 'laptop' | 'aio'

export interface SKU {
  id: string
  merchant_id: string
  device_type: DeviceType
  name: string
  brand?: string
  model?: string
  cpu: string
  gpu?: string
  ram: string
  storage: string
  motherboard?: string
  power_supply?: string
  case?: string
  screen?: string
  weight?: string
  battery?: string
  price: number
  stock: number
  status: 'active' | 'inactive'
  tags: string[]
  images: string[]
  view_count: number
  select_count: number
  created_at: string
  updated_at: string
}

export interface SKUListParams {
  device_type?: DeviceType
  status?: 'active' | 'inactive'
  search?: string
  page: number
  limit: number
}

export interface SKUListResponse {
  list: SKU[]
  total: number
  page: number
  limit: number
  pages: number
}

// ========== 线索相关 ==========
export type LeadStatus = 'pending' | 'contacted' | 'closed' | 'abandoned'

export interface CustomerNeed {
  budget: string
  device_type: string
  usage: string
  requirements?: string
  brand?: string
  portable?: string
}

export interface ConversationMessage {
  id: string
  role: 'assistant' | 'user'
  content: string
  created_at: string
}

export interface ConversationMessagesResponse {
  conversation_id: string
  items: ConversationMessage[]
  total: number
}

export interface SelectedSKU {
  id: string
  name: string
  price: number
  images?: string[]
  specs?: {
    cpu?: string
    gpu?: string
  }
}

export interface Lead {
  id: string
  phone: string
  phone_full?: string  // 完整明文手机号（用于复制）
  wechat?: string
  budget: string
  device_type: string
  usage: string
  requirements?: string
  selected_sku?: SelectedSKU
  status: LeadStatus
  created_at: string
}

export interface LeadDetail {
  id: string
  phone: string
  wechat?: string
  remark?: string
  budget: string
  device_type: string
  usage: string
  requirements?: string
  selected_sku?: SelectedSKU
  conversation?: {
    id: string
    session_id: string
    status: string
    created_at: string
  }
  notes: Note[]
  status: LeadStatus
  created_at: string
  updated_at?: string
}

export interface Note {
  id?: string
  content: string
  created_at: string
}

export interface LeadListParams {
  status?: LeadStatus
  device_type?: DeviceType
  start_date?: string
  end_date?: string
  search?: string
  page: number
  limit: number
}

// ========== 分享相关 ==========
export interface QRCodeResponse {
  qrcode_url: string
  share_link: string
}

export interface ShareStats {
  scan_count: number
  consult_count: number
  lead_count: number
  conversion_rate: number
  device_type_stats: {
    laptop: number
    desktop: number
    aio: number
  }
  budget_stats: {
    '3000-5000': number
    '5000-8000': number
    '8000-12000': number
    '12000+': number
  }
}

// ========== 首页数据 ==========
export interface DashboardStats {
  consult_count: number
  lead_count: number
  conversion_rate: number
  consult_trend: number
  lead_trend: number
  conversion_trend: number
}

export interface HotSKU {
  id: string
  name: string
  device_type: string
  select_count: number
}

// ========== 通用 ==========
export interface PaginationParams {
  page: number
  limit: number
}

export interface PaginationResponse<T> {
  list: T[]
  total: number
  page: number
  limit: number
  pages: number
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data?: T
  timestamp: number
  request_id?: string
}
