from growth.intelligence_preserver import check_think_first, check_socratic_mode

def test_think_first():
    assert check_think_first("how do I fix this?", "analytical") is True
    assert check_think_first("why does this happen?", "flow") is True
    assert check_think_first("how do I fix this?", "fatigued") is False
    assert check_think_first("what is the capital of France?", "analytical") is False

def test_socratic_mode():
    assert check_socratic_mode(0.8) is True
    assert check_socratic_mode(0.4) is False
