# 国学大师微信小程序生产级高性能全栈开发方案

## 1. 简介

"国学大师"是一款基于AI对话的微信小程序，采用响应式设计，支持跨端运行。该应用结合了传统文化与现代AI技术，为用户提供国学知识问答、智能对话等服务。通过RAG知识库检索技术，能够精准回答用户关于国学的各种问题，并支持流式记忆对话，提供更加自然的交互体验。

本方案遵循生产级开发标准，确保系统具备高可用性、可扩展性和安全性，能够支持中等规模用户并发访问。系统采用微服务架构设计，前后端分离，便于后期维护和功能扩展。

## 2. 功能

### 核心功能
- **AI对话**：支持流式记忆对话，提供沉浸式交互体验
- **RAG知识库检索**：基于向量数据库的精准国学知识检索
- **聊天记录管理**：会话历史记录的查看、删除和管理
- **用户认证系统**：
  - 微信一键登录
  - 邮箱注册/登录
  - JWT Token认证机制
- **计费系统**：基于Token使用的计费模式
- **用户体验**：新用户注册赠送10元体验金

### 页面功能
#### AI对话页面（Tabbar）
- 消息展示区：支持头像显示、消息气泡、时间戳、markdown渲染
- 输入控制区：新建会话、清空记录操作按钮
- 实时对话：流式消息显示，模拟真实对话体验

#### 个人中心页面（Tabbar）
- 用户信息区：头像、昵称展示与编辑功能
- 账户管理：余额显示与充值功能
- 数据统计：使用统计与聊天记录管理
- 系统设置：关于我们、退出登录等功能

## 3. 技术栈

### 前端技术栈
- **框架**：uni-app + Vue3
- **UI库**：uni-ui（uni-app官方组件库）
- **状态管理**：Pinia（Vue3官方状态管理）
- **网络请求**：uni.request（uni-app内置）
- **数据缓存**：uni.setStorage（uni-app内置）
- **开发工具**：HBuilder X、微信开发者工具

### 后端技术栈
- **主框架**：FastAPI（高性能Python Web框架）
- **认证机制**：JWT（JSON Web Token）+ OAuth2
- **API文档**：Swagger UI + ReDoc
- **AI框架**：Langchain + DeepSeek API
- **记忆模块**：ConversationBufferWindowMemory + Redis
- **RAG引擎**：Chroma向量数据库
- **消息队列**：Celery + Redis
- **数据库**：PostgreSQL（主数据存储）+ Redis（缓存与会话存储）
- **对象存储**：MinIO（用于存储用户上传的文件）
- **日志管理**：ELK Stack（Elasticsearch, Logstash, Kibana）
- **监控运维**：Prometheus + Grafana + AlertManager
- **服务网格**：Nginx（反向代理和负载均衡）
- **部署环境**：Docker + Docker Compose + Docker Swarm

### 开发环境
- Node.js 18.x（前端构建）
- Python 3.11（后端服务）
- Docker 24.x（容器化部署）
- Git（版本控制）

## 4. 性能优化

### 前端优化
1. **组件懒加载**：按需加载页面组件，减少初始包体积
2. **图片资源优化**：
   - 使用WebP格式图片
   - 实施图片懒加载策略
   - CDN加速静态资源
3. **网络请求优化**：
   - 请求缓存机制
   - 接口数据压缩
   - 失败重试机制
   - HTTP/2支持
4. **UI渲染优化**：
   - 虚拟滚动列表（长列表优化）
   - 防抖节流处理
   - 条件渲染优化
   - 骨架屏加载
5. **小程序性能优化**：
   - 分包加载策略
   - 预加载下一页数据
   - 合理使用页面生命周期

### 后端优化
1. **数据库优化**：
   - 索引优化策略
   - 查询缓存机制
   - 连接池配置
   - 读写分离
   - 数据库分表分库（用户量增长后）
2. **缓存策略**：
   - Redis多级缓存
   - 热点数据预加载
   - 缓存失效机制
   - 缓存穿透、击穿、雪崩防护
3. **API优化**：
   - 接口限流控制
   - 响应数据压缩
   - 异步任务处理
   - CDN加速静态资源
   - 负载均衡
4. **AI服务优化**：
   - 流式响应处理
   - 对话上下文压缩
   - 向量检索优化
   - 模型缓存
   - 并行处理多个请求

