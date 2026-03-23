# ==================== 小遥配配 - C端前端 Dockerfile ====================
# 多阶段构建：构建阶段 + 生产阶段

# ==================== 构建阶段 ====================
FROM node:18-alpine AS builder

# 设置工作目录
WORKDIR /app

# 声明构建参数（环境变量）
ARG VITE_API_BASE_URL=/api/user
ARG VITE_MER_BACKEND_URL=https://peipei-mer.xiaoyaos.com
ARG VITE_OSS_DOMAIN=https://file.xiaoyaosai.com
ARG VITE_APP_TITLE=小遥配配 - AI电脑导购
ARG VITE_REQUEST_TIMEOUT=30000
ARG VITE_USE_MOCK=false
ARG VITE_DEBUG=false
ARG VITE_SESSION_KEY=user_session
ARG VITE_MAX_RECOMMEND_COUNT=5

# 将 ARG 转为 ENV（构建时可用）
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_MER_BACKEND_URL=${VITE_MER_BACKEND_URL}
ENV VITE_OSS_DOMAIN=${VITE_OSS_DOMAIN}
ENV VITE_APP_TITLE=${VITE_APP_TITLE}
ENV VITE_REQUEST_TIMEOUT=${VITE_REQUEST_TIMEOUT}
ENV VITE_USE_MOCK=${VITE_USE_MOCK}
ENV VITE_DEBUG=${VITE_DEBUG}
ENV VITE_SESSION_KEY=${VITE_SESSION_KEY}
ENV VITE_MAX_RECOMMEND_COUNT=${VITE_MAX_RECOMMEND_COUNT}

# 配置 npm 使用阿里云源（加速国内构建）
RUN npm config set registry https://mirrors.aliyun.com/npm/

# 复制 package 文件
COPY package.json package-lock.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 构建生产版本（跳过类型检查，vue-tsc 与 Node 18 存在兼容性问题）
RUN npx vite build --mode production

# ==================== 生产阶段 ====================
FROM nginx:alpine

# 添加 nginx 服务名解析
RUN echo "resolver 127.0.0.11 valid=30s;" > /etc/nginx/conf.d/resolver.conf

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制自定义 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
