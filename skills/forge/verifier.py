def verify_skill(sandbox_output: dict) -> bool:
    """
    Stub for pytest runner evaluating sandbox output.
    """
    return sandbox_output.get("status") == "success"
