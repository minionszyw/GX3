# API文档

## 认证相关接口

### 微信登录
**POST** `/api/auth/wechat-login`

请求参数：
```json
{
  "code": "微信登录凭证"
}
```

响应：
```json
{
  "access_token": "JWT令牌",
  "token_type": "bearer"
}
```

### 邮箱登录
**POST** `/api/auth/email-login`

请求参数：
```json
{
  "email": "用户邮箱",
  "password": "用户密码"
}
```

响应：
```json
{
  "access_token": "JWT令牌",
  "token_type": "bearer"
}
```

### 用户注册
**POST** `/api/auth/register`

请求参数：
```json
{
  "email": "用户邮箱",
  "password": "用户密码",
  "nickname": "用户昵称"
}
```

响应：
```json
{
  "message": "注册成功",
  "user_id": 123
}
```

### 验证Token
**GET** `/api/auth/verify`

响应：
```json
{
  "user": {
    "id": 123,
    "email": "user@example.com",
    "nickname": "用户名",
    "tokens": 1000
  }
}
```

## 用户相关接口

### 获取用户信息
**GET** `/api/user/profile`

响应：
```json
{
  "id": 123,
  "email": "user@example.com",
  "nickname": "用户名",
  "avatar_url": "头像URL",
  "tokens": 1000,
  "created_at": "2023-01-01T00:00:00Z"
}
```

### 更新用户信息
**PUT** `/api/user/profile`

请求参数：
```json
{
  "nickname": "新昵称",
  "avatar_url": "新头像URL"
}
```

响应：
```json
{
  "id": 123,
  "email": "user@example.com",
  "nickname": "新昵称",
  "avatar_url": "新头像URL",
  "tokens": 1000,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

### 获取用户余额
**GET** `/api/user/balance`

响应：
```json
{
  "balance": 1000
}
```

## 会话相关接口

### 创建会话
**POST** `/api/sessions`

请求参数：
```json
{
  "title": "会话标题"
}
```

响应：
```json
{
  "id": 456,
  "user_id": 123,
  "title": "会话标题",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### 获取会话列表
**GET** `/api/sessions`

响应：
```json
[
  {
    "id": 456,
    "user_id": 123,
    "title": "会话标题",
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

### 删除会话
**DELETE** `/api/sessions/{session_id}`

响应：
```json
{
  "message": "会话删除成功"
}
```

## 消息相关接口

### 发送消息
**POST** `/api/sessions/{session_id}/messages`

请求参数：
```json
{
  "content": "消息内容",
  "role": "user"
}
```

响应：
```json
{
  "id": 789,
  "session_id": 456,
  "content": "AI回复内容",
  "role": "assistant",
  "tokens": 50,
  "created_at": "2023-01-01T00:00:00Z"
}
```

### 获取消息历史
**GET** `/api/sessions/{session_id}/messages`

响应：
```json
[
  {
    "id": 789,
    "session_id": 456,
    "content": "消息内容",
    "role": "user",
    "tokens": 50,
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

## 计费相关接口

### 充值
**POST** `/api/billing/recharge`

请求参数：
```json
{
  "amount": 1000
}
```

响应：
```json
{
  "message": "充值成功",
  "balance": 2000
}
```

### 获取交易记录
**GET** `/api/billing/transactions`

响应：
```json
[
  {
    "id": 1,
    "user_id": 123,
    "change_amount": 1000,
    "balance_after": 2000,
    "description": "充值",
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```