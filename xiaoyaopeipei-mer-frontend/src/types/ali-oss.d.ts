/**
 * ali-oss 类型声明
 */
declare module 'ali-oss' {
  export interface PutOptions {
    headers?: Record<string, string>
    [key: string]: any
  }

  export interface PutResult {
    name: string
    url: string
    res: any
  }

  export interface OSSOptions {
    region: string
    accessKeyId: string
    accessKeySecret: string
    stsToken?: string
    bucket: string
    endpoint?: string
    secure?: boolean
    timeout?: number
    [key: string]: any
  }

  export class OSS {
    constructor(options: OSSOptions)

    put(name: string, file: File | Buffer | string, options?: PutOptions): Promise<PutResult>

    get(name: string): Promise<any>

    delete(name: string): Promise<any>

    list(query?: any): Promise<any>

    signatureUrl(name: string): string
  }

  const default: new (options: OSSOptions) => OSS
  export default default
}
