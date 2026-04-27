from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Conversation, Message
from ..schemas import (
    ConversationOut, ConversationDetailOut, CreateConversationIn,
    MessageOut, SendMessageIn, SendMessageResponse,
)
from ..services.chat_service import send_message

router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/conversations", response_model=list[ConversationOut])
def list_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).order_by(Conversation.updated_at.desc()).all()


@router.post("/conversations", response_model=ConversationOut)
def create_conversation(body: CreateConversationIn, db: Session = Depends(get_db)):
    conv = Conversation(title=body.title, agent_id=body.agent_id)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


@router.get("/conversations/{conv_id}", response_model=ConversationDetailOut)
def get_conversation(conv_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Conversation introuvable")
    return conv


@router.delete("/conversations/{conv_id}")
def delete_conversation(conv_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Conversation introuvable")
    db.delete(conv)
    db.commit()
    return {"ok": True}


@router.post("/conversations/{conv_id}/messages", response_model=SendMessageResponse)
def post_message(conv_id: str, body: SendMessageIn, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Conversation introuvable")
    try:
        user_msg, assistant_msg = send_message(
            db=db,
            conversation_id=conv_id,
            user_content=body.content,
            preferred_agent_id=body.agent_id,
        )
    except Exception as e:
        raise HTTPException(500, str(e))
    return SendMessageResponse(
        user_message=MessageOut.model_validate(user_msg),
        assistant_message=MessageOut.model_validate(assistant_msg),
    )
