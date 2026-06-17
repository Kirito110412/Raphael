# [PROJECT_NAME] — AGENT INTERACTION MAP
**Version:** 1.0.0 — Complete and Locked  
**Prepared by:** Planning AI  
**Intended reader:** AI Coding System  
**Status:** Final — Do not alter

---

> **SYSTEM INSTRUCTION TO CODING AI:** This document maps exactly how every agent in [PROJECT_NAME] interacts with every other agent, how data flows between them, how concurrency is managed, and where HITL gates are placed. Every diagram and every description here is binding. Implement the exact interaction patterns shown.

---

## 1. HIERARCHICAL OVERVIEW

The [PROJECT_NAME] agent system is a four-layer hierarchy. Understanding the direction of authority and data flow between layers is critical to correct implementation.

**Layer 1 — Primary Orchestrator (Foreground):**  
The single always-running foreground process. It is the only entity that communicates directly with the user. It receives all user input, dispatches to domain agents, receives results, synthesises output, and delivers responses. It runs in the main foreground thread. It never waits for background agents — it receives their outputs via a thread-safe queue at the start of each new user interaction.

**Layer 2 — Domain Agents (Specialised):**  
Spawned by the orchestrator in response to specific intents. Each handles a specific domain of expertise. They can spawn sub-agents (Layer 3) to handle complex multi-step reasoning. They return their result to the orchestrator when complete. They do not communicate with each other directly — all inter-domain communication goes through the orchestrator's shared state.

**Layer 3 — Sub-agents (Adversarial Debate Circuit):**  
Spawned by domain agents for any output classified as "important." Three sub-agents: Generator (produces output), Critic (attacks output), Synthesis (integrates surviving elements). This circuit guarantees the absolute honesty mandate. Sub-agents do not access memory directly — they receive all context from their parent domain agent.

**Layer 4 — Sub-sub-agents (Atomic Task Workers):**  
Spawned by domain agents for single-focus atomic operations. One task, one result, no sub-spawning. Lightweight LangGraph subgraphs. Examples: analyse one academic paper, scan one network port, process one stock ticker, transcribe one meeting segment.

**Concurrent Background Runtime (Independent):**  
Four background agents run as asyncio tasks in a separate background thread — completely independent of the foreground orchestrator. They push results to the orchestrator via a thread-safe `queue.Queue`. They NEVER call into the foreground thread directly. They NEVER block waiting for foreground responses.

**How an atomic task bubbles up from Layer 4 to Layer 1:**
```
Layer 4 sub-sub-agent completes atomic task
→ Returns result dict to parent Layer 3 sub-agent (or directly to Layer 2 domain agent)
→ Layer 3 sub-agents debate and synthesise (if adversarial circuit was active)
→ Layer 2 domain agent receives synthesis, does any final domain-specific processing
→ Domain agent returns updated state to Layer 1 orchestrator
→ Layer 1 orchestrator runs node_synthesize_output → node_update_memory → delivers to user
```

---

## 2. THE MULTI-AGENT STATE GRAPH

