from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService
from app.database import get_db
from app.models import Message, Session as SessionModel

router = APIRouter()

# 数据模型
class MessageCreate(BaseModel):
    content: str
    role: str

class MessageResponse(BaseModel):
    id: int
    session_id: int
    content: str
    role: str
    tokens: int
    created_at: str

# 依赖项
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

def get_chat_service():
    return ChatService()

@router.post("/", response_model=MessageResponse)
async def send_message(
    session_id: int,
    message_create: MessageCreate,
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """发送消息"""
    # 验证会话属于当前用户
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 获取AI回复
    ai_response = await chat_service.chat(message_create.content, str(session_id), current_user.id)
    
    # 计算token消耗
    token_cost = len(message_create.content) // 4 + len(ai_response) // 4
    
    # 保存用户消息
    user_message = Message(
        session_id=session_id,
        content=message_create.content,
        role=message_create.role,
        tokens=len(message_create.content) // 4
    )
    db.add(user_message)
    
    # 保存AI回复
    ai_message = Message(
        session_id=session_id,
        content=ai_response,
        role="assistant",
        tokens=len(ai_response) // 4
    )
    db.add(ai_message)
    
    # 更新用户token余额
    current_user.tokens -= token_cost
    db.commit()
    
    return {
        "id": ai_message.id,
        "session_id": ai_message.session_id,
        "content": ai_message.content,
        "role": ai_message.role,
        "tokens": ai_message.tokens,
        "created_at": ai_message.created_at.isoformat() if ai_message.created_at else None
    }

@router.get("/", response_model=list[MessageResponse])
async def get_messages(
    session_id: int,
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db)
):
    """获取消息历史"""
    # 验证会话属于当前用户
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 获取消息
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    
    return [{
        "id": message.id,
        "session_id": message.session_id,
        "content": message.content,
        "role": message.role,
        "tokens": message.tokens,
        "created_at": message.created_at.isoformat() if message.created_at else None
    } for message in messages]