/**
 * 文件上传模块 API
 */

import { get, post } from '@/utils/request'

/**
 * 获取OSS直传凭证（STS临时凭证）
 */
export function getOSSUploadToken() {
  return get<{
    region: string
    bucket: string
    accessKeyId: string
    accessKeySecret: string
    stsToken: string
    host: string
    dir: string
    expire: number
  }>('/upload/oss/token')
}

/**
 * OSS上传回调
 */
export function ossUploadCallback(data: {
  key: string
  size: number
  name: string
  etag?: string
}) {
  return post<{
    url: string
    key: string
    size: number
    name: string
  }>('/upload/oss/callback', data)
}
