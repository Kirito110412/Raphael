from core.orchestrator.state_schema import ProjectState

def conversation_agent_node(state: ProjectState) -> ProjectState:
    """
    Handles everyday conversation.
    Fast path, no critic needed.
    """
    input_text = state.get("user_input", "")
    state["agent_output"] = f"Conversation response to: {input_text}"
    # Bypass critic directly for conversation
    state["final_output"] = state["agent_output"]
    return state