```mermaid
graph TD
    %% Input Sources
    UserText[User Text Input] --> FastAPI
    UserVoice[User Voice / Wake Word] --> Whisper
    Whisper --> FastAPI
    TelegramMsg[Telegram Message/Audio] --> TelegramBot
    TelegramBot --> FastAPI
    FastAPI --> node_extract_intent

    %% Core Orchestrator Foreground Flow
    node_extract_intent -->|Intent + Complexity| node_retrieve_memory
    node_retrieve_memory -->|L2 BM25 + networkx context| node_check_intelligence_preserve
    node_check_intelligence_preserve -->|Think-first gate triggered| UserOutput
    node_check_intelligence_preserve -->|Proceed| node_route_task

    %% Routing to Domain Agents
    node_route_task -->|conversation / simple| agent_conversation_entry
    node_route_task -->|security task| agent_security_entry
    node_route_task -->|finance / investment| agent_finance_entry
    node_route_task -->|content creation| agent_content_entry
    node_route_task -->|research / deep dive| agent_research_entry
    node_route_task -->|tutoring / learning| agent_tutoring_entry
    node_route_task -->|computer task / actuation| agent_digital_worker_entry
    node_route_task -->|level 6 discovery| agent_discovery_entry
    node_route_task -->|skill creation| node_skill_forge_entry
    node_route_task -->|project query| agent_project_manager_entry
    node_route_task -->|health management| agent_health_entry
    node_route_task -->|legal research| agent_legal_entry
    node_route_task -->|travel planning| agent_travel_entry
    node_route_task -->|negotiation| agent_negotiation_entry

    %% Conversation Agent (simple path - no critic needed)
    agent_conversation_entry --> node_synthesize_output

    %% Domain Agents → Adversarial Debate Circuit
    agent_security_entry --> subagent_generator
    agent_finance_entry --> subagent_generator
    agent_content_entry --> subagent_generator
    agent_research_entry --> subagent_generator
    agent_tutoring_entry --> subagent_generator
    agent_digital_worker_entry --> subagent_generator
    agent_discovery_entry --> subagent_generator
    agent_project_manager_entry --> subagent_generator

    %% Adversarial Debate Circuit
    subagent_generator -->|Proposed output| subagent_critic
    subagent_critic -->|Objections found - iterate| subagent_generator
    subagent_critic -->|Approved after debate| subagent_synthesis
    subagent_synthesis --> node_hitl_gate

    %% HITL Gate
    node_hitl_gate -->|Non-destructive output| node_synthesize_output
    node_hitl_gate -->|Destructive action - interrupt()| UserApproval[User Approval Request]
    UserApproval -->|Approved| node_execute_host
    UserApproval -->|Rejected| node_synthesize_output
    node_execute_host --> node_synthesize_output

    %% Skill Forge Path
    node_skill_forge_entry --> node_execute_sandbox
    node_execute_sandbox --> node_verify_pytest
    node_verify_pytest -->|All tests pass| node_hitl_gate
    node_verify_pytest -->|Tests fail - attempt 1| node_execute_sandbox
    node_verify_pytest -->|Tests fail - attempt 2| node_execute_sandbox
    node_verify_pytest -->|Tests fail - attempt 3| node_execute_sandbox
    node_verify_pytest -->|All 3 failed| node_synthesize_output

    %% Computer Vision + Actuation Path
    agent_digital_worker_entry --> node_execute_vision
    node_execute_vision --> node_execute_actuation
    node_execute_actuation --> node_verify_result
    node_verify_result -->|Success| node_synthesize_output
    node_verify_result -->|Failed - retry| node_execute_vision

    %% Output and Memory Update
    node_synthesize_output --> node_update_memory
    node_update_memory --> UserOutput[Response to User]

    %% Background Agents - async, non-blocking, push only
    BG_CO[CO-Mode Agent<br/>background/co_mode_agent.py]
    BG_Monitor[Proactive Monitor<br/>background/proactive_monitor.py]
    BG_Sleep[Sleep Agent<br/>background/sleep_agent.py]
    BG_Projects[Project Manager<br/>background/project_manager_agent.py]

    BG_CO -.->|Push daily plan via queue| node_route_task
    BG_Monitor -.->|Push alerts via queue| node_route_task
    BG_Sleep -.->|Push sleep complete via queue| node_route_task
    BG_Projects -.->|Push project updates via queue| node_route_task

    %% Sub-sub-agents spawned by domain agents
    agent_security_entry -.->|Spawn for atomic task| SSA_Security[Sub-sub-agent<br/>e.g. single port analysis]
    agent_research_entry -.->|Spawn for atomic task| SSA_Research[Sub-sub-agent<br/>e.g. single paper extract]
    agent_finance_entry -.->|Spawn for atomic task| SSA_Finance[Sub-sub-agent<br/>e.g. single stock analysis]
    SSA_Security -.->|Return result| agent_security_entry
    SSA_Research -.->|Return result| agent_research_entry
    SSA_Finance -.->|Return result| agent_finance_entry

    %% Memory System (accessed by orchestrator nodes)
    L1[L1 Active Memory Blocks<br/>LangGraph State Dict]
    L2[L2 BM25 Index + networkx<br/>l2_index.py]
    L3[L3 Obsidian Vault<br/>Plain Markdown Files]

    node_retrieve_memory <-->|Read| L1
    node_retrieve_memory -->|BM25 Query| L2
    L2 -->|Retrieved docs| node_retrieve_memory
    L2 <-->|Read/Write| L3
    node_update_memory -->|Write new facts| L3
    node_update_memory -->|Update index| L2
    node_update_memory -->|Update blocks| L1
```

