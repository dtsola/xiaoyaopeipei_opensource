# 小遥配配 - 项目开发规范

> 这是项目的基础文档，每次AI会话都会自动加载，用于指导AI助手进行开发工作。

---

## 项目概述

**项目名称**：小遥配配 - AI对话式电脑导购助手

**项目简介**：为电脑店老板提供智能客户需求收集和配置推荐服务的SaaS平台，通过AI对话方式收集客户需求，智能推荐合适的电脑配置方案。

**核心用户**：
- **B端（商家端）**：电脑店老板，管理配置、查看客户线索
- **C端（客户端）**：购买电脑的客户，通过AI对话获取推荐

---

## 一、个人偏好与工作规范

### 1.1 语言规范
- **AI回复**：必须使用中文回答
- **文档编写**：必须使用中文编写
- **代码注释**：必须使用中文注释

### 1.2 自我检查规范
每次完成一个功能后，必须自行检查一遍是否真正完成了需求：
- 功能是否正常运行
- 是否符合产品需求文档
- 是否有明显的bug或问题
- 代码质量是否符合规范

---

## 二、技术选型

### 2.1 前端技术栈
- **核心框架**：Vue 3.4 + Composition API + TypeScript
- **构建工具**：Vite 5
- **UI组件库**：Ant Design Vue 4.x
- **状态管理**：Pinia 2.x
- **路由管理**：Vue Router 4.x
- **HTTP客户端**：Axios
- **图表库**（B端）：ECharts 5

### 2.2 后端技术栈
- **Web框架**：FastAPI 0.109
- **ASGI服务器**：Uvicorn + Supervisor
- **Python版本**：3.10
- **ORM框架**：SQLAlchemy 2.0 + Alembic
- **数据验证**：Pydantic 2.x
- **日志管理**：Loguru 0.7
- **认证方式**：JWT Token（有效期7天）

### 2.3 AI技术栈
- **智能体框架**：LangChain 0.1
- **大语言模型**：阿里云通义千问 (qwen-plus)

### 2.4 存储技术栈
- **数据库**：MySQL 8.0（ECS本地部署）
  - 主键策略：雪花算法（BIGINT 20位）
  - 外键策略：软外键（应用层控制）
- **文件存储**：阿里云OSS + CDN加速
- **缓存方案**：cachetools（本地内存缓存）

### 2.5 部署架构
- **云服务器**：阿里云ECS 2核4G
- **Web服务器**：Nginx
- **进程管理**：Supervisor

---

## 三、代码规范

### 3.1 前端代码规范

#### 目录结构
```
src/
├── api/           # API接口层
├── components/    # 公共组件（PascalCase命名）
├── views/         # 页面组件（PascalCase命名）
├── stores/        # Pinia状态管理
├── router/        # 路由配置
├── utils/         # 工具函数
├── composables/   # 组合式函数（use开头）
├── types/         # TypeScript类型定义
└── constants/     # 常量定义
```

#### 命名规范
- **组件文件**：PascalCase（如 `ChatPage.vue`）
- **工具函数**：camelCase（如 `formatPrice()`）
- **常量**：UPPER_SNAKE_CASE（如 `API_BASE_URL`）
- **组合式函数**：use开头（如 `useChat.ts`）

### 3.2 后端代码规范

#### 目录结构
```
app/
├── api/            # API路由层（user/mer分目录）
├── core/           # 核心配置
├── models/         # SQLAlchemy ORM模型
├── schemas/        # Pydantic数据验证模型
├── services/       # 业务逻辑层
├── utils/          # 工具函数
└── middleware/     # 中间件
```

