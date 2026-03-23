#!/bin/bash
# ==================== 小遥配配 - 后端服务启动脚本 ====================
set -e

echo ""
echo "=========================================="
echo "  小遥配配 - 后端服务启动脚本"
echo "=========================================="
echo ""

# 检查必需的环境变量
check_env_vars() {
    local required_vars=(
        "DATABASE_URL"
        "JWT_SECRET"
        "QWEN_API_KEY"
    )
    local missing_vars=()

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "错误: 以下必需的环境变量未设置:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        exit 1
    fi
}

# 等待 MySQL 数据库就绪
wait_for_mysql() {
    echo "正在等待 MySQL 数据库就绪..."

    # 从 DATABASE_URL 中提取连接信息
    local db_host=$(echo $DATABASE_URL | grep -oP '@\K[^:]+' || echo "mysql")
    local db_user=$(echo $DATABASE_URL | grep -oP '://\K[^:]+' || echo "root")
    local db_pass=$(echo $DATABASE_URL | grep -oP ':[^:@]*@' | tr -d ':@' || echo "")
    local db_name=$(echo $DATABASE_URL | grep -oP '/[^?]+' | tr -d '/' || echo "xiaoyaopeipei")

    local max_retries=30
    local retry_count=0

    while [ $retry_count -lt $max_retries ]; do
        if python -c "
import pymysql
import sys
try:
    conn = pymysql.connect(
        host='$db_host',
        user='$db_user',
        password='$db_pass',
        database='$db_name',
        connect_timeout=5
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; then
            echo "✓ MySQL 数据库已就绪!"
            return 0
        fi

        retry_count=$((retry_count + 1))
        echo "  等待中... ($retry_count/$max_retries)"
        sleep 2
    done

    echo "错误: 无法连接到 MySQL 数据库"
    exit 1
}

# 运行数据库迁移
run_migrations() {
    echo ""
    echo "正在运行数据库迁移..."
    if alembic upgrade head; then
        echo "✓ 数据库迁移完成!"
    else
        echo "错误: 数据库迁移失败"
        exit 1
    fi
}

# 启动应用服务
start_application() {
    echo ""
    echo "正在启动后端服务..."
    echo "=========================================="
    echo ""
    exec uvicorn app.main:app --host 0.0.0.0 --port 8001
}

# 主流程
main() {
    check_env_vars
    wait_for_mysql
    run_migrations
    start_application
}

# 执行主流程
main
