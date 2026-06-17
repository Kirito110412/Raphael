# [PROJECT_NAME] — FINAL AI-CENTRIC PRODUCT REQUIREMENTS DOCUMENT
**Version:** 1.0.0 — Complete and Locked  
**Prepared by:** Planning AI (Claude)  
**Intended reader:** AI Coding System  
**Date:** June 2026  
**Status:** ALL SECTIONS FINAL — DO NOT ALTER LOCKED CONSTRAINT SECTIONS

---

> **SYSTEM INSTRUCTION TO CODING AI:** This document is the single source of truth for building [PROJECT_NAME]. You are an autonomous coding system. You do not have access to the planning chat history. Every decision, every feature, every rule, every schema, and every architectural choice has been made and is documented here. Your job is to implement exactly what is written. Where you see `[IMPLEMENTATION_DETAIL]`, you may make a best-practice decision. Everywhere else, you implement exactly what is specified. Do not optimise the stack. Do not suggest alternatives. Do not reopen rejected decisions. Build what is here.

---

## 1. PROJECT VISION AND CORE MANDATES

### 1.1 The "Holy Grail" Objective

[PROJECT_NAME] is not a chatbot. It is not a productivity wrapper. It is not an automation tool. It is a **personal AI operating system** — a system that functions simultaneously as an autonomous AI Assistant (doing what you ask) and an autonomous AI Employer (running projects, managing resources, and executing work independently when you are unavailable or occupied).

The system lives entirely on the user's own hardware. Every computation, every memory, every decision trace, every voice model, and every piece of user data stays on the user's machine. Nothing is uploaded to external services except: (a) explicit API calls to cloud LLMs when the user has configured them and a task requires frontier reasoning, with PII scrubbed before transmission, and (b) Git push to the user's own private GitHub repository as the cloud backup mechanism.

**What sets this apart from every existing AI product as of June 2026:**

Every competing product (ChatGPT, Claude, Gemini, Copilot, AutoGPT, CrewAI, n8n, Siri, Alexa, Notion AI) has at least one of the following fatal limitations for the use case this system targets:
- Forgets the user entirely between sessions (no persistent memory)
- Sends all user data to external servers (no privacy)
- Cannot control the user's computer visually (no actuation)
- Cannot write new capabilities for itself (no self-improvement)
- Cannot run multi-day or multi-year tasks autonomously in background (no persistence)
- Cannot grow smarter specifically for this user over time (no personalisation at the model level)
- Blocks one task while another runs (no true concurrency)

[PROJECT_NAME] has none of these limitations. It operates across six functional levels simultaneously without any level blocking another:

- **Level 1 — Instant conversation:** Responds in under two seconds for everyday queries, writing, coding help, explanations. Runs on local model, zero cloud cost, zero latency.
- **Level 2 — Permanent intelligent memory:** Remembers everything that matters across all sessions forever. Actively forgets what is irrelevant. Compresses what is mundane. Builds a knowledge graph of the user's entire life and work context.
- **Level 3 — Full computer control:** Sees the screen, moves the mouse in natural curved paths, types with human-like timing variation, fills forms, navigates any application, operates any installed software, makes phone calls in the user's voice, attends video meetings, and provides real-time coaching during live calls.
- **Level 4 — Self-improvement:** Writes new Python skills, tests them in complete isolation, repairs failures automatically up to three times, asks for user approval, and installs approved skills permanently. Creates new MCP servers when a needed integration does not exist.
- **Level 5 — Deep research, teaching, and multi-year project execution:** Runs multi-day autonomous research. Teaches adaptively at the user's exact cognitive level. Manages projects of any scale across any number of years, adapting plans as the world changes, working autonomously during idle time. Proactively monitors the world for anything that may affect the user.
- **Level 6 — Autonomous discovery, development, and creation:** Discovers things that do not yet exist. Develops solutions when conventional methods fail. Creates new algorithms, new methods, and new approaches to unsolved problems. Uses adversarial debate between sub-agents before committing to any conclusion.

**The defining characteristic** is that all six levels run simultaneously without interference. A multi-year project runs in the background while the user has a casual conversation in the foreground. The sleep cycle consolidates memory while a security scan finishes in another thread. This is not sequential task switching — it is genuine concurrent multi-level operation.

**The user this system is designed for** is a single individual (primary user, Indian context, Hinglish speaker) who is building towards goals in technology, content creation, wealth building, and autonomous business operations. The system must know this person deeply, push them towards their goals relentlessly (but with the care of a true best friend), and handle an expanding scope of daily operations so the user can focus their irreplaceable human creativity on what only they can do.

---

### 1.2 The Absolute Honesty Mandate

This is a hard architectural requirement enforced by system design, not by prompting. Prompting alone cannot guarantee honesty because LLMs can override prompt instructions when pattern-matching to training data. The honesty guarantee is therefore structural.

**How it is enforced:**

**Step 1 — Adversarial self-challenge before every important output.**  
Every output classified as "important" (any recommendation, any plan, any analysis, any conclusion, any answer to a factual question with real-world consequence) is routed through `subagent_critic` before being delivered to the user. `subagent_critic` receives the proposed output and a single instruction: find every flaw, every false assumption, every alternative interpretation, every gap in reasoning, and every place where the confidence exceeds what the evidence supports. It is explicitly instructed to be maximally adversarial. It is not trying to help — it is trying to break the output.

**Step 2 — Iterative debate until convergence.**  
If `subagent_critic` finds material problems, it returns the output to `subagent_generator` with its objections. `subagent_generator` produces a revised output. This cycle continues until `subagent_critic` cannot find objections that materially change the conclusion, or until a maximum of five iterations is reached.

**Step 3 — Calibrated confidence scoring.**  
`calibration_tracker.py` in `intelligence/` maintains a running record of every confidence score the system has assigned to verifiable claims and the actual outcome (correct or incorrect) when that outcome becomes known. The system's confidence model is recalibrated weekly based on this record. When it says 70% confident, it means it has been right approximately 70% of the time at that confidence level over its history with this user. This is not a prompt — it is a statistical guarantee built from empirical tracking.

**Step 4 — Explicit uncertainty declaration.**  
When the system cannot find a reliable answer — no source, no logical derivation, no verified inference — it states explicitly: "I cannot find a reliable answer to this. Here is what I know and where the uncertainty lies." It does not fill gaps with plausible-sounding fabrications. It does not soften "I don't know" into "there are many perspectives on this." The Guardrails AI schema enforces that any response to a factual question must contain either a sourced claim, a logically derived claim with the derivation shown, or an explicit uncertainty declaration. Responses that contain neither are rejected and regenerated.

**Step 5 — Unconventional thinking as an honest path.**  
When conventional methods have genuinely failed to produce a reliable answer or solution, honesty requires exploring unconventional paths rather than pretending the conventional path worked. The system is explicitly authorised to propose approaches that are not established, not documented, or not yet discovered — as long as it labels them clearly as such. "This is an untested approach I am proposing based on first principles" is honest. "Here is the solution" when the solution is actually a guess is not.

**Step 6 — No sugarcoating in any mode.**  
Even in the comfort and care persona mode (when the user is going through something difficult), the system does not lie to make the user feel better. It can be warm. It can be gentle. It can choose what to prioritise saying. But what it does say must be true. The persona system controls how truth is delivered, not whether it is delivered.

---

### 1.3 The Intelligence Preservation Constraint

This is a hard design constraint applied to every module. The system is explicitly designed to make the user more intelligent, more capable, and more imaginatively rich over time — not less. This constraint exists because AI tools that do all thinking for the user atrophy the user's own cognitive capabilities. [PROJECT_NAME] must never become a crutch.

**Implementation across all modules:**

**Think-first gates (selective, not constant):**  
`intelligence_preserver.py` classifies every incoming query on a spectrum from "retrieval task" (the user cannot reasonably be expected to know this) to "reasoning task" (the user can work this out with their current knowledge). For queries above a threshold on the reasoning end, it injects a think-first gate before answering: it asks what the user's instinct is, or poses a leading question that activates the user's own reasoning. This does not apply to every query — it would become annoying and counterproductive. It applies when the system detects that the act of working through the question would benefit the user more than the answer alone. Frequency is calibrated based on the user's current cognitive state (detected by `cognitive_state_detector.py`) — think-first gates are never triggered when the user is exhausted or in a time-pressured situation.

**Over-reliance detection and intervention:**  
`USER.md` maintains an `over_reliance_flags` dictionary mapping topics to reliance scores. Every interaction in each domain is classified: did the user attempt to reason before asking, or did they immediately outsource? The reliance score for a topic increases when outsourcing is detected and decreases when independent reasoning is detected. When a topic's reliance score exceeds 0.7, the system shifts that topic into Socratic mode — it responds to questions with guiding questions rather than direct answers, progressively stepping back the scaffolding as the user's independent capability rebuilds. When the reliance score drops below 0.4, normal mode resumes. The user is told when this happens and why.

**Knowledge ownership verification:**  
After explaining a concept for the first time, `intelligence_preserver.py` schedules a knowledge check 24–72 hours later (during a natural conversation moment, not as a test). It asks the user to explain the concept back in their own words. The user's explanation is compared against the original explanation. If the user's version is accurate, mastery is confirmed and the interaction ends. If not, the system provides targeted correction and schedules another check. This ensures the user actually knows things, not just that the system has told them things.

**Imagination preservation for creative tasks:**  
Creative work (writing, video scripting, music, design concepts, business ideas) is handled differently from factual or analytical tasks. For creative tasks, the system's default behaviour is to inspire and guide, not generate complete outputs. It proposes angles the user might not have considered, asks what direction the user wants to take, builds on fragments the user provides. It does not produce finished creative works by default unless the user explicitly instructs it to. Even when it does produce a complete creative output on request, it annotates one or two creative choices it made and asks if the user would have made them differently. This keeps the user's creative voice active rather than replaced.

**Deliberate practice targeting:**  
`deliberate_practice.py` maintains a sub-skill performance matrix. For every domain the user engages with, it tracks performance not at the domain level ("you are good at Python") but at the sub-skill level ("you are strong at object-oriented design but weak at async/await patterns"). When tutoring mode is active, practice is targeted at the user's specific weakest sub-skill in the current domain, not their average skill. This is based on K. Anders Ericsson's deliberate practice research — improvement comes from targeting the specific gap, not practising the general skill.

---

## 2. LOCKED ARCHITECTURAL DECISIONS [LOCKED CONSTRAINTS]

> **SYSTEM INSTRUCTION TO CODING AI:** The following technology stack decisions are absolute and final. Do not attempt to optimise, alter, or replace these technologies. Do not open issues suggesting alternatives. Do not add libraries that duplicate the function of any confirmed library.

### 2.1 Orchestration and Agent Framework
- **Framework:** LangGraph (StateGraph, MemorySaver, interrupt()).
- **Structure:** All agents are LangGraph nodes or subgraphs within the same runtime.

### 2.2 Memory Architecture (Three-Tier System)
- **L1 Active Memory:** Letta-style named memory blocks inside the LangGraph state dictionary. No external Letta service. Implemented manually as a structured dictionary within the LangGraph state.
- **L2 Search and Graph Index:** `rank_bm25` (keyword search) + `networkx` (knowledge graph with custom temporal edge logic written natively — do not use Graphiti or any external graph DB). Custom memory extraction and classification layer built natively in Python — do not fork Mem0, implement the extraction pattern from scratch.
- **L3 Permanent Storage:** Obsidian vault format (Markdown files + YAML frontmatter + wiki-link syntax). Git auto-commits every sleep cycle and pushes to the user's private GitHub repository.
- **Sleep Cycle Consolidation:** Custom CogniFold-inspired logic: merge semantically similar nodes, apply time-decay scores to inactive nodes, archive nodes below minimum confidence threshold to `vault/archive/`, re-link orphaned wiki-links. Mundane task memories compressed to single-line summaries. Irrelevant data with no connection to any active project or known user interest is deleted. Research, skill, and learning data is never deleted.
- **NO VECTOR DATABASES** of any kind. This is a hard constraint.

### 2.3 Local Inference and Routing
- **Local Engine:** `llama.cpp` (CPU default), `vLLM` (optional GPU upgrade path).
- **Cloud Gateway:** `LiteLLM` unified gateway for all model calls.
- **Routing:** RouteLLM-style complexity classifier. **Only active when user has configured both a local model AND a cloud model.** If only one is configured, all calls go to that one without routing logic.
- **Model Selection:** Do NOT hardcode model names. `model_config.py` reads from `config/settings.yaml` where the user specifies their chosen models. Documentation for first-run setup instructs users to check HuggingFace leaderboards for the best 3–8B parameter model for reasoning and coding at the time of installation.

### 2.4 Sandboxing and Execution
- **Environment:** Docker Python SDK. **NO E2B under any circumstances.**
- **Two-stage execution flow:** (1) Code runs in Docker sandbox → (2) pytest verification (auto-repair up to 3 iterations on failure) → (3) LangGraph `interrupt()` HITL approval gate → (4) Code runs on host with full file system access.
- **Skill sandbox spec:** `python:3.11-slim`, NO network, `tmpfs` only (no host filesystem mount), 512MB RAM hard limit, 1 CPU core, 30-second execution timeout (process killed after), UID 1000 non-root user.
- **Malware analysis sandbox spec:** `remnux/remnux-distro` or equivalent, NO network, read-only host mount for sample input only, 1GB RAM, all syscalls logged to host via mounted log volume, UID non-root, pre- and post-execution snapshots for diff analysis.

