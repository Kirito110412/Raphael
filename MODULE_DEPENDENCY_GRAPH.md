# [PROJECT_NAME] — MODULE DEPENDENCY GRAPH
**Version:** 1.0.0 — Complete and Locked  
**Prepared by:** Planning AI  
**Intended reader:** AI Coding System  
**Status:** Final — Do not alter

---

> **SYSTEM INSTRUCTION TO CODING AI:** This document maps every technical dependency between every module in [PROJECT_NAME]. It defines exactly which library handles which function, how data flows from the user's mouth to the computer's action, and how the memory pipeline moves information through three tiers. Implement exactly what is shown — no substitutions, no additions to the core dependency graph.

---

## 1. DATA FLOW: USER INPUT TO EXECUTION

This section traces the complete technical journey of a request from the moment it enters the system to the moment an action is taken or a response is delivered. Every library at every step is named.

### 1.1 Voice Input Path

```
USER SPEAKS
    ↓
[communication/voice/wake_word.py]
  Library: pvporcupine (wake word detection) OR silero-vad (voice activity detection)
  Function: Continuously monitors microphone at ~2% CPU
  Output: Audio buffer (raw PCM bytes) when wake word + speech detected
    ↓
[communication/voice/stt.py]
  Library: openai-whisper (local, fine-tuned Hinglish checkpoint)
  Function: Speech → text transcription
  Output: Transcript string + detected language tag
    ↓
[interfaces/api/main.py → POST /task]
  Library: FastAPI (uvicorn ASGI server)
  Input: {input: transcript, modality: "voice"}
    ↓
[core/persona/emotional_detector.py]  ← runs in parallel with STT
  Library: custom pattern analysis (no external library needed)
  Input: Audio characteristics (pace, energy) extracted before STT
  Output: detected_emotion string → written to LangGraph state
    ↓
[core/persona/cognitive_state_detector.py]  ← runs in parallel
  Library: custom analysis of speech pace, pause frequency
  Output: detected_cognitive_state string → written to LangGraph state
    ↓
CONTINUES AS TEXT INPUT PATH (see 1.2 below)
```

### 1.2 Text Input Path (all modalities converge here)

```
TEXT INPUT RECEIVED (from voice transcript, direct text, Telegram, API)
    ↓
[core/orchestrator/main_graph.py → node_extract_intent]
  Library: semantic-router (Aurelio Labs)
  Configuration: Hinglish-trained intent vectors loaded from config/
  Output: intent string (e.g., "security", "finance", "conversation")
  Also: confidence score — if < 0.85, clarification question returned to user before continuing
    ↓
[core/orchestrator/main_graph.py → node_retrieve_memory]
  ┌─────────────────────────────────────────────────────────┐
  │ L1 Read (instant, always in state):                     │
  │   core/memory/l1_active.py                              │
  │   Library: pure Python dict operations                  │
  │   Output: active memory blocks dict                     │
  │                                                         │
  │ L2 BM25 Search:                                         │
  │   core/memory/l2_index.py                               │
  │   Library: rank_bm25 (BM25Okapi)                        │
  │   Input: user_input string → tokenised query            │
  │   Output: top 10 most relevant vault document paths     │
  │                                                         │
  │ L2 Graph Expansion:                                     │
  │   core/memory/l2_index.py                               │
  │   Library: networkx (DiGraph)                           │
  │   Input: entity names extracted from top 10 docs        │
  │   Output: one-hop neighbour documents and entities      │
  │                                                         │
  │ L3 Document Read:                                       │
  │   core/memory/l3_vault.py                               │
  │   Library: pathlib + python-frontmatter (YAML parse)    │
  │   Input: file paths from BM25 + graph expansion         │
  │   Output: document content strings                      │
  └─────────────────────────────────────────────────────────┘
  Combined output → retrieved_context list → written to LangGraph state
    ↓
[growth/intelligence_preserver.py → node_check_intelligence_preserve]
  Library: pure Python logic + LangGraph state reads
  Checks: over_reliance_flags from USER.md, detected_cognitive_state, query type
  Decision: proceed | trigger think-first gate | activate Socratic mode
    ↓
[core/orchestrator/router.py → node_route_task]
  Library: semantic-router (already classified in node_extract_intent)
  Additional: core/inference/complexity_classifier.py
    Library: small local LLM call via llama.cpp (lightweight classification prompt)
    Output: complexity_score float 0.0–1.0
  Routing decision: local model OR cloud model OR specific domain agent
    ↓
[core/inference/cloud_router.py OR core/inference/local_model.py]
  Cloud: LiteLLM → configured cloud provider (OpenAI / Anthropic / Google)
    Library: litellm
    PII check: interfaces/api/middleware/pii_scrubber.py runs BEFORE any cloud call
      Library: presidio-analyzer + presidio-anonymizer (Microsoft, free, local)
  Local: llama.cpp via llama-cpp-python Python bindings
    Library: llama-cpp-python
    ↓
[Domain agent subgraph executes — see Section 1.3]
    ↓
[agents/sub_agents/critic_agent.py → subagent_critic]
  Library: LangGraph subgraph + LLM call (same routing as above)
  Input: proposed output from domain agent
  Output: "approved" | "rejected" + specific objections
    ↓
[agents/sub_agents/synthesis_agent.py → subagent_synthesis]
  Library: LangGraph subgraph + LLM call
  Input: approved output after debate convergence
  Output: final formatted response with confidence score
    ↓
[core/orchestrator/main_graph.py → node_hitl_gate]
  Library: LangGraph interrupt() + MemorySaver (state persistence)
  Condition: only if output involves destructive/irreversible action
  If triggered: state serialised to disk, execution paused, user notified
    ↓
[core/persona/mode_selector.py]
  Library: pure Python logic, reads SOUL.md, EMPATHY.md, RATIONAL.md via pathlib
  Input: detected_emotion + detected_cognitive_state + context signals
  Output: selected persona mode string
    ↓
[core/persona/voice_modulator.py]
  Library: pure Python parameter dict generation
  Output: TTS parameter overrides for selected mode
    ↓
[core/orchestrator/main_graph.py → node_synthesize_output]
  Library: LLM call for final formatting (local model)
  Input: synthesised content + persona mode + voice parameters
  Output: response string formatted for persona mode
    ↓
[communication/voice/tts_standard.py OR communication/voice/tts_emotional.py]
  Standard: kokoro (Kokoro-82M TTS model)
    Library: kokoro-onnx or kokoro Python package
  Emotional (high-emotion register responses):
    Library: TTS (Coqui XTTS via coqui-tts package)
  Output: audio bytes → played through sounddevice or pyaudio
    ↓
RESPONSE DELIVERED TO USER
```

