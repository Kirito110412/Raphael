from core.orchestrator.state_schema import ProjectState

def legal_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for legal_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[legal_agent] Output for: {input_text}"
    return state
