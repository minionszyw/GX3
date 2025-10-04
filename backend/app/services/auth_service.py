from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import User
import os
import httpx

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2密码Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希值"""
        return pwd_context.hash(password)
    
    def authenticate_user(self, email: str, password: str):
        """验证用户"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not self.verify_password(password, user.hashed_password):
            return False
        return user
    
    def authenticate_wechat_user(self, code: str):
        """验证微信用户"""
        # 检查是否为开发环境下的测试code
        environment = os.getenv("ENVIRONMENT", "production")
        if environment == "development" and code == "test_code_123456":
            # 在开发环境中，为测试code创建或返回测试用户
            user = self.db.query(User).filter(User.openid == "test_openid").first()
            if not user:
                # 创建测试用户
                user = User(
                    openid="test_openid",
                    nickname="测试用户",
                    tokens=1000  # 新用户赠送1000 tokens
                )
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
            return user
        
        try:
            # 调用微信API验证code
            app_id = os.getenv("WECHAT_APP_ID")
            app_secret = os.getenv("WECHAT_APP_SECRET")
            
            if not app_id or not app_secret:
                raise Exception("微信配置缺失")
            
            # 调用微信接口获取access_token和openid
            url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
            
            response = httpx.get(url)
            data = response.json()
            
            if "errcode" in data:
                raise Exception(f"微信登录失败: {data}")
            
            openid = data.get("openid")
            session_key = data.get("session_key")
            
            # 查找或创建用户
            user = self.db.query(User).filter(User.openid == openid).first()
            if not user:
                # 创建新用户
                user = User(
                    openid=openid,
                    nickname=f"微信用户_{openid[:8]}",
                    tokens=1000  # 新用户赠送1000 tokens
                )
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
            
            return user
        except Exception as e:
            print(f"微信登录验证失败: {str(e)}")
            return False
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        """获取当前用户"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        
        return user