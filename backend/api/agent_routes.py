from fastapi import APIRouter
from ..agents import get_agents_info
from ..schemas import AgentInfo

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("", response_model=list[AgentInfo])
def list_agents():
    return get_agents_info()
