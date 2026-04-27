from ..agents import AGENTS


def route_message(message: str) -> list[str]:
    """
    Scores each agent against the message and returns a sorted list of agent IDs.
    Orchestrateur is always included for synthesis if multiple agents match.
    """
    msg = message.lower()
    scores: dict[str, int] = {}

    for agent_id, agent in AGENTS.items():
        if agent_id == "orchestrateur":
            continue
        score = sum(1 for kw in agent.keywords if kw in msg)
        if score > 0:
            scores[agent_id] = score

    if not scores:
        return ["orchestrateur"]

    ranked = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    return ranked[:2]  # max 2 specialized agents


def get_agent_or_default(agent_id: str):
    return AGENTS.get(agent_id, AGENTS["orchestrateur"])
