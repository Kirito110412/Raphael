from core.orchestrator.state_schema import ProjectState

def tutoring_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for tutoring_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[tutoring_agent] Output for: {input_text}"
    return state
