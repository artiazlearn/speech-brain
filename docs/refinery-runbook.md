---
date: 2026-09-02
version: 0.1
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

## Status notation

The status descriptions below reproduce the design document's status information; they are not an independent inventory of the repository.

| Status | Meaning |
|---|---|
| No future label | The design does not mark the item as future. |
| Not written yet | The design explicitly says the file is not written yet. |
| `(future)` | The design explicitly marks the tool as `(future)`. |

## Operating sequence

Complete the stages in order. Each stage creates the artifact used by the stages that follow it, and each ends with its specified gate, human review, and Git commit checkpoint.

## 1. Transcript

### Purpose

Create the transcript artifact, `01-transcript.md`, from Source A by following the Transcript-stage inputs and flow.

### Codex inputs

| Input | Design status |
|---|---|
| Source A | No future label |
| `schema/speech-refinery-skill.md` | Not written yet |
| `schema/transcript-guide.md` | No future label |
| `tools/transcript-preflight.py` | `(future)` |
| `tools/validate-transcript.py` | `(future)` |

### Ordered flow

1. Start with `Prompt X1`.
2. Use `speech-refinery-skill.md`.
3. Use `transcript-guide.md`.
4. Use Source A.
5. Run `transcript-preflight.py` `(future)`.
6. Create `01-transcript.md`.
7. Run `validate-transcript.py` `(future)`.
8. Conduct human review.
9. Create the Git commit checkpoint.

### Artifact created

`01-transcript.md`

### Validation and gate

Run `transcript-preflight.py` `(future)` before creating the artifact. Run `validate-transcript.py` `(future)` after creating it.

### Human review

Human review follows validation.

### Git commit checkpoint

Git commit follows human review and closes the Transcript stage.

## 2. Structure

### Purpose

Create the structured speech artifact, `02-structure.yaml`, using the transcript and the Structure-stage schema and guidance.

### Codex inputs

| Input | Design status |
|---|---|
| `schema/speech-refinery-skill.md` | Not written yet |
| `schema/structure-guide.md` | No future label |
| `schema/speech-schema.yaml` | No future label |
| `speeches/{{speech-id}}/01-transcript.md` | No future label |
| `tools/structure-preflight.py` | `(future)` |
| `tools/validate-structure.py` | `(future)` |

### Ordered flow

1. Start with `Prompt X2`.
2. Use `speech-refinery-skill.md`.
3. Use `structure-guide.md`.
4. Use `speech-schema.yaml` and `01-transcript.md` as parallel inputs, then converge them into the next step.
5. Run `structure-preflight.py` `(future)`.
6. Create `02-structure.yaml`.
7. Run `validate-structure.py` `(future)`.
8. Conduct human review.
9. Create the Git commit checkpoint.

### Artifact created

`02-structure.yaml`

### Validation and gate

Run `structure-preflight.py` `(future)` before creating the artifact. Run `validate-structure.py` `(future)` after creating it.

### Human review

Human review follows validation.

### Git commit checkpoint

Git commit follows human review and closes the Structure stage.

## 3. Tags

### Purpose

Create the tags artifact, `03-tags.yaml`, using the transcript, structure, schema, vocabulary, and tagging guidance.

### Codex inputs

| Input | Design status |
|---|---|
| `schema/speech-refinery-skill.md` | Not written yet |
| `schema/tags-guide.md` | No future label |
| `schema/tagging-guide.md` | No future label |
| `schema/speech-schema.yaml` | No future label |
| `schema/vocabulary.yaml` | No future label |
| `speeches/{{speech-id}}/01-transcript.md` | No future label |
| `speeches/{{speech-id}}/02-structure.yaml` | No future label |
| `tools/tags-preflight.py` | `(future)` |
| `tools/validate-tags.py` | No future label |

### Ordered flow

1. Start with `Prompt X3`.
2. Use `speech-refinery-skill.md`.
3. Use `tags-guide.md`.
4. From `tags-guide.md`, proceed along parallel branches to `tagging-guide.md` and `speech-schema.yaml`.
5. From those branches, use `vocabulary.yaml`, `01-transcript.md`, and `02-structure.yaml`, then converge them into the next step.
6. Run `tags-preflight.py` `(future)`.
7. Create `03-tags.yaml`.
8. Run `validate-tags.py`.
9. Run `pytest`.
10. Conduct human review.
11. Create the Git commit checkpoint.

### Artifact created

`03-tags.yaml`

### Validation and gate

Run `tags-preflight.py` `(future)` before creating the artifact. After creating it, run `validate-tags.py`, then run `pytest`.

### Human review

Human review follows `validate-tags.py` and `pytest`.

### Git commit checkpoint

Git commit follows human review and closes the Tags stage.

## 4. Analysis

### Purpose

Create the analysis artifact, `04-analysis.md`, using the transcript, structure, tags, schema, vocabulary, and Analysis-stage guidance.

### Codex inputs

| Input | Design status |
|---|---|
| `schema/speech-refinery-skill.md` | Not written yet |
| `schema/analysis-guide.md` | No future label |
| `schema/speech-schema.yaml` | No future label |
| `schema/vocabulary.yaml` | No future label |
| `speeches/{{speech-id}}/01-transcript.md` | No future label |
| `speeches/{{speech-id}}/02-structure.yaml` | No future label |
| `speeches/{{speech-id}}/03-tags.yaml` | No future label |
| `tools/analysis-preflight.py` | `(future)` |
| `tools/validate-analysis.py` | `(future)` |

### Ordered flow

1. Start with `Prompt X4`.
2. Use `speech-refinery-skill.md`.
3. Use `analysis-guide.md`.
4. Use `speech-schema.yaml` and `vocabulary.yaml` as parallel inputs.
5. Use 01-transcript.md, 02-structure.yaml, and 03-tags.yaml together as canonical inputs to the analysis stage.
6. Run `analysis-preflight.py` `(future)`.
7. Create `04-analysis.md`.
8. Run `validate-analysis.py` `(future)`.
9. Conduct human review.
10. Create the Git commit checkpoint.

### Artifact created

`04-analysis.md`

### Validation and gate

Run `analysis-preflight.py` `(future)` before creating the artifact. Run `validate-analysis.py` `(future)` after creating it.

### Human review

Human review follows validation.

### Git commit checkpoint

Git commit follows human review and closes the Analysis stage.
