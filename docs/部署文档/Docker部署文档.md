# 小遥配配 - Docker Compose 部署文档

## 文档概述

本文档提供小遥配配项目的完整 Docker Compose 部署方案，包括后端 API 服务、C 端前端、B 端前端、MySQL 数据库和 Nginx 反向代理的一键部署配置。

---

## 一、项目架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         Docker Compose                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   C端前端   │    │   B端前端   │    │  Nginx代理  │         │
│  │   (Vue3)    │    │   (Vue3)    │    │   :80/:443  │         │
│  │   :3000     │    │   :3001     │    └──────┬──────┘         │
│  └──────┬──────┘    └──────┬──────┘           │                │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            │                                   │
│                            ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Nginx :80                             │   │
│  │  / (C端) → user-frontend:3000                            │   │
│  │  /mer/ (B端) → mer-frontend:3001                         │   │
│  │  /api/ → backend:8001                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                   │
│                            ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              后端 API 服务 (FastAPI)                      │   │
│  │                      :8001                                │   │
│  └───────────────────────────┬─────────────────────────────┘   │
│                              │                                 │
│                              ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MySQL 数据库 :3306                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、目录结构

```
xiaoyaopeipei/
├── docker/
│   ├── .env                        # 统一环境变量配置
│   ├── docker-compose.yml          # Docker Compose 配置文件
│   └── nginx/
│       ├── nginx.conf              # Nginx 主配置
│       ├── conf.d/
│       │   ├── default.conf        # 站点配置 (HTTP)
│       │   └── https.conf          # 站点配置 (HTTPS)
│       ├── ssl/                    # SSL 证书目录（生产环境）
│       └── logs/                   # Nginx 日志目录
├── xiaoyaopeipei-user-frontend/    # C端前端
│   ├── Dockerfile                  # 前端镜像构建文件
│   └── nginx.conf                  # 前端 Nginx 配置
├── xiaoyaopeipei-mer-frontend/     # B端前端
│   ├── Dockerfile                  # 前端镜像构建文件
│   └── nginx.conf                  # 前端 Nginx 配置
└── xiaoyaopeipei-user-merchant-backend/  # 后端
    ├── Dockerfile                  # 后端镜像构建文件
    └── docker-entrypoint.sh        # 容器启动脚本（自动运行数据库迁移）
```

---

## 三、Dockerfile 配置

### 3.1 后端 Dockerfile

**文件路径**: `xiaoyaopeipei-user-merchant-backend/Dockerfile`

后端服务使用启动脚本自动完成数据库初始化，实现一键部署。

```dockerfile
# ==================== 小遥配配 - 后端 Dockerfile ====================
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 复制并设置启动脚本
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8001

# 使用启动脚本作为入口点
ENTRYPOINT ["docker-entrypoint.sh"]
```

### 3.2 后端启动脚本

**文件路径**: `xiaoyaopeipei-user-merchant-backend/docker-entrypoint.sh`

启动脚本自动完成以下操作：
1. 等待 MySQL 数据库就绪
2. 运行 `alembic upgrade head` 自动创建/更新表结构
3. 启动 FastAPI 服务

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "  小遥配配 - 后端服务启动脚本"
echo "=========================================="

# 等待 MySQL 数据库就绪
wait_for_mysql() {
    echo "正在等待 MySQL 数据库就绪..."
    # ... 等待逻辑
}

# 运行数据库迁移
run_migrations() {
    echo "正在运行数据库迁移..."
    alembic upgrade head
    echo "✓ 数据库迁移完成!"
}

# 启动应用服务
start_application() {
    echo "正在启动后端服务..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8001
}

# 执行主流程
wait_for_mysql
run_migrations
start_application
```

### 3.3 C端前端 Dockerfile

**文件路径**: `xiaoyaopeipei-user-frontend/Dockerfile`

```dockerfile
# ==================== 小遥配配 - C端前端 Dockerfile ====================
# 多阶段构建：构建阶段 + 生产阶段

# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