### 1.3 Domain Agent Execution (Computer Vision + Actuation Subpath)

```
agent_digital_worker_entry (or any domain agent requiring computer control)
    ↓
[actuation/vision/screen_capture.py]
  Library: PIL/Pillow (screenshot capture via ImageGrab)
  Output: PIL Image object → held in memory ONLY, never written to disk unless explicit command
    ↓
[actuation/vision/qwen_vl.py]
  Library: transformers (HuggingFace) + local Qwen3-VL model weights
  Input: PIL Image + task description prompt
  Output: JSON with identified elements and bbox_2d coordinates
    [{element_type, text_content, bbox_2d: [x1,y1,x2,y2], confidence}]
    ↓
[actuation/vision/element_locator.py]
  Library: pure Python geometry
  Input: bbox_2d list + target element description
  Output: click coordinates (cx, cy) + display scaling adjustment
    ↓
[actuation/control/mouse_controller.py]
  Libraries:
    human_mouse (bezier curve generation — sarperavci/human_mouse)
    pyautogui (actual mouse movement execution)
  Input: target coordinates
  Process:
    1. human_mouse.move_to(cx, cy) → generates bezier path with realistic acceleration
    2. pyautogui executes movement along path
    3. pyautogui.click() with randomised press duration
  Output: click executed
    ↓
[actuation/control/keyboard_controller.py]  (if text input needed)
  Libraries:
    pyautogui (keyboard input)
    random (inter-key delay randomisation)
  Process: type character by character with 50-180ms random delays
    ↓
[actuation/vision/screen_capture.py] (verification screenshot)
    ↓
[actuation/vision/qwen_vl.py] (verify expected state change occurred)
    ↓
Result returned to domain agent → continues agent workflow
```

### 1.4 Skill Forge Execution Path

```
Need identified by domain agent OR user request
    ↓
[skills/forge/generator.py]
  Library: LLM call (local model)
  Input: skill description + context
  Output: Python function code (string)
    ↓
[skills/forge/sandbox.py]
  Library: docker (Docker Python SDK)
  Process:
    docker.from_env().containers.run(
      image="skill_sandbox:latest",
      command=f"python /tmp/sandbox/skill_candidate.py",
      network_disabled=True,
      mem_limit="512m",
      cpu_period=100000,
      cpu_quota=100000,
      read_only=True,
      tmpfs={"/tmp": ""},
      user="1000",
      remove=True,
      timeout=30
    )
  Output: stdout, stderr, exit_code
    ↓
[skills/forge/verifier.py]
  Library: pytest (via subprocess call inside container)
  Input: captured stdout/stderr/exit_code
  Decision: PASS | FAIL
    ↓ (if FAIL)
[skills/forge/repair_loop.py]
  Library: LLM call with error trace as context
  Iteration count tracked (max 3)
  Output: repaired Python function code → loops back to sandbox.py
    ↓ (if PASS or after 3 iterations)
[skills/forge/hitl_gate.py]
  Library: LangGraph interrupt()
  If PASS: present to user for approval
  If 3 failures: notify user of abandonment
    ↓ (on approval)
[skills/library/skill_registry.py]
  Library: pathlib + python-frontmatter + yaml
  Process: write skill file to vault/skills/, create health YAML, update L2 index
    ↓
[skills/mcp/server_factory.py]  (if MCP wrapping requested)
  Library: FastMCP
  Process: auto-generate MCP server wrapping the skill function
  Register new server with MCP client
```

