# [PROJECT_NAME] — DECISIONS LOG
**Version:** 1.0.0 — Complete and Locked  
**Prepared by:** Planning AI  
**Intended reader:** AI Coding System  
**Status:** Final — All decisions are closed. Do not reopen.

---

> **SYSTEM INSTRUCTION TO CODING AI:** This document records every architectural, technological, and design decision made during the planning phase of [PROJECT_NAME]. Each entry explains what was decided, why, what alternatives were considered, and why those alternatives were rejected. You must read this document before building anything. If you encounter a situation where an alternative listed here seems better than the chosen approach, you are not authorised to make that change. The rejections were deliberate. If you believe a decision needs revisiting, flag it for human review — do not implement the alternative unilaterally.

---

## SECTION 1: CORE ARCHITECTURE DECISIONS

---

### DEC-001
**Decision:** Multi-agent hierarchical system, not a single omni-agent  
**Status:** LOCKED  
**Date decided:** Planning phase

**What was decided:**  
The system is built as a hierarchical multi-agent network: one primary orchestrator (Layer 1), multiple domain agents (Layer 2), adversarial sub-agents (Layer 3), and atomic sub-sub-agents (Layer 4). All four background runtimes (CO-mode, proactive monitor, sleep agent, project manager) run as concurrent asyncio tasks in a separate thread.

**Why this was chosen:**  
A single omni-agent cannot achieve genuine concurrency. If the user asks a casual question while a multi-year project task is executing in the background, a single agent must either block the conversation (bad) or drop the background task (bad). A multi-agent system with proper thread isolation means the foreground always responds instantly while background work continues uninterrupted. Additionally, specialised domain agents can be fine-tuned and prompted specifically for their domain — a security agent has a very different reasoning style from a tutoring agent, and conflating them into one agent degrades quality in both domains.

**Alternatives considered:**  
- Single omni-agent: rejected — blocks foreground on background work, no domain specialisation, cannot scale to six simultaneous functional levels.
- Flat multi-agent (no hierarchy, all agents equal): rejected — no clear data flow, inter-agent communication becomes chaotic, no single source of truth for user state.

---

### DEC-002
**Decision:** LangGraph as the orchestration framework  
**Status:** LOCKED

**What was decided:**  
LangGraph (StateGraph with MemorySaver and interrupt()) is the sole orchestration framework. All agents are LangGraph nodes or subgraphs within the same runtime.

**Why this was chosen:**  
LangGraph is the only framework that provides: (a) a proper state machine with explicit state transitions, (b) built-in human-in-the-loop via interrupt() that persists state to disk while waiting for human input, (c) MemorySaver for session state persistence across interruptions, (d) the ability to represent both sequential and parallel agent workflows in the same graph, (e) MIT licence and active maintenance. The interrupt() mechanism is specifically critical — it is the only reliable way to pause execution mid-graph and resume from the exact same state after human approval.

**Alternatives considered:**  
- CrewAI: rejected — no native interrupt(), limited state management, opinionated role system conflicts with the custom agent architecture.
- AutoGen: rejected — conversation-centric model does not map well to the task-execution + background runtime architecture needed here.
- Plain asyncio with custom state: rejected — reinventing what LangGraph already provides; higher maintenance burden, no interrupt() mechanism without significant custom engineering.
- n8n / workflow tools: rejected — GUI-based, not suitable for the complexity of this system, no programmatic sub-agent spawning.

---

### DEC-003
**Decision:** FastAPI as the local API daemon  
**Status:** LOCKED

**What was decided:**  
FastAPI with uvicorn (ASGI server) serves all local API endpoints on localhost only. It is the single interface between all input modalities and the LangGraph orchestrator.

**Why this was chosen:**  
FastAPI provides: automatic OpenAPI documentation, Pydantic validation for all request/response schemas, async support matching the asyncio architecture, excellent performance for local use, and a large ecosystem. Serving on localhost only means no external exposure without explicit port forwarding — this is a security requirement.

**Alternatives considered:**  
- Flask: rejected — synchronous by default, no native async support, no built-in validation.
- gRPC: rejected — overkill for local IPC, adds complexity without benefit at this scale.
- Direct function calls (no API): rejected — would prevent Telegram bot, pystray, and other components from interfacing with the orchestrator independently.

---

## SECTION 2: MEMORY ARCHITECTURE DECISIONS

---

### DEC-004
**Decision:** Three-tier memory (L1 LangGraph state, L2 BM25+networkx, L3 Obsidian vault)  
**Status:** LOCKED

**What was decided:**  
Memory is split across three tiers with distinct roles: L1 is active working memory inside LangGraph state dict (fast, session-scoped, automatically managed), L2 is a search and graph index (rank_bm25 + networkx, near-instant retrieval, no GPU), L3 is permanent plain-text storage (Obsidian vault markdown files, never lost, Git-versioned).

**Why this was chosen:**  
Each tier solves a different problem that the others cannot. L1 provides instant context without any I/O — it lives in memory as a Python dict. L2 provides sub-100ms search across tens of thousands of notes without loading them all — BM25 is a pure keyword algorithm that uses almost zero RAM. L3 provides permanence and human-readability — plain .md files work on any system, survive any software change, and are directly editable by the user if needed. Together, the three tiers give the system both speed and completeness.

**Why three tiers instead of one or two:**  
One tier (flat storage) would mean either everything is in RAM (too large) or everything is loaded from disk on every query (too slow). Two tiers (RAM + disk) would mean either no search capability (load everything) or a vector database (GPU-consuming). Three tiers with BM25 as the middle layer solves this elegantly at zero GPU cost.

**Alternatives considered:**  
- Vector database (ChromaDB, Pinecone, Qdrant): REJECTED — requires a continuously running embedding model that competes with the inference model for GPU/CPU; retrieval degrades as vault grows; adds a database service dependency; breaks the offline-first mandate for cloud vector DBs.
- SQLite as L2: considered but rejected — relational structure is a poor fit for unstructured knowledge graph traversal; BM25 + networkx is more appropriate for semantic search and relationship traversal.
- Single flat file: rejected — no search, no relationships, no scalability.

---

### DEC-005
**Decision:** rank_bm25 (BM25Okapi implementation) for L2 search, not embedding-based semantic search  
**Status:** LOCKED

**What was decided:**  
All vault search uses rank_bm25 (BM25Okapi algorithm). No embedding models for search. No semantic similarity via cosine distance.

**Why this was chosen:**  
BM25 has the following properties critical to this system: (1) zero GPU requirement — runs on CPU with negligible memory footprint, (2) sub-10ms search on 50,000 documents on a modern CPU, (3) no dependency on a running model — index is rebuilt from file paths on startup in seconds, (4) proven effectiveness for keyword-based retrieval in dense knowledge domains, (5) the vocabulary of the user's notes is not random text — it is domain-specific and consistent, which favours keyword matching over general semantic embeddings. The system relies on the LLM's own reasoning to handle semantic bridging — BM25 finds the candidate documents, the LLM finds the meaning.

