/**
 * 数据统计模块 API
 */

import { get } from '@/utils/request'
import type { DashboardStats, HotSKU } from '@/types'

/**
 * 获取商家汇总统计（用于个人中心使用统计）
 */
export function getSummary() {
  return get<{
    sku_count: number
    lead_count: number
    closed_count: number
    days_since_registration: number
  }>('/dashboard/summary')
}

/**
 * 获取首页看板数据
 */
export function getDashboardData() {
  return get<{
    today_stats: DashboardStats
    trend_data: any[]
    device_type_distribution: Record<string, number>
    budget_distribution: Record<string, number>
    top_skus: HotSKU[]
  }>('/dashboard')
}

/**
 * 获取趋势数据
 */
export function getTrendData(days: number = 7) {
  return get('/dashboard/trends', { days })
}

/**
 * 获取转化率统计
 */
export function getConversionRate(period: string = 'week') {
  return get('/dashboard/conversion', { period })
}

/**
 * 获取热门配置排行
 */
export function getTopSKUs(limit: number = 10) {
  return get<HotSKU[]>('/dashboard/top-skus', { limit })
}

/**
 * 获取单个SKU统计
 */
export function getSKUStats(skuId: string | number) {
  return get('/dashboard/sku-stats', { sku_id: skuId })
}

/**
 * 获取业绩统计
 */
export function getPerformanceStats(period: string = 'week') {
  return get('/dashboard/performance', { period })
}