### 1.5 Security Research Execution Path

```
Security task received
    ↓
[security/tool_orchestrator.py]
  Checks: authorization record for target (vault/security/authorizations/)
  If no authorization: block and request confirmation
    ↓
[actuation/apps/app_controller.py]
  Visual control of security tool (Nmap, Burp Suite, Ghidra, etc.)
  Library: actuation stack (screen_capture → qwen_vl → mouse/keyboard)
    ↓
Tool output captured via:
  [actuation/vision/screen_capture.py] + [actuation/vision/qwen_vl.py]
  Library: pytesseract (OCR for terminal output if visual extraction needed)
    OR
  subprocess capture (for CLI tools called directly by Python)
    ↓
[agents/domain/security_agent.py]
  Processes tool output
  Spawns sub-sub-agents for each finding
  Adversarial debate via critic circuit for each vulnerability report
    ↓
[security/sandboxer.py] (for exploit testing and malware analysis)
  Library: docker (Docker Python SDK)
  Malware sandbox: different Dockerfile with forensics tools pre-installed
    ↓
Report generated → saved to vault/security/
```

---

## 2. MEMORY ARCHITECTURE PIPELINE

### 2.1 The Three-Tier Memory Data Flow

```
NEW INFORMATION ENTERS SYSTEM
(from any interaction, research, or background process)
         ↓
[core/memory/extractor.py]
  Library: LLM call (local model) for classification
  Classification into:
    Class A → Important, write to L3 immediately
    Class B → Session memory, write compressed version to L3
    Class C → Ephemeral, hold in L1 for session only
    Class D → Irrelevant, schedule for deletion at next sleep cycle
         ↓
    [Class A path]           [Class B path]      [Class C path]     [Class D path]
         ↓                        ↓                   ↓                  ↓
  [core/memory/l3_vault.py]  [Hold in L1]       [Hold in L1]      [Tag for deletion]
  Library: pathlib            L1 only             L1 only           in L1 state
  + python-frontmatter
  + yaml
  Write to appropriate
  vault subdirectory as
  .md file with YAML
  frontmatter
         ↓
  [core/memory/l2_index.py — BM25 update]
  Library: rank_bm25 (BM25Okapi)
  Process: tokenise new document → add to BM25 index
  In-memory index rebuilt from vault file paths list
  (BM25 index is rebuilt from scratch on each system start — fast, no persistence needed)
         ↓
  [core/memory/l2_index.py — networkx update]
  Library: networkx (DiGraph)
  Process:
    1. Entity extraction from new document (LLM or spaCy NER)
    2. For each entity: add node if not exists
    3. Add edge: document_node --contains--> entity_node
    4. Check for relationships with existing entities: add edges
    5. Temporal edges: if entity exists with different value,
       add end_date to old edge, add new edge with start_date
  Graph persisted to disk: vault/.graph/knowledge_graph.pkl
  Library: pickle (networkx built-in serialisation)
```

### 2.2 Sleep Cycle Memory Transformation Pipeline

