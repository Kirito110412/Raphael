from core.orchestrator.state_schema import ProjectState

def negotiation_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for negotiation_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[negotiation_agent] Output for: {input_text}"
    return state
