from fastapi import APIRouter

# 创建API路由实例
router = APIRouter()

# 导入各个模块的路由
from app.api import auth, user, sessions, messages, billing

# 注册路由
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/user", tags=["user"])
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
router.include_router(messages.router, prefix="/sessions/{session_id}/messages", tags=["messages"])
router.include_router(billing.router, prefix="/billing", tags=["billing"])