```
SLEEP CYCLE TRIGGERED (30 min inactivity)
         ↓
Phase 1: CONSOLIDATION
[core/memory/sleep_cycle.py]
  Library: rank_bm25 (pairwise similarity between modified nodes)
  Process:
    → Load all nodes modified since last_sleep_timestamp
    → For each pair: compute BM25 similarity score
    → If similarity > 0.85: merge (keep longer node, absorb unique sentences from shorter)
    → Delete merged-from node, redirect all networkx edges to surviving node
    → Update L2 index (remove deleted document, update surviving document)
         ↓
Phase 2: TIME-DECAY
  Library: datetime (Python standard library)
  Process:
    → For every vault node: read last_accessed from YAML frontmatter
    → decay_score = 1.0 / (1.0 + 0.1 * days_since_last_access)
    → If decay_score < 0.1 AND node NOT in any active project AND NOT in research/ or skills/:
      → Move to vault/archive/ (pathlib.rename)
      → Remove from L2 BM25 index
      → Isolate in networkx (edges preserved but node flagged as archived)
         ↓
Phase 3: COMPRESSION
  Library: LLM call (local model) + pathlib
  Process:
    → Find all Class B session memory entries (tagged in YAML frontmatter)
    → For each: LLM generates one-line summary
    → Write summary to vault as compressed entry
    → Delete original
         ↓
Phase 4: FORGETTING
  Library: pathlib + networkx
  Process:
    → Find all Class D tagged entries
    → Verify: is node connected to any active project node in networkx? Is entity in USER.md quests?
    → If disconnected: delete vault file, remove from BM25 index, remove networkx node + edges
         ↓
Phase 5: DREAM SYNTHESIS
[intelligence/dream_synthesizer.py]
  Library: LLM calls (local model or free cloud if insufficient)
  Input: list of blocked project tasks + open questions from vault
  Process: subagent_generator explores unconventional approaches per problem
  Output: proposals written to vault/projects/{id}/proposals/
         ↓
Phase 6: WEEKLY FINE-TUNING (if due)
[core/inference/local_model.py — fine-tuning mode]
  Library: unsloth (QLoRA training) + peft + transformers
  Input: successful interaction pairs from Langfuse logs
  Process:
    1. Format training examples (instruction-response pairs)
    2. unsloth.FastLanguageModel.get_peft_model() with LoRA config
    3. EWC loss: compute Fisher information matrix from base weights
       Add EWC penalty: L_total = L_task + λ * Σ F_i * (θ_i - θ*_i)²
    4. Train for configured epochs
    5. Evaluate on held-out validation set
    6. If eval score >= previous version score: deploy new adapter
    7. If eval score < previous: reject, keep previous adapter
  Library for free cloud: compute/free_cloud_orchestrator.py
    → visual control: browser automation to Google Colab / Kaggle
         ↓
Phase 7: GIT COMMIT AND PUSH
  Library: GitPython
  Process:
    repo = git.Repo(vault_path)
    repo.index.add(["vault/", "config/USER.md"])
    repo.index.commit(f"Sleep cycle {timestamp}: {summary}")
    if github_configured:
      origin = repo.remote(name="origin")
      origin.push()
  Sleep cycle completion timestamp written to settings.yaml
```

### 2.3 L1 Memory Block Lifecycle

```
L1 ACTIVE MEMORY BLOCKS (held in LangGraph state dict — not persisted between sessions)

Blocks defined in core/memory/l1_active.py:

PERSONA_BLOCK:
  Loaded from: config/SOUL.md, config/EMPATHY.md, config/RATIONAL.md
  Load trigger: System start, and whenever config files change
  Content: persona definition, interaction rules, emotional response guidelines
  Cleared: Never during session; reloaded on config change

USER_STATE_BLOCK:
  Loaded from: config/USER.md (subset: display_name, quests, preferences, timezone, currency)
  Load trigger: System start + daily refresh at CO-mode morning run
  Content: who the user is, their goals, their current CO-mode plan
  Cleared: Never during session; refreshed daily

ACTIVE_TASK_BLOCK:
  Loaded from: Last completed or current task context
  Load trigger: Each new task begins
  Content: what is currently being worked on, relevant project context
  Cleared: When task completes AND no immediate follow-up detected

WORKING_MEMORY_BLOCK:
  Loaded from: Last 3 interactions (rolling window, in-memory only)
  Load trigger: Each new interaction
  Content: Recent exchange context for conversational continuity
  Cleared: When window slides (oldest interaction dropped)

QUEST_CONTEXT_BLOCK:
  Loaded from: config/USER.md (main_quests, side_quests, progress)
  Load trigger: Daily at CO-mode morning run
  Content: current quest status for goal enforcement
  Cleared: Daily refresh

SESSION_FACTS_BLOCK:
  Loaded from: Empty at session start
  Content: New facts learned in current session, pending L3 write
  Cleared: On session end (facts committed to L3 via extractor.py)
```

---

## 3. COMPLETE TECHNICAL DEPENDENCY GRAPH