---

## 3. CONCURRENCY AND BACKGROUND PROCESSES

This section defines exactly how the four background agents operate without causing race conditions, blocking the foreground orchestrator, or corrupting shared memory state.

### 3.1 Threading Architecture

```
MAIN THREAD:
  └── FastAPI daemon (uvicorn, asyncio event loop)
       └── LangGraph StateGraph (foreground orchestrator)
            └── All domain agents, sub-agents (spawned within same event loop)

BACKGROUND THREAD:
  └── asyncio.new_event_loop() (dedicated background event loop)
       ├── co_mode_agent (asyncio task)
       ├── proactive_monitor (asyncio task)
       ├── sleep_agent (asyncio task - idle triggered)
       └── project_manager_agent (asyncio task)

COMMUNICATION CHANNEL:
  └── queue.Queue (thread-safe) — background thread pushes, foreground thread reads
       Each message: {source: str, type: str, payload: dict, priority: int, timestamp: str}
```

The background thread is started during system initialisation (`bootstrap/first_run.py` → `main.py`). It runs its own asyncio event loop entirely independently of the main thread. It has no direct reference to the LangGraph StateGraph instance running in the main thread.

### 3.2 Memory Access Without Race Conditions

**L1 Memory (LangGraph State Dict):**  
L1 memory blocks exist only within the LangGraph state — they are per-session, in-memory Python dictionaries. Background agents do NOT access L1 directly. If a background agent needs to know something from the current user state (e.g., the CO-mode agent needs to know the user's current active task), it reads from L3 vault (specifically `config/USER.md`) which is a file on disk, not the in-memory LangGraph state.

**L2 Memory (BM25 Index + networkx Graph):**  
L2 is accessed by both foreground (reads) and background (reads and writes during sleep cycle). Race condition prevention:
- `l2_index.py` uses a `threading.RLock` (reentrant lock) wrapping all read and write operations
- The sleep agent acquires this lock before any consolidation write operations
- The foreground orchestrator acquires a read lock during `node_retrieve_memory` (non-blocking for concurrent reads)
- Write operations by the sleep agent acquire exclusive lock — foreground reads queue behind it (sleep writes are fast, typically < 500ms per operation)
- `[IMPLEMENTATION_DETAIL: Consider using filelock library for cross-process safety if running as multiple processes]`

**L3 Memory (Obsidian Vault Files):**  
L3 is the most accessed layer. Both foreground and background read and write to vault files. Race condition prevention:
- Each vault file has a corresponding `.lock` file managed by the `filelock` library
- `l3_vault.py` acquires the file lock before every read and write operation
- Lock timeout: 5 seconds (if lock not acquired in 5 seconds, operation retries after 100ms)
- Sleep agent does bulk operations with individual file locks per file (not a global vault lock — maximises concurrency)
- Git commit in sleep cycle uses a global vault lock for the duration of the commit + push operation

### 3.3 Background Agent Interaction Patterns

**CO-mode agent (`agents/background/co_mode_agent.py`):**
```
Reads from:
  → vault/projects/* (project status)
  → config/USER.md (quests, rhythm data, co_mode_status)
  → External sources via visual computer control (calendar, WhatsApp, email, Instagram)
  → proactive_monitor queue (alert feed)

Writes to:
  → Pushes to foreground queue: {source: "co_mode", type: "daily_plan", payload: {plan: list}}
  → Does NOT write to vault (vault writes happen via foreground orchestrator after user acknowledgement)

Scheduling:
  → Daily planning: asyncio.create_task with scheduled time
  → Real-time updates: monitors for task completion signals via FastAPI internal event bus
```

**Proactive monitor (`agents/background/proactive_monitor.py`):**
```
Reads from:
  → config/USER.md (active projects, quest topics, portfolio holdings)
  → External news/data sources (web requests — outbound only, no sensitive data)
  → vault/projects/* (what topics to monitor)

Writes to:
  → Pushes alerts to foreground queue: {source: "monitor", type: "alert", payload: {alert: dict}}
  → For URGENT alerts: also sends Telegram notification directly via telegram_bot.py

Scheduling:
  → Check interval: asyncio.sleep(configured_interval) in a while True loop
  → Never blocks — uses asyncio.gather for concurrent source fetching
```

**Sleep agent (`agents/background/sleep_agent.py`):**
```
Reads from:
  → All of L3 vault
  → Langfuse logs (for weekly fine-tuning data collection)
  → vault/projects/* (for dream synthesis problem list)

Writes to:
  → L3 vault (consolidation, compression, archival) — with file locks
  → L2 index (re-indexing after consolidation) — with RLock
  → config/USER.md (intelligence_growth_log update)
  → Git repository (commit + push)

Scheduling:
  → Triggered by inactivity detection: asyncio.sleep(30_minutes) in monitoring loop
  → Inactivity confirmed if: no FastAPI request received in last 30 minutes
  → Cannot be interrupted once started (blocking background operations queue while running)
  → Pushes completion signal to foreground queue when done: {source: "sleep", type: "cycle_complete", payload: {summary}}
```

**Project manager (`agents/background/project_manager_agent.py`):**
```
Reads from:
  → vault/projects/* (task queues, plan files, blocker logs)
  → compute/local_checker.py (resource availability)
  → foreground queue (user answers to blockers)

Writes to:
  → vault/projects/* (task completion, proposals, plan updates)
  → Pushes to foreground queue: project updates, blocker questions, plan changes

Scheduling:
  → Resource check: asyncio.sleep(15_minutes) polling loop
  → Task execution: spawns domain agent tasks only when resources confirm availability
  → Spawned tasks run as sub-asyncio-tasks within background event loop
  → Domain agents spawned here operate without foreground orchestrator involvement
```

---

## 4. HUMAN-IN-THE-LOOP (HITL) GATES

HITL gates are implemented via LangGraph's `interrupt()` function. When `interrupt()` is called, the graph execution pauses and the current state is persisted via `MemorySaver`. Execution resumes only when the user provides explicit input through any channel (API, voice, Telegram). HITL gates are NOT popups or notifications that can be dismissed accidentally — they are hard execution pauses.

### 4.1 Complete HITL Gate Inventory

**HITL Gate 1 — New skill installation (mandatory, no exceptions):**
```
File: skills/forge/hitl_gate.py
Trigger: Skill passes pytest verification (3/3 test pass)
Pause point: Before writing skill file to vault/skills/
Presented to user:
  - Skill name and description
  - Full source code (readable)
  - Test cases and results
  - What file system locations it can access
  - What network access it requests (should be none by default)
  - Risk classification: low / medium / high
User options: APPROVE / REJECT / MODIFY (requests changes before re-evaluation)
On approval: skill written to vault/skills/, health record created, L2 index updated
On rejection: candidate code discarded, user can describe desired changes for new generation attempt
```

**HITL Gate 2 — Code execution on host (after sandbox, before host):**
```
File: core/orchestrator/main_graph.py → node_hitl_gate
Trigger: Any code execution request that has passed sandbox testing and requires host execution
Pause point: Between sandbox pass and host execution
Presented to user:
  - What the code will do on the host
  - Which files it will read/write/delete
  - What system resources it will use
  - Reversibility assessment: reversible / irreversible
User options: APPROVE / REJECT
On approval: node_execute_host runs code on host
On rejection: execution cancelled, user informed of what was not executed
```

**HITL Gate 3 — Destructive computer actions:**
```
File: actuation/apps/app_controller.py → escalation trigger
Trigger: Visual control is about to take an action classified as "destructive" by Guardrails AI
  Examples: clicking Delete, clicking Uninstall, clicking Send on a large financial transaction, confirming account closure
Pause point: Before pyautogui click is executed
Presented to user:
  - What element is about to be clicked
  - What the expected consequence is
  - Screenshot showing the current screen state
  - Reversibility assessment
User options: PROCEED / CANCEL
On proceed: click executes
On cancel: mouse moves away from element, no click
```

**HITL Gate 4 — Outbound calls and messages on user's behalf:**
```
File: communication/voip_caller.py, communication/telegram_bot.py
Trigger: System is about to initiate an outbound call OR send a message as the user to a third party
Pause point: Before call is placed or message is sent
Presented to user:
  - Who is being called/messaged
  - What will be said (full script or message content)
  - Purpose and expected outcome
User options: APPROVE / MODIFY / CANCEL
On approve: communication proceeds
On modify: user edits content, modified version sent
On cancel: communication cancelled
Note: This gate can be pre-approved for specific routine communication types (e.g., appointment reminders to specific numbers) via POST /config
```

**HITL Gate 5 — Financial transactions:**
```
File: agents/domain/finance_agent.py
Trigger: Any trade execution, payment, or financial transfer above configurable threshold
Pause point: Before broker API call or payment execution
Presented to user:
  - Transaction type (buy/sell/transfer/payment)
  - Amount and asset
  - Platform/broker
  - Why this trade/payment was triggered (rule or agent reasoning)
  - Estimated cost/gain
User options: EXECUTE / CANCEL / MODIFY SIZE
On execute: broker API call made
On cancel: transaction logged but not executed
```

**HITL Gate 6 — Multi-year project plan changes:**
```
File: agents/background/project_manager_agent.py
Trigger: World event causes significant plan adaptation (not minor adjustments — major structural changes)
Pause point: Before new plan replaces old plan in vault
Presented to user:
  - What world event triggered the change
  - What changed in the plan (diff format: old → new)
  - Why the old approach is now suboptimal
  - Confidence in the new approach (calibrated score)
User options: APPROVE / REJECT / DISCUSS
On approve: new plan saved to vault, project_manager continues with new plan
On reject: old plan kept, flag added noting user reviewed but retained old plan
On discuss: conversation initiated to refine plan before committing
```

**HITL Gate 7 — Skill self-modification (MCP server auto-creation):**
```
File: skills/mcp/server_factory.py
Trigger: System determines a new MCP server needs to be created for a capability gap
Pause point: Before new MCP server code is written and registered
Presented to user:
  - What capability gap the MCP server addresses
  - What the server will expose (tool names, permissions required)
  - Source code of the generated server
User options: APPROVE / REJECT
Same install flow as Skill Forge after approval
```

**HITL Gate 8 — CO-mode holiday evaluation (non-standard cases):**
```
File: growth/co_mode_evaluator.py
Trigger: Holiday request received that falls into Category C (repeated pattern, suspicious timing)
Pause point: Before evaluating as approved or denied
Presented to user:
  - Pattern summary ("You've requested fatigue breaks 3 times this week")
  - Quest progress data ("Your main quest has advanced 0% in the last 5 days")
  - Request for more specific reason OR acknowledgement of the pattern
User options: Provide specific reason / Accept reduced-load plan / Withdraw request
```

### 4.2 HITL State Persistence

When `interrupt()` is called, LangGraph's `MemorySaver` persists the complete current state to disk. This ensures:
- If the user does not respond for hours, the system does not lose context
- When the user responds (via any channel — text, voice, Telegram), execution resumes from exactly where it paused
- Multiple pending HITL gates can queue up — user sees them in priority order when they return
- State persistence file location: `[IMPLEMENTATION_DETAIL: use configurable path in settings.yaml]`

---

## 5. AGENT SPAWNING PATTERNS

### 5.1 When Agents Are and Are Not Spawned

**Always running (permanent):**
- `core/orchestrator/main_graph.py` — Primary orchestrator (foreground)
- `agents/background/co_mode_agent.py` — Background (when CO mode is active)
- `agents/background/proactive_monitor.py` — Background (always)
- `agents/background/project_manager_agent.py` — Background (when active projects exist)

**Spawned on demand by orchestrator (foreground domain agents):**
- All agents in `agents/domain/` — spawned per interaction, live for duration of task, terminate on result return
- All agents in `agents/foreground/` — spawned per interaction

**Spawned on demand by domain agents:**
- `subagent_critic`, `subagent_generator`, `subagent_synthesis` — for every important output
- Layer 4 sub-sub-agents — for atomic tasks within domain agent workflows

**Sleep agent:**
- Spawned by inactivity detection logic in the background event loop
- Runs as a one-shot asyncio task, terminates on completion

### 5.2 Sub-agent Spawning Threshold — When the Critic Fires

NOT every output goes through the adversarial debate circuit. The critic circuit adds latency and is reserved for outputs where correctness matters significantly. Classification happens in `node_route_task`:

**Critic IS triggered (important outputs):**
- Security vulnerability findings and reports
- Financial recommendations and trade signals
- Medical or health information (health_agent.py — all outputs mandatory)
- Legal analysis or contract review (legal_agent.py — all outputs mandatory)
- Negotiation strategy and real-time coaching (negotiation_agent.py — strategy outputs mandatory)
- Travel bookings above a cost threshold (travel_agent.py — configurable threshold)
- Scientific discovery outputs (all Level 6 outputs mandatory)
- Multi-year project plan decisions
- Any output with a factual claim about the real world that has consequences

**Critic is NOT triggered (routine outputs):**
- Casual conversation responses
- Simple factual lookups (what is X, define Y)
- Formatting tasks (reformat this text)
- Creative tasks where correctness is not applicable
- Status queries (what tasks do I have today)
- Simple code completion for low-risk scripts

This classification prevents the critic circuit from adding unnecessary latency to everyday interactions while guaranteeing it runs on all high-stakes outputs.

---

## 6. INTER-AGENT DATA CONTRACT

All agents communicate exclusively through the LangGraph state dictionary (`ProjectState`). No agent calls another agent's methods directly. No agent imports from another agent's file. This is the strict rule that prevents coupling and circular dependencies.

**What each agent receives (reads from state):**
- `user_input` — the original user request
- `l1_memory_blocks` — current active memory
- `retrieved_context` — L2 BM25 + networkx results
- `intent` — classified intent
- `detected_emotion` — current emotional state
- `detected_cognitive_state` — current cognitive state
- Agent-specific: domain agents receive only the subset of state relevant to their domain

**What each agent returns (writes to state):**
- `agent_output` — the raw output from the domain agent
- Any state fields it updated during execution (e.g., updated project status, new person profile)

**What sub-agents receive:**
- The `agent_output` from their parent domain agent as their input
- The `retrieved_context` as supporting material
- Nothing else — sub-agents are context-clean

**What background agents push (to queue, not to state):**
- `{source, type, payload, priority, timestamp}` — structured message dict
- The foreground orchestrator merges queue messages into state at the start of each new interaction

---

*End of AGENT_INTERACTION_MAP.md — Version 1.0.0*
