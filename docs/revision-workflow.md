# Speech Brain Revision Workflow

## Purpose

Use the Speech Brain corpus to improve a first draft without replacing the writer’s voice with generic AI prose.

The workflow should use corpus annotations to identify rhetorical problems, retrieve relevant examples, extract transferable techniques, and apply those techniques to the writer’s own content.

The corpus is used for **analysis and technique transfer**, not imitation.

---

## Core Principle

Do not revise by copying the wording, cadence, or voice of speeches in the corpus.

Use this sequence:

```text
Draft
  ↓
Diagnose
  ↓
Retrieve
  ↓
Abstract
  ↓
Choose Strategy
  ↓
Revise
  ↓
Review
```

The desired result is:

> the writer’s ideas and voice, with stronger rhetorical structure

not:

> the writer’s ideas rewritten in the style of another speaker or generic AI

---

# Step 1 — Preserve Author Intent

Before revising, identify:

- audience
- purpose
- central argument
- desired audience response
- current voice
- important ideas, phrases, examples, or stories that should be preserved

Do not rewrite yet.

### Output

```text
Audience:
Purpose:
Central argument:
Desired audience response:
Current voice:
Must preserve:
```

---

# Step 2 — Map the Draft Structure

Divide the draft into rhetorical sections.

For each section, identify:

- paragraph range
- current rhetorical function
- main idea

Use existing Speech Brain section-function vocabulary where appropriate.

### Output

| Section | Paragraphs | Function | Main idea |
| ------- | ---------- | -------- | --------- |
| 1       |            |          |           |
| 2       |            |          |           |
| 3       |            |          |           |

Do not force every section into an existing tag if none fits well.

---

# Step 3 — Diagnose Weaknesses

Evaluate each section before making changes.

Ask:

1. What rhetorical job is this section trying to perform?
2. Does it perform that job effectively?
3. Is an important rhetorical function missing?
4. Is the sequence of functions effective?
5. Is the problem structural or sentence-level?

Possible problems include:

- weak opening
- unclear stakes
- excessive explanation
- missing transition
- weak escalation
- abrupt call to action
- repetitive argument
- conclusion that summarizes instead of culminates
- rhetorical device used without purpose

### Output

| Section | Function | Diagnosis | Priority            |
| ------- | -------- | --------- | ------------------- |
|         |          |           | High / Medium / Low |

Only high-value problems should proceed to corpus retrieval.

---

# Step 4 — Retrieve Analogous Corpus Passages

For each high-priority problem, retrieve passages that perform a similar rhetorical function.

Prefer functional similarity over topic similarity.

Useful retrieval dimensions include:

- section function
- writing pattern
- rhetorical device
- position within the speech

Example:

```text
Problem:
Weak transition into the call to action

Relevant corpus functions:
- shift_to_citizen_responsibility
- call_to_service

Relevant writing patterns:
- transfer_responsibility
- reciprocal_call
```

Retrieve a small number of strong examples rather than many loosely related examples.

---

# Step 5 — Abstract the Technique

For every retrieved example, identify:

```text
What the speaker does
        ↓
Why it works
        ↓
What principle is transferable
        ↓
What should not be copied
```

### Output Template

```text
Reference:
Corpus location:

Rhetorical move:

Mechanism:

Effect on audience:

Transferable principle:

Do not imitate:
- distinctive wording
- historical phrasing
- speaker-specific voice
- unnecessary stylistic mannerisms
```

The goal is to extract a reusable writing principle.

---

# Step 6 — Propose Revision Strategies

Before rewriting, generate 2–3 possible rhetorical strategies derived from the corpus analysis.

Do not immediately produce revised prose.

Example:

```text
Strategy A — Transfer Responsibility

external problem
→ audience choice
→ consequence
→ action
```

```text
Strategy B — Contrast Alternatives

future A
vs
future B
→ audience decides
```

Each strategy should explain:

- the rhetorical move
- why it fits the current speech
- which corpus principle inspired it
- any risks or trade-offs

The writer chooses the strategy.

---

# Step 7 — Revise the Target Section

Revise only the selected section.

Preserve:

- argument
- facts
- examples
- terminology
- personality
- level of formality
- writer-specific phrasing where possible

Change only what is necessary:

- rhetorical structure
- sequencing
- transitions
- emphasis
- sentence rhythm
- selected rhetorical devices

### Output

```text
Original:

Revised:

What changed:

Why:

Corpus principle used:
```

Avoid introducing rhetorical devices simply because they appear in the corpus.

Every device should serve a clear purpose.

---

# Step 8 — Whole-Speech Review

After targeted revisions, inspect the entire speech.

## Structure Check

Ask:

- Does every section have a clear purpose?
- Does the sequence of sections make sense?
- Is there unnecessary repetition?
- Does rhetorical pressure build?
- Does the conclusion feel earned?

## Voice Check

Ask:

- Does this still sound like the original writer?
- Did vocabulary become unnaturally polished?
- Were AI clichés introduced?
- Did sentence rhythms become too uniform?
- Were personal quirks unnecessarily removed?

## Corpus Contamination Check

Ask:

- Did any distinctive wording from the corpus leak into the revision?
- Does the writer suddenly sound like JFK, Churchill, Reagan, Thatcher, or another corpus speaker?
- Was a technique transferred, or was a style imitated?

If imitation occurred, revise again.

---

# Revision Philosophy

Speech Brain should behave primarily as a **speechwriting coach and analytical editor**, not a ghostwriter.

The corpus should help answer:

> What is this part of the speech trying to accomplish?

> Why is it not working well enough?

> How have strong speakers solved similar rhetorical problems?

> What underlying technique can be transferred?

> How can that technique strengthen this speech while preserving the writer’s voice?

The system should prefer **diagnosis and explanation before rewriting**.

---

# Scope for Version 0.1

This workflow is intentionally manual.

Do not add:

- new validators
- new schemas
- retrieval infrastructure
- automation scripts
- new skills
- prompt libraries

until the workflow has been tested on a real first draft.

The immediate objective is to determine whether the tagged Speech Brain corpus produces meaningfully better revisions than:

1. generic AI revision
2. raw-speech RAG revision
3. tagged-corpus revision

Only after this is demonstrated should the workflow be automated or expanded.
