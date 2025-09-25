# Final Specification Package for MeUnique (Liat)

This package consolidates everything needed to replicate and extend the MeUnique research and hiring platform, tailored to the `Meunique_PRD_Reaserch` repository and your current Cursor workspace.  It includes the final specification, gap analysis, integration guides, code references, and master prompt.  Follow the instructions below to set up and run your research pipeline end‑to‑end.

## Directory Overview

- **MASTER_PROMPT.md** – Start here. This is the main orchestrator prompt specifying how the pipeline should run.  It includes environment rules, stage order, zero‑trust scoring, and cleanup logic.  Paste this prompt as your system message when launching the orchestrator.
- **/spec/** – Core specification documents:
  - **MeUnique_Final_Spec_and_Integration_Summary.docx** – Final PRD and integration summary.  Treat this as the Single Source of Truth (SSOT).
  - **00_COMPREHENSIVE_GAP_ANALYSIS.md** – Gap analysis identifying missing elements and enhancements required.
  - **EXTERNAL_RESEARCH_ENHANCEMENT_FRAMEWORK.md** – Framework for validating research through open‑source data and APIs.
  - **cursor_restructure_missing_and_failed_a.md** – Background notes on restructuring and missed/failing actions.
- **/guides/** – Integration guides:
  - **🚀 Cursor Integration & External Research Execution Guide.md** – Step‑by‑step instructions for setting up environment variables, running in Cursor, and integrating third‑party APIs.
- **/code_refs/** – Reference code used in the current workspace:
  - `mall_manager_orchestrator.js` – Orchestrates the recruitment workflow across smart stores.
  - `vp_data_devops_engine.js` – Core engine for loop recognition and weight adjustment.
  - `smart_stores_architecture.js` – Definitions for the various smart stores (Discovery, Authenticity, Culture, Time, Bias).
  - `research-executor.py` – Script for automated research execution and data augmentation.
  - `openai-integration.js` – Example of integrating OpenAI models into the pipeline.

## Environment Setup

1. **Copy this package** into the root of your GitHub repository `Liatitshman/Meunique_PRD_Reaserch`.
2. **Set your environment variables** in a `.env` file (not committed):
   - `OPENAI_API_KEY=sk-…`
   - `HUGGING_FACE_HUB_TOKEN=…`
   - `LINKEDIN_API_KEY=…`
   - etc.
3. **Install dependencies** as required by your JavaScript and Python files (Node.js for JS files, Python packages for `research-executor.py`).  Use the `guides/🚀 Cursor Integration & External Research Execution Guide.md` for details.

## Running the Pipeline

1. **Load the master prompt:**  Paste the contents of `MASTER_PROMPT.md` into your orchestrator or ChatGPT system message.  This will set the rules for how the pipeline operates, including stage order and zero‑trust validation.
2. **Execute stages sequentially:**  The prompt instructs the agent to run JD → ICP → Boolean → ATS → Evidence → Culture → Loops → Export.  After each stage, it logs progress and waits for your approval before continuing to export.
3. **Approval & Export:**  Before final export, create an `APPROVED` file in the `.artifacts/` directory or run with `--approve`.  The orchestrator will then generate a multi‑tab Excel workbook and summary report.
4. **Check deliverables:**  The outputs include `MeUnique_Research_Complete.xlsx` (12 tabs) and `Executive_Summary.md`.  Review these and iterate if necessary.

## Consolidation & Cleanup

- Use the gap analysis to ensure every specification item is met.  If you find missing items, update the spec documents and CSVs accordingly.
- Remove any outdated artifacts (e.g., old `FinalFolderLiat` or earlier versions) from your repository to keep your workspace clean.
- Always commit changes to the `main` branch with clear messages (e.g., `feat: added ICP CSV for Backend roles`).

## Additional Notes

- This package does **not** include running example data; you will need to supply candidate/job data into the `data/` CSVs.
- When merging additional research or market data, update the appropriate CSVs and reference them in your spec (use `EXTERNAL_RESEARCH_ENHANCEMENT_FRAMEWORK.md` as a guide).
- For any visual or UI components (React), refer to the `code_refs` JS files and adapt them to your needs.

With this package, your environment will be aligned with the current GitHub repository and ready to run the entire MeUnique research pipeline.  Enjoy building your Virtual Mall!
