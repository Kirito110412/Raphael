def check_think_first(query: str, cognitive_state: str) -> bool:
    """
    Evaluates if query triggers a think-first gate based on cognitive state.
    """
    if cognitive_state in ["fatigued", "scattered"]:
        return False
    return "how" in query.lower() or "why" in query.lower()

def check_socratic_mode(reliance_score: float) -> bool:
    """
    Triggers Socratic mode if reliance > 0.7
    Returns True if active.
    """
    return reliance_score > 0.7
