from core.orchestrator.state_schema import ProjectState

def critique_output(state: ProjectState, iteration: int) -> ProjectState:
    """
    Adversarial challenger. Attacks important outputs.
    Stub implementation approves after 1 revision or instantly depending on iteration.
    """
    if iteration < 1:
        state["critic_verdict"] = "revised"
    else:
        state["critic_verdict"] = "approved"
    return state
