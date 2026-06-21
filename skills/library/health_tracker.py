def update_confidence(current_confidence: float, success: bool) -> float:
    """
    Updates skill confidence based on PRD Section 6.3 schema.
    Success: min(1.0, current + 0.02)
    Failure: max(0.0, current - 0.15)
    """
    if success:
        return min(1.0, current_confidence + 0.02)
    else:
        return max(0.0, current_confidence - 0.15)

class SkillHealthTracker:
    def __init__(self):
        self.health_records = {}

    def record_usage(self, skill_id: str, success: bool):
        if skill_id not in self.health_records:
            self.health_records[skill_id] = {"confidence_score": 1.0, "success_count": 0, "failure_count": 0}

        record = self.health_records[skill_id]
        if success:
            record["success_count"] += 1
        else:
            record["failure_count"] += 1

        record["confidence_score"] = update_confidence(record["confidence_score"], success)
