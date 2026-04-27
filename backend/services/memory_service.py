from sqlalchemy.orm import Session
from ..models import MemoryItem


def get_memory_context(db: Session) -> str:
    """Returns a condensed text summary of all memory items for agent context."""
    items = db.query(MemoryItem).order_by(MemoryItem.category, MemoryItem.created_at).all()
    if not items:
        return ""
    lines = []
    current_cat = None
    for item in items:
        if item.category != current_cat:
            current_cat = item.category
            lines.append(f"\n### {item.category.upper()}")
        lines.append(f"**{item.title}**\n{item.content}")
    return "\n".join(lines)
