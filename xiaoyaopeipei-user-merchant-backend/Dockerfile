# ==================== 小遥配配 - 后端 Dockerfile ====================
# 基于 Python 3.10 官方镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 替换为阿里云 apt 源（加速国内构建）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 配置 pip 使用阿里云源（加速国内构建）
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8001

# 启动脚本：等待 MySQL -> 运行迁移 -> 启动服务
CMD ["sh", "-c", "\
    echo '等待 MySQL 数据库就绪...'; \
    sleep 10; \
    echo '运行数据库迁移...'; \
    alembic upgrade head && \
    echo '✓ 数据库迁移完成!' && \
    echo '启动后端服务...' && \
    exec uvicorn app.main:app --host 0.0.0.0 --port 8001 \
"]
