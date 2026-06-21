from growth.lie_detector import check_consistency

def test_check_consistency():
    history = ["I never did python", "I hate python"]
    statement = "I always do this in python"

    assert check_consistency(statement, history) > 0.5
    assert check_consistency("I am learning python", history) < 0.5