## 5. 页面设计

### 设计理念
采用苹果设计师标准的极简风格设计，界面简洁、操作直观，注重用户体验。

### 主要页面设计

#### 首页（AI对话页）
- 中部：消息展示区域（支持滚动）
  - 用户消息（右侧气泡）
  - AI回复（左侧气泡）
  - 时间戳分隔符
- 底部：输入控制区域
  - 左侧：操作按钮（新建会话、清空记录）
  - 中间：输入框
  - 右侧：发送按钮

#### 个人中心页
- 顶部：用户信息展示区
  - 圆形头像
  - 用户昵称与编辑按钮
  - 账户余额与充值入口
- 中部：功能菜单区
  - 聊天记录管理
  - 使用统计
  - 关于我们
- 底部：退出登录按钮

### 设计规范
- 字体：系统默认字体，标题16px，正文14px，辅助信息12px
- 颜色：主色调采用中国风色彩（朱红、墨黑、米白）
- 间距：统一8px基数，符合移动端操作习惯
- 动效：微交互动效，提升用户体验

## 6. 整体框架设计

### 前端架构
```
┌─────────────────────────────────────────────┐
│              View Layer (UI)                │
├─────────────────────────────────────────────┤
│           Business Components               │
├─────────────────────────────────────────────┤
│         Common Components/Library           │
├─────────────────────────────────────────────┤
│           State Management (Pinia)          │
├─────────────────────────────────────────────┤
│           Network Layer (API)               │
├─────────────────────────────────────────────┤
│           Utils & Configuration             │
└─────────────────────────────────────────────┘
```

### 后端架构
```
┌─────────────────────────────────────────────┐
│            API Gateway/Load Balancer        │
├─────────────────────────────────────────────┤
│         FastAPI Application Layer           │
│  ┌─────────────┬─────────────┬────────────┐ │
│  │   Routers   │ Controllers │ Validators │ │
│  └─────────────┴─────────────┴────────────┘ │
├─────────────────────────────────────────────┤
│         Business Logic Layer                │
│  ┌────────────────────────────────────────┐ │
│  │  AI Service  │  User Service  │  ...   │ │
│  └────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│         Data Access Layer                   │
│  ┌────────────────────────────────────────┐ │
│  │ PostgreSQL │  Redis  │ Chroma │ Celery │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### 数据流向
1. 用户操作 → 前端UI组件
2. UI组件 → Pinia状态管理
3. 状态管理 → API网络层
4. API请求 → 后端FastAPI路由
5. 路由分发 → 业务逻辑处理
6. 业务逻辑 → 数据访问层（数据库/缓存/AI服务）
7. 数据返回 → 前端更新UI

### 安全性设计
1. **认证授权**：
   - JWT Token认证
   - OAuth2授权机制
   - 微信登录安全验证
   - 邮箱验证码登录
2. **数据安全**：
   - HTTPS加密传输
   - 敏感信息加密存储
   - SQL注入防护
   - XSS攻击防护
3. **API安全**：
   - 接口签名验证
   - 请求频率限制
   - 参数校验
   - 访问日志记录

## 7. 目录结构

```
GX3/
├── frontend/                    # 前端代码
│   ├── components/              # 公共组件
│   │   ├── chat/                # 聊天相关组件
│   │   ├── user/                # 用户相关组件
│   │   └── common/              # 通用组件
│   ├── pages/                   # 页面文件
│   │   ├── chat/                # 聊天页面
│   │   ├── user/                # 用户中心页面
│   │   └── about/               # 关于我们页面
│   ├── store/                   # 状态管理
│   │   ├── user.js              # 用户状态
│   │   ├── chat.js              # 聊天状态
│   │   └── index.js             # 状态入口
│   ├── utils/                   # 工具函数
│   ├── static/                  # 静态资源
│   ├── App.vue                  # 根组件
│   ├── main.js                  # 入口文件
│   ├── pages.json               # 页面配置
│   └── manifest.json            # 应用配置
├── backend/                     # 后端代码
│   ├── app/                     # 主应用
│   │   ├── api/                 # API路由
│   │   ├── models/              # 数据模型
│   │   ├── schemas/             # 数据验证
│   │   ├── services/            # 业务逻辑
│   │   ├── utils/               # 工具函数
│   │   ├── middleware/          # 中间件
│   │   ├── exceptions/          # 异常处理
│   │   └── main.py              # 应用入口
│   ├── ai/                      # AI相关模块
│   │   ├── rag/                 # RAG引擎
│   │   ├── memory/              # 记忆模块
│   │   └── providers/           # AI提供商
│   ├── tasks/                   # 异步任务
│   ├── tests/                   # 测试文件
│   ├── migrations/              # 数据库迁移文件
│   ├── requirements.txt         # Python依赖
│   └── Dockerfile               # 后端Docker配置
├── docs/                        # 文档
│   ├── api/                     # API文档
│   └── deployment/              # 部署文档
├── scripts/                     # 脚本文件
├── docker-compose.yml           # Docker编排
├── docker-compose.prod.yml      # 生产环境Docker编排
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件
└── README.md                    # 项目说明
```

## 7.5 SQL数据库表设计

### 用户表 (users)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    openid VARCHAR(255) UNIQUE,  -- 微信openid
    email VARCHAR(255) UNIQUE,   -- 邮箱
    nickname VARCHAR(100),       -- 昵称
    avatar_url TEXT,             -- 头像URL
    tokens INTEGER DEFAULT 1000, -- token余额（新用户赠送10元体验金，按比例转换）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 会话表 (sessions)
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),          -- 会话标题
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 消息表 (messages)
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE,
    content TEXT,                -- 消息内容
    role VARCHAR(20),            -- 消息角色（user/assistant）
    tokens INTEGER,              -- 消息消耗的token数量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 用户登录记录表 (login_logs)
```sql
CREATE TABLE login_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    login_method VARCHAR(20),    -- 登录方式（wechat/email）
    ip_address VARCHAR(50),      -- 登录IP
    user_agent TEXT,             -- 用户代理
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 计费记录表 (billing_records)
```sql
CREATE TABLE billing_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    change_amount INTEGER,       -- 变动数量（正数为充值，负数为消费）
    balance_after INTEGER,       -- 变动后余额
    description TEXT,            -- 变动说明
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 数据库索引优化建议
```sql
-- 用户表索引
CREATE INDEX idx_users_openid ON users(openid);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- 会话表索引
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);

