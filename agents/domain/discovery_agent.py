from core.orchestrator.state_schema import ProjectState

def discovery_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for discovery_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[discovery_agent] Output for: {input_text}"
    return state
