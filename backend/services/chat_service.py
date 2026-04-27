from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Conversation, Message
from ..agents import AGENTS
from ..agents.orchestrateur import OrchestratorAgent
from .router_service import route_message
from .memory_service import get_memory_context


def send_message(
    db: Session,
    conversation_id: str,
    user_content: str,
    preferred_agent_id: str = "orchestrateur",
) -> tuple[Message, Message]:
    """
    Processes a user message and generates an AI response.
    Returns (user_message, assistant_message).
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise ValueError(f"Conversation {conversation_id} not found")

    # Save user message
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=user_content,
        agent_id=None,
    )
    db.add(user_msg)

    # Update conversation title from first user message
    existing_messages = db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.role == "user",
    ).count()
    if existing_messages == 0:
        conversation.title = user_content[:60] + ("..." if len(user_content) > 60 else "")
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user_msg)

    # Build history for context
    history_rows = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    history = [{"role": m.role, "content": m.content} for m in history_rows]

    # Get memory context
    memory_context = get_memory_context(db)

    # Route the message
    if preferred_agent_id != "orchestrateur":
        agent_ids = [preferred_agent_id]
    else:
        agent_ids = route_message(user_content)

    # Generate responses from each agent
    agent_responses: dict[str, str] = {}
    responding_agent_id = agent_ids[0] if agent_ids else "orchestrateur"

    for agent_id in agent_ids:
        agent = AGENTS.get(agent_id)
        if agent and agent_id != "orchestrateur":
            agent_responses[agent_id] = agent.generate_response(
                user_content, history, memory_context
            )

    # Orchestrate final response
    orchestrator: OrchestratorAgent = AGENTS["orchestrateur"]  # type: ignore

    if agent_responses:
        response_content = orchestrator.generate_response_orchestrated(
            message=user_content,
            history=history,
            agent_responses=agent_responses,
            memory_context=memory_context,
        )
        responding_agent_id = list(agent_responses.keys())[0] if len(agent_responses) == 1 else "orchestrateur"
    else:
        response_content = orchestrator.generate_response(
            user_content, history, memory_context
        )
        responding_agent_id = "orchestrateur"

    # Save assistant response
    assistant_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=response_content,
        agent_id=responding_agent_id,
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return user_msg, assistant_msg