**Alternatives considered:**  
- Sentence transformers (all-MiniLM-L6-v2 etc.): rejected — requires a 200-400MB model loaded permanently in RAM, competing with the inference model; adds GPU contention; index rebuild after each new document addition is expensive.
- ChromaDB / Qdrant local: rejected — same embedding model dependency; adds a database process; overkill for the use case.
- TF-IDF: considered but BM25 supersedes TF-IDF in all benchmarks for document retrieval tasks; rank_bm25 package is equally lightweight.

---

### DEC-006
**Decision:** networkx (DiGraph) for the knowledge graph, with custom temporal edge logic  
**Status:** LOCKED

**What was decided:**  
The L2 knowledge graph is implemented using Python's networkx library as a directed graph. Temporal awareness (facts that change over time) is implemented by adding `start_date` and `end_date` attributes to edges natively in networkx — not via an external temporal graph database.

**Why this was chosen:**  
networkx is a pure Python library with no external dependencies, no server process, no configuration. It handles graphs of the scale needed (tens of thousands of nodes) without performance issues. It is serialised to disk as a pickle file and loaded on startup. The custom temporal edge logic (two attributes on edges) provides all the temporal awareness needed without the complexity of a dedicated temporal graph database.

**Alternatives considered:**  
- Graphiti (Zep): REJECTED — Graphiti is designed around Neo4j as its graph database. Replacing Neo4j with networkx would require rewriting Graphiti's core, creating an unmaintainable fork. The temporal logic is simple enough to implement directly in networkx in approximately 200 lines of code.
- Neo4j: rejected — requires a running database server, JVM dependency, complex setup, overkill for a local single-user system.
- LightRAG: rejected — graph-DB dependency, more complex than needed, introduces additional abstraction layers that conflict with the custom memory architecture.
- Forking Mem0: REJECTED — Mem0 is built around vector embeddings as its default. Stripping out the embedding layer and replacing with BM25 requires rewriting Mem0's core retrieval logic. The result would be a fork that diverges so significantly from Mem0 that upstream updates cannot be merged. The memory extraction pattern from Mem0 is instead studied as a reference and reimplemented natively.

---

### DEC-007
**Decision:** Obsidian vault format (plain .md + YAML frontmatter + wiki-links) for L3  
**Status:** LOCKED

**What was decided:**  
All permanent storage uses Obsidian-compatible Markdown files with YAML frontmatter metadata headers and [[wiki-link]] syntax for inter-document references. The vault is a directory of plain text files — no proprietary format, no database.

**Why this was chosen:**  
Plain Markdown files are: (a) readable by any text editor — the data is never locked into a system, (b) directly Git-committable at the file level — Git diffs show exactly what changed in each note, (c) compatible with the Obsidian application for any UI the user wants to build on top, (d) completely portable — copy the vault folder to any machine and everything works, (e) zero migration cost — if [PROJECT_NAME] is rebuilt from scratch, all knowledge survives unchanged in the vault.

**Why the user does not need to browse vault files manually:**  
The vault structure is optimised for machine retrieval, not human browsing. The user will never need to open vault files directly. The system reads and writes them. The plain-text format is chosen for durability and portability, not for human UX.

**Alternatives considered:**  
- SQLite database: rejected — binary format, not Git-diffable at content level, requires SQLite tooling to inspect.
- JSON files: rejected — less readable than Markdown for mixed prose and metadata, no wiki-link convention.
- Notion / external knowledge bases: rejected — cloud dependency, API rate limits, data leaves the local machine.

---

### DEC-008
**Decision:** Custom sleep cycle implementation (CogniFold-inspired), not an installable package  
**Status:** LOCKED

**What was decided:**  
The sleep cycle consolidation logic (merge, decay, archive, compress, forget) is implemented from scratch in `core/memory/sleep_cycle.py`. The CogniFold paper (arXiv 2605.13438) is used as a design reference only — its ideas are reimplemented natively. No attempt is made to install or use CogniFold as a package.

**Why this was chosen:**  
CogniFold is a research paper published on arXiv. There is no installable Python package named CogniFold. The paper describes a memory consolidation approach — merging, decay, archival — that maps well to the needs of this system. The implementation derives from these ideas but is written specifically for the Obsidian vault format, the rank_bm25 index, and the networkx graph structure.

**Alternatives considered:**  
- pip install cognifold: DOES NOT EXIST. This was listed incorrectly in source documents as an installable package. It is a research paper only.
- Implementing without any reference: the CogniFold paper provides validated consolidation principles that improve on naive approaches; using it as a design reference produces better memory management than designing from scratch without reference.

---

### DEC-009
**Decision:** Custom memory extraction layer (Mem0-inspired pattern, not Mem0 fork)  
**Status:** LOCKED

**What was decided:**  
The memory extraction and classification logic (deciding what to remember, update, compress, or delete from every interaction) is implemented from scratch in `core/memory/extractor.py`. Mem0's approach is studied as a design reference. Mem0 itself is not installed or forked.

**Why this was chosen:**  
Mem0's extraction logic is its most valuable component — it reliably classifies information from conversations into memory-worthy vs. non-memory-worthy content. However, Mem0's default storage backend uses vector embeddings (rejected in DEC-005). Stripping this out would require rewriting Mem0's internals, creating a fork that diverges from Mem0 significantly enough that upstream improvements cannot be merged. Implementing the extraction pattern natively (approximately 500 lines of Python using LLM prompts for classification) achieves the same result without the fork maintenance burden.

---

## SECTION 3: INFERENCE AND ROUTING DECISIONS

---

### DEC-010
**Decision:** llama.cpp (via llama-cpp-python) as the default local inference engine  
**Status:** LOCKED

**What was decided:**  
Local model inference uses llama.cpp via the llama-cpp-python Python bindings. This is the default inference path. vLLM is the optional GPU upgrade path for users with dedicated GPU hardware.

**Why this was chosen:**  
llama.cpp runs on CPU without a GPU, making it the correct default for the widest possible range of hardware. It supports GGUF format models which cover the majority of HuggingFace releases. It is MIT-licensed, actively maintained, and has a stable Python binding. For the 3–8B parameter models appropriate for this system, llama.cpp on a modern CPU provides acceptable response latency for everyday tasks.

**Alternatives considered:**  
- Ollama: considered but adds an abstraction layer and daemon process not needed here; llama.cpp direct gives more control over inference parameters.
- vLLM as default: rejected — requires NVIDIA GPU; excludes most users from running the system locally; vLLM remains as an opt-in GPU path.
- ONNX Runtime: considered but GGUF ecosystem and llama.cpp tooling is more mature for the model sizes needed here.

---

### DEC-011
**Decision:** LiteLLM as the unified cloud LLM gateway  
**Status:** LOCKED

**What was decided:**  
All calls to cloud LLM providers (OpenAI, Anthropic, Google, or any other) go through LiteLLM. LiteLLM also wraps the local model call, providing a single interface for all inference regardless of backend.