-- 消息表索引
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_role ON messages(role);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- 登录记录表索引
CREATE INDEX idx_login_logs_user_id ON login_logs(user_id);
CREATE INDEX idx_login_logs_created_at ON login_logs(created_at);

-- 计费记录表索引
CREATE INDEX idx_billing_records_user_id ON billing_records(user_id);
CREATE INDEX idx_billing_records_created_at ON billing_records(created_at);
```

## 8. 功能模块实现

### 前端功能模块

#### 1. 聊天对话模块
```javascript
// 聊天状态管理 (store/chat.js)
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    sessions: [], // 会话列表
    currentSession: null, // 当前会话
    messages: [], // 消息列表
    isLoading: false, // 加载状态
    error: null // 错误信息
  }),
  
  actions: {
    // 创建新会话
    async createSession() {
      try {
        // 实现创建会话逻辑
        const response = await api.post('/sessions')
        this.sessions.push(response.data)
        this.currentSession = response.data
      } catch (error) {
        this.error = error.message
        throw error
      }
    },
    
    // 发送消息
    async sendMessage(content) {
      try {
        this.isLoading = true
        // 实现发送消息逻辑
        const response = await api.post(`/sessions/${this.currentSession.id}/messages`, { content })
        this.messages.push(response.data)
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    // 获取历史记录
    async fetchHistory(sessionId) {
      try {
        // 实现获取历史记录逻辑
        const response = await api.get(`/sessions/${sessionId}/messages`)
        this.messages = response.data
      } catch (error) {
        this.error = error.message
        throw error
      }
    }
  }
})
```

#### 2. 用户认证模块
```javascript
// 用户状态管理 (store/user.js)
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null, // 用户信息
    token: '', // JWT token
    isLoggedIn: false, // 登录状态
    error: null // 错误信息
  }),
  
  actions: {
    // 微信登录
    async loginWithWechat() {
      try {
        // 实现微信登录逻辑
        const response = await api.post('/auth/wechat-login')
        this.token = response.data.token
        this.userInfo = response.data.user
        this.isLoggedIn = true
        // 保存token到本地存储
        uni.setStorageSync('token', this.token)
      } catch (error) {
        this.error = error.message
        throw error
      }
    },
    
    // 邮箱登录
    async loginWithEmail(credentials) {
      try {
        // 实现邮箱登录逻辑
        const response = await api.post('/auth/email-login', credentials)
        this.token = response.data.token
        this.userInfo = response.data.user
        this.isLoggedIn = true
        // 保存token到本地存储
        uni.setStorageSync('token', this.token)
      } catch (error) {
        this.error = error.message
        throw error
      }
    },
    
    // 退出登录
    logout() {
      // 实现退出登录逻辑
      this.token = ''
      this.userInfo = null
      this.isLoggedIn = false
      // 清除本地存储的token
      uni.removeStorageSync('token')
    },
    
    // 检查登录状态
    checkAuthStatus() {
      const token = uni.getStorageSync('token')
      if (token) {
        this.token = token
        this.isLoggedIn = true
        // 验证token有效性
        this.verifyToken()
      }
    },
    
    // 验证token
    async verifyToken() {
      try {
        const response = await api.get('/auth/verify')
        this.userInfo = response.data.user
      } catch (error) {
        // token无效，清除登录状态
        this.logout()
      }
    }
  }
})
```

### 后端功能模块

#### 1. AI对话服务
```python
# backend/ai/chat_service.py
from langchain.chat_models import ChatDeepSeek
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import logging

