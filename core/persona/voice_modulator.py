def get_tts_overrides(persona_mode: str) -> dict:
    """
    Maps persona modes to TTS parameter overrides (e.g., pace, pitch).
    """
    overrides = {
        "comfort_and_care": {"speed": 0.85, "pitch": 0.95},
        "brainstorming": {"speed": 1.15, "pitch": 1.05},
        "rational_objective": {"speed": 1.0, "pitch": 1.0},
        "standard_companion": {"speed": 1.0, "pitch": 1.0}
    }
    return overrides.get(persona_mode, overrides["standard_companion"])
