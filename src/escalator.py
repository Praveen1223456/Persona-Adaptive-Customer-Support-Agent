import json
from src.config import Config

def check_hard_escalation(query: str) -> bool:
    """Verifies baseline text elements against critical account compliance strings."""
    return any(keyword in query.lower() for keyword in Config.SENSITIVE_KEYWORDS)

def generate_handoff_summary(user_query: str, persona: str, context_chunks: list, reason: str) -> dict:
    """Compiles structured handoff state specifications."""
    best_score = max([chunk["score"] for chunk in context_chunks]) if context_chunks else 0.0
    return {
        "persona": persona,
        "detected_issue": user_query if len(user_query) < 120 else user_query[:120] + "...",
        "escalation_reason": reason,
        "retrieved_sources": list(set([c["source"] for c in context_chunks])),
        "confidence_score": best_score,
        "recommended_action": "Prioritize direct outreach. Track logs via the referenced sources payload."
    }