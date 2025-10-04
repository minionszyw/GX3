from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.database import get_db

router = APIRouter()

# 数据模型
class WechatLoginRequest(BaseModel):
    code: str

class EmailLoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    nickname: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    nickname: str
    tokens: int

# 依赖项
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

@router.post("/wechat-login", response_model=Token)
async def wechat_login(request: WechatLoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    """微信登录"""
    user = auth_service.authenticate_wechat_user(request.code)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/email-login", response_model=Token)
async def email_login(request: EmailLoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    """邮箱登录"""
    user = auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    """用户注册"""
    # 检查邮箱是否已存在
    existing_user = auth_service.db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 创建新用户
    hashed_password = auth_service.get_password_hash(request.password)
    new_user = User(
        email=request.email,
        nickname=request.nickname,
        hashed_password=hashed_password
    )
    
    auth_service.db.add(new_user)
    auth_service.db.commit()
    auth_service.db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.id}

@router.get("/verify")
async def verify_token(current_user = Depends(get_auth_service().get_current_user)):
    """验证token"""
    return {"user": current_user}