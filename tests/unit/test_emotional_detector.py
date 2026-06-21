from core.persona.emotional_detector import detect_emotion
from core.persona.cognitive_state_detector import detect_cognitive_state

def test_detect_emotion():
    assert detect_emotion("test") == "neutral"

def test_detect_cognitive_state():
    assert detect_cognitive_state("test") == "analytical"
