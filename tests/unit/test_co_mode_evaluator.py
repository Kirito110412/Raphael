from growth.co_mode_evaluator import evaluate_holiday_request

def test_holiday_evaluation():
    assert evaluate_holiday_request("I have severe burnout") == "approved"
    assert evaluate_holiday_request("I am feeling lazy today") == "category_c_flag"
    assert evaluate_holiday_request("I want to skip work") == "rejected"
