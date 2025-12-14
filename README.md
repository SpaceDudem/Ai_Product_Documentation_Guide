# AI Product Documentation Guide
**A documentation-first, AI-compliant framework for building real systems without drift**

---

## What this repository is

This repository defines a **documentation and process framework** for building software, hardware, and hybrid systems using **AI-assisted development**, without losing control of scope, intent, or correctness.

It is not a codebase.  
It is a **control plane** for development.

The goal is to make product intent, technical decisions, and implementation steps:
- explicit
- traceable
- enforceable
- understandable by both humans and AI agents

This repo exists to solve a specific failure mode:

> AI-assisted development that slowly drifts away from requirements until the system no longer matches what was intended.

---

## Core idea

**No code is written unless it is anchored to documentation.**  
**No documentation is trusted unless it is enforced.**

This repository provides:
- a structured way to define product intent (MPD)
- a structured way to define implementation decisions (TDS)
- a ticket system that binds work to those decisions
- CI tooling that blocks drift
- hardened prompts so AI agents behave like disciplined engineers, not autocomplete engines

---

## The document stack

### 1. MPD — Master Product Definition
Defines **what** the product is and **why** it exists.

Covers:
- product purpose and non-goals
- users and operating environments
- functional and non-functional requirements
- operational lifecycle
- success and kill criteria

This is the source of truth for intent.

---

### 2. TDS — Technical Design Specification
Defines **how** the product will be implemented.

Covers:
- system architecture
- component responsibilities
- data models and state
- interfaces and control flow
- error handling, performance, security
- update and deployment strategy

This is the source of truth for implementation decisions.

---

### 3. Tickets
Define **what work is allowed to happen right now**.

Each ticket:
- references specific MPD and TDS section IDs
- defines explicit scope (in-scope / out-of-scope)
- includes acceptance criteria and test expectations
- declares whether changes require doc updates

No ticket → no work.

---

### 4. AI Compliance Layer
Defines how **AI agents are allowed to operate**.

Includes:
- allowed MCP tools
- forbidden actions
- agent roles and handoffs
- stop conditions
- evidence requirements
- drift audits

This layer turns AI from a creative liability into a constrained collaborator.

---

## Stable IDs and traceability

All documents use **stable semantic IDs**, not positional section numbers.

Example:

[TDS-SW-CONFIG-PERSISTENCE-001]

These IDs:
- never change
- are referenced by tickets
- are enforced by CI
- allow full traceability from intent → design → implementation → tests

Nothing is deleted.  
Deprecated sections remain as historical record.

---

## Repository layout

docs/ MPD/        # Product intent TDS/        # Technical design AI/         # AI compliance specs and guardrails

tickets/ backlog/    # Work not yet done done/       # Completed work (never deleted)

prompts/ system/     # System-level agent constraints tasks/      # Task-specific agent instructions

tools/ lint_ids.py            # Enforces doc ID format + uniqueness lint_tickets.py       # Enforces ticket structure lint_ai_compliance.py # Enforces ticket↔doc↔code linkage

.github/workflows/ ai-lint.yml            # CI enforcement

mcp/ registry.yaml          # MCP tool registry tool-contracts/        # Tool-level constraints

This structure is deliberate.  
Changing it should require a ticket.

---

## CI enforcement

CI is not decorative.

The workflows in this repo fail builds when:
- documentation IDs are malformed or duplicated
- tickets reference non-existent doc sections
- source code changes occur without a ticket reference
- acceptance criteria or scope definitions are missing

This is how drift is stopped before it becomes expensive.

---

## AI agent behavior (non-negotiable)

AI agents operating with this repo must:
- read tickets first
- read referenced MPD/TDS sections
- refuse to guess or invent requirements
- halt on ambiguity
- provide evidence for changes
- explicitly confirm scope compliance

The prompts in `prompts/system/` and `prompts/tasks/` enforce this behavior.

If an agent ignores them, the process is broken — not the agent.

---

## What this repo is NOT

- Not a framework for unconstrained rapid prototyping
- Not a replacement for engineering judgment
- Not a magic compliance solution
- Not tied to any specific language, vendor, or cloud

This is **process infrastructure**, not product code.

---

## Who this is for

This framework is useful if you:
- build long-lived systems
- care about correctness and traceability
- use AI for real engineering work
- want to avoid “AI spaghetti”
- operate in environments where failure matters

It scales from solo developers to teams, and from software-only to hardware-integrated systems.

---

## How to start

1. Fill out `docs/MPD/MPD_v1.0.0.md`
2. Create `docs/TDS/TDS_v0.1.0.md`
3. Add your first ticket in `tickets/backlog/`
4. Run the linters locally
5. Enable GitHub Actions
6. Only then start writing code

---

## Philosophy

This project assumes:
- documentation is executable intent
- constraints enable speed
- AI must be governed, not trusted
- drift is a systems failure, not a people failure

If that resonates, you’re in the right place.
