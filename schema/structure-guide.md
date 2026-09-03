# Rhetorical Structure Guide

## Purpose

This guide explains the rhetorical judgment used to create `02-structure.yaml`. The schema defines the canonical data shape; this guide explains how to decide what each group of paragraphs does within the speech.

Use `schema/speech-schema.yaml` for required fields, types, cardinalities, and identifier formats; `schema/vocabulary.yaml` for canonical section functions; and `schema/tagging-guide.md` for their meanings and distinctions.

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

The example illustrates the artifact shape; it does not prescribe a section count, section length, or function.

## Artifact Rules

Use `schema/speech-schema.yaml` as the canonical definition of the artifact shape. The following structure-stage invariants also apply:

1. Every transcript paragraph must appear in exactly one section.
2. Copy paragraph identifiers unchanged from `01-transcript.md` and list each identifier explicitly rather than using a range.
3. Within each section, paragraphs must be contiguous and remain in transcript order; the ordered sections must cover the transcript without gaps or overlaps.
4. Assign section IDs in section order, beginning with `s01` and incrementing sequentially: `s01`, `s02`, `s03`, and so on.
5. Functions must come only from `schema/vocabulary.yaml` under `section_functions`.
6. Do not place candidate taxonomy fields or concepts inside `02-structure.yaml`.
7. Structural analysis must not change transcript wording, paragraph IDs, paragraph order, or paragraph boundaries.

## Rhetorical Segmentation Judgment

Use no more sections than necessary to capture meaningful rhetorical or argumentative shifts. A section should unite contiguous paragraphs performing a common rhetorical job. There is no target section count or preferred section length: a section may contain one paragraph or many. Do not create one section per paragraph merely for convenience, divide the speech by equal lengths, or treat a topic change alone as sufficient when the rhetorical job continues.

No particular function is required in every speech. A famous or memorable passage is not automatically a `climax`; apply the distinction in `schema/tagging-guide.md` and consider whether the speech's rhetorical progression genuinely culminates there.

Assign only functions that describe the section's role as a unit. A section may have more than one function when each is defensible for the grouped passage.

Rationales should explain both why the paragraphs belong together and why the assigned functions describe their shared role. They should record section-specific analysis rather than merely restate function labels or quote large portions of the transcript.

## Vocabulary Boundary

Use only defensible canonical functions in `02-structure.yaml`. Candidate concepts and vocabulary-gap resolution do not belong in the canonical structure artifact.

## Conformance Checklist

A conforming structure file:

- follows the canonical shape in `schema/speech-schema.yaml`;
- covers every transcript paragraph exactly once and in order;
- uses contiguous section ranges and sequential section IDs;
- assigns only canonical, defensible functions;
- provides a substantive, non-empty rationale for every section;
- leaves transcript content and identifiers unchanged;
- contains no candidate concepts.