class ChatService:
    def __init__(self, api_key: str):
        self.chat_model = ChatDeepSeek(api_key=api_key)
        self.memory = ConversationBufferWindowMemory(k=5)
        self.chain = ConversationalRetrievalChain(
            retriever=self.get_retriever(),
            memory=self.memory
        )
        self.logger = logging.getLogger(__name__)
    
    def get_retriever(self):
        # 实现向量数据库检索器
        pass
    
    async def chat(self, message: str, session_id: str, user_id: int):
        try:
            # 实现聊天逻辑
            response = self.chain.run(message)
            # 记录日志
            self.logger.info(f"User {user_id} sent message in session {session_id}")
            return response
        except Exception as e:
            self.logger.error(f"Error in chat service: {str(e)}")
            raise
    
    def format_prompt(self, message: str) -> str:
        """格式化提示词，增加安全检查"""
        # 移除潜在的恶意内容
        safe_message = self.sanitize_input(message)
        return safe_message
    
    def sanitize_input(self, message: str) -> str:
        """清理输入，防止注入攻击"""
        # 实现输入清理逻辑
        return message.strip()
```

#### 2. 用户认证服务
```python
# backend/app/services/auth_service.py
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
import logging

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.logger = logging.getLogger(__name__)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希值"""
        return pwd_context.hash(password)
    
    def create_token(self, user_id: int, expires_delta: timedelta = None):
        """创建JWT token"""
        try:
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
            payload = {
                "user_id": user_id,
                "exp": expire,
                "iat": datetime.utcnow()
            }
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            self.logger.info(f"Created token for user {user_id}")
            return token
        except Exception as e:
            self.logger.error(f"Error creating token: {str(e)}")
            raise
    
    def verify_token(self, token: str):
        """验证JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            self.logger.warning(f"Invalid token: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            self.logger.error(f"Error verifying token: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        """获取当前用户"""
        payload = self.verify_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
```

#### 3. 计费服务
```python
# backend/app/services/billing_service.py
from fastapi import HTTPException
import logging

class BillingService:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def calculate_tokens(self, message: str, response: str):
        """计算消息使用的token数量"""
        try:
            # 更精确的token计算方法
            input_tokens = len(message) // 4
            output_tokens = len(response) // 4
            total_tokens = input_tokens + output_tokens
            self.logger.info(f"Calculated tokens: input={input_tokens}, output={output_tokens}, total={total_tokens}")
            return total_tokens
        except Exception as e:
            self.logger.error(f"Error calculating tokens: {str(e)}")
            raise
    
    def deduct_tokens(self, user_id: int, tokens: int):
        """扣除用户token"""
        try:
            user = self.db.get_user(user_id)
            if user.tokens < tokens:
                self.logger.warning(f"User {user_id} has insufficient tokens: {user.tokens} < {tokens}")
                raise HTTPException(status_code=400, detail="Insufficient tokens")
            
            user.tokens -= tokens
            self.db.update_user(user)
            
            # 记录计费日志
            self.db.create_billing_record(user_id, -tokens, user.tokens, f"Used {tokens} tokens for AI service")
            self.logger.info(f"Deducted {tokens} tokens from user {user_id}, balance: {user.tokens}")
        except HTTPException:
            # 重新抛出已知异常
            raise
        except Exception as e:
            self.logger.error(f"Error deducting tokens for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    def add_tokens(self, user_id: int, tokens: int, description: str = "Token recharge"):
        """为用户增加token"""
        try:
            user = self.db.get_user(user_id)
            user.tokens += tokens
            self.db.update_user(user)
            
            # 记录计费日志
            self.db.create_billing_record(user_id, tokens, user.tokens, description)
            self.logger.info(f"Added {tokens} tokens to user {user_id}, balance: {user.tokens}")
        except Exception as e:
            self.logger.error(f"Error adding tokens for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
```

## 9. 配套文件

### .env.example
```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/guoxue
REDIS_URL=redis://localhost:6379/0

# JWT配置
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI服务配置
DEEPSEEK_API_KEY=your_deepseek_api_key
CHROMA_DB_PATH=./chroma_db

# 微信小程序配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret

# 支付配置
PAYMENT_GATEWAY_KEY=your_payment_gateway_key

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Celery配置
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# MinIO配置
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=your_minio_access_key
MINIO_SECRET_KEY=your_minio_secret_key

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# 安全配置
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1

# 端口配置
BACKEND_PORT=8000
FRONTEND_PORT=3000

# 其他配置
DEBUG=False
ENVIRONMENT=production

# 新用户配置
NEW_USER_TOKENS=1000
```

### requirements.txt
```txt
# Web框架
fastapi==0.104.1
uvicorn==0.24.0

# 数据库
sqlalchemy==2.0.23
psycopg2-binary==2.9.9

# 缓存和消息队列
redis==5.0.1
celery==5.3.4

# AI和机器学习
langchain==0.0.352
langchain-community==0.0.11
chromadb==0.4.18
deepseek-coder==1.0.0

# 安全和认证
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
bcrypt==4.0.1

# 数据验证
pydantic==2.5.0
pydantic-settings==2.0.3

# 日志和监控
python-json-logger==2.0.7

# 工具
requests==2.31.0
python-dotenv==1.0.0

# 测试
pytest==7.4.3
pytest-cov==4.1.0

# 代码质量
black==23.11.0
flake8==6.1.0
```

### Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY ./app ./app
COPY ./ai ./ai
COPY ./tasks ./tasks
COPY ./migrations ./migrations

# 创建非root用户
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# 创建日志目录
RUN mkdir -p /app/logs

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### nginx.conf (Nginx配置文件)
```nginx
# nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    sendfile on;
    keepalive_timeout 65;
    
    # 限流配置
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    # 服务器配置
    server {
        listen 80;
        server_name localhost;
        
        # 安全头
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        
        # API路由
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # 健康检查
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
        
        # 错误页面
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }
}
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  # PostgreSQL数据库
  postgres:
    image: postgres:15-alpine
    container_name: guoxue_postgres
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-guoxue}
      POSTGRES_USER: ${POSTGRES_USER:-user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    networks:
      - guoxue_network

  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: guoxue_redis
    restart: always
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    networks:
      - guoxue_network

  # Chroma向量数据库
  chroma:
    image: chromadb/chroma:0.4.18
    container_name: guoxue_chroma
    restart: always
    ports:
      - "${CHROMA_PORT:-8001}:8000"
    volumes:
      - chroma_data:/chroma/chroma/
    environment:
      - CHROMA_DB_IMPL=clickhouse
    networks:
      - guoxue_network

  # MinIO对象存储
  minio:
    image: minio/minio:RELEASE.2023-11-20T22-40-07Z
    container_name: guoxue_minio
    restart: always
    ports:
      - "${MINIO_PORT:-9000}:9000"
      - "${MINIO_CONSOLE_PORT:-9001}:9001"
    volumes:
      - minio_data:/data
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
    command: server /data --console-address :9001
    networks:
      - guoxue_network

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    container_name: guoxue_nginx
    restart: always
    ports:
      - "${NGINX_PORT:-80}:80"
      - "${NGINX_SSL_PORT:-443}:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/certs:/etc/nginx/certs
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - backend
    networks:
      - guoxue_network

  # 后端服务
  backend:
    build:
      context: ./backend
    container_name: guoxue_backend
    restart: always
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-user}:${POSTGRES_PASSWORD:-password}@postgres:5432/${POSTGRES_DB:-guoxue}
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_DB_URL=http://chroma:8000
      - MINIO_ENDPOINT=http://minio:9000
    depends_on:
      - postgres
      - redis
      - chroma
      - minio
    volumes:
      - ./backend:/app
    networks:
      - guoxue_network

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
    container_name: guoxue_celery_worker
    restart: always
    command: celery -A tasks.worker worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-user}:${POSTGRES_PASSWORD:-password}@postgres:5432/${POSTGRES_DB:-guoxue}
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_DB_URL=http://chroma:8000
    depends_on:
      - postgres
      - redis
      - chroma
    volumes:
      - ./backend:/app
    networks:
      - guoxue_network

  # Celery Beat (定时任务)
  celery_beat:
    build:
      context: ./backend
    container_name: guoxue_celery_beat
    restart: always
    command: celery -A tasks.worker beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-user}:${POSTGRES_PASSWORD:-password}@postgres:5432/${POSTGRES_DB:-guoxue}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    networks:
      - guoxue_network

  # Prometheus监控
  prometheus:
    image: prom/prometheus:v2.48.0
    container_name: guoxue_prometheus
    restart: always
    ports:
      - "${PROMETHEUS_PORT:-9090}:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - guoxue_network

  # Grafana监控面板
  grafana:
    image: grafana/grafana-enterprise:10.2.2
    container_name: guoxue_grafana
    restart: always
    ports:
      - "${GRAFANA_PORT:-3000}:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-admin}
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - guoxue_network

  # ELK Stack - Elasticsearch
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: guoxue_elasticsearch
    restart: always
    ports:
      - "${ES_PORT:-9200}:9200"
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - guoxue_network

  # ELK Stack - Logstash
  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: guoxue_logstash
    restart: always
    ports:
      - "${LOGSTASH_PORT:-5044}:5044"
    volumes:
      - ./logstash/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
      - ./logstash/logs:/logs
    depends_on:
      - elasticsearch
    networks:
      - guoxue_network

  # ELK Stack - Kibana
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: guoxue_kibana
    restart: always
    ports:
      - "${KIBANA_PORT:-5601}:5601"
    environment:
      - ELASTICSEARCH_HOSTS=["http://elasticsearch:9200"]
    depends_on:
      - elasticsearch
    networks:
      - guoxue_network