```mermaid
graph LR
    %% ═══════════════════════════════════════════
    %% INPUT LAYER
    %% ═══════════════════════════════════════════
    subgraph INPUT ["Input Layer"]
        MIC[Microphone]
        TEXT[Text / Keyboard]
        CAM[Camera]
        TGRAM[Telegram Bot API]
    end

    %% ═══════════════════════════════════════════
    %% COMMUNICATION LAYER
    %% ═══════════════════════════════════════════
    subgraph COMM ["Communication Layer"]
        WAKE[wake_word.py<br/>pvporcupine / silero-vad]
        STT[stt.py<br/>Whisper local + Hinglish FT]
        TTS_STD[tts_standard.py<br/>Kokoro-82M]
        TTS_EMO[tts_emotional.py<br/>Coqui XTTS]
        TG_BOT[telegram_bot.py<br/>python-telegram-bot]
        VOIP[voip_caller.py<br/>pjsua2 / VoIP lib]
        MEET[meeting_attendee.py<br/>visual control + STT]
        COACH[realtime_coach.py<br/>STT + LLM streaming]
        V_CLONE[voice_clone.py<br/>local voice model]
    end

    %% ═══════════════════════════════════════════
    %% SECURITY AND MIDDLEWARE
    %% ═══════════════════════════════════════════
    subgraph SECURITY ["Security and Middleware"]
        PII[pii_scrubber.py<br/>presidio-analyzer]
        GUARD[guardrails.py<br/>Guardrails AI]
        AUTH[auth.py<br/>local token]
    end

    %% ═══════════════════════════════════════════
    %% FASTAPI GATEWAY
    %% ═══════════════════════════════════════════
    FASTAPI[FastAPI Daemon<br/>main.py<br/>uvicorn]

    %% ═══════════════════════════════════════════
    %% PERSONA LAYER
    %% ═══════════════════════════════════════════
    subgraph PERSONA ["Persona Layer"]
        EMOT[emotional_detector.py]
        COG[cognitive_state_detector.py]
        MODE[mode_selector.py<br/>SOUL.md / EMPATHY.md]
        VMOD[voice_modulator.py]
    end

    %% ═══════════════════════════════════════════
    %% ROUTING AND INFERENCE
    %% ═══════════════════════════════════════════
    subgraph INFERENCE ["Routing and Inference Layer"]
        SEMROUTE[semantic-router<br/>Hinglish intent vectors]
        COMPLEX[complexity_classifier.py<br/>local LLM call]
        LITELLM[LiteLLM Gateway<br/>cloud_router.py]
        LLAMACPP[llama.cpp<br/>local_model.py<br/>llama-cpp-python]
        CLOUD[Cloud LLM<br/>OpenAI / Anthropic / Google]
    end

    %% ═══════════════════════════════════════════
    %% ORCHESTRATION
    %% ═══════════════════════════════════════════
    subgraph ORCH ["Orchestration Layer"]
        LG[LangGraph StateGraph<br/>main_graph.py<br/>MemorySaver]
        INTEL[intelligence_preserver.py]
        ROUTER[router.py]
    end

    %% ═══════════════════════════════════════════
    %% AGENT LAYER
    %% ═══════════════════════════════════════════
    subgraph AGENTS ["Agent Layer"]
        AG_SEC[security_agent.py]
        AG_FIN[finance_agent.py]
        AG_CONT[content_agent.py]
        AG_RES[research_agent.py]
        AG_TUT[tutoring_agent.py]
        AG_DW[digital_worker_agent.py]
        AG_DISC[discovery_agent.py]
        AG_CONV[conversation_agent.py]
    end

    %% ═══════════════════════════════════════════
    %% SUB-AGENTS
    %% ═══════════════════════════════════════════
    subgraph SUBAGENTS ["Adversarial Debate Circuit"]
        GEN[subagent_generator]
        CRIT[subagent_critic]
        SYNTH[subagent_synthesis]
    end

    %% ═══════════════════════════════════════════
    %% BACKGROUND AGENTS
    %% ═══════════════════════════════════════════
    subgraph BACKGROUND ["Background Layer (Separate Thread)"]
        BG_CO[co_mode_agent.py]
        BG_MON[proactive_monitor.py]
        BG_SLP[sleep_agent.py]
        BG_PRJ[project_manager_agent.py]
        BG_QUEUE[thread-safe queue.Queue]
    end

    %% ═══════════════════════════════════════════
    %% MEMORY LAYER
    %% ═══════════════════════════════════════════
    subgraph MEMORY ["Three-Tier Memory"]
        L1[L1 Active Blocks<br/>l1_active.py<br/>LangGraph state dict]
        L2_BM25[L2 BM25 Index<br/>rank_bm25<br/>l2_index.py]
        L2_NX[L2 Knowledge Graph<br/>networkx DiGraph<br/>l2_index.py]
        L3[L3 Obsidian Vault<br/>Markdown + YAML<br/>l3_vault.py]
        EXTRACT[extractor.py<br/>LLM classification]
        SLEEP[sleep_cycle.py<br/>consolidation logic]
    end

    %% ═══════════════════════════════════════════
    %% ACTUATION LAYER
    %% ═══════════════════════════════════════════
    subgraph ACTUATION ["Actuation Layer"]
        SCAP[screen_capture.py<br/>PIL/Pillow]
        QWEN[qwen_vl.py<br/>Qwen3-VL<br/>transformers]
        ELOC[element_locator.py]
        MOUSE[mouse_controller.py<br/>human_mouse + pyautogui]
        KB[keyboard_controller.py<br/>pyautogui + random]
        BROW[browser_controller.py<br/>browser-use]
        FACE[face_recognizer.py<br/>face_recognition / DeepFace]
        VOICE_REC[voice_recognizer.py<br/>pyannote.audio]
    end

    %% ═══════════════════════════════════════════
    %% SKILLS LAYER
    %% ═══════════════════════════════════════════
    subgraph SKILLS ["Skills Layer"]
        FORGE[generator.py<br/>LLM call]
        SANDBOX[sandbox.py<br/>Docker Python SDK]
        VERIFY[verifier.py<br/>pytest]
        REPAIR[repair_loop.py<br/>LLM call]
        HITL[hitl_gate.py<br/>LangGraph interrupt()]
        REG[skill_registry.py<br/>pathlib + yaml]
        HEALTH[health_tracker.py<br/>yaml + logic]
        MCP_C[client.py<br/>MCP Python SDK]
        MCP_F[server_factory.py<br/>FastMCP]
    end

    %% ═══════════════════════════════════════════
    %% INTELLIGENCE LAYER
    %% ═══════════════════════════════════════════
    subgraph INTELLIGENCE ["Intelligence Layer"]
        CAUSAL[causal_modeler.py<br/>DoWhy + CausalPy]
        SEREND[serendipity_engine.py<br/>BM25 cross-domain]
        CALIB[calibration_tracker.py<br/>Brier score tracking]
        RHYTHM[rhythm_learner.py<br/>time-series analysis]
        DREAM[dream_synthesizer.py<br/>LLM overnight runs]
        SOCIAL[social_graph.py<br/>networkx]
    end

    %% ═══════════════════════════════════════════
    %% GROWTH LAYER
    %% ═══════════════════════════════════════════
    subgraph GROWTH ["Growth and Accountability Layer"]
        QUEST[quest_tracker.py]
        LIE[lie_detector.py]
        CO_EVAL[co_mode_evaluator.py]
        INTEL_P[intelligence_preserver.py]
        DEL_PRAC[deliberate_practice.py]
    end

    %% ═══════════════════════════════════════════
    %% COMPUTE AND OBSERVABILITY
    %% ═══════════════════════════════════════════
    subgraph COMPUTE ["Compute and Observability"]
        LOCAL_CHK[local_checker.py<br/>psutil]
        CLOUD_ORCH[free_cloud_orchestrator.py<br/>visual control]
        LANGFUSE[langfuse_client.py<br/>self-hosted Langfuse]
        OTEL[otel_spans.py<br/>opentelemetry]
        DASH[dashboard_filter.py<br/>major decisions only]
    end

    %% ═══════════════════════════════════════════
    %% CONFIG AND GIT
    %% ═══════════════════════════════════════════
    subgraph CONFIG ["Config and Version Control"]
        CFG[settings.yaml<br/>project_name.txt]
        GIT[GitPython<br/>auto-commit + push]
        GITHUB[Private GitHub Repo<br/>cloud backup]
    end

    %% ═══════════════════════════════════════════
    %% TRAY AND EXTERNAL
    %% ═══════════════════════════════════════════
    TRAY[pystray<br/>System Tray]

    %% ═══════════════════════════════════════════
    %% CONNECTIONS
    %% ═══════════════════════════════════════════

    %% Input → Communication
    MIC --> WAKE
    WAKE --> STT
    MIC --> MEET
    MIC --> COACH
    CAM --> FACE
    MIC --> VOICE_REC
    TGRAM --> TG_BOT

    %% Communication → FastAPI
    STT --> FASTAPI
    TG_BOT --> FASTAPI
    TEXT --> FASTAPI

    %% FastAPI → Security Middleware → Orchestration
    FASTAPI --> AUTH
    AUTH --> EMOT
    AUTH --> COG
    AUTH --> SEMROUTE
    EMOT --> LG
    COG --> LG
    SEMROUTE --> LG

    %% Orchestration internal
    LG --> INTEL
    LG --> ROUTER
    ROUTER --> COMPLEX
    COMPLEX --> LITELLM
    COMPLEX --> LLAMACPP
    LITELLM --> PII
    PII --> CLOUD
    LLAMACPP --> LG

    %% LG → Memory
    LG <--> L1
    LG --> L2_BM25
    L2_BM25 --> LG
    LG --> L2_NX
    L2_NX --> LG
    L2_BM25 <--> L3
    L2_NX <--> L3

    %% LG → Agents
    LG --> AG_SEC
    LG --> AG_FIN
    LG --> AG_CONT
    LG --> AG_RES
    LG --> AG_TUT
    LG --> AG_DW
    LG --> AG_DISC
    LG --> AG_CONV

    %% Domain Agents → Sub-agents
    AG_SEC --> GEN
    AG_FIN --> GEN
    AG_CONT --> GEN
    AG_RES --> GEN
    AG_TUT --> GEN
    AG_DW --> GEN
    AG_DISC --> GEN

    %% Adversarial Circuit
    GEN --> CRIT
    CRIT -->|Rejected| GEN
    CRIT -->|Approved| SYNTH
    SYNTH --> HITL

    %% HITL → Output
    HITL --> MODE
    MODE --> VMOD
    VMOD --> TTS_STD
    VMOD --> TTS_EMO
    TTS_STD --> EXTRACT
    TTS_EMO --> EXTRACT

    %% Memory Write Pipeline
    EXTRACT --> L3
    EXTRACT --> L2_BM25
    EXTRACT --> L2_NX
    EXTRACT --> L1

    %% Actuation Pipeline
    AG_DW --> SCAP
    SCAP --> QWEN
    QWEN --> ELOC
    ELOC --> MOUSE
    ELOC --> KB
    ELOC --> BROW

    %% Skills Pipeline
    LG --> FORGE
    FORGE --> SANDBOX
    SANDBOX --> VERIFY
    VERIFY -->|Fail| REPAIR
    REPAIR --> SANDBOX
    VERIFY -->|Pass| HITL
    HITL -->|Approved| REG
    REG --> L3
    REG --> MCP_F
    MCP_F --> MCP_C

    %% Intelligence → Domain Agents
    CAUSAL --> AG_FIN
    CAUSAL --> AG_SEC
    SEREND --> AG_DISC
    SEREND --> AG_RES
    CALIB --> SYNTH
    RHYTHM --> BG_CO
    DREAM --> BG_SLP
    SOCIAL --> BG_CO

    %% Growth → Orchestration
    INTEL_P --> LG
    CO_EVAL --> BG_CO
    LIE --> BG_CO
    QUEST --> BG_CO
    DEL_PRAC --> AG_TUT

    %% Background → Queue → LG
    BG_CO --> BG_QUEUE
    BG_MON --> BG_QUEUE
    BG_SLP --> BG_QUEUE
    BG_PRJ --> BG_QUEUE
    BG_QUEUE -.->|Non-blocking push| LG

    %% Compute
    LOCAL_CHK --> CLOUD_ORCH
    CLOUD_ORCH --> ACTUATION
    CLOUD_ORCH --> BG_SLP

    %% Observability
    LG --> LANGFUSE
    LG --> OTEL
    LANGFUSE --> DASH
    OTEL --> DASH
    DASH --> FASTAPI

    %% Voice output
    V_CLONE --> VOIP
    V_CLONE --> MEET

    %% Config
    CFG --> LG
    CFG --> BG_CO
    L3 --> GIT
    GIT --> GITHUB

    %% Tray
    TRAY --> FASTAPI
```

