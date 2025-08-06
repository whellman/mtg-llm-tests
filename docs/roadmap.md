# 📍 MTG-LLM Test Suite — Roadmap

This document outlines the development milestones for the MTG-LLM benchmark suite — a structured framework for evaluating large language models on their ability to reason about Magic: The Gathering (MTG) rules, strategy, and design.

---

## 🎯 Project Goals

- Evaluate LLMs on structured game reasoning within MTG.
- Support diverse test types (rules, gameplay, drafting, flavor, etc).
- Remain model-agnostic: run OpenAI, local models, Hugging Face, etc.
- Use a modular, extensible codebase compatible with broader eval tooling.
- Allow reproducible and interpretable results (not just black-box scores).
- Serve as a reference point for similar game or logic-focused LLM tests.

---

## 🧩 Phase 1 — Core Framework w/ Hugging Face Transformers (Local, Autodownloaded)

✅ Goal: run a transformer model from Hugging Face (autodownloaded via transformers), load a few MTG test prompts, and evaluate basic correctness—all from a fresh RunPod SSH session with HF token as env var.
Milestones:

- [ ] runner.py loads .yaml test scenarios from scenarios/, runs a transformer model via transformers.AutoModelForCausalLM.
- [ ] models/hf_transformer.py loads Hugging Face model via name (e.g. meta-llama/Llama-2-7b-chat-hf) and caches locally.
- [ ] Hugging Face token (HF_TOKEN) pulled via environment variable (sourced from RunPod secret).
- [ ] Add 5–10 basic tests to scenarios/rules/ (e.g., layer rules, simple triggered abilities).
- [ ] evaluators.py includes exact and contains matchers for early-stage reliability.
- [ ] Add requirements.txt including transformers, accelerate, torch, PyYAML.
- [ ] Docs: docs/running_on_runpod.md to walk through full RunPod setup, secret injection, and one-liner to clone + run.

---

## 🧠 Phase 2 — Expansion of Scenario Types

✅ *Goal: cover a wide variety of MTG-specific reasoning types.*

### Milestones:
- [ ] Add `scenarios/draft/` with draft pick choice tests.
- [ ] Add `scenarios/deckbuilding/` with synergy decisions or archetype builds.
- [ ] Add `scenarios/explainer/` for explanatory questions (e.g. "What is the stack?").
- [ ] Add creative tasks like flavor text or card balancing.
- [ ] Document YAML schema format and how to contribute new tests (`docs/adding_new_tests.md`).

---

## ⚙️ Phase 3 — Evaluation & Reporting Tools

✅ *Goal: track test results across models and runs, with meaningful outputs.*

### Milestones:
- [ ] Add pass/fail logging to JSON or CSV.
- [ ] Aggregate results by category, evaluator type, and difficulty.
- [ ] Add CLI flag to compare multiple models side by side.
- [ ] Support evaluation consistency (repeat same test N times).
- [ ] Support token usage and latency logging (if available).

---

## 🌍 Phase 4 — Interoperability & Community

✅ *Goal: plug into broader LLM evaluation tools and share with others.*

### Milestones:
- [ ] Adapt model API to Hugging Face `transformers` and local GGUF models.
- [ ] Add support for LM-Eval-Harness style output formatting.
- [ ] Publish starter scenarios as a public GitHub repo.
- [ ] Add GitHub Actions CI to run tests on push.
- [ ] Add CONTRIBUTING.md and open first community issue for scenario submission.

---

## 🧪 Phase 5 — Advanced Capabilities

✅ *Goal: simulate dynamic MTG situations and analyze strategic output.*

### Milestones:
- [ ] Integrate with a simple game engine (e.g. MAGE or custom sim) for legality validation.
- [ ] Add multi-turn scenario simulations or win-rate estimation tasks.
- [ ] Add Monte Carlo evaluation support or branching scenario trees.
- [ ] Build scoreboard or dashboard for tracking model performance over time.

---

## 📦 Optional Future Ideas

- [ ] Web-based test submission interface.
- [ ] Tournament report generation from logs.
- [ ] Multiplayer or bluffing scenario tests (e.g., Commander or political decisions).
- [ ] Extend to other TCGs or board games via plugins (e.g., Pokémon, Hearthstone).
- [ ] Build a leaderboard and public model comparison site.

---

## 🛠 Tech Stack Overview

| Component      | Tool / Format               |
|----------------|-----------------------------|
| Language       | Python 3.x                  |
| Scenarios      | YAML                        |
| Models         | OpenAI API, local LLMs      |
| Matching       | Exact, semantic (e.g., cosine sim) |
| Storage        | GitHub repo, optionally S3/SQL later |
| CI/CD          | GitHub Actions              |
| Optional       | Docker, FastAPI, Streamlit  |

---

## 🤝 How to Contribute

Start by:
- Running the included sample tests with your own model.
- Writing a new test scenario in `scenarios/`.
- Checking out the docs in `docs/adding_new_tests.md`.
- Opening issues or PRs with new test types, models, or features.

---

## 📅 Timeline (Sketch)

| Phase # | Target Date      |
|---------|------------------|
| Phase 1 | Week 1–2         |
| Phase 2 | Week 2–3         |
| Phase 3 | Week 4           |
| Phase 4 | Week 5–6         |
| Phase 5 | Week 7+          |

(Subject to chaos, bugs, and elder dragons.)

---

## 🧙 Final Notes

This project is both a test suite and a reflection on what structured reasoning looks like under high-context domains like MTG. It can evolve with the game, the LLM ecosystem, and the creativity of contributors.

