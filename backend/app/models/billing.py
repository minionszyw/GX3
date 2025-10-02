from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BillingRecord(Base):
    __tablename__ = 'billing_records'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    change_amount = Column(Integer)  # 正数为充值，负数为消费
    balance_after = Column(Integer)
    description = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", back_populates="billing_records")
    
    def __repr__(self):
        return f"<BillingRecord(id={self.id}, change_amount={self.change_amount})>"