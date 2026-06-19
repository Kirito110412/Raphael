from core.orchestrator.state_schema import ProjectState
from core.orchestrator.router import classify_intent, get_complexity_score
from agents.sub_agents.debate_orchestrator import run_debate_circuit
from agents.foreground.conversation_agent import conversation_agent_node
from agents.foreground.task_agent import task_agent_node

def node_extract_intent(state: ProjectState) -> ProjectState:
    text = state.get("user_input", "")
    state["intent"] = classify_intent(text)
    return state

def node_retrieve_memory(state: ProjectState) -> ProjectState:
    return state

def node_check_intelligence_preserve(state: ProjectState) -> ProjectState:
    return state

def node_route_task(state: ProjectState) -> ProjectState:
    text = state.get("user_input", "")
    state["complexity_score"] = get_complexity_score(text)
    intent = state.get("intent", "conversation")
    state["routed_agent"] = intent
    return state

def agent_conversation_entry(state: ProjectState) -> ProjectState:
    return conversation_agent_node(state)

def agent_task_entry(state: ProjectState) -> ProjectState:
    return task_agent_node(state)

def node_debate_circuit(state: ProjectState) -> ProjectState:
    return run_debate_circuit(state)

def node_hitl_gate(state: ProjectState) -> ProjectState:
    return state

def node_synthesize_output(state: ProjectState) -> ProjectState:
    if "final_output" not in state:
        state["final_output"] = state.get("agent_output", "Fallback Output")
    return state

def node_update_memory(state: ProjectState) -> ProjectState:
    return state
