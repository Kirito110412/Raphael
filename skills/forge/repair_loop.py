def repair_code(code: str, error_trace: str, iteration: int = 0) -> str:
    """
    Stub for LLM repairing failed code. Max 3 iterations.
    """
    if iteration >= 3:
        raise Exception("Max repair iterations reached.")
    return f"{code}\n# Repaired code based on {error_trace}"
