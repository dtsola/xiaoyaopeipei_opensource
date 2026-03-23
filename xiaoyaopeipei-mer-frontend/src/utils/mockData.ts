/**
 * 小遥配配 B端 - Mock数据
 */

import type { MerchantUser, SKU, Lead, LeadDetail, DashboardStats, HotSKU } from '@/types'

// ========== Mock用户数据 ==========
export const mockUser: MerchantUser = {
  id: '1234567890123456789',
  username: 'shop_admin',
  shop_name: 'XX电脑城',
  phone: '138-1234-5678',
  address: 'XX市XX区XX路XX号',
  business_hours: '9:00 - 21:00',
  share_link: 'https://xiaoyao.com/shop/abc123',
  created_at: '2025-12-01T00:00:00Z',
  membership_expires_at: '2026-12-31T00:00:00Z'
}

// ========== Mock SKU数据 ==========
export const mockSKUs: SKU[] = [
  {
    id: '1234567890123456790',
    merchant_id: '1234567890123456789',
    device_type: 'laptop',
    name: '联想拯救者Y7000P',
    brand: '联想',
    model: 'Y7000P 2023款',
    cpu: 'i7-12700H',
    gpu: 'RTX 4060 8G',
    ram: '16GB DDR5',
    storage: '512GB SSD',
    screen: '15.6英寸 2.5K 165Hz',
    weight: '2.4kg',
    battery: '5-6小时',
    price: 7499,
    stock: 5,
    status: 'active',
    tags: ['gaming', 'brand', 'high-performance'],
    images: ['https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=300&fit=crop'],
    view_count: 45,
    select_count: 12,
    created_at: '2025-12-22T10:00:00Z',
    updated_at: '2025-12-22T10:00:00Z'
  },
  {
    id: '1234567890123456791',
    merchant_id: '1234567890123456789',
    device_type: 'laptop',
    name: '华硕天选4',
    brand: '华硕',
    model: '天选4 2023款',
    cpu: 'R7-7735HS',
    gpu: 'RTX 4050 6G',
    ram: '16GB DDR5',
    storage: '512GB SSD',
    screen: '15.6英寸 2.5K 165Hz',
    weight: '2.3kg',
    battery: '4-5小时',
    price: 6799,
    stock: 3,
    status: 'active',
    tags: ['gaming', 'brand'],
    images: ['https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=300&fit=crop'],
    view_count: 38,
    select_count: 9,
    created_at: '2025-12-22T10:00:00Z',
    updated_at: '2025-12-22T10:00:00Z'
  },
  {
    id: '1234567890123456792',
    merchant_id: '1234567890123456789',
    device_type: 'desktop',
    name: '游戏主机-入门款',
    brand: null,
    model: null,
    cpu: 'i5-12400F',
    gpu: 'RTX 3050 8G',
    ram: '16GB DDR4',
    storage: '512GB SSD',
    motherboard: 'B660M',
    power_supply: '650W 80Plus金牌',
    case: 'ATX中塔机箱',
    price: 4999,
    stock: 0,
    status: 'inactive',
    tags: ['gaming', 'budget'],
    images: ['https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=400&h=300&fit=crop'],
    view_count: 28,
    select_count: 7,
    created_at: '2025-12-22T10:00:00Z',
    updated_at: '2025-12-22T10:00:00Z'
  },
  {
    id: '1234567890123456793',
    merchant_id: '1234567890123456789',
    device_type: 'desktop',
    name: '办公主机-标准款',
    brand: null,
    model: null,
    cpu: 'i5-13400F',
    gpu: '集成显卡',
    ram: '16GB DDR4',
    storage: '512GB SSD',
    motherboard: 'B760M',
    power_supply: '500W 80Plus铜牌',
    case: 'MATX小机箱',
    price: 3999,
    stock: 8,
    status: 'active',
    tags: ['office'],
    images: ['https://images.unsplash.com/photo-1593062096033-9a26b09da705?w=400&h=300&fit=crop'],
    view_count: 35,
    select_count: 5,
    created_at: '2025-12-22T10:00:00Z',
    updated_at: '2025-12-22T10:00:00Z'
  },
  {
    id: '1234567890123456794',
    merchant_id: '1234567890123456789',
    device_type: 'aio',
    name: '设计师一体机',
    brand: '戴尔',
    model: 'XPS 27',
    cpu: 'i7-13700',
    gpu: 'RTX 4060',
    ram: '32GB DDR5',
    storage: '1TB SSD',
    screen: '27英寸 4K 触控',
    price: 12999,
    stock: 2,
    status: 'active',
    tags: ['design', 'high-performance'],
    images: ['https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=300&fit=crop'],
    view_count: 18,
    select_count: 3,
    created_at: '2025-12-22T10:00:00Z',
    updated_at: '2025-12-22T10:00:00Z'
  }
]