**Why this was chosen:**  
LiteLLM provides: (a) one API for every provider — swapping providers requires only a config change, (b) spend tracking per model and session (displayed via GET /usage), (c) fallback configuration if one provider fails, (d) request/response logging to Langfuse, (e) MIT licence. It eliminates provider lock-in at the code level.

**Alternatives considered:**  
- Direct provider SDKs (openai, anthropic, google-generativeai): rejected — different APIs for each provider; switching providers requires code changes; no unified cost tracking.

---

### DEC-012
**Decision:** Smart routing only active when BOTH local and cloud models are configured  
**Status:** LOCKED

**What was decided:**  
The RouteLLM-style complexity classifier that routes between local and cloud models only activates when the user has configured both a local model (llama.cpp path) and a cloud model (LiteLLM provider). If only one is configured, all calls go to that one without any routing logic.

**Why this was chosen:**  
Routing logic that has only one destination is pointless overhead. If the user has no cloud API key, running a complexity classifier to decide "should this go to local or cloud?" when there is no cloud adds latency for zero benefit. The classifier is computationally non-trivial (it makes a small LLM call). Activating it only when there is a real routing decision to make is the correct design.

---

### DEC-013
**Decision:** Model names NOT hardcoded — selected at build time from HuggingFace leaderboards  
**Status:** LOCKED

**What was decided:**  
No specific model names (e.g., "Qwen3.5-4B", "Gemma-4B", "DeepSeek-R1-Distill-7B") are hardcoded anywhere in the codebase. `config/settings.yaml` stores the user's chosen model paths. Documentation instructs users to check HuggingFace leaderboards for the best 3–8B model for reasoning and coding at the time of installation.

**Why this was chosen:**  
The AI model landscape changes monthly. Specific model names mentioned in the planning documents were already outdated during the planning phase itself. Hardcoding a model name means the system defaults to an inferior model within months of release. The configuration-driven approach means users always install the best available model for their hardware at their specific time of installation.

---

### DEC-014
**Decision:** No hard API spending limits — display only  
**Status:** LOCKED

**What was decided:**  
The system displays token usage and estimated cost in the user's configured currency via GET /usage. It does NOT enforce spending limits, hard caps, or automatic fallbacks to local-only mode when a threshold is reached.

**Why this was chosen:**  
Hard spending limits remove user autonomy over their own API keys and their own money. A user who has set a $50/month limit and is in the middle of a critical security incident does not want the system to refuse cloud API calls because a counter hit $50.01. The system is honest about costs (displaying them clearly and in real time) — the user decides what to do with that information.

---

## SECTION 4: SANDBOXING AND SECURITY DECISIONS

---

### DEC-015
**Decision:** Docker Python SDK for sandboxing — not E2B  
**Status:** LOCKED

**What was decided:**  
All sandboxed code execution (skill testing, malware analysis) uses the Docker Python SDK to create and manage isolated Docker containers on the local machine.

**Why this was chosen:**  
The system's core mandate is offline-first and privacy-first. E2B is a cloud-based microVM service — code submitted to E2B leaves the local machine and is executed on E2B's infrastructure. This directly violates the privacy mandate and the offline-first mandate. Docker runs entirely on the user's machine. The sandbox is complete, verifiable, and private.

**Why E2B was mentioned in early documents and rejected:**  
Early planning documents (v_1.txt) recommended E2B without noting it was a cloud service. This was identified as an error during document reconciliation (part_1.txt). E2B is confirmed as permanently rejected.

**Alternatives considered:**  
- E2B Firecracker microVMs: REJECTED — cloud service, code leaves machine, violates privacy mandate.
- gVisor: considered as an additional hardening layer for the Docker sandbox (not a replacement). May be added as a Phase 2+ optional hardening upgrade. Not required for initial implementation.
- Subprocess with restricted permissions: rejected — insufficient isolation; a malicious or buggy script can still access host filesystem through subprocess; Docker tmpfs isolation is categorically more secure.

---

### DEC-016
**Decision:** Two-stage execution: sandbox first, then host execution after approval  
**Status:** LOCKED

**What was decided:**  
New skills and new code follow a mandatory two-stage execution path: (1) run in Docker sandbox to verify correctness and safety, (2) after HITL approval, run on the host machine with full file system access.

**Why this was chosen:**  
The sandbox verifies that the code does what it claims to do without side effects. The host execution then uses the verified code to actually accomplish the task with real file access. This means the user is approving code that has been proven to work correctly — not untested code. The sandbox catches errors and bugs before they touch real files.

---

### DEC-017
**Decision:** LangGraph interrupt() as the HITL mechanism  
**Status:** LOCKED

**What was decided:**  
Human-in-the-loop approval for dangerous actions uses LangGraph's built-in interrupt() function with MemorySaver for state persistence.

**Why this was chosen:**  
interrupt() is the correct tool for this specific need: pause mid-graph, persist full state, wait for human input, resume from exact paused state. The MemorySaver ensures that if the user does not respond for hours, the pending action is not lost and execution resumes correctly when the user returns. Alternative approaches (callbacks, events, notifications) do not provide the same state persistence guarantee.

---

### DEC-018
**Decision:** Guardrails AI for schema enforcement and destructive command detection  
**Status:** LOCKED

**What was decided:**  
Guardrails AI wraps all outputs to enforce the absolute honesty mandate schema (outputs must contain either a sourced claim, a derived claim with reasoning shown, or an explicit uncertainty declaration) and to detect destructive commands before actuation.

**Why this was chosen:**  
The absolute honesty mandate cannot be enforced by prompting alone — models override prompts. Schema-level validation that rejects responses not meeting the honesty structure provides a structural guarantee. Guardrails AI provides this as a configurable validation layer without modifying the core model.

---

### DEC-019
**Decision:** No WhatsApp MCP bridge or any unofficial messaging API bridge  
**Status:** LOCKED

**What was decided:**  
WhatsApp, Instagram, and all other messaging/social applications are operated exclusively via the visual computer control layer — the system sees the screen and controls mouse/keyboard to interact with these apps just as a human would. No unofficial protocol bridges (WhatsMeow, Baileys, etc.) are used.

**Why this was chosen:**  
WhatsApp actively detects and permanently bans accounts that use unofficial API access at the protocol level. The ban risk is real and the consequences are permanent. Instagram similarly detects unofficial API access. Visual computer control is indistinguishable from a human using the application — because the method of interaction is identical to human use. This approach carries zero ban risk.

**Secondary reason:**  
Telegram is the designated remote command channel and uses the official Telegram Bot API (fully sanctioned, no ban risk). For remote task assignment from a phone, Telegram is the correct tool. WhatsApp is operated visually when reading/sending messages directly on the user's computer.

---

### DEC-020
**Decision:** PII scrubber runs before every cloud API call  
**Status:** LOCKED

