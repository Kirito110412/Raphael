from core.orchestrator.state_schema import ProjectState

def finance_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for finance_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[finance_agent] Output for: {input_text}"
    return state
