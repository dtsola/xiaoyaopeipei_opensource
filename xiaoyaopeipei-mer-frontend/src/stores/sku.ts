/**
 * 小遥配配 B端 - SKU状态管理
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { SKU, SKUListParams } from '@/types'
import * as skuApi from '@/api/sku'

export const useSkuStore = defineStore('sku', () => {
  // 状态
  const skuList = ref<SKU[]>([])
  const currentSku = ref<SKU | null>(null)
  const total = ref(0)
  const loading = ref(false)
  const summary = ref<any>(null)

  // 获取列表
  async function fetchList(params: SKUListParams) {
    loading.value = true
    try {
      const res = await skuApi.getSKUList(params)
      skuList.value = res.data.data.items
      total.value = res.data.data.total
      return res.data.data
    } finally {
      loading.value = false
    }
  }

  // 获取详情
  async function fetchDetail(id: string | number) {
    loading.value = true
    try {
      const res = await skuApi.getSKUDetail(id)
      currentSku.value = res.data.data
      return res.data.data
    } finally {
      loading.value = false
    }
  }

  // 创建
  async function create(data: any) {
    const res = await skuApi.createSKU(data)
    return res.data.data
  }

  // 更新
  async function update(id: string | number, data: any) {
    await skuApi.updateSKU(id, data)
  }

  // 删除
  async function remove(id: string | number) {
    await skuApi.deleteSKU(id)
  }

  // 批量删除
  async function batchRemove(ids: (string | number)[]) {
    await skuApi.batchDeleteSKU(ids)
  }

  // 获取统计
  async function fetchSummary() {
    const res = await skuApi.getSKUSummary()
    summary.value = res.data.data
  }

  return {
    skuList,
    currentSku,
    total,
    loading,
    summary,
    fetchList,
    fetchDetail,
    create,
    update,
    remove,
    batchRemove,
    fetchSummary
  }
})
