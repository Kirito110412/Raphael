from intelligence.calibration_tracker import CalibrationTracker

def test_calibration_score():
    tracker = CalibrationTracker()
    assert tracker.get_calibration() == 1.0 # default empty

    tracker.log_prediction(0.8, True)  # squared diff: (0.8 - 1.0)^2 = 0.04
    tracker.log_prediction(0.9, False) # squared diff: (0.9 - 0.0)^2 = 0.81
    # Brier score = (0.04 + 0.81) / 2 = 0.425

    score = tracker.get_calibration()
    assert abs(score - 0.425) < 0.001
