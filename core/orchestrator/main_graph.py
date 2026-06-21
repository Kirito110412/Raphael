from langgraph.graph import StateGraph, END
from core.orchestrator.state_schema import ProjectState
from core.orchestrator.node_handlers import (
    node_extract_intent,
    node_retrieve_memory,
    node_check_intelligence_preserve,
    node_route_task,
    agent_conversation_entry,
    agent_task_entry,
    node_debate_circuit,
    node_hitl_gate,
    node_synthesize_output,
    node_update_memory
)

def build_graph():
    workflow = StateGraph(ProjectState)

    workflow.add_node("extract_intent", node_extract_intent)
    workflow.add_node("retrieve_memory", node_retrieve_memory)
    workflow.add_node("check_intelligence_preserve", node_check_intelligence_preserve)
    workflow.add_node("route_task", node_route_task)

    workflow.add_node("agent_conversation", agent_conversation_entry)
    workflow.add_node("agent_task", agent_task_entry)

    workflow.add_node("debate_circuit", node_debate_circuit)

    workflow.add_node("hitl_gate", node_hitl_gate)
    workflow.add_node("synthesize_output", node_synthesize_output)
    workflow.add_node("update_memory", node_update_memory)

    workflow.set_entry_point("extract_intent")
    workflow.add_edge("extract_intent", "retrieve_memory")
    workflow.add_edge("retrieve_memory", "check_intelligence_preserve")
    workflow.add_edge("check_intelligence_preserve", "route_task")

    # Routing
    def route_to_agent(state: ProjectState) -> str:
        if state.get("routed_agent") == "conversation":
            return "agent_conversation"
        return "agent_task"

    workflow.add_conditional_edges("route_task", route_to_agent)

    workflow.add_edge("agent_conversation", "debate_circuit")
    workflow.add_edge("agent_task", "debate_circuit")

    workflow.add_edge("debate_circuit", "hitl_gate")
    workflow.add_edge("hitl_gate", "synthesize_output")
    workflow.add_edge("synthesize_output", "update_memory")
    workflow.add_edge("update_memory", END)

    return workflow.compile()

graph = build_graph()
