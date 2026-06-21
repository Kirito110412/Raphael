def calculate_brier_score(predictions: list, outcomes: list) -> float:
    """Stub for Brier score tracking."""
    return sum((p - o)**2 for p, o in zip(predictions, outcomes)) / len(predictions) if predictions else 0.0

class CalibrationTracker:
    def __init__(self):
        self.history = []

    def log_prediction(self, confidence: float, outcome: bool):
        self.history.append((confidence, float(outcome)))

    def get_calibration(self) -> float:
        if not self.history: return 1.0
        preds = [p for p, _ in self.history]
        outs = [o for _, o in self.history]
        return calculate_brier_score(preds, outs)
