from core.orchestrator.state_schema import ProjectState

def content_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for content_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[content_agent] Output for: {input_text}"
    return state
