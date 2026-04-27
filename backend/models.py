import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


def _uuid():
    return str(uuid.uuid4())


def _now():
    return datetime.utcnow()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=_uuid)
    title = Column(String, default="Nouvelle conversation")
    agent_id = Column(String, default="orchestrateur")
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now)

    messages = relationship(
        "Message", back_populates="conversation",
        cascade="all, delete-orphan", order_by="Message.created_at"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"))
    role = Column(String)          # "user" | "assistant"
    content = Column(Text)
    agent_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=_now)

    conversation = relationship("Conversation", back_populates="messages")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=_uuid)
    title = Column(String)
    description = Column(Text, nullable=True)
    priority = Column(String, default="medium")   # low | medium | high
    status = Column(String, default="todo")        # todo | in_progress | done
    agent_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now)


class MemoryItem(Base):
    __tablename__ = "memory_items"

    id = Column(String, primary_key=True, default=_uuid)
    category = Column(String)   # camping | vanea | objectives | constraints | notes
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now)


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True)
    value = Column(Text, default="")
    updated_at = Column(DateTime, default=_now)
