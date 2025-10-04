from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.database import get_db
from app.models import Session as SessionModel

router = APIRouter()

# 数据模型
class SessionCreate(BaseModel):
    title: str

class SessionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: str

# 依赖项
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

@router.post("/", response_model=SessionResponse)
async def create_session(
    session_create: SessionCreate,
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db)
):
    """创建会话"""
    db_session = SessionModel(
        user_id=current_user.id,
        title=session_create.title
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return {
        "id": db_session.id,
        "user_id": db_session.user_id,
        "title": db_session.title,
        "created_at": db_session.created_at.isoformat() if db_session.created_at else None
    }

@router.get("/", response_model=list[SessionResponse])
async def get_sessions(
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db)
):
    """获取会话列表"""
    sessions = db.query(SessionModel).filter(SessionModel.user_id == current_user.id).all()
    return [{
        "id": session.id,
        "user_id": session.user_id,
        "title": session.title,
        "created_at": session.created_at.isoformat() if session.created_at else None
    } for session in sessions]

@router.delete("/{session_id}")
async def delete_session(
    session_id: int,
    current_user = Depends(get_auth_service().get_current_user),
    db: Session = Depends(get_db)
):
    """删除会话"""
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    
    return {"message": "Session deleted successfully"}