---

## 4. DOCKER SANDBOX ISOLATION

### 4.1 Skill Sandbox — Complete Isolation Specification

The skill sandbox must be completely isolated from the host system. No exceptions. No configuration options that weaken this isolation.

```
docker/skill_sandbox.Dockerfile contents:

FROM python:3.11-slim
RUN useradd -u 1000 -m sandboxuser
USER 1000
WORKDIR /tmp/sandbox
# No pip installs in Dockerfile — skills get only stdlib
# Additional packages can be installed per-skill in a requirements step
# that runs inside the container before the skill code

Runtime flags (enforced in skills/forge/sandbox.py):
  network_disabled = True          # --network none
  mem_limit = "512m"               # Hard memory limit
  memswap_limit = "512m"           # No swap either
  cpu_period = 100000              # CPU scheduling period
  cpu_quota = 100000               # 1 full CPU core maximum
  read_only = True                 # Root filesystem read-only
  tmpfs = {"/tmp": "size=100m"}    # Only writable location, in RAM
  user = "1000"                    # Non-root sandboxuser
  cap_drop = ["ALL"]               # All Linux capabilities dropped
  security_opt = ["no-new-privileges:true"]
  remove = True                    # Container deleted immediately after execution
  timeout = 30                     # Hard 30-second kill

What the sandbox CAN do:
  → Read its own source code (written to /tmp before container start)
  → Write to /tmp/sandbox/output/ (results captured before container deletion)
  → Execute Python code
  → Use Python standard library

What the sandbox CANNOT do:
  → Access the internet
  → Access any host filesystem path
  → Read other processes or system information
  → Persist any data after execution (tmpfs, container removed)
  → Run as root or escalate privileges
  → Spawn child processes with elevated permissions
  → Access any environment variables from host (sanitised env passed explicitly)
```

