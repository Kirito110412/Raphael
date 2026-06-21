from core.orchestrator.state_schema import ProjectState

def task_agent_node(state: ProjectState) -> ProjectState:
    """
    Handles immediate task execution requests.
    Routes to critic sub-agent after generation.
    """
    input_text = state.get("user_input", "")
    state["agent_output"] = f"Task execution proposal for: {input_text}"
    return state
