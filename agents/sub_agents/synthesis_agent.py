from core.orchestrator.state_schema import ProjectState

def synthesize_output(state: ProjectState) -> ProjectState:
    """Integrates debate outcome into final deliverable."""
    state["final_output"] = f"Synthesized Final: {state.get('agent_output', '')}"
    return state