# 声明构建参数（环境变量）
ARG VITE_API_BASE_URL=/api/user
ARG VITE_MER_BACKEND_URL=https://peipei-mer.xiaoyaos.com
ARG VITE_OSS_DOMAIN=https://file.xiaoyaosai.com
ARG VITE_APP_TITLE=小遥配配 - AI电脑导购
ARG VITE_REQUEST_TIMEOUT=30000

# 将 ARG 转为 ENV（构建时可用）
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
# ... 其他环境变量

# 安装 pnpm
RUN npm install -g pnpm@latest

# 安装依赖并构建
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# 生产阶段
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制自定义 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3.4 B端前端 Dockerfile

**文件路径**: `xiaoyaopeipei-mer-frontend/Dockerfile`

```dockerfile
# ==================== B端前端 Dockerfile ====================
# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

# 复制 package 文件
COPY package.json pnpm-lock.yaml ./

# 安装 pnpm
RUN npm install -g pnpm

# 安装依赖
RUN pnpm install --frozen-lockfile

# 复制源代码
COPY . .

# 构建生产版本
RUN pnpm build

# 生产阶段
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制自定义 nginx 配置（可选）
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3001

CMD ["nginx", "-g", "daemon off;"]
```

---

## 四、Docker Compose 配置

**文件路径**: `docker/docker-compose.yml`

```yaml
# ==================== Docker Compose 配置 ====================
version: '3.8'

services:
  # ==================== MySQL 数据库 ====================
  mysql:
    image: mysql:8.0
    container_name: xiaoyaopeipei-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-your_secure_password}
      MYSQL_DATABASE: ${MYSQL_DATABASE:-xiaoyaopeipei}
      MYSQL_USER: ${MYSQL_USER:-xiaoyaopeipei}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-xiaoyaopeipei_password}
      TZ: Asia/Shanghai
    ports:
      - "${MYSQL_PORT:-3306}:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    command: >
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --default-time-zone=+08:00
      --max_connections=1000
      --max_allowed_packet=256M
    networks:
      - xiaoyaopeipei-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==================== 后端 API 服务 ====================
  backend:
    build:
      context: ../xiaoyaopeipei-user-merchant-backend
      dockerfile: Dockerfile
    container_name: xiaoyaopeipei-backend
    restart: unless-stopped
    ports:
      - "${BACKEND_PORT:-8001}:8001"
    environment:
      # 应用配置
      APP_ENV: ${APP_ENV:-production}
      APP_DEBUG: ${APP_DEBUG:-false}
      APP_HOST: 0.0.0.0
      APP_PORT: 8001

      # 数据库配置
      DATABASE_URL: mysql+pymysql://${MYSQL_USER:-xiaoyaopeipei}:${MYSQL_PASSWORD:-xiaoyaopeipei_password}@mysql:3306/${MYSQL_DATABASE:-xiaoyaopeipei}?charset=utf8mb4

      # JWT 配置
      JWT_SECRET: ${JWT_SECRET}
      JWT_ALGORITHM: HS256
      JWT_EXPIRE_MINUTES: 10080

      # 通义千问配置
      QWEN_API_KEY: ${QWEN_API_KEY}
      QWEN_MODEL: ${QWEN_MODEL:-qwen-plus}
      QWEN_TEMPERATURE: ${QWEN_TEMPERATURE:-0.7}
      QWEN_MAX_TOKENS: ${QWEN_MAX_TOKENS:-2000}

      # OSS 配置
      OSS_ACCESS_KEY_ID: ${OSS_ACCESS_KEY_ID}
      OSS_ACCESS_KEY_SECRET: ${OSS_ACCESS_KEY_SECRET}
      OSS_BUCKET: ${OSS_BUCKET}
      OSS_ENDPOINT: ${OSS_ENDPOINT}
      OSS_REGION: ${OSS_REGION}
      OSS_HOST: ${OSS_HOST}

      # 缓存配置
      CACHE_MAX_SIZE: ${CACHE_MAX_SIZE:-1000}
      CACHE_TTL: ${CACHE_TTL:-3600}

      # AES 加密
      AES_KEY: ${AES_KEY}

      # 日志配置
      LOG_LEVEL: ${LOG_LEVEL:-INFO}

      # CORS 配置
      CORS_ORIGINS: ${CORS_ORIGINS:-["https://peipei.xiaoyaos.com","https://peipei-mer.xiaoyaos.com"]}
      CORS_ALLOW_CREDENTIALS: "true"
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - xiaoyaopeipei-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # ==================== C端前端 ====================
  user-frontend:
    build:
      context: ../xiaoyaopeipei-user-frontend
      dockerfile: Dockerfile
      args:
        VITE_API_BASE_URL: ${VITE_USER_API_BASE_URL:-/api/user}
        VITE_MER_BACKEND_URL: ${VITE_MER_BACKEND_URL:-https://peipei-mer.xiaoyaos.com}
        VITE_OSS_DOMAIN: ${VITE_OSS_DOMAIN}
        VITE_APP_TITLE: ${VITE_APP_TITLE:-小遥配配 - AI电脑导购}
        VITE_REQUEST_TIMEOUT: ${VITE_REQUEST_TIMEOUT:-30000}
    container_name: xiaoyaopeipei-user-frontend
    restart: unless-stopped
    ports:
      - "${USER_FRONTEND_PORT:-3000}:80"
    networks:
      - xiaoyaopeipei-network

  # ==================== B端前端 ====================
  mer-frontend:
    build:
      context: ../xiaoyaopeipei-mer-frontend
      dockerfile: Dockerfile
      args:
        VITE_API_BASE_URL: ${VITE_MER_API_BASE_URL:-/api/mer}
        VITE_REQUEST_TIMEOUT: ${VITE_REQUEST_TIMEOUT:-30000}
    container_name: xiaoyaopeipei-mer-frontend
    restart: unless-stopped
    ports:
      - "${MER_FRONTEND_PORT:-3001}:80"
    networks:
      - xiaoyaopeipei-network

  # ==================== Nginx 反向代理 ====================
  nginx:
    image: nginx:alpine
    container_name: xiaoyaopeipei-nginx
    restart: unless-stopped
    ports:
      - "${NGINX_HTTP_PORT:-80}:80"
      - "${NGINX_HTTPS_PORT:-443}:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - backend
      - user-frontend
      - mer-frontend
    networks:
      - xiaoyaopeipei-network

# ==================== 网络配置 ====================
networks:
  xiaoyaopeipei-network:
    driver: bridge

# ==================== 数据卷 ====================
volumes:
  mysql_data:
    driver: local
```

