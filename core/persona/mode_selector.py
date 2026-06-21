def select_mode(emotion: str, cognitive_state: str) -> str:
    """
    Selects one of 8 friend modes based on PRD Section 7.10 rules.
    Stub implementation for Phase 3.
    """
    if emotion == "frustrated" or cognitive_state == "fatigued":
        return "comfort_and_care"
    elif cognitive_state == "creative":
        return "brainstorming"
    elif cognitive_state == "analytical":
        return "rational_objective"
    return "standard_companion"
