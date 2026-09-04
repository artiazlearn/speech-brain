---
date: 2026-09-04
version: 0.2.1
---

# Speech Refinery Runbook

## Purpose and authority

This runbook, `docs/refinery-runbook.md`, is the human-facing operating guide and source of truth for the Speech Refinery Ingestion Track.

`docs/refinery-workflow.mmd` will later be generated from this runbook as a visual representation. The generated Mermaid file is not the source of truth and is not created as part of this runbook.

## Scope

This runbook covers only the four Ingestion stages, in this order:

1. Transcript
2. Structure
3. Tags
4. Analysis

It does not define Evolution Track rules, Migration Track rules, or any workflow beyond the locked Ingestion Track design.

## Operating sequence

Complete the stages in order. Each stage creates the artifact used by the stages that follow it, and each ends with its specified gate, human review, and Git commit checkpoint.

## Execution agent

The refinery agent is the tool or platform used to execute a stage. It may be Codex, ChatGPT Work, Claude Code, Cursor, a local script, or another compatible execution environment.

The runbook defines the required workflow and inputs. It does not depend on a specific execution platform.

## Canonical prompt discipline

Direct prompts for the Ingestion stages must use the canonical thin launcher templates for the refinery agent. ChatGPT, a human, or any execution platform must not compose a Rendered Prompt from scratch. Instead:

1. Select the canonical template for the stage from `prompts/ingestion/`.
2. Fill only its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

Responsibility is divided among authoritative repository artifacts:

- `prompts/ingestion/*.md` contains the canonical launcher templates and controls what direct prompts may contain.
- `skills/speech-refinery/SKILL.md` contains refinery workflow and orchestration rules. It is not written yet.
- The stage guides contain stage-specific artifact rules and judgment.
- `schema/speech-schema.yaml` defines canonical data shape.
- `schema/vocabulary.yaml` supplies the allowed taxonomy.
- Validators provide deterministic enforcement.

A direct stage prompt may contain only run-specific information: the stage, `speech_id`, source or input paths, target output path, genuine speech-specific cautions, and stop condition. Not every stage requires every field.

Direct prompts must not redefine or duplicate reusable rules such as paragraph-ID conventions, transcript metadata requirements, source-faithfulness rules, segmentation rules, schema fields or types, taxonomy inventories, tagging semantics, analysis-template rules, validator rules, overall workflow sequencing, Git workflow, or Evolution or Migration rules. Those rules belong in the appropriate authoritative repository artifact.

Every launcher applies this conflict guardrail:

> Follow the refinery skill and stage-specific authoritative files. Do not treat this prompt as permission to redefine, supplement, or override reusable framework rules. If this prompt conflicts with an authoritative repository instruction, report the conflict instead of silently resolving it.

`speech_specific_cautions` may be `None`. When present, it may contain only information genuinely specific to the speech or source; it must not be an escape hatch for reusable framework instructions. Do not add a general additional-instructions or requirements mechanism.

## 1. Transcript

### Purpose

Create the transcript artifact `01-transcript.md` from Source A by following the Transcript-stage inputs and flow.

### Launcher

1. Select `prompts/ingestion/transcript.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/transcript-guide.md`
- Source A, referenced by `source` in the Rendered Prompt

### Preflight

Run `tools/transcript-preflight.py` (future).

### Execution

Create `01-transcript.md`.

### Validation

Run `tools/validate-transcript.py` (future).

### Human Review

Human review follows validation.

### Git Commit

Git commit follows human review, closes the Transcript stage, and proceeds to the Structure launcher.

## 2. Structure

### Purpose

Create the structure artifact `02-structure.yaml` using the transcript and the Structure-stage schema and guidance.

### Launcher

1. Select `prompts/ingestion/structure.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/structure-guide.md`
- `schema/speech-schema.yaml`
- `speeches/{{speech-id}}/01-transcript.md`

### Preflight

Run `tools/structure-preflight.py` (future).

### Execution

Create `02-structure.yaml`.

### Validation

Run `tools/validate-structure.py` (future).

### Human Review

Human review follows validation.

### Git Commit

Git commit follows human review, closes the Structure stage, and proceeds to the Tags launcher.

## 3. Tags

### Purpose

Create the tags artifact `03-tags.yaml` using the transcript, structure, schema, vocabulary, and tagging guidance.

### Launcher

1. Select `prompts/ingestion/tags.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/tags-guide.md`
- `schema/tagging-guide.md`
- `schema/speech-schema.yaml`
- `schema/vocabulary.yaml`
- `speeches/{{speech-id}}/01-transcript.md`
- `speeches/{{speech-id}}/02-structure.yaml`

### Preflight

Run `tools/tags-preflight.py` (future).

### Execution

Create `03-tags.yaml`.

### Validation

1. Run `tools/validate-tags.py`.
2. Run `pytest`.

### Human Review

Human review follows `validate-tags.py` and `pytest`.

### Git Commit

Git commit follows human review, closes the Tags stage, and proceeds to the Analysis launcher.

## 4. Analysis

### Purpose

Create the analysis artifact `04-analysis.md` using the transcript, structure, tags, schema, vocabulary, and Analysis-stage guidance.

### Launcher

1. Select `prompts/ingestion/analysis.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/analysis-guide.md`
- `schema/speech-schema.yaml`
- `schema/vocabulary.yaml`
- `speeches/{{speech-id}}/01-transcript.md`
- `speeches/{{speech-id}}/02-structure.yaml`
- `speeches/{{speech-id}}/03-tags.yaml`

### Preflight

Run `tools/analysis-preflight.py` (future).

### Execution

Create `04-analysis.md`.

### Validation

Run `tools/validate-analysis.py` (future).

### Human Review

Human review follows validation.

### Git Commit

Git commit follows human review and closes the Analysis stage.