### 4.2 Malware Analysis Sandbox — Extended Isolation

```
docker/malware_sandbox.Dockerfile contents:

FROM remnux/remnux-distro  (or capa/flare-vm equivalent)
RUN useradd -u 2000 -m malwareuser
USER 2000

Runtime flags (enforced in security/malware_sandbox.py):
  network_disabled = True           # Absolute — no network under any circumstance
  mem_limit = "1g"
  read_only = False                 # Forensics tools need to write
  mounts = [
    docker.types.Mount("/samples", host_samples_dir, type="bind", read_only=True),
    docker.types.Mount("/logs", host_logs_dir, type="bind", read_only=False),
    docker.types.Mount("/tmp", "", type="tmpfs")
  ]
  cap_drop = ["ALL"]
  cap_add = ["SYS_PTRACE"]          # Needed for dynamic analysis / debugger
  security_opt = ["seccomp=malware_sandbox_seccomp.json"]
                                    # Custom seccomp profile logging all syscalls

Pre-execution:
  → SHA256 hash of sample recorded
  → Full filesystem snapshot (tarball of container state) saved to /logs/pre_snapshot.tar

Post-execution:
  → Full filesystem snapshot again saved to /logs/post_snapshot.tar
  → Diff computed: /logs/filesystem_diff.txt
  → Network connection attempts logged (should be empty — network disabled)
  → All written files listed

The malware sandbox is a separate Docker image from the skill sandbox.
They must never share resources or networks.
The malware sandbox must never be used for skill testing.
The skill sandbox must never be used for malware analysis.
```