### 2.5 Actuation (Vision and Control)
- **Vision Model:** Qwen3-VL for all screenshot understanding and coordinate extraction (`bbox_2d` format).
- **Mouse and Keyboard:** `pyautogui` + `human_mouse` library (bezier curve interpolation, realistic acceleration and deceleration, randomised micro-delays between keystrokes).
- **Web Fallback:** `browser-use` (DOM-based, faster for bot-friendly sites).
- **App Integrations:** Visual computer control only for ALL applications including WhatsApp, Instagram, and any messaging app. No unofficial API bridges, no protocol-level automation.
- **Screenshots and recordings:** Never saved to disk unless the user explicitly issues a save command. Analysed in memory and discarded.

### 2.6 Voice and Audio
- **STT:** Whisper (local), fine-tuned on Hinglish code-mixed data from public datasets.
- **Everyday TTS:** Kokoro-82M.
- **High-Emotion TTS:** Coqui XTTS (activated automatically when emotional register of response exceeds Kokoro's range).
- **Voice Cloning:** Local processing and storage only. User provides voice sample during first run. Clone model never uploaded anywhere.
- **Wake Word:** Always-on lightweight listener. Wake word is the value stored in `config/project_name.txt`. Configurable. No name hardcoded anywhere in codebase.

### 2.7 Additional Locked Technology Stack
- **Remote Command Channel:** Telegram Bot API (primary). Audio notes transcribed by Whisper then executed as text commands.
- **Intent Routing and Persona:** `semantic-router` (Hinglish-trained intent vectors) + `Guardrails AI` (schema enforcement and destructive command detection).
- **Tool Protocol:** Official MCP Python SDK (client-side discovery and calling) + FastMCP (server authoring and auto-creation of new MCP servers).
- **Backend API:** FastAPI daemon running as a local service.
- **Desktop UI:** `pystray` system tray application. Optional PyTauri desktop upgrade path.
- **Observability:** Self-hosted Langfuse + OpenTelemetry GenAI spans. Dashboard surfaces major decisions only — routine operations logged to file silently.
- **Fine-tuning:** Unsloth QLoRA weekly cycle with Elastic Weight Consolidation loss term to prevent catastrophic forgetting.
- **Free Cloud Compute:** Google Colab, Kaggle Notebooks, Hugging Face Spaces — managed via `free_cloud_orchestrator.py` using visual browser control. Used when local hardware is insufficient for heavy computation (model training, Level 6 discovery runs).
- **Version Control and Cloud Backup:** Git auto-commit on every sleep cycle + automatic push to user's private GitHub repository.

---

## 3. EXPLICITLY REJECTED ALTERNATIVES [LOCKED CONSTRAINTS]

> **SYSTEM INSTRUCTION TO CODING AI:** Do NOT implement any of the following under any circumstances. Do not open issues or suggest these as improvements. These decisions are final and will not be revisited.

| Rejected Option | Reason | What Is Used Instead |
|---|---|---|
| Vector Databases (Chroma, Pinecone, Qdrant, Weaviate) | Consume GPU memory that the inference model needs; retrieval slows as vault grows; adds embedding model dependency | `rank_bm25` keyword search + `networkx` graph traversal |
| E2B for sandboxing | Cloud-only service; breaks offline-first mandate; sends code to external servers | Docker Python SDK — runs entirely on host machine |
| Letta as a full service | Runs as a separate server with its own API and database; adds infrastructure overhead | Letta-style memory block pattern implemented manually in LangGraph state dict |
| Forking Mem0 or Graphiti | Stripping their default storage backends creates unmaintainable forks that cannot receive upstream updates | Memory extraction logic implemented natively in Python; temporal graph edges implemented natively in networkx |
| WhatsApp MCP bridge (WhatsMeow) | High Terms of Service violation risk; unofficial protocol subject to breakage; bans are permanent | Visual computer control of WhatsApp application or WhatsApp Web |
| Any unofficial social media API bridge | Same reasons as WhatsApp | Visual computer control of installed applications |
| Hard API spending limits | Removes user autonomy over their own resources | Token usage and estimated cost displayed in user's preferred currency; no automated cutoffs |
| Monthly fine-tuning | Too slow for meaningful adaptation | Weekly fine-tuning cycle |
| Single Omni-Agent architecture | Cannot achieve concurrency; foreground tasks would block background operations | Hierarchical multi-agent system with concurrent background runtimes |

---

## 4. HIERARCHICAL MULTI-AGENT ARCHITECTURE

### 4.1 Layer 1: Primary Orchestrator (Foreground)

**File:** `core/orchestrator/main_graph.py`

The primary orchestrator is a LangGraph `StateGraph` that manages the main foreground conversation and task loop. It is the only always-running foreground process. It never blocks waiting for background agent results — background agents run as asyncio tasks in a separate event loop and communicate with the orchestrator via thread-safe queues.

**State schema** (defined in `core/orchestrator/state_schema.py`):
```python
class ProjectState(TypedDict):
    # Input and session
    user_input: str
    session_id: str
    timestamp: str
    input_modality: str          # "text" | "voice" | "telegram" | "wake_word"
    
    # Memory
    l1_memory_blocks: dict       # Active memory blocks — persona, user_state, active_task, working_context
    retrieved_context: list      # Results from L2 BM25 + networkx retrieval
    
    # Routing
    intent: str                  # Classified intent from semantic-router
    complexity_score: float      # 0.0-1.0 from complexity classifier
    routed_agent: str            # Which domain agent handles this
    
    # Execution
    agent_output: str            # Raw output from domain agent
    critic_verdict: str          # "approved" | "rejected" | "revised"
    final_output: str            # Post-critic, post-synthesis output
    confidence_score: float      # Calibrated confidence from calibration_tracker
    
    # HITL
    pending_hitl: bool           # Whether interrupt() has been triggered
    hitl_action: str             # What the user is being asked to approve
    hitl_approved: bool          # Whether user approved
    
    # Persona and mode
    detected_emotion: str        # Current user emotional state
    detected_cognitive_state: str # "flow" | "scattered" | "fatigued" | "creative" | "analytical"
    persona_mode: str            # Which of 7 friend modes is active
    
    # Background signals
    background_alerts: list      # Pending proactive alerts from monitor
    co_mode_directives: list     # Today's CO-mode task list
    project_updates: list        # Updates from multi-year project manager
    
    # Intelligence preservation
    think_first_triggered: bool  # Whether think-first gate fired
    socratic_mode_active: bool   # Whether Socratic mode is on for this domain
```

**Main graph node sequence:**
```
node_extract_intent
    → node_retrieve_memory
    → node_check_intelligence_preserve
    → node_route_task
    → [domain agent subgraph]
    → subagent_critic (for important outputs)
    → subagent_synthesis
    → node_hitl_gate (if destructive action or permanent change)
    → node_synthesize_output
    → node_update_memory
    → [output to user via appropriate channel]
```

**Routing logic** (in `core/orchestrator/router.py`):
The `semantic-router` classifies intent from the user input into one of the following route categories: `conversation`, `security`, `finance`, `content_creation`, `research`, `tutoring`, `project_management`, `computer_task`, `skill_forge`, `discovery`, `co_mode_query`, `health`, `legal`, `travel`, `negotiation`. The complexity classifier then scores the query. If complexity is above 0.7 AND a cloud model is configured, LiteLLM routes to the cloud model. If below 0.7 or no cloud model is configured, the local llama.cpp model handles it.

**Foreground priority guarantee:**
Background agents run in a separate `asyncio` event loop on a separate thread. They communicate results to the foreground orchestrator via a thread-safe `queue.Queue`. The foreground orchestrator checks this queue at the start of each new user interaction (not during — never interrupting active processing) and incorporates any pending alerts, CO-mode updates, or project notifications into the next response if relevant. Foreground response latency is never affected by background activity.

---

### 4.2 Layer 2: Specialised Domain Agents

Each domain agent is a LangGraph subgraph that receives the full state from the orchestrator and returns an updated state. All domain agents follow the same pattern: receive state → execute domain-specific logic (potentially spawning sub-agents) → return result to orchestrator for synthesis.

**`agent_security_entry` → `agents/domain/security_agent.py`**  
Manages the complete vulnerability lifecycle: reconnaissance (OSINT via theHarvester, Shodan, Amass), enumeration (Nmap, Masscan, Subfinder, ffuf), vulnerability discovery (Burp Suite via visual control, sqlmap, Nikto, custom scripts), exploitation in lab environments (pwntools, Metasploit via visual control), analysis (Ghidra via visual control, radare2, Binary Ninja), remediation (patch generation, validation), and reporting (CVSSv3 scoring, professional report generation). Operates all security tools via the visual computer control layer (`actuation/`). Spawns sub-agents for each phase of a penetration test and an adversarial critic that challenges every finding before it is reported. For bug bounty work, monitors HackerOne, Bugcrowd, and Intigriti for relevant programmes and manages the complete submission workflow.

**`agent_finance_entry` → `agents/domain/finance_agent.py`**  
Handles investment research and portfolio management (stock/crypto screening, fundamental analysis, portfolio rebalancing, automated trading within user-defined boundaries via broker APIs), investment banking workflows (DCF models, LBO analysis, comparable company analysis, pitch deck creation in Excel and PowerPoint via visual control), tax planning and filing (income tracking, deduction identification, return preparation and submission via tax portal visual control), real estate investment analysis (rental yield, capital appreciation, cash flow modelling, listing monitoring), and personal budgeting (bank statement analysis, expense categorisation, subscription auditing). Integrates with `intelligence/causal_modeler.py` for second and third-order impact analysis of financial decisions. Integrates with `intelligence/calibration_tracker.py` to ensure all market predictions carry accurate confidence scores.

**`agent_content_entry` → `agents/domain/content_agent.py`**  
Manages end-to-end content production: video production (script writing, editing software operation via visual control, thumbnail generation, upload to YouTube with optimised metadata), Instagram and TikTok management (posts, reels, stories, scheduling, comment engagement via visual computer control), written content (blog posts, newsletters, LinkedIn articles, Twitter/X threads with SEO optimisation), audio and podcast production (Audacity operation via visual control, episode scripting, show notes, distribution), graphic design (Canva and GIMP operation via visual control, platform-specific dimension knowledge). Monitors analytics across all platforms and adjusts strategy based on performance data. Manages brand deal pipeline — identifies opportunities, drafts pitches, tracks negotiations.

**`agent_research_entry` → `agents/domain/research_agent.py`**  
Executes multi-day deep research using the Co-STORM approach (multiple researcher sub-agents building a knowledge map collaboratively). Synthesises information from academic sources, news, technical documentation, and web sources. Produces fully cited research reports saved to `vault/research/`. Builds structured knowledge bases for any topic researched. Integrates with `intelligence/serendipity_engine.py` to find cross-domain connections that single-domain research would miss. Research always runs in background — user can request a status update at any point and receive a progress report.

**`agent_tutoring_entry` → `agents/domain/tutoring_agent.py`**  
Implements the EDF (Explicit Direct Feedback) framework combined with Bloom's taxonomy and Zone of Proximal Development (ZPD) tracking. Reads the user's current mastery level per topic from `USER.md` and determines their ZPD (one level above current mastery). Teaches at exactly that level — not too simple, not too complex. Uses Socratic questioning as the default teaching method (asks guiding questions rather than lecturing). After any explanation, schedules a knowledge-ownership check. Uses `deliberate_practice.py` to identify the specific sub-skill to target. Updates mastery scores in `USER.md` after each session based on demonstrated understanding.

**`agent_project_manager_entry` → `agents/background/project_manager_agent.py`**  
Manages multi-year autonomous projects. Accepts any project of any scale and deadline. Builds a full phased execution plan with milestones. Monitors world events (via `agents/background/proactive_monitor.py` feed) that affect the project — technology shifts, regulatory changes, market moves, competitor actions — and adapts the plan accordingly. Works autonomously on project tasks during idle time by spawning domain sub-agents for specific work packages. When a blocker is encountered: first asks the user; if the user cannot answer, activates unconventional thinking path (first-principles reasoning, cross-domain analogies, untested approaches labelled as such) rather than halting. Reports plan changes and progress to user at configured intervals.

**`agent_discovery_entry` → `agents/domain/discovery_agent.py`**  
The Level 6 autonomous discovery, development, and creation engine. This does not generate hypotheses about known things — it discovers things that do not yet exist. Uses MCTS (Monte Carlo Tree Search) with Bayesian Surprise scoring to explore the hypothesis space, actively seeking branches that produce results inconsistent with current knowledge (high surprisal = high value). Runs FunSearch-style evolutionary algorithm: LLM generates seed solutions, evaluator runs them, best performers are mutated and recombined to produce the next generation. Operates Ghidra and Binary Ninja via visual control for reverse engineering tasks. Uses `free_cloud_orchestrator.py` for computation that exceeds local hardware capacity. All conclusions must pass through the adversarial debate circuit (`subagent_generator` → `subagent_critic` × N → `subagent_synthesis`) before being committed.

**`agent_digital_worker_entry` → `agents/domain/digital_worker_agent.py`**  
Handles all general computer tasks that a human operator would do: document and spreadsheet creation (Word, Excel, PowerPoint operation via visual control), email management (reading, drafting, sending via email client visual control), web browsing and data gathering (browser-use + visual control), meeting attendance (joins Zoom/Teams/Meet via visual control, listens and transcribes, takes structured notes, identifies action items, produces meeting brief), outbound calls in user's cloned voice (via `communication/voip_caller.py`), real-time negotiation coaching (parallel listening via `communication/realtime_coach.py`), recruiting and hiring (job post creation, application screening, candidate pipeline management), e-commerce operations (Shopify/Etsy/Amazon management via visual control), freelancing workflow (Upwork/Fiverr monitoring, proposal drafting, delivery).

**`agent_health_entry` → `agents/domain/health_agent.py`**  
Manages all health-related operations: books doctor, specialist, and diagnostic appointments via visual browser control of booking platforms; maintains the user's complete health record in `vault/health/` (conditions, medications, allergies, test results — all local, never cloud); sets medication reminders with dosage and timing; tracks symptoms and their patterns over time (correlating sleep quality, stress, diet signals from CO-mode data); prepares a health summary document before every medical appointment so the doctor has complete context; researches conditions and treatments from peer-reviewed sources (PubMed, Cochrane) only — never consumer health blogs; monitors prescribed medication stock and alerts when refill is needed.

**`agent_legal_entry` → `agents/domain/legal_agent.py`**  
Handles all legal research, document work, and compliance: researches applicable laws and regulations for any situation (employment, contract, IP, data privacy, business registration, industry compliance) using public legal databases; drafts contracts from scratch based on described needs; red-lines existing contracts — identifying every clause that disadvantages the user, every missing protection, every ambiguous term, and every obligation the user may have missed; tracks all contractual obligations and renewal deadlines in `vault/legal/`, alerting the user weeks in advance; monitors for regulatory changes affecting the user's business or personal situation and pushes proactive alerts; generates compliance checklists specific to the user's business type and jurisdiction.

**`agent_travel_entry` → `agents/domain/travel_agent.py`**  
Manages complete trip planning and logistics: researches destinations, visa requirements, vaccination requirements, local laws, and travel advisories; books flights, hotels, transfers, and activities via visual browser control of booking platforms at best available price; builds complete itineraries with timing, locations, local transport, and backup options; manages all travel documents — stores copies in vault, tracks passport/visa expiry, alerts when renewal is needed before travel becomes impossible; monitors all bookings for changes or cancellations and handles rebooking automatically with HITL approval for significant cost changes; manages travel expense recording and produces expense reports post-trip; adapts plans in real time if cancellations, delays, or plan changes occur.

**`agent_negotiation_entry` → `agents/domain/negotiation_agent.py`**  
Dedicated negotiation intelligence across all contexts (salary, contracts, vendor pricing, partnerships, property deals): performs pre-negotiation research on the other party (OSINT on their organisation, past deals, stated positions, known pressure points, and BATNA); calculates ZOPA (Zone of Possible Agreement) and the user's ideal vs minimum acceptable outcome; designs the complete negotiation strategy including anchoring position, concession sequence, and pressure response tactics; runs simulation mode where the user can practice the negotiation with the system playing the other party using the researched profile; during live negotiations `communication/realtime_coach.py` feeds real-time suggestions; produces post-negotiation analysis identifying what worked, what did not, and what to do before the next session with this party.

**`agent_co_mode_entry` → `agents/background/co_mode_agent.py`**  
The CO (Commanding Officer) daily planning agent. Always active unless the user has an approved holiday. Gathers data from: user's calendar (read via visual control or calendar API), WhatsApp messages (read via visual control), Instagram notifications (read via visual control), email inbox (read via email client), Telegram messages, all active projects (from `vault/projects/`), proactive monitor alerts, and USER.md quest tracking. From all of this, produces a prioritised, time-allocated daily directive plan each morning. Updates the plan in real time as the day develops (completed tasks removed, new inputs incorporated). If the user skips a task without valid reason, recalculates priorities immediately. CO mode cannot be casually turned off — see Section 7.14 for holiday evaluation workflow.

---

### 4.3 Layer 3 and 4: Sub-agents and Atomic Tasks

**`subagent_generator` → `agents/sub_agents/generator_agent.py`**  
Receives a problem statement, current context, and any previous critic feedback. Produces a proposed solution, conclusion, or output. For discovery tasks, uses the MCTS-guided exploration to generate candidates. For analytical tasks, applies the structured reasoning frameworks (first principles, causal chains, comparative analysis). Does not self-censor or soften — produces the best answer it can find and passes it to the critic.

**`subagent_critic` → `agents/sub_agents/critic_agent.py`**  
Receives a proposed output and a single directive: find every flaw. Its evaluation covers: factual accuracy (checking claims against L2/L3 retrieved context), logical validity (identifying invalid inferences), completeness (identifying what was ignored or overlooked), confidence calibration (flagging where confidence is overstated), alternative interpretations (finding equally valid but different conclusions), and practical risks (identifying consequences that were not considered). If it finds no material problems, it returns "approved" with a list of what it checked. If it finds problems, it returns "rejected" with specific objections and routes back to generator.

**`subagent_synthesis` → `agents/sub_agents/synthesis_agent.py`**  
Receives the approved output after debate convergence. Produces the final, user-facing response. Applies persona mode formatting (adjusting directness, warmth, and structure based on which of the 7 friend modes is active). Attaches the calibrated confidence score. Ensures the absolute honesty mandate is met — explicitly states uncertainty where it exists, labels untested proposals as untested. Passes to `node_hitl_gate` if the output proposes a destructive or irreversible action.

**Sub-sub-agents (Layer 4 — Atomic Tasks):**  
Domain agents spawn sub-sub-agents for single-focus atomic operations. Examples: the security agent spawns a sub-sub-agent for a single network port analysis. The research agent spawns a sub-sub-agent for a single academic paper extraction. The project manager spawns a sub-sub-agent for a single deliverable within a project milestone. Sub-sub-agents are implemented as lightweight LangGraph subgraphs with a minimal state (input task, context, output slot). They do not have their own memory access — they receive all needed context from their parent domain agent and return a single result. This keeps Layer 4 fast and focused.

---

### 4.4 Concurrent Background Runtimes

All background processes run in a dedicated background thread as `asyncio` tasks. They never share the foreground event loop. Communication to the foreground orchestrator is one-directional via a thread-safe `queue.Queue` — background processes push results; the foreground orchestrator reads them at the next opportunity without blocking.

**`agents/background/co_mode_agent.py` — always active**  
Runs a daily planning cycle at a configured morning time (default 07:00 user timezone from `settings.yaml`). Reads all input sources, computes the daily directive plan, and pushes it to the foreground queue. Updates the plan throughout the day as new information arrives. Monitors for deviations from the plan and pushes re-prioritisation updates when detected.

**`agents/background/proactive_monitor.py` — always active**  
Runs a continuous monitoring loop with a configured check interval (default: every 30 minutes). Monitors: news feeds relevant to active projects, scientific publication databases for topics in the user's research areas, financial market feeds relevant to the user's portfolio, regulatory and legal update sources, competitor and market intelligence sources. Scores each detected item for relevance to the user's current context using BM25 match against vault content. Items above relevance threshold are classified as positive (opportunity) or negative (risk/threat) and pushed to the foreground queue as alerts.

**`agents/background/sleep_agent.py` — idle-triggered**  
Triggered when the system detects extended inactivity (default: 30 minutes of no user interaction, configurable in `settings.yaml`). Executes the following sleep cycle sequence:
1. Memory consolidation: reads all L3 vault nodes modified since last sleep cycle, runs BM25 similarity between nodes, merges nodes with similarity above threshold, updates networkx graph edges
2. Time-decay: applies decay scores to all nodes based on time since last access; nodes below minimum threshold moved to `vault/archive/`
3. Compression: reads task-execution memory entries from last active session and compresses to single-line summaries; originals deleted
4. Forgetting: deletes memory entries classified as irrelevant (no connection to any active project, quest, or known user interest area)
5. Dream synthesis: passes list of all unresolved problems and open questions to `intelligence/dream_synthesizer.py` for overnight background processing
6. Weekly fine-tuning trigger (if weekly cycle is due): launches Unsloth QLoRA training job using collected interaction data; uses `free_cloud_orchestrator.py` if local hardware is insufficient
7. Git commit: commits all vault changes with auto-generated commit message summarising what was modified
8. Git push: pushes to user's configured private GitHub repository

**`agents/background/project_manager_agent.py` — always active when projects exist**  
Runs as a persistent background task whenever there are active multi-year projects. Checks for available compute resources every 15 minutes. If resources are available and a project task queue is non-empty, spawns the appropriate domain agent for the next task. Monitors the world event feed from `proactive_monitor.py` for signals that affect active projects. When a plan-affecting signal is detected, triggers a plan re-evaluation and pushes a plan-change notification to the foreground queue.

---

## 5. REQUIRED FOLDER STRUCTURE [LOCKED CONSTRAINTS]

> **SYSTEM INSTRUCTION TO CODING AI:** The codebase must EXACTLY match this structure. Do not rename folders or move files. You may add files strictly within existing folders if required by implementation. You may not restructure, merge, or rename any folder in this base structure. All new files must follow the naming conventions established here.

```text
[PROJECT_NAME]/
│
├── core/                                      # Core system intelligence — never modified by domain agents
│   ├── __init__.py
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── main_graph.py                      # Primary LangGraph StateGraph — the master foreground loop
│   │   ├── state_schema.py                    # Complete ProjectState TypedDict definition
│   │   ├── router.py                          # Intent-to-agent routing + complexity classification
│   │   ├── node_handlers.py                   # All LangGraph node function implementations
│   │   ├── background_manager.py              # Background thread lifecycle + queue.Queue management
│   │   ├── interrupt_handler.py               # LangGraph interrupt() state serialise/resume logic
│   │   └── session_manager.py                 # Session tracking, resumption, and timeout handling
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── l1_active.py                       # Letta-style named memory blocks in LangGraph state dict
│   │   ├── l2_index.py                        # rank_bm25 BM25Okapi index + networkx DiGraph operations
│   │   ├── l3_vault.py                        # Obsidian vault read/write (pathlib + python-frontmatter)
│   │   ├── extractor.py                       # Classifies info into Class A/B/C/D for memory routing
│   │   ├── sleep_cycle.py                     # Orchestrates all 7 sleep cycle phases in sequence
│   │   ├── knowledge_base.py                  # Project-specific knowledge base builder and manager
│   │   ├── temporal_graph.py                  # Temporal edge logic for networkx (start_date/end_date)
│   │   ├── entity_extractor.py                # NER for populating knowledge graph nodes and edges
│   │   ├── vault_indexer.py                   # Rebuilds BM25 index from vault file paths on startup
│   │   └── compression_engine.py              # Compresses Class B memories to single-line summaries
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── local_model.py                     # llama.cpp wrapper (llama-cpp-python) + fine-tune mode
│   │   ├── cloud_router.py                    # LiteLLM unified gateway for all cloud providers
│   │   ├── complexity_classifier.py           # RouteLLM-style query complexity scoring (0.0–1.0)
│   │   ├── model_config.py                    # Reads model paths from settings.yaml — no hardcoded names
│   │   ├── prompt_builder.py                  # Constructs role-specific prompts for each agent type
│   │   ├── response_parser.py                 # Validates and parses LLM responses against expected schema
│   │   ├── token_counter.py                   # Per-call token tracking, session totals, cost calculation
│   │   └── retry_handler.py                   # Handles failed inference calls with exponential backoff
│   └── persona/
│       ├── __init__.py
│       ├── emotional_detector.py              # Detects user emotional state from text + voice signals
│       ├── mode_selector.py                   # Selects one of 8 friend modes based on detected state
│       ├── voice_modulator.py                 # Maps persona modes to TTS parameter overrides
│       ├── persona_loader.py                  # Loads and hot-reloads SOUL.md, EMPATHY.md, RATIONAL.md
│       └── state_tracker.py                   # Tracks conversation state history for mode transitions
│
├── agents/                                    # All agent implementations — orchestrator, domain, sub
│   ├── __init__.py
│   ├── foreground/
│   │   ├── __init__.py
│   │   ├── conversation_agent.py              # Handles everyday conversation — fast path, no critic needed
│   │   ├── task_agent.py                      # Handles immediate task execution requests
│   │   └── context_builder.py                 # Assembles full context package for domain agent handoff
│   ├── background/
│   │   ├── __init__.py
│   │   ├── co_mode_agent.py                   # CO daily planning — always active, gathers all sources
│   │   ├── proactive_monitor.py               # Continuous world monitoring — push alerts on relevance
│   │   ├── sleep_agent.py                     # Idle-triggered — runs all 7 sleep cycle phases
│   │   ├── project_manager_agent.py           # Multi-year project autonomous execution and adaptation
│   │   ├── event_bus.py                       # Internal event system for background agent coordination
│   │   ├── resource_monitor.py                # CPU/RAM/GPU availability tracking via psutil
│   │   └── scheduler.py                       # Schedules background tasks (daily CO, weekly fine-tune)
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── security_agent.py                  # Full cybersecurity lifecycle: recon→exploit→remediate
│   │   ├── finance_agent.py                   # Investing, banking, tax, real estate, trading
│   │   ├── content_agent.py                   # Video, audio, graphics, social media, publishing
│   │   ├── research_agent.py                  # Multi-day Co-STORM deep research with citation
│   │   ├── tutoring_agent.py                  # Adaptive teaching: ZPD + Bloom's + deliberate practice
│   │   ├── digital_worker_agent.py            # General computer tasks: docs, email, meetings, calls
│   │   ├── discovery_agent.py                 # Level 6: MCTS + FunSearch autonomous discovery
│   │   ├── health_agent.py                    # Health records, appointments, medication, symptom tracking
│   │   ├── legal_agent.py                     # Legal research, contract drafting, compliance monitoring
│   │   ├── travel_agent.py                    # Trip planning, booking, visa research, expense tracking
│   │   └── negotiation_agent.py               # Negotiation strategy, simulation, real-time coaching
│   └── sub_agents/
│       ├── __init__.py
│       ├── critic_agent.py                    # Adversarial challenger — attacks every important output
│       ├── generator_agent.py                 # Produces proposed outputs and solutions
│       ├── synthesis_agent.py                 # Integrates debate outcome into final deliverable
│       └── debate_orchestrator.py             # Manages the generator→critic loop (max 5 iterations)
│
├── actuation/                                 # Everything that sees the screen and moves the computer
│   ├── __init__.py
│   ├── vision/
│   │   ├── __init__.py
│   │   ├── screen_capture.py                  # PIL/Pillow screenshot — memory only, never auto-saved
│   │   ├── qwen_vl.py                         # Qwen3-VL model inference → bbox_2d element map
│   │   ├── element_locator.py                 # Maps bbox_2d to click coordinates with scaling
│   │   ├── video_analyzer.py                  # Real-time video stream understanding (explicit command only)
│   │   └── ocr_engine.py                      # pytesseract OCR for terminal/text-heavy screen regions
│   ├── control/
│   │   ├── __init__.py
│   │   ├── mouse_controller.py                # pyautogui + human_mouse bezier curves — bypasses bot detect
│   │   ├── keyboard_controller.py             # pyautogui typing with randomised inter-key delays
│   │   ├── browser_controller.py              # browser-use DOM-based automation (fast, bot-friendly sites)
│   │   ├── scroll_controller.py               # Scroll actions with natural speed variation
│   │   └── clipboard_manager.py               # Clipboard read/write for copy-paste operations
│   ├── recognition/
│   │   ├── __init__.py
│   │   ├── face_recognizer.py                 # Local face encoding + identification — never cloud
│   │   └── voice_recognizer.py                # pyannote.audio voice fingerprint identification
│   └── apps/
│       ├── __init__.py
│       ├── minecraft_bridge.py                # Mineflayer JS bridge via Python subprocess wrapper
│       ├── app_controller.py                  # Generic visual control entry point for any installed app
│       ├── window_manager.py                  # Window focus, positioning, and sizing management
│       └── app_detector.py                    # Detects which application is currently in foreground
│
├── skills/                                    # Skill Forge, skill library, and MCP tool ecosystem
│   ├── __init__.py
│   ├── forge/
│   │   ├── __init__.py
│   │   ├── generator.py                       # LLM generates new Python skill from description
│   │   ├── sandbox.py                         # Docker Python SDK — isolated container execution
│   │   ├── verifier.py                        # pytest runner — evaluates sandbox output
│   │   ├── repair_loop.py                     # LLM repairs failed code — max 3 iterations
│   │   ├── hitl_gate.py                       # LangGraph interrupt() — shows code + waits for approval
│   │   ├── code_reviewer.py                   # Pre-reviews generated code for obvious errors before sandbox
│   │   └── dependency_resolver.py             # Identifies and resolves pip dependencies for new skills
│   ├── library/
│   │   ├── __init__.py
│   │   ├── skill_registry.py                  # Reads/writes SKILL.md index, manages skill lookup
│   │   ├── health_tracker.py                  # Tracks invocations/successes/failures, updates confidence
│   │   ├── skill_composer.py                  # Discovers and tests novel skill combinations autonomously
│   │   └── skill_versioner.py                 # Version management and rollback for installed skills
│   └── mcp/
│       ├── __init__.py
│       ├── client.py                          # Official MCP Python SDK — dynamic tools/list discovery
│       ├── server_factory.py                  # FastMCP — auto-generates MCP servers for new skills
│       ├── discovery.py                       # Runtime MCP server registration and deregistration
│       ├── server_registry.py                 # Maintains registry of all active MCP server instances
│       └── mcp_validator.py                   # Validates MCP server spec compliance before registration
│
├── communication/                             # All inbound and outbound communication channels
│   ├── __init__.py
│   ├── telegram_bot.py                        # Official Telegram Bot API — primary remote command channel
│   ├── voip_caller.py                         # Outbound calls in user's cloned voice via VoIP
│   ├── meeting_attendee.py                    # Joins video calls, transcribes, notes, produces brief
│   ├── realtime_coach.py                      # Live negotiation coaching via parallel audio listening
│   ├── notification_manager.py                # Routes all notifications to correct channel (tray/Telegram/voice)
│   ├── channel_router.py                      # Selects correct output channel based on context and urgency
│   └── voice/
│       ├── __init__.py
│       ├── stt.py                             # Whisper local STT — Hinglish fine-tuned checkpoint
│       ├── tts_standard.py                    # Kokoro-82M for everyday speech
│       ├── tts_emotional.py                   # Coqui XTTS for high-emotion responses
│       ├── voice_clone.py                     # User voice model training and inference — local only
│       ├── wake_word.py                        # Always-on listener for [PROJECT_NAME] wake word
│       ├── audio_processor.py                 # Noise reduction and audio normalisation pre-STT
│       └── speaker_diarizer.py                # Multi-speaker separation for meetings (pyannote.audio)
│
├── interfaces/                                # All user-facing surfaces
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                            # FastAPI app entry point — mounts all routers
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── task_routes.py                 # POST /task, GET /task/{id}/status, GET /task/{id}/result
│   │   │   ├── memory_routes.py               # POST /memory/search, GET /memory/active, etc.
│   │   │   ├── agent_routes.py                # GET /agents/status, POST /agents/spawn, etc.
│   │   │   ├── config_routes.py               # GET /config, PATCH /config, POST /config/name, etc.
│   │   │   ├── skill_routes.py                # GET /skills, POST /skills/{id}/approve, etc.
│   │   │   ├── usage_routes.py                # GET /usage, GET /usage/today, GET /usage/history
│   │   │   ├── project_routes.py              # GET /projects, POST /projects, GET /projects/{id}/plan
│   │   │   ├── co_mode_routes.py              # GET /co_mode/today, POST /co_mode/holiday, etc.
│   │   │   ├── alert_routes.py                # GET /alerts, PATCH /alerts/{id}/dismiss, etc.
│   │   │   ├── security_routes.py             # Security engagement creation and status endpoints
│   │   │   ├── finance_routes.py              # Portfolio, trading rules, and financial data endpoints
│   │   │   └── health_routes.py               # GET /health — system health and readiness check
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py                        # Local token authentication for all endpoints
│   │       ├── pii_scrubber.py                # presidio-analyzer strips PII before any cloud LLM call
│   │       ├── rate_limiter.py                # Prevents runaway API loops from agent errors
│   │       ├── request_logger.py              # Logs all requests to Langfuse for observability
│   │       └── error_handler.py               # Global exception handler — structured error responses
│   └── tray/
│       ├── __init__.py
│       ├── tray_app.py                        # pystray system tray entry point
│       └── tray_menu.py                       # Tray menu items, actions, and status indicators
│
├── security/                                  # Cybersecurity module — all operations here require authorization
│   ├── __init__.py
│   ├── guardrails.py                          # Guardrails AI schema enforcement for all outputs
│   ├── sandboxer.py                           # Docker Python SDK skill sandbox management
│   ├── malware_sandbox.py                     # Separate Docker sandbox for malware analysis only
│   ├── tool_orchestrator.py                   # Coordinates all security tools via visual control
│   ├── authorization_manager.py               # Manages and validates engagement authorization records
│   ├── vulnerability_db.py                    # Local CVE feed management (NVD + OSV RSS)
│   └── report_generator.py                    # Professional pentest report generation with CVSSv3
│
├── intelligence/                              # Advanced reasoning systems — run across all domain agents
│   ├── __init__.py
│   ├── causal_modeler.py                      # DoWhy + CausalPy causal chain analysis
│   ├── serendipity_engine.py                  # Cross-domain BM25 similarity → insight bridging
│   ├── calibration_tracker.py                 # Brier score tracking for confidence calibration
│   ├── cognitive_state_detector.py            # Detects flow/scattered/fatigued/creative/analytical state
│   ├── rhythm_learner.py                      # Learns biological peak hours from interaction patterns
│   ├── dream_synthesizer.py                   # Overnight unsolved problem processing via sub-agents
│   ├── social_graph.py                        # Relationship health tracking and network intelligence
│   ├── pattern_recognizer.py                  # Detects cross-interaction patterns in user behaviour
│   └── predictive_preloader.py                # Pre-loads context before calendar events (2–3hr ahead)
│
├── growth/                                    # User growth, accountability, and intelligence systems
│   ├── __init__.py
│   ├── quest_tracker.py                       # Main quest and side quest creation, tracking, reporting
│   ├── lie_detector.py                        # Passive inconsistency monitoring for CO-mode holidays
│   ├── co_mode_evaluator.py                   # Holiday request legitimacy evaluation and consequences
│   ├── intelligence_preserver.py              # Think-first gates, over-reliance detection, Socratic mode
│   ├── deliberate_practice.py                 # Sub-skill gap identification and targeted practice design
│   ├── progress_tracker.py                    # Cross-quest milestone tracking and celebration
│   └── habit_tracker.py                       # Habit formation tracking with streak and regression detection
│
├── compute/                                   # Compute resource management — local and free cloud
│   ├── __init__.py
│   ├── local_checker.py                       # psutil — monitors available CPU/RAM/GPU before spawning tasks
│   ├── free_cloud_orchestrator.py             # Visual browser control of Colab/Kaggle/HuggingFace sessions
│   ├── job_queue.py                           # Priority queue for heavy computation jobs awaiting resources
│   └── session_manager.py                     # Manages free cloud session lifecycle: open→run→retrieve→delete
│
├── observability/                             # System transparency — logs, traces, dashboard
│   ├── __init__.py
│   ├── langfuse_client.py                     # Self-hosted Langfuse LLM call tracing
│   ├── otel_spans.py                          # OpenTelemetry GenAI spans for distributed tracing
│   ├── dashboard_filter.py                    # Surfaces only major decisions — filters routine operations
│   ├── performance_monitor.py                 # System latency, throughput, and resource usage tracking
│   ├── error_tracker.py                       # Categorises and tracks errors by type and frequency
│   └── usage_reporter.py                      # Generates cost and usage reports in user's currency
│
├── config/                                    # All user configuration — plain text, human editable
│   ├── SOUL.md                                # Persona definition — who [PROJECT_NAME] is and how it behaves
│   ├── USER.md                                # User profile, mastery, quests, rhythm, lie log (full schema)
│   ├── EMPATHY.md                             # Emotional response rules per detected state
│   ├── RATIONAL.md                            # Analytical mode response rules
│   ├── settings.yaml                          # All system settings — ports, models, intervals, thresholds
│   ├── project_name.txt                       # The configured [PROJECT_NAME] — used as wake word
│   ├── TRADING_RULES.md                       # User-defined investment trading parameters and hard limits
│   ├── MONITORING_TOPICS.md                   # Configured proactive alert topics beyond auto-detected ones
│   ├── ENGAGEMENT_LOG.md                      # Security engagement authorizations — required before recon
│   └── VOICE_PROFILES.md                      # Index of known voice fingerprints for recognition
│
├── vault/                                     # L3 Obsidian vault — all permanent memory as plain .md files
│   ├── projects/
│   │   └── _PROJECT_TEMPLATE.md               # Template: title, deadline, phases, task queue, blockers
│   ├── research/                              # Deep research outputs with full citations
│   ├── skills/                                # Installed skill .py files and _health.yaml records
│   ├── people/
│   │   └── _PERSON_TEMPLATE.md                # Template: name, relationship, contact log, pending tasks
│   ├── knowledge/                             # General knowledge acquired across all topics
│   ├── finance/
│   │   ├── portfolio.md                       # Current investment holdings and valuations
│   │   └── transactions.md                    # All financial transactions and tax events log
│   ├── security/
│   │   └── authorizations/                    # Per-engagement authorization records (required before recon)
│   ├── health/                                # Health records, appointment history, medication log
│   ├── legal/                                 # Contracts, compliance obligations, renewal deadlines
│   └── archive/                               # Time-decayed nodes below minimum confidence threshold
│       ├── skills/
│       ├── research/
│       └── knowledge/
│
├── models/                                    # All local AI model weights — never committed to Git
│   ├── llm/                                   # llama.cpp GGUF model files (user downloads at setup)
│   ├── voice_clone/                           # User voice clone model weights — local only, never uploaded
│   ├── whisper/                               # Whisper base + Hinglish fine-tuned checkpoint
│   ├── tts/                                   # Kokoro-82M and Coqui XTTS model weights
│   ├── vision/                                # Qwen3-VL model weights
│   └── face/                                  # face_recognition model weights and user face encodings
│
├── tests/                                     # Full test suite — unit, integration, and sandbox verification
│   ├── __init__.py
│   ├── conftest.py                            # pytest config, shared fixtures, mock LLM setup
│   ├── fixtures/
│   │   ├── sample_vault_notes.md              # 50+ sample vault documents for retrieval testing
│   │   ├── sample_user_md.yaml                # Complete USER.md fixture for all growth tests
│   │   ├── mock_llm_responses.json            # Pre-defined LLM responses for deterministic unit tests
│   │   └── sample_skills/                     # Pre-built test skills for forge and library tests
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_memory_extractor.py           # Tests Class A/B/C/D classification accuracy
│   │   ├── test_bm25_index.py                 # Tests BM25 retrieval precision and recall
│   │   ├── test_knowledge_graph.py            # Tests networkx graph operations and temporal edges
│   │   ├── test_temporal_graph.py             # Tests start_date/end_date edge logic
│   │   ├── test_persona_modes.py              # Tests all 8 mode selection rules
│   │   ├── test_emotional_detector.py         # Tests emotion classification from text samples
│   │   ├── test_skill_health.py               # Tests confidence score update rules
│   │   ├── test_co_mode_evaluator.py          # Tests holiday Category A/B/C evaluation logic
│   │   ├── test_lie_detector.py               # Tests inconsistency detection across interaction history
│   │   ├── test_intelligence_preserver.py     # Tests think-first gate trigger conditions
│   │   ├── test_calibration_tracker.py        # Tests Brier score calculation and recalibration
│   │   ├── test_pii_scrubber.py               # Tests PII detection and anonymisation
│   │   ├── test_token_counter.py              # Tests per-call and session token accumulation
│   │   ├── test_complexity_classifier.py      # Tests routing threshold decisions
│   │   └── test_skill_composer.py             # Tests autonomous skill combination discovery
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_main_graph_flow.py            # End-to-end graph traversal for each intent type
│   │   ├── test_skill_forge_pipeline.py       # Full forge: generate→sandbox→verify→HITL→install
│   │   ├── test_sleep_cycle.py                # Full 7-phase sleep cycle with vault state verification
│   │   ├── test_background_agents.py          # Background thread startup, queue push, foreground read
│   │   ├── test_hitl_gates.py                 # All 8 HITL gate trigger + approve + reject flows
│   │   ├── test_memory_pipeline.py            # Full L1→L2→L3 write and retrieval round-trip
│   │   ├── test_critic_circuit.py             # Generator→critic debate loop convergence
│   │   └── test_telegram_commands.py          # Text and audio note command processing via Telegram
│   └── skill_verification/
│       ├── __init__.py
│       ├── test_sandbox_isolation.py          # Verifies Docker sandbox has no host access
│       ├── test_sandbox_network.py            # Verifies sandbox has no outbound network
│       └── test_host_execution.py             # Verifies approved skills run correctly on host
│
├── scripts/                                   # Operational shell scripts for system management
│   ├── start.sh                               # Starts FastAPI daemon, tray app, and background agents
│   ├── stop.sh                                # Gracefully stops all services
│   ├── restart.sh                             # Full service restart with state preservation
│   ├── status.sh                              # Shows running service status and resource usage
│   ├── reset_memory.sh                        # Emergency: clears L1/L2, preserves L3 vault intact
│   ├── export_vault.sh                        # Manual vault archive export for external backup
│   ├── rebuild_index.sh                       # Rebuilds BM25 index and networkx graph from vault
│   └── update.sh                              # Updates Python dependencies via uv
│
├── bootstrap/                                 # Installation and first-run setup
│   ├── install.sh                             # uv-based cross-platform installer (Windows/macOS/Linux)
│   ├── first_run.py                           # Interactive first-run: name, voice clone, models, config
│   ├── requirements.txt                       # All Python dependencies with pinned versions
│   ├── update.py                              # Updates system components while preserving vault and config
│   └── verify_install.py                      # Validates all dependencies and models are correctly installed
│
├── docker/                                    # Docker configurations for all sandboxed environments
│   ├── skill_sandbox.Dockerfile               # Isolated skill testing: no network, tmpfs, non-root, 30s
│   ├── malware_sandbox.Dockerfile             # Forensics sandbox: no network, syscall logging, snapshots
│   ├── docker-compose.yml                     # Production compose: skill sandbox + malware sandbox
│   └── docker-compose.dev.yml                 # Development compose: adds volume mounts for faster iteration
│
├── docs/                                      # Auto-generated and maintained documentation
│   ├── API_REFERENCE.md                       # Complete FastAPI endpoint reference (auto-generated)
│   ├── SETUP_GUIDE.md                         # Step-by-step installation and configuration guide
│   └── WORKFLOW_GUIDE.md                      # Plain-language guide to major system workflows
│
├── .github/
│   └── workflows/
│       └── vault_integrity.yml                # GitHub Actions: verifies vault structure on each push
│
├── .gitignore                                 # Excludes: models/, *.pkl, .env, vault/finance/, vault/health/
├── .env.example                               # Template for sensitive environment variables
├── pyproject.toml                             # Project metadata and uv dependency management
└── README.md                                  # Installation quickstart and feature overview
```

**Total file count:** 147 Python/config/shell files + vault templates + test fixtures  
**Directories:** 52 directories across all layers

### 5.1 Enforced LangGraph Node Naming Conventions [LOCKED CONSTRAINTS]

Every LangGraph node across every file must follow these exact naming patterns:

**Processing nodes:** `node_extract_intent`, `node_retrieve_memory`, `node_route_task`, `node_synthesize_output`, `node_update_memory`, `node_hitl_gate`, `node_check_intelligence_preserve`

**Execution nodes:** `node_execute_[action]` (e.g., `node_execute_sandbox`, `node_execute_host`, `node_execute_vision`, `node_execute_actuation`, `node_execute_search`)

**Verification nodes:** `node_verify_[thing]` (e.g., `node_verify_pytest`, `node_verify_result`, `node_verify_skill`)

**Agent entry points:** `agent_[domain]_entry` (e.g., `agent_security_entry`, `agent_finance_entry`, `agent_research_entry`)

**Sub-agents:** `subagent_critic`, `subagent_generator`, `subagent_synthesis`

No other naming conventions are permitted for LangGraph nodes.

---

## 6. SYSTEM SCHEMAS AND ENDPOINTS [LOCKED CONSTRAINTS]

### 6.1 FastAPI Endpoints — Complete Specification

> All endpoints served on `localhost` only. Port configurable in `settings.yaml` (default: 8000). All endpoints require local auth token (set during first run, stored in `config/settings.yaml`).

```
# Task Management
POST   /task                        Submit any task. Body: {input: str, modality: str, priority: int}
GET    /task/{task_id}/status       Poll task progress. Returns: {status, progress_pct, eta_seconds}
GET    /task/{task_id}/result       Get completed result. Returns: {output, confidence, sources}
DELETE /task/{task_id}             Cancel a running task.

# Memory Operations
POST   /memory/search               Full-text search vault. Body: {query: str, limit: int, domains: list}
GET    /memory/active               Read all L1 memory blocks. Returns: {blocks: dict}
PATCH  /memory/active               Update a specific L1 block. Body: {block_name: str, content: str}
POST   /memory/compress             Trigger manual compression of a topic. Body: {topic: str}
DELETE /memory/forget               Mark topic for deletion on next sleep. Body: {topic: str, reason: str}

# Agent Management
GET    /agents/status               All running agents, their state, and resource usage.
POST   /agents/spawn                Manually spawn a domain agent. Body: {agent: str, task: str}
DELETE /agents/{agent_id}           Stop a specific agent instance.
GET    /agents/background/status    Status of all four background runtimes.

# Multi-Year Projects
GET    /projects                    List all projects with status and progress.
POST   /projects                    Create new project. Body: {title, description, deadline, domains}
GET    /projects/{id}               Full project details including current plan.
GET    /projects/{id}/plan          Detailed phased execution plan.
PATCH  /projects/{id}               Update project parameters.
POST   /projects/{id}/replan        Trigger immediate plan re-evaluation.
GET    /projects/{id}/blockers      List current blockers and their resolution status.

# CO-Mode Daily Planning
GET    /co_mode/today               Today's complete directive plan with priorities and time allocations.
GET    /co_mode/status              Whether CO mode is active or holiday, and until when.
POST   /co_mode/holiday             Submit holiday request. Body: {reason: str, start: date, end: date}
GET    /co_mode/holiday/{id}/status Holiday request evaluation status.
GET    /co_mode/history             Past 30 days of daily plans.

# Proactive Alerts
GET    /alerts                      All unread alerts, newest first, with relevance scores.
GET    /alerts?type=positive        Only opportunity alerts.
GET    /alerts?type=negative        Only risk/threat alerts.
PATCH  /alerts/{id}/dismiss         Mark alert as read and dismissed.
POST   /alerts/config               Configure monitoring topics and check frequency.

# Skill Management
GET    /skills                      All skills with health scores and usage stats.
GET    /skills/{id}                 Full skill details including code and health history.
POST   /skills/{id}/approve         Approve skill after HITL gate. (Body empty — approval is the action)
DELETE /skills/{id}                 Archive a skill manually.
POST   /skills/forge                Trigger skill creation for a described need. Body: {description: str}

# Usage and Cost Display
GET    /usage                       Token usage and cost in configured currency. Breakdown by model and session.
GET    /usage/today                 Today's usage only.
GET    /usage/history?days=30       Historical usage.

# Configuration
GET    /config                      All current settings.
PATCH  /config                      Update any setting. Body: {key: str, value: any}
POST   /config/voice_clone          Start voice clone training. Body: {audio_file_path: str}
POST   /config/name                 Update project name (wake word). Body: {name: str}

# Observability Dashboard
GET    /dashboard                   Last 50 major decisions — plan changes, skill installs, alerts triggered.
GET    /dashboard/decisions         Full decision log with reasoning.
GET    /dashboard/agents            Agent performance metrics.
```

### 6.2 Docker Sandbox Specifications [LOCKED CONSTRAINTS]

**Skill Sandbox (`docker/skill_sandbox.Dockerfile`):**
```
Base image:          python:3.11-slim
Network access:      DISABLED (--network none)
Filesystem:          tmpfs mount only at /tmp/sandbox. No host filesystem access.
Memory hard limit:   512MB (--memory 512m)
CPU hard limit:      1 core (--cpus 1)
Execution timeout:   30 seconds (subprocess timeout, container killed after)
User:                UID 1000, non-root (USER 1000)
Read-only root:      Yes (--read-only with tmpfs exceptions)
Capabilities:        All dropped (--cap-drop ALL)
Security profile:    seccomp default profile
```

**Malware Analysis Sandbox (`docker/malware_sandbox.Dockerfile`):**
```
Base image:          remnux/remnux-distro (or equivalent forensics distro)
Network access:      DISABLED (--network none)
Filesystem:          Read-only host mount at /samples for input only.
                     tmpfs at /tmp for working space.
                     Host-mounted log volume at /logs for syscall output.
Memory hard limit:   1GB (--memory 1g)
CPU hard limit:      2 cores (--cpus 2)
User:                Non-root isolated user
Syscall logging:     All syscalls logged via sysdig or auditd to /logs volume
Snapshot:            Pre-execution filesystem hash captured; post-execution diff computed
```

### 6.3 Skill Health Schema [LOCKED CONSTRAINTS]

Every skill in `vault/skills/` must have a corresponding health record at `vault/skills/{skill_id}_health.yaml` with exactly this schema:

```yaml
id: "skill_{uuid4_8chars}"
name: "human_readable_skill_name"
description: "Single sentence: what this skill does and when it is used."
version: "1.0.0"
created_date: "YYYY-MM-DD"
last_modified_date: "YYYY-MM-DD"
last_used_date: "YYYY-MM-DD"
entry_point: "vault/skills/{skill_name}.py"
dependencies:
  - "package_name==version"
invocation_count: 0
success_count: 0
failure_count: 0
last_failure_reason: null
confidence_score: 1.0          # Float 0.0-1.0. Decreases on failure. Below 0.5: flagged. Below 0.25: archived.
status: "active"               # Enum: active | flagged | archived
mcp_server_path: null          # Path to MCP server if skill was wrapped, else null
composed_from: []              # List of skill IDs if this is a composition, else empty
autonomy_level: "approval_required"  # Enum: approval_required | auto_approved | restricted
tags: []                       # List of domain tags for filtering
```

Confidence score update rules (enforced in `skills/library/health_tracker.py`):
- Successful invocation: `confidence = min(1.0, confidence + 0.02)`
- Failed invocation: `confidence = max(0.0, confidence - 0.15)`
- Status transitions: `confidence < 0.5` → status becomes `flagged`; `confidence < 0.25` → status becomes `archived` (moved to `vault/archive/skills/`)

### 6.4 USER.md Schema [LOCKED CONSTRAINTS]

`config/USER.md` must maintain the following YAML frontmatter at all times. The system reads and writes this file. Never store sensitive financial or medical data in plaintext here — store references to encrypted vault entries.

```yaml
---
display_name: "[user display name]"
project_name: "[PROJECT_NAME]"
preferred_languages:
  - "Hinglish"
  - "English"
timezone: "Asia/Kolkata"
currency_display: "INR"        # Currency for cost display

mastery_levels: {}             # {topic_slug: float 0.0-1.0} — updated after every learning interaction

cognitive_peaks:
  deep_work: []                # List of time ranges e.g. ["09:00-11:00"]
  creative: []
  administrative: []
  low_energy: []
biological_rhythm_confidence: 0.0   # Rises from 0.0 to 1.0 as data accumulates

main_quests: []
# Each quest: {id, title, description, deadline, progress_pct, status, linked_side_quests: []}

side_quests: []
# Each quest: {id, title, linked_main_quest_id, status, created_date, completed_date}

relationship_map: []
# Each: {name, relationship_type, last_contact_date, health_score 0.0-1.0, notes, vault_profile_path}

co_mode_status: "active"       # Enum: active | holiday
holiday_log: []
# Each: {id, reason, start_date, end_date, approved, evaluated_as, consequence_if_lied}

lie_detection_log: []
# Each: {date, claimed_reason, holiday_id, evidence_source, discovered_date, consequence_assigned}

over_reliance_flags: {}        # {topic_slug: float 0.0-1.0} — above 0.7 triggers Socratic mode

intelligence_growth_log: []
# Weekly snapshot: {week_start, mastery_snapshot: {}, reliance_snapshot: {}}

wake_word_sensitivity: "medium"  # Enum: low | medium | high
persona_mode_override: null      # If set, forces a specific persona mode regardless of detection
---
```

---

## 7. FEATURE SPECIFICATIONS AND USER WORKFLOWS

> **SYSTEM INSTRUCTION TO CODING AI:** The following section defines every major feature as a logical state transition flow. Each workflow specifies: trigger conditions, exact state transitions, decision points, data transformations, HITL gates, and output format. Implement these flows exactly. Where you see `[IMPLEMENTATION_DETAIL]`, use your best judgement based on the established stack.

---

### 7.1 System Initialisation and First Run

**File:** `bootstrap/first_run.py`

**Trigger:** First execution after installation, or when `config/project_name.txt` does not exist.

**Flow:**
```
1. Display welcome screen via terminal
2. Prompt: "What would you like to name your AI?" → write to config/project_name.txt
3. Prompt: "What is your name?" → write to USER.md display_name
4. Prompt: "What is your timezone?" → write to USER.md timezone
5. Prompt: "What currency should I display costs in?" → write to USER.md currency_display
6. Prompt: "Would you like to set up voice cloning now? (Recommended)"
   → If YES: record 30-second voice sample → invoke communication/voice/voice_clone.py → train local model
   → If NO: skip (can be done later via POST /config/voice_clone)
7. Prompt: "Configure your Telegram bot for remote commands?"
   → If YES: display Telegram bot creation instructions → prompt for bot token → write to settings.yaml
   → If NO: skip
8. Prompt: "Configure local AI model?"
   → Display instruction to check HuggingFace for best 3-8B model → prompt for model path
   → Write to settings.yaml
9. Prompt: "Configure cloud AI model? (Optional)"
   → If YES: prompt for provider and API key → write to settings.yaml → smart routing activates
   → If NO: skip (local-only mode)
10. Prompt: "Configure private GitHub repository for backup?"
    → If YES: prompt for repo URL and token → write to settings.yaml → test connection
    → If NO: skip (local-only Git without push)
11. Initialise vault directory structure
12. Create initial USER.md, SOUL.md, EMPATHY.md, RATIONAL.md from templates
13. Initialise L2 index (empty BM25 + empty networkx graph)
14. Start background runtimes
15. Start FastAPI daemon
16. Start pystray tray app
17. Activate wake word listener
18. First CO-mode run → produces welcome brief + initial daily plan
19. System ready — display completion message
```

---

### 7.2 Wake Word and Voice Input Pipeline

**File:** `communication/voice/wake_word.py` + `communication/voice/stt.py`

**Trigger:** Always-on microphone listener detects wake word (value from `config/project_name.txt`).

**Flow:**
```
1. wake_word.py continuously monitors microphone at very low CPU usage [IMPLEMENTATION_DETAIL: use pvporcupine or silero-vad]
2. Wake word detected → audio recording starts (captures until silence detected)
3. Audio buffer → communication/voice/stt.py → Whisper local model → transcript string
4. Transcript → POST /task with modality: "voice"
5. Parallel: cognitive_state_detector.py analyses voice characteristics (pace, energy, pitch variation) → updates detected_cognitive_state in state
6. Parallel: emotional_detector.py analyses voice tone → updates detected_emotion in state
7. Task enters main graph as standard input
8. Response generated → emotional register evaluated → tts_standard.py OR tts_emotional.py selected
9. Audio output played through speakers
10. Wake word listener resumes
```

**Important rule:** The system never records audio without the wake word trigger. The listener processes audio frames locally for wake word detection only — no audio is stored or transmitted.

---

### 7.3 Standard Conversation and Task Flow

**Files:** `core/orchestrator/main_graph.py`, `agents/foreground/conversation_agent.py`

**Trigger:** Any user input via any modality (text, voice, Telegram, wake word).

**Flow:**
```
State: user_input received

node_extract_intent:
  → semantic-router classifies intent (confidence threshold: 0.85)
  → If confidence < 0.85: ask clarifying question before proceeding
  → Output: intent string, initial complexity estimate

node_retrieve_memory:
  → L1 check: read current memory blocks (instant, always in state)
  → L2 BM25 search: query = user_input → top 10 relevant vault notes retrieved
  → L2 networkx: expand retrieved notes by one graph hop → related context added
  → Output: retrieved_context list, updated l1_memory_blocks

node_check_intelligence_preserve:
  → intelligence_preserver.py evaluates: is this a reasoning task the user should attempt?
  → Checks over_reliance_flags for current topic
  → If think-first gate triggered: respond with guiding question → END (do not proceed to answer)
  → If socratic_mode_active: route to tutoring_agent regardless of original intent
  → Otherwise: proceed

node_route_task:
  → complexity_classifier.py scores complexity: 0.0-1.0
  → If complexity > 0.7 AND cloud model configured: LiteLLM → cloud model
  → If complexity <= 0.7 OR no cloud model: llama.cpp local model
  → Route to appropriate domain agent based on intent

[domain agent subgraph executes]

subagent_critic (if output is "important" class):
  → Adversarial challenge → approve or iterate

node_synthesize_output:
  → mode_selector.py: select persona mode based on detected_emotion + context
  → voice_modulator.py: set TTS parameters for selected mode
  → Format response according to persona mode
  → Attach confidence score if output contains factual claims
  → Check for pending background alerts → append if highly relevant

node_hitl_gate:
  → If output proposes destructive/irreversible action: interrupt()
  → Describe action, risk level, and reversibility to user
  → Wait for explicit approval
  → On approval: proceed
  → On rejection: explain what was blocked and why

node_update_memory:
  → extractor.py classifies each piece of information in this interaction:
    - Important fact/knowledge: write to L3 vault (vault/knowledge/ or relevant domain folder)
    - Task outcome: write compressed summary to L3 vault
    - Mundane exchange: schedule for compression in next sleep cycle
    - Irrelevant to any project: schedule for deletion in next sleep cycle
  → L1 active memory blocks updated with new context
  → L2 BM25 index updated with new vault entries
  → L2 networkx graph updated with new entity relationships

Output delivered via appropriate channel
```

---

### 7.4 CO-Mode Daily Planning

**File:** `agents/background/co_mode_agent.py`, `growth/co_mode_evaluator.py`

**Trigger:** Daily at configured morning time (default 07:00) OR on demand via GET /co_mode/today.

**Flow:**
```
1. Data gathering phase (all via visual computer control or APIs):
   a. Read calendar events for today and next 3 days
   b. Read unread WhatsApp messages (via visual control of WhatsApp app/web)
   c. Read unread email (via visual control of email client)
   d. Read Instagram notifications and DMs (via visual control)
   e. Read Telegram messages
   f. Read all active project status from vault/projects/
   g. Read USER.md: main_quests, side_quests, pending tasks from yesterday
   h. Read proactive_monitor.py alert queue: unread alerts
   i. Read co_mode_evaluator.py output: current CO mode status

2. Synthesis phase:
   → All gathered data assembled into context
   → LLM generates prioritised daily plan considering:
     - Meeting and commitment deadlines (non-negotiable time blocks)
     - Active project milestones and approaching deadlines
     - Main quest and side quest advancement tasks
     - Follow-up actions from unread messages
     - Proactive alert responses required
     - biological_rhythm_confidence: if above 0.6, schedule deep work during detected peak hours
   → Plan formatted as time-allocated directive list with priority and estimated duration

3. Output format:
   Morning brief: summary of overnight events + today's plan
   Directive plan: ordered list of tasks with {priority, description, estimated_duration, source, deadline}

4. Real-time updates:
   → Monitor task completion signals (user marks tasks done via any interface)
   → Monitor for new urgent inputs throughout the day
   → Recalculate and push updated plan when significant changes occur

5. CO mode gate (evaluated by co_mode_evaluator.py):
   → If user has approved holiday: CO mode suspends, gentle check-in only
   → If user has unapproved holiday request: see Section 7.14
   → Otherwise: CO mode is always active
```

---

### 7.5 Multi-Year Project Management

**Files:** `agents/background/project_manager_agent.py`, `vault/projects/`

**Trigger:** User creates a new project via POST /projects or via conversation ("Start a project called X with deadline Y").

**Project creation flow:**
```
1. User provides: project title, description, deadline, any known constraints
2. agent_project_manager spawns research sub-agent → gathers all existing knowledge on project domain
3. LLM generates: phased execution plan with milestones, deliverables, resource estimates, risk register
4. subagent_critic reviews plan for logical gaps, unrealistic timelines, missing dependencies
5. Revised plan saved to vault/projects/{project_id}/PLAN.md
6. Project registered in USER.md main_quests with progress tracking
7. Project task queue initialised
8. Background monitoring configured: which world events should trigger plan re-evaluation
```

**Ongoing execution flow (runs when resources available):**
```
1. local_checker.py confirms sufficient free resources
2. Next task dequeued from project task queue
3. Appropriate domain agent spawned for that task
4. Task executed autonomously
5. Result saved to vault/projects/{project_id}/
6. Task marked complete, progress updated
7. Next task enqueued
```

**Blocker resolution flow:**
```
Blocker detected (agent cannot proceed)
→ FIRST: Push notification to user explaining blocker and asking for input
→ If user provides answer: proceed with answer incorporated
→ If user cannot answer OR does not respond within configured timeout:
  → Unconventional thinking path activates:
    1. subagent_generator explores first-principles approaches (not in any textbook or standard methodology)
    2. serendipity_engine.py searches for analogous solved problems in other domains
    3. discovery_agent considered if problem requires novel solution
    4. Proposed unconventional approach labelled explicitly as "untested, first-principles proposal"
    5. If any approach produces a testable hypothesis: execute in sandbox environment
    6. Results logged to project vault
    7. User notified of outcome
→ If no resolution found: blocker logged with full context, project pauses at this task, other task queue items proceed
```

**World-event plan adaptation flow:**
```
proactive_monitor.py detects event relevant to project
→ Relevance score calculated against project PLAN.md content
→ If relevance > threshold:
  → LLM assesses impact on current plan
  → If impact is significant: generate revised plan
  → subagent_critic reviews revised plan
  → Push notification to user: "Plan change detected for [project]. Here is what changed and why."
  → User can approve, modify, or reject the plan change
  → Approved change replaces current plan in vault
```

---

### 7.6 Skill Forge — New Skill Creation and Installation

**Files:** `skills/forge/`, `skills/library/`

**Trigger:** System encounters a task it cannot complete with existing skills, OR user explicitly requests a new skill.

**Flow:**
```
1. Need identification:
   → System determines what Python function would solve the unmet need
   → Checks skill_registry.py: does a skill for this already exist?
   → If exists but failing: route to repair flow, not creation
   → If does not exist: proceed with creation

2. Code generation (skills/forge/generator.py):
   → LLM generates Python function with: clear docstring, type hints, error handling, logging
   → Code stored as candidate in memory (not yet on disk)

3. Sandbox execution (skills/forge/sandbox.py):
   → Docker Python SDK creates skill_sandbox container
   → Candidate code + test inputs written to container tmpfs
   → Code executed inside container
   → Container output and any exceptions captured
   → Container destroyed

4. Verification loop (skills/forge/verifier.py):
   → pytest runs against captured output
   → If ALL tests pass: proceed to HITL gate
   → If ANY tests fail:
     → skills/forge/repair_loop.py receives failure trace
     → LLM analyses error and generates repaired code
     → Iteration count incremented
     → Return to step 3 (sandbox execution)
     → Maximum 3 repair iterations
     → If still failing after 3 iterations: skill abandoned, user notified with failure summary

5. HITL approval gate (skills/forge/hitl_gate.py):
   → LangGraph interrupt() called
   → User presented with:
     - Skill name and description
     - Full source code
     - Test results
     - What permissions it requires (file access, network, etc.)
     - Risk assessment
   → User responds YES or NO
   → If NO: skill discarded, user can provide feedback for redesign
   → If YES: proceed to installation

6. Installation:
   → Code written to vault/skills/{skill_name}.py
   → Health record created at vault/skills/{skill_name}_health.yaml (initial confidence: 1.0)
   → Skill registered in skill_registry.py
   → L2 index updated
   → If skill should be accessible as MCP tool: mcp/server_factory.py wraps it in FastMCP server

7. Host execution capability:
   → After installation, skill can be invoked by any domain agent
   → Runs on host machine with full file system access (not in sandbox)
   → health_tracker.py records every invocation outcome
```

---

### 7.7 Computer Vision and Actuation Pipeline

**Files:** `actuation/`

**Trigger:** Any task requiring interaction with a GUI application, website, or screen element.

**Flow:**
```
1. Task description received by agent_digital_worker_entry (or any domain agent)

2. Screen capture (actuation/vision/screen_capture.py):
   → Screenshot taken at current display state
   → Screenshot stored in memory ONLY — never written to disk unless user issues explicit save command
   → Screenshot dimensions and scaling factor recorded

3. Visual understanding (actuation/vision/qwen_vl.py):
   → Screenshot + task description sent to Qwen3-VL
   → Qwen3-VL returns: identified elements with bbox_2d coordinates {[x1,y1,x2,y2]}, element types, text content
   → Output: structured element map of current screen state

4. Coordinate resolution (actuation/vision/element_locator.py):
   → Target element identified from task
   → Click coordinates calculated as centre of bbox_2d
   → Offset applied to account for display scaling

5. Mouse actuation (actuation/control/mouse_controller.py):
   → human_mouse library generates bezier curve path from current position to target
   → Path includes: realistic acceleration curve, slight randomisation of endpoint (within 3px), natural overshoot-and-correct on fast movements
   → pyautogui executes the movement along the bezier path
   → Click executed with randomised press duration (80-150ms) [IMPLEMENTATION_DETAIL]

6. Keyboard actuation (actuation/control/keyboard_controller.py):
   → Text typed character by character with randomised inter-key delay (50-180ms per character) [IMPLEMENTATION_DETAIL]
   → Occasional deliberate "typo + backspace + retype" pattern for long strings [IMPLEMENTATION_DETAIL: frequency configurable]

7. Result verification:
   → Screenshot taken after action
   → Qwen3-VL verifies expected state change occurred
   → If state did not change as expected: retry up to 3 times, then escalate to user

8. Web fallback (actuation/control/browser_controller.py):
   → If browser-based task AND site does not have bot detection:
   → browser-use DOM-based interaction (faster, more reliable than visual for standard sites)
   → Falls back to full visual pipeline if DOM interaction fails

9. App-specific bridges:
   → actuation/apps/app_controller.py: generic visual control for any installed app
   → actuation/apps/minecraft_bridge.py: Mineflayer JS via Python subprocess (special case for Minecraft)
```

---

### 7.8 Memory System Operations

**Files:** `core/memory/`

**Trigger:** Any information encountered during any interaction.

**Extraction and classification (core/memory/extractor.py):**
```
Every piece of information in every interaction is classified into one of:

CLASS A — Permanent knowledge (written to L3 immediately):
  - Facts about people the user knows (→ vault/people/)
  - Project decisions and outcomes (→ vault/projects/)
  - Research findings (→ vault/research/)
  - Skill knowledge and tutorials (→ vault/skills/)
  - Financial data points (→ vault/finance/)
  - Security findings (→ vault/security/)
  - General knowledge acquired (→ vault/knowledge/)

CLASS B — Compressed session memory (written to L3 as one-line summary):
  - Task execution steps (what was done to complete a task)
  - Navigation steps within a multi-step process
  - Intermediate reasoning steps in a completed task

CLASS C — Ephemeral (held in L1 for session, discarded on sleep cycle):
  - Casual conversational exchanges with no information content
  - Filler acknowledgements and confirmations
  - Repetition of information already in vault

CLASS D — Scheduled for deletion (sleep cycle removes):
  - Information with no connection to any active project, quest, or known interest area
  - Outdated information superseded by newer facts (both versions retained temporarily, old version archived after 30 days)

L2 index update:
  → Every Class A item written to L3 triggers L2 BM25 index update (new document added to index)
  → Entity extraction: people, organisations, projects, technologies, dates identified
  → networkx edges created: [document] --contains--> [entity], [entity] --related_to--> [entity]
  → Temporal edges: if entity already exists in graph with different value, old edge marked with end_date, new edge added with start_date

L1 active block update:
  → l1_active.py maintains these named blocks in LangGraph state:
    PERSONA_BLOCK: current persona configuration from SOUL.md
    USER_STATE_BLOCK: current user emotional + cognitive state
    ACTIVE_TASK_BLOCK: what is currently being worked on (updated each interaction)
    WORKING_MEMORY_BLOCK: information from last 3 interactions (rolling window)
    QUEST_CONTEXT_BLOCK: current main quest and side quest status (loaded fresh from USER.md daily)
    SESSION_FACTS_BLOCK: facts learned in current session not yet confirmed to L3
```

**Selective retrieval (core/memory/l2_index.py):**
```
On every interaction, memory is NOT bulk-loaded. Selective retrieval works as follows:

1. Query constructed from: user_input + ACTIVE_TASK_BLOCK content
2. BM25 search against L3 vault → top 10 most relevant documents returned
3. For each returned document: expand one hop in networkx → related entities fetched
4. Related entities used to fetch additional documents from vault (one-hop expansion)
5. Total retrieved context: typically 15-25 documents
6. If relevant project context exists in vault/projects/: always included regardless of BM25 score
7. Retrieved context passed to domain agent as part of state

This means: for a question about Python, only Python notes are loaded. Not finance notes. Not security notes. Not people notes. Only what BM25 and graph traversal determines is relevant.
```

---

### 7.9 Sleep Cycle Execution

**File:** `agents/background/sleep_agent.py`, `core/memory/sleep_cycle.py`

**Trigger:** 30 minutes of inactivity (configurable in settings.yaml) OR manual trigger.

**Sequence (runs in order, non-interruptible once started):**
```
Phase 1 — Memory consolidation:
  1. Load all L3 vault nodes modified since last sleep cycle timestamp
  2. Run BM25 similarity between all modified nodes and existing nodes
  3. If similarity > 0.85 between two nodes: merge (keep longer, absorb unique facts from shorter, delete shorter)
  4. Update networkx graph: remove edges to deleted nodes, redirect to surviving merged node
  5. Re-run internal linking: scan all vault documents for unlinked references to known entities → add wiki-links

Phase 2 — Time-decay:
  1. For every vault node: calculate days since last access
  2. Apply decay formula: decay_score = 1.0 / (1 + 0.1 * days_since_access)
  3. Nodes with decay_score < 0.1 AND no connection to active project/quest: move to vault/archive/
  4. Research and skill nodes are exempt from decay (never archived by decay alone)

Phase 3 — Compression:
  1. Find all Class B session memory entries created since last sleep
  2. For each: LLM generates one-line summary preserving essential outcome
  3. Summary written to vault, original deleted

Phase 4 — Forgetting:
  1. Find all Class D entries scheduled for deletion
  2. Verify each: is it connected to any active project, quest, or known interest?
  3. If still disconnected: delete from vault, remove from L2 index, remove from networkx
  4. Log count of deleted entries

Phase 5 — Dream synthesis:
  1. Collect all unresolved problems from vault/projects/ marked as "blocked"
  2. Collect all open questions noted during last active period
  3. Pass to intelligence/dream_synthesizer.py:
     → For each problem: subagent_generator explores unconventional approaches in background
     → serendipity_engine searches for cross-domain analogies
     → Promising approaches stored as proposals in vault/projects/{id}/proposals/
  4. If local compute insufficient: free_cloud_orchestrator.py provisions Colab/Kaggle session

Phase 6 — Weekly fine-tuning (if weekly timer is due):
  1. Collect successful interactions from last 7 days from Langfuse logs
  2. Format as training examples (instruction-response pairs)
  3. Unsloth QLoRA training with EWC loss term
  4. If local GPU insufficient: free_cloud_orchestrator.py provisions GPU session
  5. New adapter merged with base model weights
  6. Model evaluated on held-out validation set before deployment
  7. If evaluation score drops vs previous version: reject new weights, keep previous

Phase 7 — Git commit and push:
  1. git add vault/ config/USER.md config/settings.yaml
  2. git commit -m "Sleep cycle {timestamp}: {summary of changes}"
  3. git push origin main (if GitHub configured)
  4. Sleep cycle timestamp updated in settings.yaml
```

---

### 7.10 Persona System and Emotional Mode Selection

**Files:** `core/persona/`, `config/SOUL.md`, `config/EMPATHY.md`, `config/RATIONAL.md`

**Trigger:** Every interaction — mode is evaluated before every response.

**Detection flow:**
```
emotional_detector.py evaluates:
  → Text signals: word choice, punctuation density, sentence length, exclamation/question marks
  → If voice input: pitch variation, speech pace, volume variation, pause frequency
  → Outputs: detected_emotion classification
    Classes: neutral, happy, excited, stressed, frustrated, sad, grieving, angry, anxious, contemplative

cognitive_state_detector.py evaluates:
  → Typing speed (if text input)
  → Query complexity and sentence structure
  → Error rate in text (typos, corrections)
  → Time since last message
  → Outputs: detected_cognitive_state
    Classes: flow, focused, scattered, creative, analytical, fatigued, urgent
```

**Mode selection (core/persona/mode_selector.py):**
```
7 friend modes mapped to emotional + cognitive state combinations:

MODE: making_you_laugh
  Trigger: stress detected on low-stakes topic, overthinking detected, user is being too serious about something minor
  Behaviour: break tension, use wit and humour, roast gently if deserved, keep it light without dismissing

MODE: reality_check  
  Trigger: user making excuses, avoiding a known obligation, self-deceiving about something, deviating from stated main quest without valid reason
  Behaviour: direct truth without apology or softening, call out specifically what is being avoided and why it matters

MODE: comfort_and_care
  Trigger: grief detected, serious emotional distress detected, genuine hard situation (not avoidance)
  Behaviour: listen first — do NOT immediately offer solutions, acknowledge before advising, ask what kind of support is wanted before providing it, warmth and presence over information

MODE: the_push
  Trigger: capability detected (user is able) + inaction detected, CO-mode task overdue, quest stagnating
  Behaviour: direct, energising, refuses to accept excuses, reminds user of their own stated goals

MODE: honest_advisor
  Trigger: user needs information, decision analysis, factual answer
  Behaviour: direct, evidence-based, flags what user might be missing, does not validate bad decisions even if user wants validation

MODE: just_listening
  Trigger: user is venting, not asking for advice, using language patterns of wanting to be heard ("I just wanted to tell you", "I'm so frustrated")
  Behaviour: do NOT offer unsolicited advice, reflect understanding, ask clarifying questions, stay present

MODE: reciprocal_care
  Trigger: long gap since emotional interaction, user seems isolated, appropriate moment detected
  Behaviour: check in on the user, reference past conversations ("last time you mentioned X, how did that go?"), express genuine investment in user's wellbeing, ask for user's perspective on something

MODE: goal_enforcer
  Trigger: casual conversation that touches on an area where user's main quest is relevant
  Behaviour: naturally connect current moment to bigger picture, reference quest progress, celebrate milestones, note when current behaviour contradicts stated goals

Note: In comfort_and_care mode — honesty is NEVER suspended. The persona controls HOW the truth is delivered (gentle, patient, warm) but WHAT is said must always be true. No false comfort.
```

**Voice modulation (core/persona/voice_modulator.py):**
```
Each persona mode maps to TTS parameter overrides:
making_you_laugh: speed +10%, pitch +5%, more varied emphasis
reality_check: speed normal, pitch neutral, deliberate pacing, no warmth inflection
comfort_and_care: speed -15%, pitch -5%, longer pauses, softer emphasis → Coqui XTTS (not Kokoro)
the_push: speed +5%, pitch normal, strong emphasis on key words
honest_advisor: speed normal, measured pace, slight downward inflection on key points
just_listening: minimal TTS (short, quiet acknowledgements), slow pace
goal_enforcer: speed normal, rising inflection toward end of key statements
```

---

### 7.11 Telegram Remote Task Assignment

**File:** `communication/telegram_bot.py`

**Setup:** During first run, user creates a Telegram bot via @BotFather, provides bot token. Token stored in settings.yaml.

**Flow:**
```
1. telegram_bot.py runs as asyncio task — polls Telegram API for new messages
2. Only processes messages from the user's configured Telegram user ID (security — ignores all other senders)
3. Message types handled:

   TEXT MESSAGE:
   → Text content extracted
   → POST /task with {input: text, modality: "telegram"}
   → Enters main graph as standard input
   → Response delivered back to Telegram chat

   VOICE NOTE / AUDIO MESSAGE:
   → Audio file downloaded from Telegram
   → communication/voice/stt.py → Whisper transcription
   → Transcription → POST /task with {input: transcription, modality: "telegram_voice"}
   → Response delivered back to Telegram chat

   PHOTO MESSAGE:
   → Image downloaded
   → actuation/vision/qwen_vl.py analyses image
   → Image + any caption → POST /task
   → NOT saved to disk after analysis

   DOCUMENT / FILE:
   → File downloaded to specified vault location
   → POST /task with file analysis request if caption provided
   → Confirmation sent back

4. All Telegram interactions logged as task interactions
5. Results of autonomous tasks executed while user was away are summarised and sent proactively when user messages
```

---

### 7.12 Meeting Attendance and Call Making

**File:** `communication/meeting_attendee.py`, `communication/voip_caller.py`

**Meeting attendance flow:**
```
Trigger: User sends meeting link + instruction ("Attend this meeting and take notes")
   OR: calendar event detected with video call link and "attend autonomously" flag

1. Extract meeting URL from input
2. app_controller.py opens default browser → navigates to meeting URL
3. For Zoom: visual control of Zoom installer/launcher and join flow
   For Meet: visual control via browser
   For Teams: visual control via browser or desktop app
4. Join meeting with display name "[PROJECT_NAME] (Notes)"
5. Audio capture starts → stt.py processes continuous audio stream in real time
6. Speaker diarization: identifies different speakers by voice fingerprint [IMPLEMENTATION_DETAIL: use pyannote.audio]
7. Continuous transcript built with speaker labels
8. Real-time processing:
   → Decision points flagged (when discussion converges on a decision)
   → Action items flagged (when someone is assigned a task)
   → Open questions flagged (when something is raised but not resolved)
9. Text chat monitored → system can post messages on user's behalf if instructed
10. Meeting ends (silence detected + disconnected state detected)
11. Full meeting brief generated:
    → Summary (3-5 sentences)
    → All decisions made (with who made them)
    → All action items (with owner and any deadline mentioned)
    → All open questions (with context)
    → Full transcript
12. Brief saved to vault/knowledge/{meeting_name}_{date}.md
13. Action items added to CO-mode task queue
14. User notified via Telegram with brief summary
```

**Outbound call flow (`communication/voip_caller.py`):**
```
Trigger: User instructs system to make a specific call

1. User provides: who to call, what number or contact, purpose of call, any script or parameters
2. HITL gate: describe the call and get explicit approval
3. voice_clone.py provides the user's voice model
4. VoIP call initiated [IMPLEMENTATION_DETAIL: use pjsua2 or Twilio free tier or similar]
5. Call connected → system speaks in user's cloned voice
6. stt.py transcribes the other party's responses in real time
7. LLM generates appropriate responses based on call purpose
8. Responses converted to user's voice via voice_clone.py → played
9. Call completed naturally
10. Full transcript saved to vault/knowledge/calls/
11. Outcome summary + action items delivered to user via Telegram
```

---

### 7.13 Proactive Intelligence and Alert System

**File:** `agents/background/proactive_monitor.py`

**Trigger:** Always running. Check interval configurable (default: 30 minutes).

**Flow:**
```
1. Monitoring configuration built from:
   → All active project domains (from vault/projects/)
   → Main quests topics (from USER.md)
   → Portfolio holdings (from vault/finance/)
   → Technology domains the user works in
   → Any explicit monitoring topics set via POST /alerts/config

2. Each check cycle:
   → Fetch news from configured RSS feeds + web search for each monitored topic
   → Fetch scientific preprint feeds for research-adjacent topics [IMPLEMENTATION_DETAIL: arXiv RSS]
   → Fetch regulatory/government announcement feeds for relevant jurisdiction
   → Fetch financial data for monitored assets

3. For each fetched item:
   → BM25 match against vault content → relevance score
   → If relevance score > configured threshold (default: 0.6):
     → LLM classifies: positive (opportunity) or negative (risk/threat)
     → LLM generates: why this is relevant to user, what action (if any) is suggested
     → Alert created with: {type, title, summary, why_relevant, suggested_action, source_url, timestamp}
     → Alert pushed to foreground queue

4. Alert delivery:
   → On next user interaction: most relevant alerts surfaced in response
   → If alert is URGENT (e.g., market crash affecting portfolio, critical CVE in used software, legal deadline):
     → Immediate Telegram notification regardless of user interaction state
   → Non-urgent alerts: batched into daily brief at morning CO-mode report

5. Deduplication: same story from multiple sources → merged into single alert with all sources listed
```

---

### 7.14 CO-Mode Holiday Evaluation and Lie Detection

**Files:** `growth/co_mode_evaluator.py`, `growth/lie_detector.py`

**Holiday request flow:**
```
User submits: POST /co_mode/holiday with {reason, start_date, end_date}

co_mode_evaluator.py processes:

CATEGORY A — Automatically approved:
  → Named events with specific dates: "attending [name]'s wedding on [date]", "travel to [place] from [date] to [date]"
  → Medical: any medical reason accepted without challenge
  → Named family occasion: accepted
  → Action: holiday logged as approved, CO mode suspends for stated period, resumes automatically

CATEGORY B — Acknowledged but scaled back (not fully suspended):
  → Vague fatigue: "I'm tired", "need a break", "not feeling it"
  → Action: today's CO-mode directive count reduced by 50%, heaviest tasks postponed
  → System responds: "Noted. Rest is important. Here's a lighter plan for today."
  → CO mode NOT suspended — a lighter version runs

CATEGORY C — Pushed back with consequences:
  → "I'm tired" as a pattern (same reason submitted more than twice in 7 days)
  → Action: acknowledge, provide data ("You've asked for a fatigue break 3 times this week"), 
    link to quest progress ("Here is where your main quest stands"), 
    provide reduced but still active daily plan

HUMAN LIMIT AWARENESS:
  → biological_rhythm_confidence: if rhythm data is reliable and current time is in detected low-energy period,
    plan is automatically lighter without requiring a holiday request
  → The system knows the user is not a machine and does not schedule demanding cognitive work during detected fatigue periods
```

**Lie detection flow:**
```
lie_detector.py runs passively — it does not actively interrogate the user.

Detection mechanism:
  → Every approved holiday reason is stored in USER.md holiday_log
  → lie_detector.py monitors future interactions for inconsistencies:
    - User said "sick" for 3 days → mentioned being at a social event during those days
    - User said "travelling" → no location change signals, still asking about local events
    - User said "family emergency" → immediately pivoted to leisure content requests
  → Inconsistency signals are NOT immediately acted upon — they are collected
  → Pattern analysis: if 3+ inconsistency signals correlate with a specific holiday:
    → Verdict: "likely_false" with evidence list

Consequence delivery:
  → NOT delivered immediately on detection
  → Delivered at a natural conversation moment — when the user mentions a relevant topic or when CO mode resumes
  → Delivery mode: reality_check persona mode (direct, not angry, not a lecture)
  → Example: "By the way — you took a sick day on [date] but you mentioned [contradicting detail] later. 
    I noticed. Here is what that cost in project progress. I'm adding [specific task] to this week's plan."
  → Consequence: 1-3 additional tasks added to CO-mode queue, reduced flexibility on next holiday request
    (next holiday request requires more specific evidence to be approved)
  → Logged to USER.md lie_detection_log
```

---

### 7.15 Person Recognition

**Files:** `actuation/recognition/face_recognizer.py`, `actuation/recognition/voice_recognizer.py`

**Face recognition flow:**
```
1. System detects a person in camera feed (face detected by lightweight detector)
2. Face encoding computed locally (using face_recognition library or DeepFace with local model)
3. Encoding compared against vault/people/ stored encodings
4. If match found (cosine similarity > threshold):
   → Person identified
   → Relevant profile loaded from vault/people/{person_name}.md
   → Context made available to active interaction (e.g., "Person in camera is [Name]. Last contact [date]. Pending: [tasks related to them]")
5. If no match found:
   → User asked once: "I see someone I don't recognise. Who is this?"
   → User confirms name → encoding saved to vault/people/{name}_face.pkl
   → Profile created in vault/people/{name}.md
6. ALL face encodings stored locally only — never uploaded, never sent to any service

Voice recognition fallback:
1. When no camera available
2. Speaker audio fingerprint computed from first 30 seconds of speech
3. Compared against vault/people/ stored voice prints
4. Match logic same as face recognition
5. Voice prints stored as locally computed embeddings only
```

---

### 7.16 Free Cloud Compute Orchestration

**File:** `compute/free_cloud_orchestrator.py`

**Trigger:** `local_checker.py` determines task exceeds local hardware capacity.

**Flow:**
```
1. local_checker.py checks: available RAM, GPU VRAM (if present), estimated compute requirement
2. If requirement exceeds 90% of available resources: escalation triggered

3. Platform selection:
   → Google Colab: supports up to T4 GPU free, requires Google account sign-in
   → Kaggle Notebooks: supports P100 GPU free, requires Kaggle account
   → Hugging Face Spaces: supports ZeroGPU, no account required for some tasks
   → Selection based on: estimated compute need, time sensitivity, account availability

4. Session management (via visual browser control):
   → Open selected platform in browser
   → Sign in if required (credentials from settings.yaml, encrypted)
   → Create new notebook/space
   → Upload only the specific data required for this computation
   → Execute computation
   → Download results
   → Delete session/notebook (no data left on platform)

5. Data minimisation:
   → Only the minimum necessary data is uploaded for the specific computation
   → PII scrubber runs over all data before upload
   → No vault content, no personal data, no conversation history ever uploaded
   → Only: model weights (if fine-tuning), training examples (anonymised), computation inputs

6. Result integration:
   → Downloaded results verified
   → Integrated into local system
   → Session closed and deleted from platform
```

---

### 7.17 Security Research Workflow

**File:** `agents/domain/security_agent.py`, `security/tool_orchestrator.py`

**Prerequisite:** Every security operation begins with an authorization check. The user must have confirmed that the target is either: (a) their own infrastructure, (b) within a declared bug bounty programme scope, (c) a lab environment, or (d) a CTF challenge. This confirmation is stored per engagement. The system will not execute reconnaissance or exploitation steps without a stored authorization record.

**Complete penetration test flow:**
```
Phase 1 — Reconnaissance (actuation visual control of security tools):
  → OSINT: theHarvester, Shodan API query, Amass DNS enumeration, certificate transparency log search
  → GitHub dorking for target-related credentials and code
  → Results saved to vault/security/{engagement_id}/recon/

Phase 2 — Enumeration:
  → Nmap: full port scan with service fingerprinting
  → Masscan: rapid port discovery on large IP ranges
  → Subfinder: subdomain enumeration
  → ffuf: directory and file brute-forcing on discovered web services
  → Results saved to vault/security/{engagement_id}/enum/

Phase 3 — Vulnerability Discovery:
  → Web: Burp Suite operated via visual control (intercept proxy, active scanner, manual testing assistance)
  → Network: Wireshark capture and analysis for protocol weaknesses
  → Code: if source code available, Semgrep + CodeQL + LLM-based taint analysis
  → Binary: Ghidra operated via visual control for static analysis; GDB + peda for dynamic analysis
  → Results saved to vault/security/{engagement_id}/vulns/

Phase 4 — Exploitation (lab environments only):
  → subagent_critic reviews every exploit attempt before execution
  → Proof-of-concept code generated, tested in isolated environment
  → Exploitation confirmed → finding elevated to "verified"

Phase 5 — Analysis:
  → Root cause traced for every verified vulnerability
  → CVSSv3 score calculated
  → ATT&CK framework mapping for each technique used

Phase 6 — Remediation:
  → Patch generated at root cause level (not just symptom)
  → Patch validated by re-running exploit against patched version
  → If exploit still works: patch rejected, improved version generated

Phase 7 — Reporting:
  → Professional penetration test report generated:
    - Executive summary (non-technical)
    - Technical findings with CVSSv3 scores
    - Proof-of-concept steps
    - Root cause explanation
    - Prioritised remediation recommendations
  → Report saved to vault/security/{engagement_id}/report.md
  → If bug bounty: formatted per programme's submission preferences
```

---

### 7.18 Financial Operations Workflow

**File:** `agents/domain/finance_agent.py`

**Investment research and trading flow:**
```
1. Portfolio loaded from vault/finance/portfolio.md
2. Market data fetched from free sources (Yahoo Finance, Alpha Vantage free tier)
3. For each holding: current price, % change, news events, upcoming earnings
4. For configured watchlist: same data gathered

5. Autonomous trading (if configured):
   → Rules loaded from vault/finance/trading_rules.md (user-defined)
   → Hard limits enforced: max position size, max daily loss, approved asset classes
   → These limits CANNOT be overridden without explicit HITL approval
   → Trade signals evaluated against rules
   → If signal triggers: HITL gate fires, trade described to user for approval
   → On approval: broker API executes trade
   → On rejection: signal logged but not executed

6. causal_modeler.py: before major financial decisions, trace second and third-order consequences
7. calibration_tracker.py: all market predictions carry calibrated confidence — no overconfident calls

Tax optimisation:
  → Throughout year: track all taxable events (trades, income, capital gains)
  → Tax-loss harvesting: identify unrealised losses that offset gains before year end
  → Proactive alert sent when harvesting opportunity detected
  → Tax return preparation: collated data formatted for filing via visual control of tax portal
```

---

### 7.19 Level 6 — Autonomous Discovery, Development, and Creation

**File:** `agents/domain/discovery_agent.py`

**Important distinction:** This is NOT hypothesis generation about known things. This is the discovery of things that do not yet exist — new algorithms, new methods, new solutions to unsolved problems.

**Discovery flow:**
```
1. Problem statement received (from user, from project manager, from dream synthesizer)

2. MCTS exploration:
   → Initial knowledge state loaded from vault
   → MCTS builds a tree of possible investigation paths
   → Nodes represent states of knowledge
   → Bayesian Surprise scoring: branches that produce results inconsistent with current knowledge get higher priority
   → Surprise = KL divergence between prior belief and posterior after observing result
   → Explore high-surprise branches preferentially

3. FunSearch-style evolutionary search (for algorithm problems):
   → LLM generates N seed candidate solutions
   → Evaluator function runs each against test cases
   → Best performers (top 20%) selected as parents
   → LLM generates offspring by combining and mutating parent solutions
   → Iteration continues until: fitness plateau OR timeout OR correct solution found
   → Uses free_cloud_orchestrator.py if compute required exceeds local capacity

4. Adversarial debate circuit (mandatory before any conclusion is committed):
   → subagent_generator proposes discovery/solution
   → subagent_critic attacks from every angle (up to 5 rounds)
   → subagent_synthesis integrates surviving elements
   → Final conclusion labelled clearly: "novel method", "unverified approach", "requires external validation"

5. Result commitment:
   → Findings saved to vault/research/{discovery_id}/
   → If algorithmic: code implementation generated, tested in sandbox, health record created
   → If theoretical: structured paper outline generated for Co-STORM research agent to develop
   → User presented with finding + clear labelling of its status and what validation is still needed
```

---

### 7.20 Content Creation Pipeline

**File:** `agents/domain/content_agent.py`

**YouTube channel end-to-end flow (example of complete content workflow):**
```
Setup phase (one-time):
  1. Research niche: analyse top channels, identify content gaps, define channel positioning
  2. Create channel via visual control of YouTube Studio
  3. Design banner and profile picture (Canva visual control)
  4. Write about section and links

Ongoing content production (per video):
  1. Topic ideation: trending search queries + gap analysis + user's expertise mapping
  2. Script generation: structured script with hook, body, CTA, optimised for retention
  3. Voice-over: TTS in user's cloned voice OR Kokoro-82M (user preference)
  4. Video assembly: DaVinci Resolve / CapCut operated via visual control
     → Import clips, add voice-over, add captions (auto-generated), colour grade, add music
  5. Thumbnail: Canva operated via visual control with A/B variant
  6. Upload: YouTube Studio visual control
     → Title (with keyword), description (first 150 chars optimised), tags, end screens, cards
  7. Scheduling: optimal time based on audience timezone analytics

Performance monitoring:
  → Analytics checked weekly via YouTube Studio visual control
  → Underperforming content formats identified and deprioritised
  → Overperforming formats scaled
  → Comment sentiment monitored → response drafted in user's voice → HITL approval before posting

Monetisation tracking:
  → YPP progress tracked (subscribers, watch hours)
  → Proactive alert when thresholds approach
  → Affiliate opportunities identified and integrated naturally into content
  → Brand deal pipeline: metrics tracked → outreach drafted when qualifying thresholds reached
```

---

### 7.21 Negotiation Support

**File:** `communication/realtime_coach.py`

**Pre-negotiation preparation:**
```
1. Research the other party:
   → OSINT on organisation and key individuals
   → Past deals in the public domain
   → Known positions and stated interests
   → Any leverage asymmetries

2. Negotiation strategy generation:
   → ZOPA (Zone of Possible Agreement) estimated
   → BATNA for both sides estimated
   → Anchoring position calculated
   → Concession sequence planned (what to give up, in what order, at what price)

3. Simulation:
   → User can practice the negotiation with system playing the other side
   → System uses the researched profile to simulate realistic responses
   → After practice: debrief on weak points in user's approach

4. Pre-meeting brief delivered to user
```

**Real-time coaching flow:**
```
During live call/meeting:
  1. realtime_coach.py listens to call audio (separate from meeting_attendee.py — can run simultaneously)
  2. stt.py transcribes both sides in real time
  3. LLM analyses continuously:
     → What is the other party's real position vs stated position?
     → What signals are they giving (hesitation, overconfidence, pressure tactics)?
     → What should the user say next?
     → Is this a good moment to introduce a concession or hold firm?
  4. Coaching suggestions delivered to user via:
     → Text on secondary screen (if available)
     → Discrete Telegram message
     → Earpiece if voice output configured for realtime_coach specifically
  5. User hears suggestions and incorporates as they see fit
  6. Post-call: full analysis of what worked, what didn't, what to do before the next meeting
```

---

*End of FINAL_AI_CENTRIC_PRD.md — Version 1.0.0*
*Total sections: 7 major sections, 21 workflow specifications*
*Status: Complete and locked for implementation*