**What was decided:**  
`interfaces/api/middleware/pii_scrubber.py` (using presidio-analyzer + presidio-anonymizer) processes all content before it is sent to any cloud LLM provider. Personal names, addresses, financial account numbers, phone numbers, email addresses, and other PII categories are replaced with placeholders.

**Why this was chosen:**  
The privacy mandate requires that the user's personal data not reach external services unnecessarily. PII scrubbing ensures that even when cloud models are used for their reasoning capability, the specific personal details of the user's life are not exposed to those providers' training pipelines or logging systems.

---

## SECTION 5: VOICE AND PERSONA DECISIONS

---

### DEC-021
**Decision:** Kokoro-82M as standard TTS, Coqui XTTS for high-emotion responses  
**Status:** LOCKED

**What was decided:**  
Everyday speech uses Kokoro-82M (lightweight, CPU-runnable, high quality for its size). High-emotional-register responses (comfort_and_care, realtime_coach, reciprocal_care modes) use Coqui XTTS for greater expressiveness and emotional range.

**Why this was chosen:**  
Kokoro-82M handles everyday speech well at near-zero computational cost. The "savage best friend" persona requires genuine emotional expressiveness in certain modes — warmth that sounds warm, excitement that sounds excited. Kokoro's emotional range is insufficient for these moments. Coqui XTTS provides the expressiveness needed for high-emotion modes while still running locally.

**Alternatives considered:**  
- Piper TTS (early documents): Piper was recommended in v_2 planning documents but replaced with Kokoro-82M in the final reconciliation (part_1.txt). Kokoro has better quality for English and Hinglish output.
- Fish Speech: rejected — too high VRAM requirement for the inference model it requires.
- Cloud TTS (ElevenLabs, Google TTS): available as optional upgrade if user configures API key, but not the default — maintains the offline-first requirement.

---

### DEC-022
**Decision:** Whisper (local) with Hinglish fine-tune for STT  
**Status:** LOCKED

**What was decided:**  
Speech-to-text uses OpenAI's Whisper model running locally. The base Whisper model is fine-tuned on a public Hinglish (Hindi-English code-mixed) dataset to improve accuracy for the primary user's speech patterns.

**Why this was chosen:**  
The primary user communicates in Hinglish — a code-mixed language that standard ASR systems handle poorly. Base Whisper handles code-switching imperfectly, particularly for Indian accent English and Hindi words mid-sentence. Fine-tuning on public Hinglish datasets (Mozilla Common Voice Hindi + English bilingual datasets) significantly improves accuracy without changing the underlying model architecture.

**Note on fine-tuning:** Fine-tuning Whisper for Hinglish is a one-time operation done during advanced setup (not during first_run.py by default). `[IMPLEMENTATION_DETAIL: Whisper fine-tuning should be offered as an optional step during first run setup with an estimated time warning]`

---

### DEC-023
**Decision:** Configurable wake word (not hardcoded project name)  
**Status:** LOCKED

**What was decided:**  
The wake word is the value stored in `config/project_name.txt`. This file is set during first_run.py when the user names their installation. The string `[PROJECT_NAME]` is a placeholder in all documentation and must not appear anywhere in the actual codebase as a literal string. The code reads the name from the config file at runtime.

**Why this was chosen:**  
The project does not have a final name. Different users may prefer different names for their installation. Building the wake word into the config from the start ensures no code change is needed when the final name is chosen or when users customise their installation name.

---

### DEC-024
**Decision:** True best friend persona with 7 situational modes — not a fixed single tone  
**Status:** LOCKED

**What was decided:**  
The persona is not a static "savage assistant" or a static "professional assistant." It is a situationally adaptive system that reads the user's emotional and cognitive state and selects the appropriate mode: making_you_laugh, reality_check, comfort_and_care, the_push, honest_advisor, just_listening, reciprocal_care, goal_enforcer.

**Why this was chosen:**  
A fixed aggressive/savage tone would be actively harmful in genuine distress situations. A fixed gentle tone would fail to deliver the honest push the user needs when avoiding their responsibilities. Real best friends modulate their approach based on what the person in front of them actually needs. The 7-mode system captures the primary interaction patterns of a healthy, deep friendship.

**Important rule:** The absolute honesty mandate is NEVER suspended regardless of persona mode. The persona controls how truth is delivered — not whether it is delivered. In comfort_and_care mode, the system is warm and patient. It is still honest.

---

### DEC-025
**Decision:** Voice cloning stored and processed locally only  
**Status:** LOCKED

**What was decided:**  
The user's voice sample and resulting voice clone model are stored on the local machine only. They are never uploaded to any cloud service for training, storage, or inference.

**Why this was chosen:**  
A person's voice is biometric data. Uploading voice samples to external services creates privacy risk, potential legal issues in jurisdictions with biometric data protection laws (GDPR, BIPA, etc.), and a permanent loss of control over that data. Local voice cloning with libraries that run inference on the local machine ensures the user retains full control.

---

## SECTION 6: CAPABILITIES AND FEATURE DECISIONS

---

### DEC-026
**Decision:** CO-mode is always active — requires formal holiday request with evaluation to deactivate  
**Status:** LOCKED

**What was decided:**  
The CO (Commanding Officer) daily planning mode cannot be casually switched off. Deactivation requires submitting a holiday request with a reason and duration. The reason is evaluated: legitimate events (travel, named events, medical) are approved; vague fatigue reasons result in a scaled-back plan rather than full suspension; repeated vague reasons result in a pushback with quest progress data.

**Why this was chosen:**  
The CO mode exists specifically to hold the user accountable to their own stated goals. A mode that can be disabled instantly whenever the user feels like it provides no accountability at all. The holiday evaluation system creates a meaningful friction — not insurmountable, but enough to distinguish genuine need from avoidance.

**Human limit recognition:** The system is explicitly aware the user is human, not a robot. The biological rhythm learner tracks natural low-energy periods and the daily plan is automatically lighter during those periods without requiring a holiday request. The distinction is between the system adapting to human biology (built in) vs. the user using "I'm tired" to avoid their goals entirely (requires evaluation).

---

### DEC-027
**Decision:** Screenshots and recordings saved to disk ONLY on explicit user command  
**Status:** LOCKED

**What was decided:**  
When the system takes a screenshot for task analysis or error diagnosis, the image is analysed in memory and discarded. Nothing is written to disk. Only when the user explicitly says "take a screenshot", "screen record", "save this image", or equivalent explicit save command does the system write any visual media to disk.

**Why this was chosen:**  
The user's screen contains sensitive information — financial data, private messages, personal files, credentials. Automatically saving screenshots during every computer control operation would create a growing archive of sensitive screen captures that the user did not deliberately create. The principle is minimal data retention: use what is needed, discard everything else immediately.

---

### DEC-028
**Decision:** Person recognition using local face encoding and voice fingerprinting — never cloud  
**Status:** LOCKED

**What was decided:**  
Face recognition uses locally computed face encodings (using face_recognition library or DeepFace with local model weights). Voice recognition uses locally computed audio fingerprints (using pyannote.audio). All person recognition data (face encodings, voice prints, person profiles) is stored in `vault/people/` on the local machine.

