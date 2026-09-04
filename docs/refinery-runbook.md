---
date: 2026-09-04
version: 0.2.3
---

# Speech Refinery Runbook

## Purpose and authority

This runbook, `docs/refinery-runbook.md`, is the human-facing operating guide and source of truth for the Speech Refinery workflow.

`docs/refinery-workflow.mmd` will later be generated from this runbook as a visual representation. The generated Mermaid file is not the source of truth and is not created as part of this runbook.

## Scope

This runbook currently covers:

1. Ingestion Track
2. Evolution Track
3. Migration Track

## Operating sequence

For the Ingestion Track, complete the stages in order. Each stage creates the artifact used by the stages that follow it, and each ends with its specified gate, human review, and Git commit checkpoint.

The Evolution Track begins only when ingestion work, validation, or human review identifies a possible framework change.

The Migration Track begins only when a human decides to apply accumulated accepted Evolution Track changes to existing speech artifacts.

## Execution agent

The refinery agent is the tool or platform used to execute a stage. It may be Codex, ChatGPT Work, Claude Code, Cursor, a local script, or another compatible execution environment.

The runbook defines the required workflow and inputs. It does not depend on a specific execution platform.

## Ingestion Track

### Canonical ingestion prompt discipline

Direct prompts for Ingestion Track stages must use the canonical thin launcher templates in `prompts/ingestion/`. ChatGPT, a human, or any execution platform must not compose a Rendered Prompt from scratch. Instead:

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

### 1. Transcript

#### Purpose

Create the transcript artifact `01-transcript.md` from Source A by following the Transcript-stage inputs and flow.

#### Launcher

1. Select `prompts/ingestion/transcript.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

#### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/transcript-guide.md`
- Source A, referenced by `source` in the Rendered Prompt

#### Preflight

Run `tools/transcript-preflight.py` (future).

#### Execution

Create `01-transcript.md`.

#### Validation

Run `tools/validate-transcript.py` (future).

#### Human Review

Human review follows validation.

#### Git Commit

Git commit follows human review, closes the Transcript stage, and proceeds to the Structure launcher.

### 2. Structure

#### Purpose

Create the structure artifact `02-structure.yaml` using the transcript and the Structure-stage schema and guidance.

#### Launcher

1. Select `prompts/ingestion/structure.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

#### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/structure-guide.md`
- `schema/speech-schema.yaml`
- `speeches/{{speech-id}}/01-transcript.md`

#### Preflight

Run `tools/structure-preflight.py` (future).

#### Execution

Create `02-structure.yaml`.

#### Validation

Run `tools/validate-structure.py` (future).

#### Human Review

Human review follows validation.

#### Git Commit

Git commit follows human review, closes the Structure stage, and proceeds to the Tags launcher.

### 3. Tags

#### Purpose

Create the tags artifact `03-tags.yaml` using the transcript, structure, schema, vocabulary, and tagging guidance.

#### Launcher

1. Select `prompts/ingestion/tags.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

#### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/tags-guide.md`
- `schema/tagging-guide.md`
- `schema/speech-schema.yaml`
- `schema/vocabulary.yaml`
- `speeches/{{speech-id}}/01-transcript.md`
- `speeches/{{speech-id}}/02-structure.yaml`

#### Preflight

Run `tools/tags-preflight.py` (future).

#### Execution

Create `03-tags.yaml`.

#### Validation

1. Run `tools/validate-tags.py`.
2. Run `pytest`.

#### Human Review

Human review follows `validate-tags.py` and `pytest`.

#### Git Commit

Git commit follows human review, closes the Tags stage, and proceeds to the Analysis launcher.

### 4. Analysis

#### Purpose

Create the analysis artifact `04-analysis.md` using the transcript, structure, tags, schema, vocabulary, and Analysis-stage guidance.

#### Launcher

1. Select `prompts/ingestion/analysis.md`.
2. Fill its permitted run-specific values.
3. Produce the Rendered Prompt and pass it to the refinery agent.

#### Required Inputs

The following are required inputs to this stage. They are provided together, and their listing order does not imply workflow sequence.

- Rendered Prompt
- `skills/speech-refinery/SKILL.md` (not written yet)
- `schema/analysis-guide.md`
- `schema/speech-schema.yaml`
- `schema/vocabulary.yaml`
- `speeches/{{speech-id}}/01-transcript.md`
- `speeches/{{speech-id}}/02-structure.yaml`
- `speeches/{{speech-id}}/03-tags.yaml`

#### Preflight

Run `tools/analysis-preflight.py` (future).

#### Execution

Create `04-analysis.md`.

#### Validation

Run `tools/validate-analysis.py` (future).

#### Human Review

Human review follows validation.

#### Git Commit

Git commit follows human review and closes the Analysis stage.

## Evolution Track

### 1. Trigger

A possible framework change is discovered during ingestion, validation, or human review.

Triggers include possible changes to:

- vocabulary
- schema
- guides
- validators/tests
- prompt templates
- refinery skill/workflow rules
- runbook/workflow diagram


### 2. Record candidate change

Record the proposed change before accepting it.

Use:

- `review/candidate-tags.yaml` — for candidate vocabulary/tag changes
- `review/evolution-candidates.yaml` (future) — for broader framework changes when the corpus becomes larger

The candidate record should include:

- proposed change
- reason current framework is insufficient
- affected framework files
- status: pending_review / approved / rejected / deferred / revised


### 3. Classify change type

Classify the proposal as one or more of:

