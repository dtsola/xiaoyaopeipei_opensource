#!/bin/bash
# 部署脚本

echo "========================================="
echo "小遥配配 - 后端部署脚本"
echo "========================================="

# 1. 拉取最新代码
echo "1. 拉取最新代码..."
git pull origin main

# 2. 激活虚拟环境
echo "2. 激活虚拟环境..."
source venv/bin/activate

# 3. 安装依赖
echo "3. 安装依赖..."
pip install -r requirements.txt

# 4. 复制环境变量
echo "4. 配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "请编辑 .env 文件配置环境变量"
    exit 1
fi

# 5. 运行数据库迁移
echo "5. 运行数据库迁移..."
alembic upgrade head

# 6. 重启服务
echo "6. 重启服务..."
sudo supervisorctl restart xiaoyaopeipei

echo "========================================="
echo "部署完成！"
echo "========================================="
