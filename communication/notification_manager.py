def route_notification(message: str, urgency: str = "normal"):
    """
    Routes notification to appropriate channel based on urgency.
    """
    print(f"[NOTIFICATION] {urgency.upper()}: {message}")
