from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class LoginLog(Base):
    __tablename__ = 'login_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    login_method = Column(String(20))  # wechat or email
    ip_address = Column(String(50))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", back_populates="login_logs")
    
    def __repr__(self):
        return f"<LoginLog(id={self.id}, login_method='{self.login_method}')>"