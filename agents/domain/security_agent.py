from core.orchestrator.state_schema import ProjectState

def security_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for security_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[security_agent] Output for: {input_text}"
    return state
