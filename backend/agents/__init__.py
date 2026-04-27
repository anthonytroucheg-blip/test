from .orchestrateur import OrchestratorAgent
from .finance import FinanceAgent
from .camping import CampingAgent
from .vanea import VaneaAgent
from .operations import OperationsAgent
from .strategie import StrategieAgent

AGENTS = {
    "orchestrateur": OrchestratorAgent(),
    "finance": FinanceAgent(),
    "camping": CampingAgent(),
    "vanea": VaneaAgent(),
    "operations": OperationsAgent(),
    "strategie": StrategieAgent(),
}


def get_agents_info() -> list[dict]:
    return [
        {
            "id": a.id,
            "name": a.name,
            "role": a.role,
            "expertise": a.expertise,
            "color": a.color,
            "icon": a.icon,
            "description": a.description,
        }
        for a in AGENTS.values()
    ]
