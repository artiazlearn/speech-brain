# Canonical Tags File Guide

## Purpose and Division of Responsibility

This guide explains the tagging judgment used to create `03-tags.yaml`. Supporting files have distinct responsibilities:

- `schema/speech-schema.yaml` defines the canonical data shape.
- `schema/vocabulary.yaml` supplies the allowed canonical tags.
- `schema/tagging-guide.md` defines how those tags are interpreted.
- `schema/tags-guide.md` explains how to apply that shape and taxonomy in a canonical tags file.

The current authoritative tag list is always `schema/vocabulary.yaml`.

## Standard Tags File

```yaml
speech_id: example-speech
schema_version: 0.2.0
vocabulary_version: 0.3.0

speech_level:
  purposes:
    primary:
      - tag: inspire
        rationale: >
          Explain why this is central to why the speech exists.
        confidence: high

    secondary:
      - tag: warn
        rationale: >
          Explain why this meaningfully supports the speech without
          being one of its central purposes.
        confidence: high

  themes:
    - tag: freedom
      rationale: >
        Explain why the theme is substantively developed.
      confidence: high

  tone:
    - tag: resolute
      rationale: >
        Explain why the tone applies across meaningful portions of the
        speech.
      confidence: high

passage_annotations:
  - id: a001
    category: rhetorical_devices
    tag: antithesis
    section: s01
    paragraphs:
      - p001
    evidence: "short textual evidence"
    rationale: >
      Explain why the canonical annotation applies.
    confidence: high
```

The file shape and tag values in this example are illustrative. Use `schema/speech-schema.yaml` for structural requirements; the example does not prescribe tag combinations or collection sizes.

## Speech-Level Rules

Only canonical vocabulary may appear in `03-tags.yaml`. Unresolved taxonomy gaps belong outside the canonical artifact.

Speech-level tags describe the speech as a whole or qualities developed across a substantial part of it:

- `purposes` describe intended audience outcomes. Primary purposes are central reasons the speech exists; secondary purposes meaningfully support the speech without being central. Apply the detailed tests in `schema/tagging-guide.md`.
- `themes` identify subjects or ideas developed with meaningful emphasis, not every topic mentioned.
- `tone` identifies sustained qualities of attitude or emotional character, not an isolated sentence's mood.

The schema requires at least one primary purpose. Beyond schema requirements, there is no fixed or target number of purposes, themes, or tones. Select only tags supported by the speech:

- a purpose must not appear in both primary and secondary;
- a tag must not be duplicated within the same speech-level collection.

For every speech-level tag, write a rationale that explains how the classification is supported at speech level. A separate `evidence` field is not part of a speech-level entry. Confidence records certainty that the classification fits, not the tag's importance or rhetorical strength.

## Passage Annotation Rules

Passage annotations record specific, localized observations. The `rhetorical_devices` category identifies language-level techniques; the `writing_patterns` category identifies compositional strategies operating across a passage. Use `schema/tagging-guide.md` for the detailed distinctions.

Create a passage annotation only for a meaningful, defensible observation. Do not annotate every possible occurrence, and do not require every paragraph or section to have an annotation. More than one annotation may cite the same passage when the evidence independently supports each classification.

Apply these rules:

1. Annotation IDs must be unique and stable.
2. Annotation IDs represent identity rather than document order; they need not be sequential, and gaps are valid.
3. The annotation category and tag must correspond to the same category in `schema/vocabulary.yaml`.
4. `section` must reference an existing rhetorical section.
5. Every paragraph reference must exist in the transcript and belong to the referenced section.
6. Evidence must be a concise, faithful textual excerpt or evidence string related to the referenced paragraphs.
7. The rationale must explain why the assigned tag fits the cited evidence rather than merely repeat the tag or excerpt.
8. Confidence must express certainty in the classification, not the observation's importance or rhetorical strength.
9. Candidate or unresolved taxonomy terms must not appear as canonical annotations.

## Taxonomy Boundary

Canonical tags must come from the current `schema/vocabulary.yaml`. Taxonomy proposals, review, and migration are outside the canonical `03-tags.yaml` artifact and outside this guide.

## Conformance Checklist

A conforming tags file:

- follows the canonical shape in `schema/speech-schema.yaml`;
- assigns canonical tags to the correct collections and categories;
- distinguishes primary from secondary purposes and contains no collection-level duplicates;
- uses unique, stable annotation IDs;
- resolves section and paragraph references to canonical records;
- provides relevant evidence and rationales;
- uses confidence to express classification certainty;
- contains no candidate or unresolved taxonomy terms.
