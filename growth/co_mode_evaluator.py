def evaluate_holiday_request(reason: str) -> str:
    """
    Evaluates CO-mode holiday request.
    Returns: "approved", "rejected", "category_c_flag"
    """
    if "burnout" in reason.lower() or "vacation" in reason.lower():
        return "approved"
    if "lazy" in reason.lower():
        return "category_c_flag"
    return "rejected"
