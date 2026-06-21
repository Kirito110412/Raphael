from core.orchestrator.state_schema import ProjectState

def digital_worker_agent_node(state: ProjectState) -> ProjectState:
    """Stub implementation for digital_worker_agent."""
    input_text = state.get("user_input", "")
    state["agent_output"] = f"[digital_worker_agent] Output for: {input_text}"
    return state