---

## 五、Nginx 配置

### 5.1 Nginx 主配置

**文件路径**: `docker/nginx/nginx.conf`

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 2048;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # 性能优化
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 50M;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    # 包含站点配置
    include /etc/nginx/conf.d/*.conf;
}
```

### 5.2 站点配置（HTTP）

**文件路径**: `docker/nginx/conf.d/default.conf`

```nginx
# ==================== HTTP 配置（开发/测试环境）====================
server {
    listen 80;
    server_name _;

    # C端前端
    location / {
        proxy_pass http://user-frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # B端前端
    location /mer {
        proxy_pass http://mer-frontend:80/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API - C端接口
    location /api/user/ {
        proxy_pass http://backend:8001/api/user/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 300s;
    }

    # 后端 API - B端接口
    location /api/mer/ {
        proxy_pass http://backend:8001/api/mer/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 300s;
    }
}
```

### 5.3 站点配置（HTTPS）

**文件路径**: `docker/nginx/conf.d/https.conf`

```nginx
# ==================== HTTPS 配置（生产环境）====================
# HTTP 跳转 HTTPS
server {
    listen 80;
    server_name peipei.xiaoyaos.com peipei-mer.xiaoyaos.com;
    return 301 https://$server_name$request_uri;
}

# C端 HTTPS
server {
    listen 443 ssl http2;
    server_name peipei.xiaoyaos.com;

    # SSL 证书配置
    ssl_certificate /etc/nginx/ssl/peipei.xiaoyaos.com.crt;
    ssl_certificate_key /etc/nginx/ssl/peipei.xiaoyaos.com.key;

    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全头部
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # C端前端
    location / {
        proxy_pass http://user-frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
    location /api/user/ {
        proxy_pass http://backend:8001/api/user/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 300s;
    }
}

# B端 HTTPS
server {
    listen 443 ssl http2;
    server_name peipei-mer.xiaoyaos.com;

    # SSL 证书配置
    ssl_certificate /etc/nginx/ssl/peipei-mer.xiaoyaos.com.crt;
    ssl_certificate_key /etc/nginx/ssl/peipei-mer.xiaoyaos.com.key;

    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全头部
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # B端前端
    location / {
        proxy_pass http://mer-frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
    location /api/mer/ {
        proxy_pass http://backend:8001/api/mer/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 300s;
    }
}
```

---

## 六、环境变量配置

### 6.1 环境变量文件

**文件路径**: `docker/.env`

```bash
# ==================== 环境配置 ====================
APP_ENV=production
APP_DEBUG=false

# ==================== 端口配置 ====================
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
BACKEND_PORT=8001
USER_FRONTEND_PORT=3000
MER_FRONTEND_PORT=3001
MYSQL_PORT=3306

# ==================== MySQL 配置 ====================
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_DATABASE=xiaoyaopeipei
MYSQL_USER=xiaoyaopeipei
MYSQL_PASSWORD=your_secure_db_password

# ==================== JWT 配置 ====================
JWT_SECRET=your_jwt_secret_key_change_in_production

# ==================== 通义千问配置 ====================
QWEN_API_KEY=sk-your_qwen_api_key_here
QWEN_MODEL=qwen-plus
QWEN_TEMPERATURE=0.7
QWEN_MAX_TOKENS=2000

# ==================== OSS 配置 ====================
OSS_ACCESS_KEY_ID=your_oss_access_key_id
OSS_ACCESS_KEY_SECRET=your_oss_access_key_secret
OSS_BUCKET=your_bucket_name
OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com
OSS_REGION=cn-shanghai
OSS_HOST=https://file.xiaoyaosai.com

# ==================== 加密配置 ====================
AES_KEY=your_aes_key_32_characters_long

# ==================== 日志配置 ====================
LOG_LEVEL=INFO

# ==================== 缓存配置 ====================
CACHE_MAX_SIZE=1000
CACHE_TTL=3600

# ==================== 前端配置 ====================
VITE_API_BASE_URL=/api
VITE_OSS_DOMAIN=https://file.xiaoyaosai.com
VITE_APP_TITLE=小遥配配 - AI电脑导购
VITE_REQUEST_TIMEOUT=30000
VITE_MER_BACKEND_URL=https://peipei-mer.xiaoyaos.com
```

---

## 七、部署步骤

### 7.1 前置条件

- 已安装 Docker 20.10+
- 已安装 Docker Compose 2.0+
- 已有 SSL 证书（生产环境）

### 7.2 一键部署流程

所有配置文件已就绪，只需以下步骤即可完成部署：

**第一步：配置环境变量**

编辑 `docker/.env` 文件，填写以下必需配置：

```bash
# ==================== 公共配置 ====================
# 环境类型: development | staging | production
# 获取方式：根据当前部署环境选择
APP_ENV=development

# 是否启用调试模式（生产环境请设置为 false）
APP_DEBUG=true

# ==================== 端口配置 ====================
# Nginx 端口（本地访问端口，可自定义）
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443

# 后端端口（容器内部端口，一般无需修改）
BACKEND_PORT=8001

# 前端端口（容器内部端口，一般无需修改）
USER_FRONTEND_PORT=3000
MER_FRONTEND_PORT=3001

# MySQL 端口（本地访问端口，可自定义）
MYSQL_PORT=3306

# ==================== MySQL 数据库配置 ====================
# MySQL root 密码
# 获取方式：自定义设置，建议使用强密码
# 生成命令：openssl rand -base64 16
MYSQL_ROOT_PASSWORD=your_secure_root_password_change_me

# 数据库名称
# 获取方式：自定义设置，默认为 xiaoyaopeipei
MYSQL_DATABASE=xiaoyaopeipei

# 数据库用户名
# 获取方式：自定义设置，默认为 xiaoyaopeipei
MYSQL_USER=xiaoyaopeipei

# 数据库密码
# 获取方式：自定义设置，建议使用强密码
# 生成命令：openssl rand -base64 16
MYSQL_PASSWORD=your_secure_db_password_change_me

# ==================== 后端配置（运行时环境变量）====================
# JWT 密钥（用于 Token 签名验证）
# 获取方式：自定义设置，必须是随机字符串（32位以上）
# 生成命令：openssl rand -base64 32
JWT_SECRET=your_jwt_secret_key_change_in_production

# JWT 加密算法（默认 HS256，无需修改）
JWT_ALGORITHM=HS256

# Token 有效期（分钟），10080 = 7天
# 获取方式：根据业务需求自定义
JWT_EXPIRE_MINUTES=10080

# ==================== 通义千问 AI 配置 ====================
# 通义千问 API 密钥（必填）
# 获取方式：
#   1. 访问阿里云百炼平台：https://bailian.console.aliyun.com/
#   2. 开通通义千问服务
#   3. 创建 API-KEY，复制此处
QWEN_API_KEY=sk-your_qwen_api_key_here

# 使用的模型
# 获取方式：根据需求选择
#   - qwen-turbo: 速度快，成本低（推荐日常使用）
#   - qwen-plus: 性能平衡（推荐）
#   - qwen-max: 性能最强，成本高
QWEN_MODEL=qwen-plus

# 温度参数（0-1，越高越随机）
# 获取方式：根据需求调整，0.7 为推荐值
QWEN_TEMPERATURE=0.7

# 最大 token 数
# 获取方式：根据需求调整，2000 为推荐值
QWEN_MAX_TOKENS=2000

# ==================== 阿里云 OSS 配置 ====================
# OSS 访问密钥 ID（必填）
# 获取方式：
#   1. 访问阿里云 OSS 控制台：https://oss.console.aliyun.com/
#   2. 创建 AccessKey（推荐使用 RAM 子账号）
#   3. 复制 AccessKey ID
OSS_ACCESS_KEY_ID=your_oss_access_key_id

# OSS 访问密钥 Secret（必填）
# 获取方式：同上，复制 AccessKey Secret
OSS_ACCESS_KEY_SECRET=your_oss_access_key_secret

# OSS 存储桶名称（必填）
# 获取方式：在 OSS 控制台创建 Bucket 后，复制 Bucket 名称
OSS_BUCKET=your_bucket_name

# OSS 终端节点
# 获取方式：根据 Bucket 所在区域选择
#   - 华东1（杭州）：oss-cn-hangzhou.aliyuncs.com
#   - 华东2（上海）：oss-cn-shanghai.aliyuncs.com
#   - 华北2（北京）：oss-cn-beijing.aliyuncs.com
#   - 华南1（深圳）：oss-cn-shenzhen.aliyuncs.com
OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com

# OSS 区域
# 获取方式：与终端节点对应
#   - cn-hangzhou、cn-shanghai、cn-beijing、cn-shenzhen
OSS_REGION=cn-shanghai

# OSS 自定义域名（用于文件访问）
# 获取方式：
#   方式一（有自定义域名）：填写绑定的自定义域名，如 https://file.xiaoyaosai.com
#   方式二（无自定义域名）：填写 OSS 默认域名，格式：https://{bucket-name}.{endpoint}
#   示例：https://xiaoyaopeipei.oss-cn-shanghai.aliyuncs.com
OSS_HOST=https://your-bucket-name.oss-cn-shanghai.aliyuncs.com

# OSS STS 角色 ARN（可选，用于生成临时凭证）
# 获取方式：
#   1. 在 RAM 控制台创建角色并授权
#   2. 复制角色 ARN，格式：acs:ram::<主账号ID>:role/<角色名>
#   注意：开发环境可留空，使用永久 AccessKey
OSS_STS_ROLE_ARN=

# ==================== 缓存配置 ====================
# 缓存最大条目数
# 获取方式：根据服务器内存调整
CACHE_MAX_SIZE=1000

# 缓存默认过期时间（秒）
# 获取方式：根据业务需求调整，3600 = 1小时
CACHE_TTL=3600

# ==================== 加密配置 ====================
# AES 加密密钥（32位字符串）
# 获取方式：自定义设置，必须是 32 位字符串
# 生成命令：openssl rand -base64 24 | head -c 32
AES_KEY=your_aes_key_32_characters_long

# ==================== 日志配置 ====================
# 日志级别: DEBUG | INFO | WARNING | ERROR
# 获取方式：开发环境用 DEBUG，生产环境用 INFO
LOG_LEVEL=DEBUG

# ==================== CORS 配置 ====================
# CORS 允许的域名（JSON 数组格式）
# 获取方式：本地开发使用 http://localhost，生产环境改为实际域名
# 注意：["*"] 表示允许所有域名（仅开发环境使用）
CORS_ORIGINS=["*"]

# 是否允许携带凭证
CORS_ALLOW_CREDENTIALS=true

# ==================== C端前端配置（构建时）====================
# API 基础路径（使用相对路径，由 Nginx 代理）
# 获取方式：Docker 环境使用 /api/user，由 Nginx 转发到后端
VITE_USER_API_BASE_URL=/api/user

# 商户端后台地址（用于跳转）
# 获取方式：本地开发填 http://localhost/mer，生产环境填实际域名
VITE_USER_MER_BACKEND_URL=http://localhost/mer

# OSS 访问域名（前端直接访问 OSS 的地址）
# 获取方式：与 OSS_HOST 保持一致
VITE_USER_OSS_DOMAIN=https://your-bucket-name.oss-cn-shanghai.aliyuncs.com

# 应用标题
# 获取方式：自定义设置
VITE_USER_APP_TITLE=小遥配配 - AI电脑导购

# 请求超时时间（毫秒）
# 获取方式：根据网络情况调整，默认 30000ms = 30秒
VITE_REQUEST_TIMEOUT=30000

# ==================== B端前端配置（构建时）====================
# API 基础路径（使用相对路径，由 Nginx 代理）
# 获取方式：Docker 环境使用 /api/mer，由 Nginx 转发到后端
VITE_MER_API_BASE_URL=/api/mer

# Token 存储键名
# 获取方式：默认即可，无需修改
VITE_TOKEN_KEY=mer_token
```

**第二步：启动服务**

```bash
# 1. 放置 SSL 证书（仅生产环境）
# 将证书文件放置到 docker/nginx/ssl/ 目录

# 2. 启动所有服务（数据库迁移自动运行）
cd docker
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志（可选）
docker-compose logs -f backend

# 等待约 30-60 秒，服务即可正常使用
```

### 7.3 启动流程说明

```
docker-compose up -d
        │
        ▼
┌───────────────────┐
│   MySQL 启动       │
│   (健康检查)       │
└─────────┬─────────┘
          │
          ▼ (MySQL 健康)
┌───────────────────┐
│   后端容器启动     │
│   执行启动脚本     │
└─────────┬─────────┘
          │
          ▼ (等待 MySQL 就绪)
┌───────────────────┐
│ alembic upgrade   │ ← 自动创建/更新表结构
│    head           │
└─────────┬─────────┘
          │
          ▼ (迁移完成)
┌───────────────────┐
│  FastAPI 启动     │
│   :8001           │
└───────────────────┘
```

**注意**: 数据库迁移由后端启动脚本自动执行，无需手动运行 `alembic upgrade head`。

### 7.3 常用命令

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose stop

# 重启所有服务
docker-compose restart

# 停止并删除所有服务
docker-compose down

# 停止并删除所有服务及数据卷
docker-compose down -v

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec backend bash
docker-compose exec mysql bash

# 重新构建服务
docker-compose build [service_name]
docker-compose up -d --build [service_name]

# 查看资源使用情况
docker stats
```

---

## 八、健康检查与监控

### 8.1 服务健康检查

```bash
# 检查后端健康状态
curl http://localhost:8001/health

# 检查 MySQL 连接
docker-compose exec mysql mysqladmin ping -h localhost

# 检查 Nginx 状态
docker-compose exec nginx nginx -t
```

### 8.2 日志查看

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs mysql
docker-compose logs nginx

# 实时查看日志
docker-compose logs -f --tail=100 backend
```

---

## 九、数据备份与恢复

### 9.1 数据备份

```bash
# MySQL 数据备份
docker-compose exec mysql mysqldump -u root -p xiaoyaopeipei > backup.sql

# 使用 Docker 卷备份
docker run --rm -v xiaoyaopeipei_mysql_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/mysql_backup.tar.gz -C /data .
```

### 9.2 数据恢复

```bash
# MySQL 数据恢复
docker-compose exec -T mysql mysql -u root -p xiaoyaopeipei < backup.sql

# 恢复 Docker 卷
docker run --rm -v xiaoyaopeipei_mysql_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/mysql_backup.tar.gz -C /data
```

---

## 十、常见问题

### 10.1 端口冲突

如果端口被占用，修改 `docker/.env` 中的端口配置：

```bash
# 修改对应端口
NGINX_HTTP_PORT=8080
BACKEND_PORT=8002
```

### 10.2 容器无法启动

```bash
# 查看详细日志
docker-compose logs [service_name]

# 检查容器状态
docker-compose ps -a
```

### 10.3 数据库连接失败

1. 检查 MySQL 容器是否正常运行
2. 检查环境变量 `DATABASE_URL` 配置
3. 确认网络连接正常

```bash
# 测试数据库连接
docker-compose exec backend python -c "
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://xiaoyaopeipei:password@mysql:3306/xiaoyaopeipei')
conn = engine.connect()
print('Connection successful!')
"
```

### 10.4 前端页面空白

1. 检查构建是否成功
2. 查看浏览器控制台错误
3. 检查 Nginx 配置

```bash
# 重新构建前端
docker-compose build user-frontend
docker-compose up -d user-frontend
```

### 10.5 SSL 证书问题

```bash
# 检查证书文件是否存在
ls -la docker/nginx/ssl/

# 检查证书有效期
openssl x509 -in docker/nginx/ssl/peipei.xiaoyaos.com.crt -noout -dates

# 测试 Nginx 配置
docker-compose exec nginx nginx -t
```

---

## 十一、生产环境优化建议

### 11.1 资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 11.2 日志轮转

配置日志驱动避免日志文件过大：

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 11.3 安全加固

1. 使用非 root 用户运行容器
2. 定期更新镜像
3. 启用 TLS 1.3
4. 配置防火墙规则
5. 使用 secrets 管理敏感信息

---

## 十二、版本更新

### 12.1 滚动更新

```bash
# 拉取最新代码
git pull

# 重新构建并启动（数据库迁移自动运行）
docker-compose build
docker-compose up -d

# 查看日志确认迁移成功
docker-compose logs -f backend
```

### 12.2 回滚操作

```bash
# 回滚到上一个版本
git checkout <previous_commit>
docker-compose build
docker-compose up -d
```

---

## 附录

### A. 端口映射表

| 服务 | 容器端口 | 宿主机端口 | 说明 |
|------|---------|-----------|------|
| Nginx | 80 | 80 | HTTP |
| Nginx | 443 | 443 | HTTPS |
| Backend | 8001 | 8001 | 后端 API |
| User Frontend | 80 | 3000 | C端前端 |
| Mer Frontend | 80 | 3001 | B端前端 |
| MySQL | 3306 | 3306 | 数据库 |

### B. 目录挂载说明

| 服务 | 宿主机路径 | 容器路径 | 说明 |
|------|-----------|---------|------|
| MySQL | mysql_data (volume) | /var/lib/mysql | 数据持久化 |
| Nginx | ./nginx/nginx.conf | /etc/nginx/nginx.conf | 主配置 |
| Nginx | ./nginx/conf.d | /etc/nginx/conf.d | 站点配置 |
| Nginx | ./nginx/ssl | /etc/nginx/ssl | SSL 证书 |
| Nginx | ./nginx/logs | /var/log/nginx | 日志文件 |

### C. 相关文档链接

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [Nginx 官方文档](https://nginx.org/en/docs/)

---

**文档版本**: v1.0
**最后更新**: 2026-02-26
**维护者**: 小遥配配开发团队
