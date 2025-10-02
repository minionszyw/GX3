from sqlalchemy.orm import Session
from app.models import User, BillingRecord
from fastapi import HTTPException, status
import logging

class BillingService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def get_user_balance(self, user_id: int) -> int:
        """获取用户余额"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.tokens
    
    def recharge_tokens(self, user_id: int, amount: int, description: str = "Token recharge"):
        """为用户充值tokens"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # 更新用户余额
            user.tokens += amount
            
            # 创建交易记录
            billing_record = BillingRecord(
                user_id=user_id,
                change_amount=amount,
                balance_after=user.tokens,
                description=description
            )
            
            self.db.add(billing_record)
            self.db.commit()
            self.db.refresh(user)
            
            self.logger.info(f"用户 {user_id} 充值 {amount} tokens，余额: {user.tokens}")
            return user
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"充值失败: {str(e)}")
            raise HTTPException(status_code=500, detail="Recharge failed")
    
    def deduct_tokens(self, user_id: int, amount: int, description: str = "Token consumption"):
        """扣除用户tokens"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # 检查余额是否充足
            if user.tokens < amount:
                raise HTTPException(status_code=400, detail="Insufficient tokens")
            
            # 扣除tokens
            user.tokens -= amount
            
            # 创建交易记录
            billing_record = BillingRecord(
                user_id=user_id,
                change_amount=-amount,
                balance_after=user.tokens,
                description=description
            )
            
            self.db.add(billing_record)
            self.db.commit()
            self.db.refresh(user)
            
            self.logger.info(f"用户 {user_id} 消费 {amount} tokens，余额: {user.tokens}")
            return user
        except HTTPException:
            # 重新抛出已知异常
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"扣费失败: {str(e)}")
            raise HTTPException(status_code=500, detail="Deduction failed")
    
    def get_transaction_history(self, user_id: int, limit: int = 50):
        """获取交易历史"""
        transactions = self.db.query(BillingRecord)\
            .filter(BillingRecord.user_id == user_id)\
            .order_by(BillingRecord.created_at.desc())\
            .limit(limit)\
            .all()
        return transactions