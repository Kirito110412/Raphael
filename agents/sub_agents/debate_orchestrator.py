from core.orchestrator.state_schema import ProjectState
from agents.sub_agents.generator_agent import generate_output
from agents.sub_agents.critic_agent import critique_output
from agents.sub_agents.synthesis_agent import synthesize_output

def run_debate_circuit(state: ProjectState) -> ProjectState:
    """Manages the generator -> critic loop (max 5 iterations)."""
    # Bypass debate completely for pure conversation
    if state.get("routed_agent") == "conversation":
        return state

    max_iterations = 5
    for iteration in range(max_iterations):
        state = generate_output(state)
        state = critique_output(state, iteration)

        if state.get("critic_verdict") == "approved":
            break

    return synthesize_output(state)