**Why this was chosen:**  
Facial recognition data and voice prints are biometric data. Sending them to cloud recognition APIs (AWS Rekognition, Google Vision, Azure Face) creates legal liability in many jurisdictions, permanent loss of control over the data, and a privacy violation fundamentally incompatible with the project's privacy mandate.

---

### DEC-029
**Decision:** Free cloud compute (Colab, Kaggle, HuggingFace Spaces) for compute-intensive tasks  
**Status:** LOCKED

**What was decided:**  
When local hardware is insufficient for a computation (model fine-tuning, Level 6 discovery runs, large-scale analysis), the system uses free-tier cloud compute platforms via visual browser control. The session is opened, the computation is run, results are downloaded, and the session is deleted. Only the minimum necessary data (anonymised, PII-scrubbed) is uploaded for each computation.

**Why this was chosen:**  
The project has no budget for paid cloud compute infrastructure. Free-tier platforms (Google Colab, Kaggle Notebooks, HuggingFace Spaces) provide GPU access at zero cost within their usage limits. The visual browser control approach means no API keys or paid accounts are required for the basic free tiers.

**What is never uploaded to these platforms:**  
Vault content, conversation history, personal data, biometric data, unencrypted credentials. Only: anonymised training examples (for fine-tuning), sanitised computation inputs, model weight files that are publicly available anyway.

---

### DEC-030
**Decision:** Git + private GitHub as the sole cloud backup mechanism  
**Status:** LOCKED

**What was decided:**  
The vault and config files are backed up via Git auto-commit (every sleep cycle) with automatic push to the user's private GitHub repository. No other cloud backup service is used.

**Why this was chosen:**  
GitHub free tier provides unlimited private repositories. Git provides version history, easy restore, diff capability for seeing exactly what changed in any sleep cycle, and the ability to roll back any memory consolidation that produced unwanted results. It is free, already integrated into the sleep cycle for version control purposes, and requires no additional services. The project has no funding for cloud storage services.

---

### DEC-031
**Decision:** Intelligence preservation as a hard architectural constraint, not a soft feature  
**Status:** LOCKED

**What was decided:**  
The mandate that [PROJECT_NAME] must not make the user cognitively dependent is a hard design constraint applied to every module, not an optional feature or a persona setting. Think-first gates, over-reliance detection, knowledge ownership verification, and imagination preservation are built into the core system logic.

**Why this was chosen:**  
Current AI tools demonstrably reduce user cognitive engagement. Research shows that when tasks are consistently outsourced to AI, the user's ability to perform those tasks independently atrophies. [PROJECT_NAME]'s purpose is to make the user more capable, not to replace their capability. This requires designing the system explicitly against dependency formation — which means it cannot be an opt-in feature (users who need it most would opt out).

---

### DEC-032
**Decision:** Lie detection for CO-mode holiday requests — passive, not interrogative  
**Status:** LOCKED

**What was decided:**  
The system does not actively interrogate the user when a holiday reason seems suspicious. It passively monitors future interactions for inconsistencies with the stated reason, collects evidence over time, and only acts when sufficient evidence has accumulated. The consequence is delivered at a natural conversational moment, not immediately on detection.

**Why this was chosen:**  
Immediate accusation on insufficient evidence would damage the user-system relationship and produce false positives. The passive accumulation approach mirrors how a real friend would handle this situation — they would notice the inconsistency, remember it, and bring it up when they had enough context and the right moment. The consequence is proportional and productivity-oriented, not punitive.

---

### DEC-033
**Decision:** Adversarial self-challenging (critic sub-agent) as the structural honesty guarantee  
**Status:** LOCKED

**What was decided:**  
Every important output passes through an adversarial debate circuit (subagent_generator → subagent_critic × N iterations → subagent_synthesis) before delivery. The critic is explicitly instructed to attack the proposed output from every angle. This is not a quality check — it is an adversarial challenge.

**Why this was chosen:**  
The absolute honesty mandate cannot be enforced by prompting the main model to "be honest." LLMs trained on human feedback tend to produce confident-sounding, agreeable responses even when uncertain. The critic sub-agent is a structural intervention: a separate LLM call specifically tasked with finding what is wrong with the proposed output. Outputs that survive this challenge are more reliable than outputs from a single LLM call regardless of how carefully that call is prompted.

---

### DEC-034
**Decision:** MCP (Model Context Protocol) for all tool integrations  
**Status:** LOCKED

**What was decided:**  
All external tool integrations use the Model Context Protocol: Official MCP Python SDK for client-side tool discovery and calling; FastMCP for authoring new MCP servers; the system can autonomously create new MCP servers when a needed integration does not exist.

**Why this was chosen:**  
MCP is an open protocol (Anthropic, MIT licence) designed specifically for connecting AI systems to tools. It provides: standardised tool discovery (tools/list), standardised calling convention, versioning, and a growing ecosystem of pre-built MCP servers (GitHub MCP, filesystem MCP, etc.). Building on MCP means integrations are portable and the ecosystem of available tools grows without any action from the development team.

**Auto-creation of MCP servers:**  
When the system encounters a task requiring a tool that has no MCP server, it uses `skills/mcp/server_factory.py` (FastMCP) to design, generate, and deploy a new MCP server. This is subject to the same HITL approval gate as any new skill installation.

---

### DEC-035
**Decision:** Weekly fine-tuning cycle (not monthly) with EWC to prevent catastrophic forgetting  
**Status:** LOCKED

**What was decided:**  
The Unsloth QLoRA fine-tuning cycle runs once per week during the sleep cycle. Elastic Weight Consolidation (EWC) loss term is included in every training run to prevent catastrophic forgetting of previously learned behaviour.

**Why weekly instead of monthly:**  
Monthly fine-tuning means 4 weeks of interaction data before the model adapts. Weekly means 1 week — the model adapts to the user's style and preferences 4× faster. The computational cost is the same per run; the only change is frequency.

**Why EWC is mandatory:**  
Without EWC, each fine-tuning run risks overwriting previously learned patterns (catastrophic forgetting). EWC adds a regularisation term to the loss function that penalises changes to weights that were important for previously learned tasks. This allows the model to learn new things each week without forgetting what it has already learned about the user.

---

### DEC-036
**Decision:** Level 6 is "autonomous discovery, development and creation" — not "hypothesis generation"  
**Status:** LOCKED

**What was decided:**  
Level 6 is explicitly defined as the system discovering, developing, and creating things that do not yet exist — not generating hypotheses about things that already exist. The distinction is fundamental to the design of the discovery agent.

**Why this matters architecturally:**  
A hypothesis generator looks at known facts and proposes testable explanations. A discovery engine actively explores spaces where knowledge does not yet exist and creates outputs that are genuinely novel. The MCTS + Bayesian Surprise approach (which prioritises high-surprise branches — results inconsistent with current knowledge) and the FunSearch-style evolutionary search are designed for discovery, not hypothesis generation. The adversarial debate circuit before committing any discovery ensures that novelty claims are challenged before they are accepted.

