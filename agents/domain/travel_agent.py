from core.orchestrator.state_schema import ProjectState

def travel_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for travel_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[travel_agent] Output for: {input_text}"
    return state
