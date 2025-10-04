from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.database import get_db
from app.models import User

router = APIRouter()

# 数据模型
class UserProfileResponse(BaseModel):
    id: int
    email: str
    nickname: str
    avatar_url: str
    tokens: int
    created_at: str

class UserProfileUpdate(BaseModel):
    nickname: str
    avatar_url: str

class UserBalanceResponse(BaseModel):
    balance: int

# 依赖项
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(current_user = Depends(get_auth_service().get_current_user)):
    """获取用户信息"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "avatar_url": current_user.avatar_url,
        "tokens": current_user.tokens,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    current_user.nickname = profile_update.nickname
    current_user.avatar_url = profile_update.avatar_url
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "avatar_url": current_user.avatar_url,
        "tokens": current_user.tokens,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

@router.get("/balance", response_model=UserBalanceResponse)
async def get_user_balance(current_user = Depends(get_auth_service().get_current_user)):
    """获取用户余额"""
    return {"balance": current_user.tokens}