/**
 * SKU管理模块 API
 */

import { get, post, put, del } from '@/utils/request'
import type { SKU, SKUListParams } from '@/types'

/**
 * 获取SKU列表（分页）
 */
export function getSKUList(params: SKUListParams) {
  return get<{
    items: SKU[]
    total: number
    page: number
    limit: number
    pages: number
  }>('/skus', params)
}

/**
 * 获取SKU详情
 */
export function getSKUDetail(id: string | number) {
  return get<SKU>(`/skus/${id}`)
}

/**
 * 创建SKU
 */
export function createSKU(data: Partial<Sku>) {
  return post<{ id: string }>('/skus', data)
}

/**
 * 更新SKU
 */
export function updateSKU(id: string | number, data: Partial<Sku>) {
  return put(`/skus/${id}`, data)
}

/**
 * 删除SKU
 */
export function deleteSKU(id: string | number) {
  return del(`/skus/${id}`)
}

/**
 * 批量删除SKU
 */
export function batchDeleteSKU(ids: (string | number)[]) {
  return del('/skus', { ids })
}

/**
 * 获取SKU统计摘要
 */
export function getSKUSummary() {
  return get<{
    total: number
    active_count: number
    inactive_count: number
    device_type_stats: Record<string, number>
  }>('/skus/stats/summary')
}
