from core.orchestrator.state_schema import ProjectState

def research_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for research_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[research_agent] Output for: {input_text}"
    return state
