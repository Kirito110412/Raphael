from core.orchestrator.state_schema import ProjectState

def generate_output(state: ProjectState) -> ProjectState:
    """Produces proposed outputs and solutions."""
    input_text = state.get("user_input", "")
    agent_output = state.get("agent_output", f"Generated solution for {input_text}")

    # If revised by critic, append revision tag
    if state.get("critic_verdict") == "revised":
        agent_output += " (Revised after critique)"

    state["agent_output"] = agent_output
    return state