- vocabulary change
- schema change
- guide change
- validator/test change
- prompt template change
- skill/workflow rule change
- runbook/workflow diagram change


### 4. Review impact

Check affected framework files, as relevant:

- `schema/vocabulary.yaml`
- `schema/tagging-guide.md`
- `schema/speech-schema.yaml`
- `schema/transcript-guide.md`
- `schema/structure-guide.md`
- `schema/tags-guide.md`
- `schema/analysis-guide.md`
- `tools/validate-tags.py`
- `tests/test_validate_tags.py`
- `prompts/ingestion/*.md`
- `docs/refinery-runbook.md`
- `docs/refinery-workflow.mmd`
- `skills/speech-refinery/SKILL.md` (not written yet)


### 5. Human decision gate

Human decides whether to:

- accept
- reject
- defer
- revise

Update the candidate record if one is used.


### 6. Update authoritative framework artifact first

Change the highest-authority file before dependent files.

Examples:

- vocabulary change → `schema/vocabulary.yaml`
- tagging semantics change → `schema/tagging-guide.md`
- schema change → `schema/speech-schema.yaml`
- transcript rules change → `schema/transcript-guide.md`
- structure rules change → `schema/structure-guide.md`
- tags-stage rules change → `schema/tags-guide.md`
- analysis rules change → `schema/analysis-guide.md`
- validator rule change → `tools/validate-tags.py`
- test expectation change → `tests/test_validate_tags.py`
- prompt template change → `prompts/ingestion/*.md`
- workflow rule change → `docs/refinery-runbook.md`
- skill/orchestration rule change → `skills/speech-refinery/SKILL.md` (not written yet)


### 7. Update dependent framework artifacts

Update any framework files that must stay consistent with the authoritative change.

May include:

- guides
- schema
- vocabulary
- validators
- tests
- prompt templates
- runbook
- generated workflow diagram
- refinery skill

Do **not** update existing speech artifacts here. Existing speech artifacts belong to the Migration Track.


### 8. Regenerate derived files if needed

If `docs/refinery-runbook.md` changes, regenerate:

- `docs/refinery-workflow.mmd`

Rule:

- `docs/refinery-runbook.md` = source of truth
- `docs/refinery-workflow.mmd` = derived visual


### 9. Run validation

Run relevant checks:

- `tools/validate-tags.py`
- `tests/test_validate_tags.py`
- `pytest`

Future checks:

- `tools/validate-transcript.py` (future)
- `tools/validate-structure.py` (future)
- `tools/validate-analysis.py` (future)
- `tools/transcript-preflight.py` (future)
- `tools/structure-preflight.py` (future)
- `tools/tags-preflight.py` (future)
- `tools/analysis-preflight.py` (future)


### 10. Human review

Confirm the framework change is correct and does not introduce drift.

Update the candidate record if one is used.


### 11. Git commit

Commit the accepted framework change.

```bash
git status
git diff --check
git add <changed-framework-files>
git commit -m "Describe framework change"
git push
```

### 12. Return to ingestion or queue migration

After the framework change:

- If no existing speech artifacts are affected → return to the Ingestion Track.
- If existing speech artifacts may need updating → queue them for a future Migration Track batch.

## Migration Track

### 1. Trigger

Migration begins when a human decides to apply accumulated accepted Evolution Track changes to existing speech artifacts.

Triggers include accepted framework changes to:

- vocabulary
- schema
- tagging rules
- structure rules
- analysis rules
- validator behavior
- workflow rules that affect existing artifacts

Migration must not begin from an unapproved framework change.

### 2. Identify affected speech artifacts

Identify which existing speech artifacts may need updates.

Affected files may include:

- `speeches/{{speech-id}}/01-transcript.md`
- `speeches/{{speech-id}}/02-structure.yaml`
- `speeches/{{speech-id}}/03-tags.yaml`
- `speeches/{{speech-id}}/04-analysis.md`

### 3. Create migration plan

Record the migration scope before editing existing speech artifacts.

The migration plan should include:

- accepted framework change
- affected speech IDs
- affected artifact types
- intended edits
- validation commands
- review criteria

Use:

- `review/migration-plan.yaml` (future) — for larger corpus migrations

For now, the migration plan may be recorded in the migration prompt or commit notes.

### 4. Human decision gate

Human decides whether to:

- proceed
- defer
- narrow scope
- reject migration need

Do not proceed unless the migration scope is clear.

### 5. Update existing speech artifacts

Update only the existing speech artifacts affected by the accepted framework change.

Important rule:

Do **not** change schema, vocabulary, guides, validators, prompt templates, skills, runbooks, or workflow diagrams here. Those belong to the Evolution Track.

If migration reveals that the framework still needs to change, stop migration and return to the Evolution Track.

### 6. Run validation

Run relevant checks:

- `tools/validate-tags.py`
- `tests/test_validate_tags.py`
- `pytest`

Future checks:

- `tools/validate-transcript.py` (future)
- `tools/validate-structure.py` (future)
- `tools/validate-analysis.py` (future)

### 7. Human review

Confirm migrated artifacts are correct and remain faithful to the original speech.

Review should check:

- no framework drift
- no invented tags
- no accidental meaning changes
- no broken references
- no over-broad migration
- no unrelated edits

### 8. Git commit

Commit migration changes separately from framework changes.

```bash
git status
git diff --check
git add speeches/
git commit -m "Migrate speech artifacts for accepted framework change"
git push
```

### 9. Return to ingestion

After migration is complete, return to the Ingestion Track or normal corpus work.