#### 命名规范
- **模块/包**：snake_case（如 `chat_service.py`）
- **类名**：PascalCase（如 `AIService`）
- **函数/方法**：snake_case（如 `get_message_list()`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_RETRY_COUNT`）

### 3.3 API接口规范

#### 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1703232000000,
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 接口命名
- **C端接口**：`/api/user/*`
- **B端接口**：`/api/mer/*`

---

## 四、Git规范

### 4.1 分支策略
- `main`：生产环境分支
- `develop`：开发环境分支
- `feature/*`：功能分支
- `bugfix/*`：bug修复分支

### 4.2 提交信息格式
```
<type>(<scope>): <subject>

type: feat | fix | docs | style | refactor | test | chore
```

### 4.3 提交前检查
```bash
# 前端
npm run lint && npm run format

# 后端
black app/ && isort app/ && flake8 app/ && pytest
```

---

## 五、测试与部署

### 5.1 测试规范
- **单元测试**：测试单个函数/类
- **集成测试**：测试API接口
- **E2E测试**：端到端用户流程测试

### 5.2 部署流程
1. 拉取最新代码
2. 安装依赖
3. 运行数据库迁移
4. 构建前端资源
5. 重启后端服务

### 5.3 数据库备份
- **备份频率**：每日凌晨3点
- **备份保留**：最近7天
- **备份存储**：阿里云OSS

---

## 六、文档引用

### 产品文档
- [项目提示词](docs/项目提示词.md) - AI助手的快捷任务提示词列表
- [MRD文档](docs/00-mrd.md) - 精益市场需求文档
- [PRD文档](docs/01-prd.md) - 产品需求文档
- [C端原型](docs/02-C端（客户端）原型.md) - 客户端产品原型设计
- [B端原型](docs/02-B端（商家后台）原型.md) - 商家后台产品原型设计

### 技术文档
- [技术选型](docs/技术选型.md) - 技术栈选型说明与对比
- [技术方案](docs/03-技术方案.md) - 技术架构设计方案
- [代码架构](docs/代码架构.md) - 完整项目代码结构说明
- [接口文档](docs/接口文档.md) - RESTful API接口设计文档
- [数据库文档](docs/数据库文档.md) - 数据库设计文档
- [部署文档](docs/部署文档.md) - 生产环境部署指南

### 管理文档
- [开发任务清单](docs/04-开发任务清单.md) - 功能开发任务分解
- [开发排期](docs/05-开发排期.md) - 开发时间规划
- [开发进度](docs/开发进度.md) - 当前开发进度跟踪

### 其他文档
- [测试文档](docs/测试文档/) - 完整测试规范
- [提示词设计](docs/提示词设计.md) - AI提示词设计方案
- [商品推荐逻辑](docs/商品推荐逻辑.md) - 商品推荐算法说明
- [数据统计文档](docs/数据统计文档.md) - 数据统计指标说明

### Base文件夹（基础模板文档）
- [精益开发流程](docs/base/精益开发流程.md) - 精益开发流程说明
- [初始需求](docs/base/初始需求.md) - 项目初始需求文档
- [00-精益MRD-模版](docs/base/00-精益MRD-模版.md) - 市场需求文档模板
- [01-精简PRD-模版](docs/base/01-精简PRD-模版.md) - 产品需求文档模板
- [02-精简原型-标准](docs/base/02-精简原型-标准.md) - 原型设计标准模板
- [03-技术方案文档-模版](docs/base/03-技术方案文档-模版.md) - 技术方案文档模板
- [04-开发任务清单-模版](docs/base/04-开发任务清单-模版.md) - 开发任务清单模板
- [05-开发排期-模版](docs/base/05-开发排期-模版.md) - 开发排期模板
- [06-技术选型-模版](docs/base/06-技术选型-模版.md) - 技术选型文档模板
- [07-代码架构-模版](docs/base/07-代码架构-模版.md) - 代码架构文档模板
- [08-数据库文档-模版](docs/base/08-数据库文档-模版.md) - 数据库设计文档模板
- [09-接口文档-模版](docs/base/09-接口文档-模版.md) - 接口文档模板
- [10-部署文档-模版](docs/base/10-部署文档-模版.md) - 部署文档模板
- [11-架构决策-模版](docs/base/11-架构决策-模版.md) - 架构决策记录模板
- [12-测试文档-模版](docs/base/12-测试文档-模版.md) - 测试文档模板

### 高保真原型文件夹
- [C端原型](docs/高保真原型/C端原型/) - 客户端高保真原型（v0.1版本）
- [B端原型](docs/高保真原型/B端原型/) - 商家后台高保真原型（v0.1版本）

### 架构决策
- [B端视觉设计](docs/架构决策/AD-20251223-001-B端视觉设计方案选择.md) - B端界面设计决策记录
- [C端视觉设计](docs/架构决策/AD-20251223-002-C端视觉设计选型.md) - C端界面设计决策记录

---

## 七、快速开发指南

### 后端启动
```bash
cd xiaoyaopeipei-user-merchant-backend
python3.10 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

### 前端启动（C端）
```bash
cd xiaoyaopeipei-user-frontend
pnpm install && pnpm dev
```

### 前端启动（B端）
```bash
cd xiaoyaopeipei-mer-frontend
pnpm install && pnpm dev
```

---

## 八、当前开发状态

### 已完成工作（截至 2026-02-25）

| 项目 | 进度 |
|------|------|
| **后端项目** | 100% 完成 |
| **C端前端** | 100% 完成 |
| **B端前端** | 100% 完成 |
| **数据库** | 100% 完成 |

### 下一步任务
- 生产环境部署（ECS、Nginx、域名、SSL）
- 生产环境验证测试
- 上线监控与运维

---

**文档版本**：v2.1（简化版）
**最后更新**：2026-02-25
**项目状态**：开发完成（100%），待部署上线