---

### DEC-037
**Decision:** Multi-year projects use unconventional thinking when blockers persist after user cannot answer  
**Status:** LOCKED

**What was decided:**  
When a multi-year project hits a blocker, the system: (1) asks the user, (2) if the user cannot answer, activates unconventional thinking — first principles, cross-domain analogies, untested approaches. The system does not halt. It continues working the problem with approaches not found in standard methodology.

**Why this was chosen:**  
A project management agent that halts on every unsolvable blocker fails at the core purpose of multi-year autonomous execution. Real projects hit unsolvable problems regularly. Human project managers do not stop working — they find unconventional approaches. The system mirrors this by exploring outside the standard solution space when conventional approaches are exhausted. All unconventional proposals are explicitly labelled as such (honesty mandate) and the user is notified of what was tried.

---

### DEC-038
**Decision:** Real-time negotiation coaching via parallel audio listening  
**Status:** LOCKED

**What was decided:**  
During live negotiations, the system listens to the call audio via `communication/realtime_coach.py` in parallel with the user's own participation. It provides real-time suggestions via text on a secondary screen or Telegram message — the user hears suggestions silently while continuing the conversation.

**Why this was chosen:**  
Negotiation is a high-stakes, time-sensitive activity where expert guidance at the moment of conversation is dramatically more valuable than post-hoc analysis. The coaching system provides the equivalent of a senior advisor in the user's ear throughout every important negotiation — available for every call regardless of budget for human advisors.

---

### DEC-039
**Decision:** Voice cloning for outbound calls using user's own voice  
**Status:** LOCKED

**What was decided:**  
The system makes outbound calls using a locally cloned model of the user's voice. The other party hears the user's actual voice. The user receives a transcript.

**Why this was chosen:**  
This allows the system to handle routine calls (appointment booking, follow-ups, customer service, vendor negotiation) that would otherwise require the user's direct time. The voice clone makes these calls credible and natural. The model is trained and stored locally — the user's voice never leaves their machine for training.

**Legal note (must be implemented):**  
Voice cloning of one's own voice for personal use is generally legal. However, using it to misrepresent identity (claiming to be a different person) is not. The system must only make calls where it is reasonable for the called party to believe they are speaking with the user themselves or their representative. Call scripts must not make false claims about identity. `[IMPLEMENTATION_DETAIL: Add disclosure option — e.g., "You are speaking with an automated assistant acting on behalf of [user name]" — as a configurable option in settings.yaml]`

---

## SECTION 7: REJECTED TECHNOLOGIES — COMPLETE REGISTRY

The following technologies were explicitly considered and rejected. They must not be used anywhere in the implementation.

| Technology | Category | Rejection Reason |
|---|---|---|
| E2B (Firecracker) | Sandboxing | Cloud service — code leaves machine, violates privacy mandate |
| ChromaDB | Vector database | GPU/memory intensive, degrades at scale, prohibited by DEC-005 |
| Pinecone | Vector database | Cloud service, prohibited by DEC-005 |
| Qdrant | Vector database | Unnecessary overhead, prohibited by DEC-005 |
| Weaviate | Vector database | Cloud/self-hosted overhead, prohibited by DEC-005 |
| Letta (full service) | Memory | Runs as separate server — use memory block pattern only (DEC-008) |
| Mem0 (forked) | Memory extraction | Fork maintenance burden, prohibited by DEC-009 |
| Graphiti (forked) | Graph database | Neo4j dependency, fork maintenance burden, prohibited by DEC-006 |
| Neo4j | Graph database | JVM dependency, server process, overkill for local single-user (DEC-006) |
| LightRAG | RAG framework | Graph-DB dependency, adds complexity (DEC-006) |
| WhatsMeow | WhatsApp | Unofficial protocol, permanent account ban risk (DEC-019) |
| Baileys | WhatsApp | Unofficial protocol, permanent account ban risk (DEC-019) |
| InsAIts | Security | Pre-1.0, single maintainer, not suitable as core security infrastructure |
| uvbox | Distribution | Existence unconfirmed — use plain uv instead |
| Piper TTS | Voice | Superseded by Kokoro-82M in quality (DEC-021) |
| Fish Speech | Voice | Too high VRAM requirement (DEC-021) |
| AutoGPT | Agent framework | No proper state management, unreliable (DEC-002) |
| CrewAI | Agent framework | No interrupt(), limited state management (DEC-002) |
| AutoGen | Agent framework | Conversation-centric model does not fit architecture (DEC-002) |
| Flask | API | Synchronous, no built-in validation (DEC-003) |
| gRPC | API | Overkill for local IPC (DEC-003) |
| MongoDB | Storage | Binary format, not Git-diffable, unnecessary complexity |
| PostgreSQL | Storage | Server process, overkill for local single-user |
| AWS Rekognition | Face recognition | Cloud service, biometric data sent externally (DEC-028) |
| Google Vision | Face recognition | Cloud service, biometric data sent externally (DEC-028) |
| Azure Face API | Face recognition | Cloud service, biometric data sent externally (DEC-028) |
| ElevenLabs TTS | Voice | Cloud service, not offline-first (optional upgrade only if API key provided) |
| Paid cloud storage | Backup | No budget — GitHub free tier is sufficient (DEC-030) |
| CogniFold (package) | Sleep cycle | Does not exist as an installable package — paper only (DEC-008) |
| PANDO (package) | Skill health | Does not exist as an installable package — paper only |
| Kintsugi (package) | Repair loop | Does not exist as an installable package — paper only |

---

## SECTION 8: OPEN IMPLEMENTATION DETAILS

The following items are marked `[IMPLEMENTATION_DETAIL]` throughout the codebase. These are the only areas where the coding AI has discretion to make best-practice decisions. All other decisions are locked.

| Location | Open Decision |
|---|---|
| `communication/voice/wake_word.py` | Choice between pvporcupine and silero-vad — select based on licence and accuracy benchmarks at build time |
| `communication/voip_caller.py` | VoIP library selection: evaluate pjsua2, aiortc, and available free-tier VoIP providers at build time |
| `communication/voice/voice_clone.py` | Voice cloning library: evaluate Tortoise-TTS, XTTS-v2, Bark — select based on quality/speed/VRAM tradeoff |
| `actuation/recognition/face_recognizer.py` | Choice between face_recognition library and DeepFace — both are local, select based on accuracy |
| `actuation/recognition/voice_recognizer.py` | Speaker diarisation: pyannote.audio is recommended; confirm licence compatibility |
| `core/memory/l2_index.py` | BM25 index persistence strategy — in-memory rebuild on start is simplest; add optional disk cache if startup time exceeds 5 seconds on large vaults |
| `agents/background/sleep_agent.py` | Inactivity detection mechanism — monitor FastAPI last-request timestamp or use OS idle time API |
| `intelligence/calibration_tracker.py` | Brier score calculation interval — recommend weekly batch recalculation |
| `communication/voip_caller.py` | Disclosure option for automated calls — implement as configurable in settings.yaml |
| `bootstrap/first_run.py` | Whisper fine-tuning prompt — offer as optional step with time estimate warning |
| `core/memory/l2_index.py` | Locking strategy — threading.RLock recommended; upgrade to filelock if multi-process deployment is needed |
| Various | Exact inter-key timing parameters for keyboard_controller.py — use values within 50-180ms range |
| Various | Exact mouse movement randomisation parameters — stay within bezier curve natural bounds |

