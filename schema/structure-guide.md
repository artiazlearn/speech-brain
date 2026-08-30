# Rhetorical Structure Guide

## Purpose

This guide governs generation of `02-structure.yaml`. The schema defines the required data shape; rhetorical segmentation still requires judgment about what each group of paragraphs does within the speech.

Use `schema/speech-schema.yaml` for structural requirements, `schema/vocabulary.yaml` for canonical section functions, and `schema/tagging-guide.md` for their meanings and distinctions.

## Standard Structure File

```yaml
speech_id: example-speech
schema_version: 0.2.0
vocabulary_version: 0.3.0

sections:
  - id: s01
    paragraphs:
      - p001
      - p002
    functions:
      - opening
    rationale: >
      Explain why these paragraphs form one rhetorical unit and why the
      assigned canonical section functions fit.
```

## Schema Rules

Every structure file requires `speech_id`, `schema_version`, `vocabulary_version`, and `sections`. Every section requires:

- a section `id`;
- a non-empty ordered list of `paragraphs`;
- a non-empty list of canonical `functions`;
- a non-empty explanatory `rationale`.

The following invariants apply:

1. Every transcript paragraph must appear exactly once.
2. Paragraphs must remain in transcript order.
3. Sections must be contiguous.
4. Section IDs must be sequential and ordered: `s01`, `s02`, `s03`, and so on.
5. Every section must contain at least one paragraph.
6. Every section must contain at least one canonical section function.
7. Functions must come only from `schema/vocabulary.yaml` under `section_functions`.
8. Every rationale must be a non-empty explanatory string.
9. Do not place candidate taxonomy fields or concepts inside `02-structure.yaml`.
10. Do not change transcript wording, paragraph IDs, paragraph order, or paragraph boundaries during structural analysis.

## Rhetorical Segmentation Judgment

Use the smallest number of sections that captures meaningful rhetorical shifts. A section should unite contiguous paragraphs performing a common rhetorical job. Do not create one section per paragraph merely for convenience, and do not divide the speech solely by paragraph length or topic.

A famous or memorable passage is not automatically a `climax`. Apply the definition in `schema/tagging-guide.md` and consider whether the speech's rhetorical progression genuinely culminates there.

Rationales should explain both why the paragraphs belong together and why the assigned functions describe their shared role. They should record analysis rather than quote large portions of the transcript.

## Vocabulary Gaps and Candidate Concepts

Candidate taxonomy proposals belong in `review/candidate-tags.yaml`, never in canonical structure data. If the vocabulary does not adequately describe a section:

1. use only defensible canonical functions in `02-structure.yaml`;
2. report the vocabulary gap clearly;
3. quarantine the proposed concept in `review/candidate-tags.yaml` with pending-review status;
4. do not silently modify `schema/vocabulary.yaml`.

Human review, rather than structural analysis, determines whether a candidate is approved, rejected, or merged with an existing concept.

## Consistency Checklist

Before completing a structure file, verify that:

- all required top-level and section fields are present;
- every transcript paragraph is covered exactly once and in order;
- section ranges are contiguous and section IDs are sequential;
- all functions are canonical and defensible;
- all rationales are substantive and non-empty;
- no transcript content or identifiers changed;
- no candidate concept appears in the canonical structure file.
