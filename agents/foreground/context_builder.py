from core.orchestrator.state_schema import ProjectState

def assemble_context(state: ProjectState) -> dict:
    """
    Assembles full context package for domain agent handoff.
    """
    return {
        "l1_memory": state.get("l1_memory_blocks", {}),
        "retrieved_l2": state.get("retrieved_context", []),
        "emotion": state.get("detected_emotion", "neutral"),
        "cognitive_state": state.get("detected_cognitive_state", "analytical")
    }
