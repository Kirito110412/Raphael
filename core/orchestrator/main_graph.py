from langgraph.graph import StateGraph, END
from core.orchestrator.state_schema import ProjectState
from core.orchestrator.node_handlers import (
    node_extract_intent,
    node_retrieve_memory,
    node_check_intelligence_preserve,
    node_route_task,
    node_hitl_gate,
    node_synthesize_output,
    node_update_memory,
    agent_conversation_entry,
    agent_task_entry
)

def build_graph():
    workflow = StateGraph(ProjectState)

    # Core Orchestration Nodes
    workflow.add_node("extract_intent", node_extract_intent)
    workflow.add_node("retrieve_memory", node_retrieve_memory)
    workflow.add_node("check_intelligence_preserve", node_check_intelligence_preserve)
    workflow.add_node("route_task", node_route_task)

    # Agent Nodes (Stubs)
    workflow.add_node("agent_conversation", agent_conversation_entry)
    workflow.add_node("agent_task", agent_task_entry)

    # Synthesis & Update Nodes
    workflow.add_node("hitl_gate", node_hitl_gate)
    workflow.add_node("synthesize_output", node_synthesize_output)
    workflow.add_node("update_memory", node_update_memory)

    # Define simple linear edges for stub Phase 1
    workflow.set_entry_point("extract_intent")
    workflow.add_edge("extract_intent", "retrieve_memory")
    workflow.add_edge("retrieve_memory", "check_intelligence_preserve")
    workflow.add_edge("check_intelligence_preserve", "route_task")

    # Routing logic will be conditional later, linear for now
    workflow.add_edge("route_task", "agent_conversation")
    workflow.add_edge("agent_conversation", "hitl_gate")
    workflow.add_edge("hitl_gate", "synthesize_output")
    workflow.add_edge("synthesize_output", "update_memory")
    workflow.add_edge("update_memory", END)

    return workflow.compile()

graph = build_graph()
