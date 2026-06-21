from core.persona.mode_selector import select_mode
from core.persona.voice_modulator import get_tts_overrides

def test_select_mode():
    assert select_mode("frustrated", "scattered") == "comfort_and_care"
    assert select_mode("neutral", "fatigued") == "comfort_and_care"
    assert select_mode("neutral", "creative") == "brainstorming"
    assert select_mode("neutral", "analytical") == "rational_objective"
    assert select_mode("happy", "flow") == "standard_companion"

def test_voice_modulator():
    comfort = get_tts_overrides("comfort_and_care")
    assert comfort["speed"] < 1.0

    brainstorm = get_tts_overrides("brainstorming")
    assert brainstorm["speed"] > 1.0

    standard = get_tts_overrides("unknown_mode")
    assert standard["speed"] == 1.0
