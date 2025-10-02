## 项目简介：
国学大师是一款AI对话微信小程序，采用响应式设计，支持跨端运行。该应用结合了传统文化与现代AI技术，为用户提供国学知识问答、智能对话等服务。

## 主要功能：
- AI对话（流式记忆对话）
- RAG知识库检索
- 聊天记录管理
- 注册登录（微信登录/邮箱注册登录）
- JWT认证
- token计费


## 主要页面：
- AI对话（tabbar）：
  - 消息区：头像、消息气泡、时间戳
  - 输入区：操作按钮、输入框、发送按钮
    - 操作按钮功能：新建会话、清空记录
- 个人中心（tabbar）：
  - 信息区：
    - 头像、昵称、编辑按钮
    - 余额、充值
  - 菜单区：
    - 聊天记录管理
    - 使用统计
    - 关于我们
  - 退出登录

  ## 前端要求：
  - 采用苹果设计师标准的极简风格设计
  - 使用uni-app组件、样式、api
  - 界面与逻辑分离，便于维护和扩展

## 商业模式：
- 按使用token计费。
- 注册登录送10元体验。

## 技术栈：
### 前端技术栈
- 前端框架：uni-app + vue3
- UI库：uni-ui （uni-app内置）
- 状态管理：Pinia （uni-app内置）
- 网络请求：uni.request （uni-app内置）
- 数据缓存：uni.setStorage （uni-app内置）

### 后端技术栈
- 后端框架：FastAPI
- 认证：JWT
- AI框架：langchain + deepseek API 
- 记忆模块: ConversationBufferWindowMemory + Redis
- RAG引擎: Chroma向量数据库
- 消息队列: Celery + Redis
- 数据库：PostgreSQL + redis
- 监控运维: Prometheus + Grafana

## 开发工具：
- Node.js
- Python 3.11
- HBuilder X
- 微信开发者工具

## 部署方式：
Docker + Docker Compose

## 开发文档：
- [全栈开发方案](dev.md)
- [API文档](docs/api/api-documentation.md)
- [部署指南](docs/deployment/deployment-guide.md)