// ========== Mock线索数据 ==========
export const mockLeads: Lead[] = [
  {
    id: '1234567890123456800',
    phone: '138****5678',
    wechat: 'user_wechat',
    budget: '6000左右',
    device_type: '笔记本',
    usage: '游戏',
    requirements: '玩原神',
    selected_sku: {
      id: '1234567890123456790',
      name: '联想拯救者Y7000P',
      price: 7499
    },
    status: 'pending',
    created_at: '2025-12-22T14:30:00Z'
  },
  {
    id: '1234567890123456801',
    phone: '139****1234',
    wechat: null,
    budget: '5000左右',
    device_type: '台式机',
    usage: '办公',
    requirements: null,
    selected_sku: {
      id: '1234567890123456793',
      name: '办公主机-标准款',
      price: 3999
    },
    status: 'contacted',
    created_at: '2025-12-22T14:00:00Z'
  },
  {
    id: '1234567890123456802',
    phone: '136****7890',
    wechat: 'customer_c',
    budget: '8000左右',
    device_type: '笔记本',
    usage: '设计',
    requirements: '视频剪辑',
    selected_sku: {
      id: '1234567890123456794',
      name: '华硕天选4 Plus',
      price: 8799
    },
    status: 'closed',
    created_at: '2025-12-22T12:00:00Z'
  },
  {
    id: '1234567890123456803',
    phone: '135****4567',
    wechat: null,
    budget: '4000左右',
    device_type: '台式机',
    usage: '游戏',
    requirements: 'LOL',
    selected_sku: {
      id: '1234567890123456792',
      name: '游戏主机-入门款',
      price: 4999
    },
    status: 'abandoned',
    created_at: '2025-12-22T10:00:00Z'
  }
]

// ========== Mock线索详情 ==========
export const mockLeadDetail: LeadDetail = {
  id: '1234567890123456800',
  phone: '13812345678',
  wechat: 'user_wechat',
  remark: '希望尽快联系',
  budget: '6000左右',
  device_type: '笔记本',
  usage: '游戏',
  requirements: '玩原神',
  selected_sku: {
    id: '1234567890123456790',
    name: '联想拯救者Y7000P',
    price: 7499,
    specs: {
      cpu: 'i7-12700H',
      gpu: 'RTX 4060 8G'
    }
  },
  status: 'pending',
  created_at: '2025-12-22T14:30:00Z',
  needs: {
    budget: '6000左右',
    device_type: '笔记本',
    usage: '游戏',
    requirements: '玩原神',
    portable: '主要在家用'
  },
  conversation: {
    messages: [
      {
        role: 'assistant',
        content: '您好！我是小遥，我来帮您选一台合适的电脑～请问您的预算大概是多少呢？',
        created_at: '2025-12-22T14:30:15Z'
      },
      {
        role: 'user',
        content: '我想要一台6000左右的游戏笔记本能玩原神',
        created_at: '2025-12-22T14:30:42Z'
      },
      {
        role: 'assistant',
        content: '明白了！6000左右的游戏笔记本，玩原神完全够用～\n您需要经常携带吗？还是主要在家用？',
        created_at: '2025-12-22T14:30:45Z'
      },
      {
        role: 'user',
        content: '主要在家用',
        created_at: '2025-12-22T14:31:02Z'
      },
      {
        role: 'assistant',
        content: '好的！我已经为您找到3个适合的游戏笔记本🎉\n\n1. 联想拯救者Y7000P - ¥7,499\n   搭载RTX 4060显卡，原神可以稳定60帧高画质运行\n\n2. 华硕天选4 - ¥6,799\n   AMD处理器性能强劲，同样是RTX 4060显卡\n\n3. 机械革命蛟龙16 - ¥6,299\n   性价比之选，同样配置价格更实惠\n\n请问您对哪款更感兴趣呢？',
        created_at: '2025-12-22T14:31:05Z'
      }
    ]
  },
  notes: [
    {
      content: '已电话沟通，客户表示很满意，明天来店看实物',
      created_at: '2025-12-22T14:35:00Z'
    },
    {
      content: '客户询问是否可以分期付款',
      created_at: '2025-12-22T14:40:00Z'
    }
  ]
}

// ========== Mock首页数据 ==========
export const mockDashboardStats: DashboardStats = {
  consult_count: 23,
  lead_count: 15,
  conversion_rate: 65.2,
  consult_trend: 12,
  lead_trend: 8,
  conversion_trend: 5
}

export const mockHotSKUs: HotSKU[] = [
  { id: '1234567890123456790', name: '联想拯救者Y7000P', device_type: '笔记本', select_count: 12 },
  { id: '1234567890123456791', name: '华硕天选4', device_type: '笔记本', select_count: 9 },
  { id: '1234567890123456793', name: '办公主机-标准款', device_type: '台式机', select_count: 7 }
]

// ========== Mock分享数据 ==========
// 使用公共二维码API生成二维码图片
export const mockQRCodeUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://xiaoyao.com/shop/abc123'
export const mockShareLink = 'https://xiaoyao.com/shop/abc123'

// ========== 延迟函数模拟API请求 ==========
export const delay = (ms: number = 500) => new Promise(resolve => setTimeout(resolve, ms))
