def target_skill_gap(performance_matrix: dict) -> str:
    """
    Identifies weakest sub-skill in the current domain.
    """
    if not performance_matrix: return "general_practice"
    return min(performance_matrix, key=performance_matrix.get)
