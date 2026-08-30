# Canonical Tags File Guide

## Purpose and Division of Responsibility

This guide governs generation of `03-tags.yaml`. The supporting files and validator have distinct responsibilities:

- `speech-schema.yaml` defines the shape of the data.
- `vocabulary.yaml` supplies the allowed canonical tags.
- `tagging-guide.md` defines how those tags are interpreted.
- `tags-guide.md` explains how to construct a canonical tags file.
- `validate-tags.py` mechanically enforces corpus requirements.

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

The tag values in this example are illustrative only. They do not replace or independently define the canonical vocabulary.

## Speech-Level Rules

Only canonical vocabulary may appear in `03-tags.yaml`. Candidate concepts belong in `review/candidate-tags.yaml`.

The `speech_level` mapping contains `purposes`, `themes`, and `tone`. Purposes are divided into `primary` and `secondary`:

- `purposes.primary` must contain at least one tag. Prefer no more than four. These are the central reasons the speech exists.
- `purposes.secondary` contains meaningful supporting purposes that are not central reasons for the speech.
- A purpose must not appear in both primary and secondary.

No tag may be duplicated within an individual speech-level collection. For example, two `freedom` entries within `themes`, or two `inspire` entries within `purposes.primary`, are invalid even if their rationales differ.

Every speech-level tag entry requires:

- `tag`;
- a non-empty `rationale`;
- `confidence`, with a value of `high`, `medium`, or `low`.

Themes identify substantive recurring ideas, not every topic mentioned. Tone tags should be applied conservatively and supported across meaningful portions of the speech.

## Passage Annotation Rules

Every passage annotation requires:

- `id`;
- `category`;
- `tag`;
- `section`;
- `paragraphs`;
- `evidence`;
- `rationale`;
- `confidence`.

The only allowed annotation categories are `rhetorical_devices` and `writing_patterns`.

Apply these rules:

1. Annotation IDs must be unique and stable.
2. Annotation IDs do not need to be sequential; gaps are explicitly allowed. For example, `a007`, `a008`, `a010`, and `a011` may coexist after `a009` is removed.
3. Do not renumber existing annotations merely to restore a numerical sequence. Deleting one annotation must not change the identity of unrelated annotations.
4. For a new annotation, normally use an unused identifier above the highest existing ID rather than filling a historical gap. If the existing IDs are `a001`, `a002`, and `a004`, the next annotation should normally be `a005`, not `a003`.
5. The annotation category must match the canonical tag category in `schema/vocabulary.yaml`.
6. `section` must reference an existing rhetorical section.
7. Every paragraph reference must exist in the transcript and belong to the referenced section.
8. Paragraph evidence must relate to the referenced paragraph or paragraphs.
9. `evidence` must be a non-empty textual excerpt or concise evidence string.
10. `rationale` must be non-empty and explain why the annotation applies.
11. `confidence` must be `high`, `medium`, or `low`.
12. Prefer representative, defensible annotations rather than exhaustive tagging.
13. Do not create annotations merely because a device or pattern could technically be detected.
14. Do not use pending candidates as canonical annotations.

## Identifier Distinction

Section IDs and annotation IDs serve different purposes:

- Section IDs represent ordered structural position and are normally sequential: `s01`, `s02`, `s03`, and so on.
- Annotation IDs represent stable annotation identity. They require uniqueness, not sequence, and gaps are allowed.

This distinction preserves section order while preventing unrelated annotations from changing identity when one annotation is removed.

## Candidate Taxonomy Rule

If tagging reveals an important concept not adequately covered by the vocabulary:

1. do not invent it inside `03-tags.yaml`;
2. add a pending record to `review/candidate-tags.yaml`;
3. preserve existing canonical data;
4. leave approval, rejection, or merger to human review;
5. require an explicit vocabulary migration before using an approved addition canonically.

## Consistency Checklist

Before completing a tags file, verify that:

- all required top-level and nested fields are present;
- purpose placement and speech-level collections contain no duplicates;
- every tag is canonical for its category;
- annotation IDs are unique and existing IDs remain stable;
- section and paragraph references resolve to canonical records;
- evidence and rationales are relevant and non-empty;
- confidence values are valid;
- no pending candidate appears as canonical data.
