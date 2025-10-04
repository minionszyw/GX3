from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.database import get_db
from app.models import User, BillingRecord

router = APIRouter()

# 数据模型
class RechargeRequest(BaseModel):
    amount: int

class RechargeResponse(BaseModel):
    message: str
    balance: int

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    change_amount: int
    balance_after: int
    description: str
    created_at: str

# 依赖项
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

@router.post("/recharge", response_model=RechargeResponse)
async def recharge(
    recharge_request: RechargeRequest,
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db)
):
    """充值"""
    # 更新用户余额
    current_user.tokens += recharge_request.amount
    
    # 创建交易记录
    billing_record = BillingRecord(
        user_id=current_user.id,
        change_amount=recharge_request.amount,
        balance_after=current_user.tokens,
        description=f"充值 {recharge_request.amount} tokens"
    )
    db.add(billing_record)
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Recharge successful",
        "balance": current_user.tokens
    }

@router.get("/transactions", response_model=list[TransactionResponse])
async def get_transactions(
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db)
):
    """获取交易记录"""
    transactions = db.query(BillingRecord).filter(BillingRecord.user_id == current_user.id).order_by(BillingRecord.created_at.desc()).all()
    
    return [{
        "id": transaction.id,
        "user_id": transaction.user_id,
        "change_amount": transaction.change_amount,
        "balance_after": transaction.balance_after,
        "description": transaction.description,
        "created_at": transaction.created_at.isoformat() if transaction.created_at else None
    } for transaction in transactions]