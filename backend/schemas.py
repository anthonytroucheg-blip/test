from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# ── Messages ──────────────────────────────────────────────────────────────────

class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    role: str
    content: str
    agent_id: Optional[str] = None
    created_at: datetime


class SendMessageIn(BaseModel):
    content: str
    agent_id: str = "orchestrateur"


# ── Conversations ─────────────────────────────────────────────────────────────

class ConversationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    agent_id: str
    created_at: datetime
    updated_at: datetime


class ConversationDetailOut(ConversationOut):
    messages: List[MessageOut] = []


class CreateConversationIn(BaseModel):
    title: str = "Nouvelle conversation"
    agent_id: str = "orchestrateur"


class SendMessageResponse(BaseModel):
    user_message: MessageOut
    assistant_message: MessageOut


# ── Tasks ─────────────────────────────────────────────────────────────────────

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    agent_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CreateTaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "todo"
    agent_id: Optional[str] = None


class UpdateTaskIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    agent_id: Optional[str] = None


# ── Memory ────────────────────────────────────────────────────────────────────

class MemoryItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    category: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class CreateMemoryIn(BaseModel):
    category: str
    title: str
    content: str


class UpdateMemoryIn(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None


# ── Settings ──────────────────────────────────────────────────────────────────

class SettingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    key: str
    value: str


class UpdateSettingsIn(BaseModel):
    company_name: Optional[str] = None
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    response_style: Optional[str] = None


# ── Agents ────────────────────────────────────────────────────────────────────

class AgentInfo(BaseModel):
    id: str
    name: str
    role: str
    expertise: List[str]
    color: str
    icon: str
    description: str
