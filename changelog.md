## v1.2（2025-10-04）
- 新增 后端API模块实现
  - 新增 user.py API模块，实现用户信息获取/更新、余额查询接口
  - 新增 sessions.py API模块，实现会话创建、查询、删除接口
  - 新增 messages.py API模块，实现消息发送、历史查询接口
  - 新增 billing.py API模块，实现充值、交易记录查询接口
- 优化 修复API路由中引用的缺失模块问题
  - 解决了app/api/routes.py中引用未实现模块的问题
  - 完善了后端API接口的完整实现
- 新增 部署说明
  - 添加了依赖安装和启动服务的详细指南
  - 补充了Docker部署说明
- 新增 API导入测试
  - 创建了test_api_import.py文件用于验证API模块导入


