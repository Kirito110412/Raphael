from core.orchestrator.state_schema import ProjectState

def health_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for health_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[health_agent] Output for: {input_text}"
    return state
