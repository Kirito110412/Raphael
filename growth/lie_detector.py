def check_consistency(current_statement: str, history: list) -> float:
    """
    Passive inconsistency monitoring. Returns inconsistency score 0.0 - 1.0.
    """
    # Stub: compare statement with history
    if "always do this" in current_statement.lower() and "never did" in str(history).lower():
        return 0.9
    return 0.1
