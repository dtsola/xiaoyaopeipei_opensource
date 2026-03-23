# 小遥配配 - 后端项目

AI对话式电脑导购助手后端服务

## 技术栈

- **Web框架**: FastAPI 0.109
- **ASGI服务器**: Uvicorn
- **Python版本**: 3.10
- **ORM框架**: SQLAlchemy 2.0 + Alembic
- **数据验证**: Pydantic 2.x
- **日志管理**: Loguru 0.7
- **认证方式**: JWT Token
- **AI框架**: LangChain 0.1
- **大模型**: 阿里云通义千问

## 快速开始

### 1. 创建虚拟环境

```bash
python3.10 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填写真实配置
```

### 4. 数据库迁移

```bash
alembic upgrade head
```

### 5. 启动服务

```bash
uvicorn app.main:app --reload --port 8001
```

访问：http://localhost:8001
API文档：http://localhost:8001/docs

## 项目结构

```
xiaoyaopeipei-user-merchant-backend/
├── app/                    # 应用主目录
│   ├── api/               # API路由层
│   ├── core/              # 核心配置
│   ├── db/                # 数据库
│   ├── models/            # 数据模型
│   ├── schemas/           # 数据验证模型
│   ├── services/          # 业务逻辑层
│   ├── utils/             # 工具函数
│   ├── middleware/        # 中间件
│   └── main.py            # 应用入口
├── alembic/               # 数据库迁移
├── tests/                 # 测试
├── logs/                  # 日志目录
├── scripts/               # 脚本
├── .env                   # 环境变量
├── .env.example           # 环境变量示例
├── requirements.txt       # 依赖配置
└── README.md              # 项目说明
```

## 开发指南

### 代码格式化

```bash
# 代码格式化
black app/

# import排序
isort app/

# 代码检查
flake8 app/
```

### 运行测试

```bash
pytest

# 查看覆盖率
pytest --cov=app --cov-report=html
```

## API文档

启动服务后访问 http://localhost:8001/docs 查看完整API文档