networks:
  guoxue_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  chroma_data:
  minio_data:
  prometheus_data:
  grafana_data:
  es_data:
```

### docker-compose.prod.yml (生产环境配置)
```yaml
version: '3.8'

services:
  # PostgreSQL数据库 (生产环境使用云数据库)
  postgres:
    image: postgres:15-alpine
    container_name: guoxue_postgres_prod
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-guoxue}
      POSTGRES_USER: ${POSTGRES_USER:-user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    networks:
      - guoxue_network
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

  # Redis缓存 (生产环境使用云Redis)
  redis:
    image: redis:7-alpine
    container_name: guoxue_redis_prod
    restart: always
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    networks:
      - guoxue_network
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M

  # 后端服务 (生产环境扩展)
  backend:
    build:
      context: ./backend
    container_name: guoxue_backend_prod
    restart: always
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-user}:${POSTGRES_PASSWORD:-password}@postgres:5432/${POSTGRES_DB:-guoxue}
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_DB_URL=http://chroma:8000
      - MINIO_ENDPOINT=http://minio:9000
    depends_on:
      - postgres
      - redis
      - chroma
      - minio
    volumes:
      - ./backend:/app
    networks:
      - guoxue_network
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

  # Nginx负载均衡
  nginx:
    image: nginx:alpine
    container_name: guoxue_nginx_prod
    restart: always
    ports:
      - "${NGINX_PORT:-80}:80"
      - "${NGINX_SSL_PORT:-443}:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/certs:/etc/nginx/certs
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - backend
    networks:
      - guoxue_network
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

networks:
  guoxue_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

以上就是"国学大师"微信小程序的完整生产级高性能全栈开发方案。该方案涵盖了从项目简介到技术实现的各个方面，确保项目能够高效、稳定地运行，并具备良好的可扩展性和维护性。