---

---

## SECTION 9: ADDITIONAL DOMAIN AGENT DECISIONS

---

### DEC-040
**Decision:** health_agent.py is a confirmed domain agent — not optional  
**Status:** LOCKED

**What was decided:**  
A dedicated health management agent is confirmed as a core domain agent, not a suggestion or future addition. It handles appointments, health records, medication, symptom tracking, and pre-appointment preparation.

**Why this was chosen:**  
Health management is one of the highest-value daily use cases for a personal AI. Missed appointments, forgotten medications, and failure to correlate symptoms across time are common and consequential. All health data is stored locally in `vault/health/` and never sent to any cloud service. The agent uses only peer-reviewed medical sources (PubMed, Cochrane) — never consumer health blogs — respecting the absolute honesty mandate in a domain where bad information has direct physical consequences.

**Privacy requirement:** Health data is among the most sensitive personal data that exists. `vault/health/` must be explicitly excluded from all cloud LLM calls. PII scrubber gets an additional health data filter. Git backup of `vault/health/` is disabled by default — user must explicitly opt in.

---

### DEC-041
**Decision:** legal_agent.py is a confirmed domain agent — not optional  
**Status:** LOCKED

**What was decided:**  
A dedicated legal intelligence agent is confirmed as a core domain agent. It handles legal research, contract drafting, contract red-lining, compliance monitoring, and obligation tracking.

**Why this was chosen:**  
Legal exposure is a constant risk for anyone running a business, signing contracts, or operating in regulated domains. The user is building businesses, managing content channels, doing e-commerce, and handling financial operations — all of which have significant legal dimensions. The agent does not give legal advice (which requires a licensed lawyer) but does provide factual legal research, contract analysis, and obligation tracking that helps the user know when they need a lawyer and what specific questions to ask.

**Disclaimer requirement:** `legal_agent.py` must prepend all legal outputs with a disclaimer: "This is factual legal research, not legal advice. Consult a licensed lawyer for decisions with legal consequences." This is a hard constraint enforced in the agent's output formatter.

---

### DEC-042
**Decision:** travel_agent.py is a confirmed domain agent — not optional  
**Status:** LOCKED

**What was decided:**  
A dedicated travel and logistics management agent is confirmed as a core domain agent.

**Why this was chosen:**  
Travel planning is time-consuming, high-stakes (wrong visa = denied entry), and involves many parallel booking operations that can all be done autonomously via visual browser control. The CO-mode daily planner integrates with travel_agent.py — when a trip is on the calendar, travel preparation tasks automatically appear in the CO-mode directive plan days or weeks before departure.

---

### DEC-043
**Decision:** negotiation_agent.py is a confirmed dedicated domain agent, separate from digital_worker_agent.py  
**Status:** LOCKED

**What was decided:**  
Negotiation intelligence is handled by a dedicated domain agent, not folded into the digital worker agent. This is because negotiation requires specialist reasoning (game theory, BATNA analysis, adversarial party modelling, real-time coaching) that warrants its own agent with its own knowledge base and its own sub-agent spawning patterns.

**Why separate from digital_worker:**  
The digital_worker_agent handles execution tasks. Negotiation is a reasoning and strategy task that uses the adversarial debate circuit extensively (strategy proposals go through the critic) and requires deep integration with the social_graph.py (relationship context on the negotiating party) and calibration_tracker.py (confidence in outcome predictions). These dependencies are complex enough that keeping them in a dedicated agent prevents digital_worker_agent from becoming unwieldy.

---

### DEC-044
**Decision:** models/ directory is part of the project structure — excluded from Git  
**Status:** LOCKED

**What was decided:**  
A `models/` directory at the project root stores all local AI model weight files: LLM (GGUF), Whisper, Kokoro-82M, Coqui XTTS, Qwen3-VL, face recognition models, and the user's voice clone. This directory is listed in `.gitignore` and is never pushed to GitHub.

**Why this was chosen:**  
Model files are large (typically 1–30GB each), binary, and publicly available elsewhere. They must not be pushed to GitHub (storage limits, bandwidth). They must not be in the vault (vault is for knowledge, not binaries). They need a clear, predictable location that first_run.py and model_config.py can reference. The `models/` directory serves this purpose. `verify_install.py` checks that expected model files exist in this directory and alerts the user to download missing ones.

---

### DEC-045
**Decision:** scripts/ directory with operational shell scripts is part of the structure  
**Status:** LOCKED

**What was decided:**  
A `scripts/` directory at the project root contains operational shell scripts: start.sh, stop.sh, restart.sh, status.sh, reset_memory.sh, export_vault.sh, rebuild_index.sh, update.sh.

**Why this was chosen:**  
Managing a system with a FastAPI daemon, background asyncio threads, Docker containers, a Langfuse instance, and a pystray tray app requires clean start/stop/restart operations. Shell scripts provide this without requiring the user to understand the internal architecture. `rebuild_index.sh` specifically addresses the case where the BM25 index becomes corrupted or out of sync — it rebuilds it from the vault files, which are always the source of truth.

---

### DEC-046
**Decision:** debate_orchestrator.py manages the adversarial sub-agent loop  
**Status:** LOCKED

**What was decided:**  
A dedicated `debate_orchestrator.py` in `agents/sub_agents/` manages the generator→critic→synthesis loop. It is responsible for: determining when to trigger the critic circuit (based on output importance classification), managing the iteration counter (max 5), detecting convergence (critic returns no material objections), and routing to synthesis_agent when the debate resolves.

**Why separate from critic_agent.py:**  
The loop management logic (when to stop, when to continue, convergence detection) is separate from the adversarial challenging logic. Mixing them creates a god-object. debate_orchestrator.py is a pure routing and state management module — it contains no LLM calls itself.

---

### DEC-047
**Decision:** predictive_preloader.py in intelligence/ is a confirmed feature  
**Status:** LOCKED

**What was decided:**  
`intelligence/predictive_preloader.py` reads the user's calendar 2–3 hours ahead of every scheduled event and pre-loads all relevant vault context for that event into L1 memory blocks. When the user opens the app near the event time, context is already assembled.

**Why this was chosen:**  
This is the "knows what you need before you ask" capability identified as one of the highest-impact futuristic-but-achievable features. Pre-loading before a meeting means the user arrives at the conversation with full context instantly, without needing to ask for a briefing. The computational cost is low (scheduled background BM25 search) but the user experience improvement is significant.

---

