# Speech Brain Revision Workflow

## Purpose

Use the Speech Brain corpus to improve a draft without blindly imitating famous speakers.

Speech Brain should help:

- diagnose rhetorical weaknesses;
- retrieve relevant corpus examples;
- extract transferable techniques;
- improve structure and rhetoric;
- preserve or transform the speaker’s voice according to the user’s goal.

The corpus is used for **technique transfer, not style imitation**.

---

# Revision Controls

The user controls three dimensions:

| Control                     | Governs                                                |
| --------------------------- | ------------------------------------------------------ |
| **Voice fidelity*-          | How much the speaker’s existing voice is preserved     |
| **Structural intervention*- | How aggressively ideas and sections may be reorganized |
| **Rhetorical intensity*-    | How strongly rhetorical techniques are applied         |

Revision scope is separate. It determines **what parts of the speech may be changed**.

## Voice Fidelity

**High**
Preserve vocabulary, informality, sentence habits, roughness, and personality.

**Medium**
Preserve the general voice while allowing noticeable improvement in phrasing and rhythm.

**Low**
Prioritize effectiveness even if the result sounds substantially more polished than the original.

## Structural Intervention

**Low**
Keep the existing architecture and repair obvious weaknesses only.

**Medium**
Allow restructuring of weak sections, transitions, and argument sequence.

**High**
Allow major reordering, combining, splitting, or rebuilding of sections.

## Rhetorical Intensity

**Low**
Prioritize clarity and naturalness.

**Medium**
Use selective contrast, repetition, parallelism, escalation, and audience activation.

**High**
Allow deliberate use of stronger devices such as anaphora, antithesis, tricolon, rhetorical questions, and climax.

---

# Revision Scope

Choose one:

- **Entire speech**
- **Selected section**
- **High-priority weaknesses only**

For normal editing, prefer high-priority weaknesses only.

---

# Corpus Roles

| Corpus layer           | Main use              |
| ---------------------- | --------------------- |
| Raw transcript         | Evidence and examples |
| Section functions      | Structural diagnosis  |
| Writing patterns       | Rhetorical strategy   |
| Rhetorical devices     | Rhetorical intensity  |
| Purpose / theme / tone | Secondary context     |

Current testing suggests that **section functions and writing patterns provide the strongest direct value for revision**.

---

# Workflow

```text
1. Set revision controls
        ↓
2. Preserve author intent
        ↓
3. Map the draft structure
        ↓
4. Diagnose weaknesses
        ↓
5. Retrieve analogous corpus passages
        ↓
6. Abstract the technique
        ↓
7. Choose a revision strategy
        ↓
8. Revise selected material
        ↓
9. Review the whole speech
```

---

# 1. Set Revision Controls

Record:

```text
Revision scope:
Voice fidelity:
Structural intervention:
Rhetorical intensity:
```

Example:

```text
Revision scope: High-priority weaknesses only
Voice fidelity: High
Structural intervention: Medium
Rhetorical intensity: Medium
```

---

# 2. Preserve Author Intent

Identify:

- audience;
- purpose;
- central argument;
- desired audience response;
- current voice;
- facts, examples, stories, or phrases that should be preserved.

Do not rewrite yet.

---

# 3. Map the Draft Structure

Divide the draft into rhetorical sections.

For each section identify:

- paragraph range;
- rhetorical function;
- main idea.

Use existing Speech Brain section functions where appropriate.

Do not force a section into an existing tag if none fits.

---

# 4. Diagnose Weaknesses

Ask:

1. What job is this section trying to perform?
2. Does it perform that job effectively?
3. Is an important function missing?
4. Is the sequence effective?
5. Is the problem structural or sentence-level?
6. Would fixing it materially improve the speech?

Prioritize only high-value problems.

---

# 5. Retrieve Analogous Corpus Passages

Retrieve a small number of passages performing a similar rhetorical job.

Prefer:

> **functional similarity**

over:

> topic similarity.

Useful retrieval dimensions:

- section function;
- writing pattern;
- rhetorical device;
- position within the speech.

---

# 6. Abstract the Technique

For each useful example identify:

```text
What the speaker does
        ↓
Why it works
        ↓
Transferable principle
        ↓
What should not be copied
```

Do not copy distinctive wording, historical phrasing, cadence, or speaker-specific voice.

---

# 7. Choose a Revision Strategy

Before rewriting, consider 2–3 possible rhetorical moves.

For each strategy ask:

- Why does it fit?
- Which corpus principle supports it?
- Does it match the requested voice fidelity?
- Does it match the requested rhetorical intensity?
- Is it appropriate for this genre?

Do not automatically choose the most dramatic technique.

---

# 8. Revise Selected Material

Revise according to the chosen controls.

A useful output format is:

```text
Original:

Revised:

What changed:

Why:

Corpus principle used:
```

For high voice fidelity, prefer the smallest useful change.

High structural intervention may still substantially reorganize the speech while preserving the speaker’s natural language.

---

# 9. Whole-Speech Review

## Structure

Check:

- clear purpose for each section;
- logical progression;
- unnecessary repetition;
- appropriate momentum;
- earned conclusion.

## Voice

Check whether the amount of voice change matches the selected setting.

Watch for:

- unnecessarily sophisticated vocabulary;
- overly uniform sentence rhythm;
- loss of personality;
- excessive polish.

## Rhetoric

Check whether devices:

- serve a purpose;
- match the requested intensity;
- fit the audience and genre;
- avoid making the speech feel over-written.

## Corpus Contamination

Check that techniques were transferred without making the speaker sound like a specific corpus speaker.

---

# Genre Appropriateness

A technique that works in a political speech may be inappropriate in a union update, product launch, weekly report, or company presentation.

Always distinguish between:

> **effective in the source speech**

and:

> **appropriate for the target speech.**

---

# Current Findings

Initial testing suggests:

**Section functions — KEEP**
Strong value for structural diagnosis and intervention.

**Writing patterns — KEEP**
Strong value for selecting rhetorical strategies.

**Rhetorical devices — KEEP, but use selectively**
Useful for intensity and memorability, but can cause over-polishing.

**Purpose / theme / tone — RETAIN**
Current revision value is less clear, but changing the existing tagging infrastructure is not justified.

---

# Scope Discipline

Keep this workflow lightweight.

Do not create new schemas, validators, scripts, benchmark systems, retrieval infrastructure, or skills unless repeated manual use proves they are necessary.

> **Every new piece of infrastructure must earn its maintenance cost.**

Prefer stable and good-enough over theoretically cleaner but substantially more complex.

---

# Current Objective

Continue testing Speech Brain on different rhetorical situations, especially more everyday genres such as:

- product launches;
- company updates;
- stakeholder reports;
- leadership communications;
- presentations;
- crisis announcements.

The goal is to determine whether Speech Brain can become a general speechwriting system rather than only a political-speech analysis system.
