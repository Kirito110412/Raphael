from typing import TypedDict, Optional, List, Dict, Any

class ProjectState(TypedDict):
    # Input and session
    user_input: str
    session_id: str
    timestamp: str
    input_modality: str          # "text" | "voice" | "telegram" | "wake_word"

    # Memory
    l1_memory_blocks: dict       # Active memory blocks
    retrieved_context: list      # L2 BM25 + networkx retrieval results

    # Routing
    intent: str                  # semantic-router classification
    complexity_score: float      # 0.0–1.0 from complexity_classifier
    routed_agent: str            # Which domain agent handles this

    # Execution
    agent_output: str            # Raw output from domain agent
    critic_verdict: str          # "approved" | "rejected" | "revised"
    final_output: str            # Post-critic, post-synthesis output
    confidence_score: float      # Calibrated confidence from calibration_tracker

    # HITL
    pending_hitl: bool
    hitl_action: str
    hitl_approved: bool

    # Persona and mode
    detected_emotion: str
    detected_cognitive_state: str  # "flow" | "scattered" | "fatigued" | "creative" | "analytical"
    persona_mode: str              # One of 8 friend modes

    # Background signals
    background_alerts: list
    co_mode_directives: list
    project_updates: list

    # Intelligence preservation
    think_first_triggered: bool
    socratic_mode_active: bool