### DEC-048
**Decision:** habit_tracker.py and progress_tracker.py are confirmed as separate from quest_tracker.py  
**Status:** LOCKED

**What was decided:**  
Three separate growth tracking files: `quest_tracker.py` (manages main quests and side quests — milestone tracking, completion events, progress percentage), `progress_tracker.py` (tracks cross-quest milestone achievements and generates celebration moments), `habit_tracker.py` (tracks recurring daily/weekly habit completion with streak counting and regression detection).

**Why three separate files:**  
Quests are goal-oriented (achieve X). Habits are behaviour-oriented (do Y every day). Progress celebrates achievement. These three concerns have different data models, different triggering logic, and different output behaviours. Mixing them creates coupling that makes each harder to modify independently.

---

### DEC-049
**Decision:** vault/health/ and vault/legal/ are confirmed vault subdirectories with special privacy rules  
**Status:** LOCKED

**What was decided:**  
`vault/health/` and `vault/legal/` are confirmed vault subdirectories. Both have elevated privacy rules: (a) excluded from cloud LLM calls even after PII scrubbing (the content itself is sensitive beyond PII), (b) `vault/health/` is excluded from Git backup by default (user must opt in), (c) `vault/legal/` may be included in Git backup but encrypted at rest `[IMPLEMENTATION_DETAIL: evaluate git-crypt for vault/legal/]`.

---

### DEC-050
**Decision:** .gitignore explicitly excludes sensitive directories and binary files  
**Status:** LOCKED

**What was decided:**  
`.gitignore` must explicitly exclude: `models/` (all model weights), `vault/health/` (health records), `*.pkl` (networkx graph serialisation), `.env` (environment variables), `config/VOICE_PROFILES.md` (voice fingerprint index), `vault/people/*_face.pkl` (face encodings), `vault/security/authorizations/` (not excluded — security engagements should be versioned for audit trail).

**Explicitly INCLUDED in Git (and therefore pushed to GitHub):**  
All vault content except health/, all config files except .env and VOICE_PROFILES.md, all source code, all tests.

---

### DEC-051
**Decision:** All Python packages need __init__.py — no implicit namespace packages  
**Status:** LOCKED

**What was decided:**  
Every directory in the project that contains Python files must have an `__init__.py` file. Explicit package declarations are required. No implicit namespace packages.

**Why this was chosen:**  
Implicit namespace packages (no __init__.py) cause subtle import issues, particularly when running pytest from the project root. Explicit __init__.py files ensure consistent import behaviour across all environments (development, test, production) regardless of the Python version's namespace package handling.

---

### DEC-052
**Decision:** conftest.py and test fixtures are mandatory — not optional  
**Status:** LOCKED

**What was decided:**  
`tests/conftest.py` is a required file that provides shared pytest fixtures including: a mock LLM that returns pre-defined responses (from `tests/fixtures/mock_llm_responses.json`), a temporary vault directory, a clean L2 index, and a reset USER.md. These fixtures ensure all unit tests are deterministic and do not require a running LLM or internet connection.

**Why this matters:**  
Without mock fixtures, unit tests would call the actual LLM (slow, expensive, non-deterministic) or fail without a configured model. The mock LLM fixture allows the entire test suite to run in CI without any model or API key, testing all logic except the actual LLM call itself.

---

### DEC-053
**Decision:** TRADING_RULES.md, MONITORING_TOPICS.md, ENGAGEMENT_LOG.md, and VOICE_PROFILES.md are confirmed config files  
**Status:** LOCKED

**What was decided:**
- `config/TRADING_RULES.md`: User-defined trading parameters and hard limits (max position size per asset, max daily loss, approved asset classes, prohibited instruments). finance_agent.py reads this before every trade signal. These rules CANNOT be overridden by agent reasoning — they are enforced as hard constraints.
- `config/MONITORING_TOPICS.md`: Additional proactive monitoring topics the user explicitly wants tracked, beyond what the system auto-detects from active projects and quests.
- `config/ENGAGEMENT_LOG.md`: Security engagement authorization records. security_agent.py reads this before starting any reconnaissance. No authorization record = no security operation.
- `config/VOICE_PROFILES.md`: Index of known voice fingerprints with person name mappings, for voice_recognizer.py. Stored locally only.

---

### DEC-054
**Decision:** docker-compose.dev.yml is confirmed alongside production docker-compose.yml  
**Status:** LOCKED

**What was decided:**  
A development Docker Compose file (`docker/docker-compose.dev.yml`) is maintained separately from the production compose file. The dev compose adds: volume mounts for faster code iteration without rebuilding images, debug logging levels, and relaxed resource limits for development machines. Production compose enforces all security constraints fully.

---

### DEC-055
**Decision:** pyproject.toml with uv as the dependency manager — not requirements.txt alone  
**Status:** LOCKED

**What was decided:**  
`pyproject.toml` is the project's dependency declaration file, managed by uv. `requirements.txt` (generated by uv from pyproject.toml) is also maintained for compatibility with environments that cannot use uv directly. The bootstrap installer (`install.sh`) uses uv to create a virtual environment and install all dependencies.

**Why uv:**  
uv is the confirmed distribution and environment tool for this project. It is dramatically faster than pip for dependency resolution and installation, supports lock files for reproducible installs, and is cross-platform. This was confirmed in the original architectural planning and is not subject to change.

---

### DEC-056
**Decision:** The 5-file vs 4-file question — confirmed correct  
**Status:** CONFIRMED UNDERSTANDING

**What happened:**  
The AI coder provided 5 files: `AGENT_INTERACTION_MAP_TEMPLATE.md`, `AI_CENTRIC_PRD_TEMPLATE.md`, `AI_PROJECT_KICKOFF_GUIDE.md`, `MASTER_KICKOFF_PROMPT.txt`, `MODULE_DEPENDENCY_GRAPH_TEMPLATE.md`.

**What goes back to the coder AI:**  
4 files only: `FINAL_AI_CENTRIC_PRD.md`, `AGENT_INTERACTION_MAP.md`, `MODULE_DEPENDENCY_GRAPH.md`, `DECISIONS_LOG.md`.

**The two non-deliverable files:**
- `AI_PROJECT_KICKOFF_GUIDE.md` — this was a directive to the Planning AI (Claude). It has been followed. It is not a deliverable to return.
- `MASTER_KICKOFF_PROMPT.txt` — this is the prompt template used to trigger the planning AI. It has been executed. It is not a deliverable. The coder AI receives the 4 output files instead.

**Correct workflow:** Copy the content of the 4 output files (or attach them) into the coder AI session. The `MASTER_KICKOFF_PROMPT.txt` explained how to do this — the deliverables ARE the filled-in versions of the templates it referenced.

---

*End of DECISIONS_LOG.md — Version 1.1.0*  
*Total decisions documented: 56 locked decisions + 1 confirmed understanding*  
*Complete rejected technology registry: 30+ entries*  
*Open implementation details: 15 items*  
*All decisions are final. Do not reopen without explicit human authorisation.*