### 4.3 Host Execution After Sandbox Approval

```
After HITL approval of a skill or code output:

[node_execute_host]
  The approved code runs as a Python subprocess on the host machine
  Library: subprocess (Python standard library)
  User context: same user as the [PROJECT_NAME] process (not root)
  File system access: FULL access to user's home directory and configured paths
  Network access: FULL access (skills may need to call APIs)

  Security constraints maintained even on host:
    → Guardrails AI schema validation wraps every host execution call
    → Any system command (rm, mv, format, etc.) triggers additional HITL gate
    → File operations logged to observability layer
    → Output captured and logged before delivery to domain agent
```

---

## 5. LIBRARY DEPENDENCY MANIFEST

Complete list of all Python packages required, with their purpose. This is the source of truth for `bootstrap/requirements.txt`.

```
# Orchestration
langgraph                    # Primary agent orchestration framework
langchain-core               # LangGraph dependency

# LLM Inference
llama-cpp-python             # Local LLM inference via llama.cpp
litellm                      # Unified LLM gateway for all providers
unsloth                      # QLoRA fine-tuning (GPU required)
peft                         # LoRA adapters
transformers                 # HuggingFace model loading (Qwen3-VL, etc.)

# Memory
rank-bm25                    # L2 BM25 keyword search
networkx                     # L2 knowledge graph
python-frontmatter           # YAML frontmatter parsing for vault files
gitpython                    # Git operations for vault version control and backup
filelock                     # Cross-process file locking for vault safety
pyyaml                       # YAML reading/writing

# Routing and Intent
semantic-router              # Intent classification (Aurelio Labs)
guardrails-ai                # Schema enforcement and safety checks

# Speech
openai-whisper               # Local STT
kokoro-onnx                  # Kokoro-82M TTS
TTS                          # Coqui XTTS for high-emotion TTS
sounddevice                  # Audio playback and capture
pvporcupine                  # Wake word detection (OR silero-vad)

# Vision and Actuation
Pillow                       # Screenshots via ImageGrab
pyautogui                    # Mouse and keyboard control
human-mouse                  # Bezier curve mouse movement
browser-use                  # DOM-based web automation
pytesseract                  # OCR for terminal output capture
face-recognition             # Local face recognition
pyannote.audio               # Speaker diarisation and voice fingerprinting

# Skills and Sandboxing
docker                       # Docker Python SDK for sandbox management
pytest                       # Skill verification testing
fastmcp                      # MCP server authoring
mcp                          # Official MCP Python SDK (client)

# API and Interface
fastapi                      # Local API daemon
uvicorn                      # ASGI server for FastAPI
pystray                      # System tray application
python-telegram-bot          # Telegram Bot API client

# Security and PII
presidio-analyzer            # PII detection before cloud API calls
presidio-anonymizer          # PII anonymisation
semgrep                      # Static code analysis for security audits

# Intelligence and Analysis
dowhy                        # Causal modelling
causalpy                     # Additional causal analysis utilities
scipy                        # Statistical computation (Brier score tracking)
numpy                        # Numerical operations

# Observability
langfuse                     # Self-hosted LLM observability
opentelemetry-api            # Distributed tracing
opentelemetry-sdk            # OpenTelemetry implementation

# Utilities
psutil                       # System resource monitoring (local_checker.py)
python-dotenv                # Environment variable loading
httpx                        # Async HTTP client for API calls
aiofiles                     # Async file operations
schedule                     # Background task scheduling

# Voice Cloning
[IMPLEMENTATION_DETAIL: evaluate Tortoise-TTS, XTTS-v2, or Bark for voice cloning
 — select based on quality/speed tradeoff on target hardware at build time]

# VoIP
[IMPLEMENTATION_DETAIL: evaluate pjsua2, aiortc, or Twilio SDK
 — select based on platform and free tier availability at build time]
```

---

*End of MODULE_DEPENDENCY_GRAPH.md — Version 1.0.0*
