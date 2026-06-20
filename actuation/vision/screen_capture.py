from PIL import ImageGrab

def capture_screen_memory() -> object:
    """
    Captures a screenshot directly to memory.
    Never auto-saves to disk per DEC-027 constraint.
    """
    # Returns PIL Image object in memory
    try:
        return ImageGrab.grab()
    except Exception:
        return None
