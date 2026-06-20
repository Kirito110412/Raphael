from skills.forge.generator import generate_skill
from skills.forge.sandbox import run_in_sandbox
from skills.forge.verifier import verify_skill
from skills.forge.hitl_gate import require_human_approval

from skills.library.health_tracker import update_confidence, SkillHealthTracker

def test_forge_pipeline():
    # 1. Generate
    code = generate_skill("Sort a list")
    assert "def run_skill(): pass" in code

    # 2. Sandbox
    output = run_in_sandbox(code)
    assert output["status"] == "success"

    # 3. Verify
    is_valid = verify_skill(output)
    assert is_valid is True

    # 4. HITL Approval
    is_approved = require_human_approval(code)
    assert is_approved is True

    print("Integration test test_forge_pipeline passed.")

def test_health_tracker():
    tracker = SkillHealthTracker()

    # Record success -> increment from 1.0 (should stay 1.0)
    tracker.record_usage("test_skill", True)
    assert tracker.health_records["test_skill"]["confidence_score"] == 1.0

    # Record failure -> drop by 0.15
    tracker.record_usage("test_skill", False)
    assert tracker.health_records["test_skill"]["confidence_score"] == 0.85

    # Record success -> increment by 0.02
    tracker.record_usage("test_skill", True)
    assert round(tracker.health_records["test_skill"]["confidence_score"], 2) == 0.87

    print("Integration test test_health_tracker passed.")

if __name__ == '__main__':
    test_forge_pipeline()
    test_health_tracker()
    print("ALL PHASE 7 TESTS PASSED")
