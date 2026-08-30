# Speech Analysis Guide

Analysis Template Version: 1.0.0

## Purpose and Authority

Each `04-analysis.md` file is derived, human-readable material intended for study, comparison, and teaching. It is generated from the validated rhetorical sections in `02-structure.yaml` and the validated tags in `03-tags.yaml`, with the transcript supplying textual evidence.

The analysis is not the canonical tagging source. Canonical structured data remains the source of truth. If prose in an analysis conflicts with the structure or tag files, the structured data governs and the analysis should be regenerated.

## Required Front Matter

Every analysis begins with:

```yaml
---
speech_id: <speech id>
derived_from_schema_version: <schema version>
derived_from_vocabulary_version: <vocabulary version>
analysis_template_version: 1.0.0
---
```

The derived version fields record the canonical data used to generate the document. They are provenance, not independent version declarations.

## Fixed H2 Structure

Every analysis must use exactly these H2 headings, in this order:

1. `## 1. Speech at a Glance`
2. `## 2. Rhetorical Structure`
3. `## 3. Rhetorical Progression`
4. `## 4. Rhetorical Devices`
5. `## 5. Reusable Writing Patterns`
6. `## 6. Speech-Specific Analysis`
7. `## 7. Climax and Closing`
8. `## 8. Speechwriting Blueprint`
9. `## 9. Questions for Study`
10. `## 10. Taxonomy Notes`

Do not add, remove, rename, or reorder H2 sections. Material unique to a speech belongs under one to four H3 subsections within Section 6. Do not create an H3 merely to fill space.

## Section Requirements

### 1. Speech at a Glance

Cover the validated primary purposes, secondary purposes, themes, and tone. Briefly explain why primary purposes define the central reason the speech exists while secondary purposes support that work. End with a concise architecture summary.

### 2. Rhetorical Structure

Cover every validated section without changing segmentation. For each section, provide a human-readable title, paragraph range, canonical section functions, rhetorical job, and connection to the surrounding sections.

### 3. Rhetorical Progression

Describe the speech's beginning-to-end movement in analytical prose. The progression should be specific to the speech and should not be presented as a sequence of canonical tags unless those classifications are explicitly validated.

### 4. Rhetorical Devices

Use only rhetorical-device annotations present in `03-tags.yaml`. For each representative annotation, provide the canonical tag, paragraph location, brief evidence, effect, and explanation of why the placement matters.

### 5. Reusable Writing Patterns

Use only validated canonical writing-pattern annotations. Explain each pattern in plain English, locate it, explain why it works, and derive a cautious speechwriting principle. Pending candidates may be identified as noncanonical review concepts but must not be presented as validated patterns.

### 6. Speech-Specific Analysis

Use one to four H3 subsections for distinctive material that deserves greater depth. This flexible section preserves speech-specific insight without altering the shared document skeleton.

### 7. Climax and Closing

Identify what functions as the climax and explain how the speech closes. If the climax and closing coincide, explain why; if they differ, explain the distinction. Ground the analysis in validated section functions, writing patterns, and devices rather than assuming that the most famous or final line is automatically the climax.

### 8. Speechwriting Blueprint

Extract a concise numbered sequence from the speech. State clearly that the blueprint is derived from this speech and is not a universal formula.

### 9. Questions for Study

Provide approximately eight to twelve close-reading questions covering structure, purposes, audience, stakes, devices, writing patterns, climax and closing, and the speech's distinctive rhetorical work.

### 10. Taxonomy Notes

Record which existing taxonomy concepts were especially useful, where vocabulary felt stretched, and which relevant pending candidates already appear in `review/candidate-tags.yaml`. State whether any new candidate appears necessary. This section records analytical observations; it does not create, approve, or modify vocabulary.

## Formatting Convention

In analysis files, canonical taxonomy terms use Markdown code formatting, such as `inspire`, `console`, `antithesis`, and `build_to_climax`. Ordinary analytical concepts remain normal prose. Bold may provide ordinary emphasis, but it is not the convention for canonical tags. Paragraph and section IDs normally remain plain text.

Candidate names must remain visibly noncanonical. Do not format a pending candidate in a way that implies canonical status.

## Grounding Rules

1. Treat `02-structure.yaml` and `03-tags.yaml` as the canonical analytical sources.
2. Use the transcript for textual evidence.
3. Do not invent canonical classifications absent from the validated tags.
4. Higher-level observations are permitted in ordinary prose when clearly distinguished from taxonomy.
5. Keep pending candidates visibly noncanonical.
6. Do not claim universality from a single speech.
7. Prefer analytical precision and representative examples over exhaustive commentary.

## Consistency Checklist

Before completion, verify that:

- the front matter contains all four required fields;
- the ten H2 headings match this guide exactly and appear in order;
- speech-specific H3 subsections occur only in Section 6;
- section and paragraph references match the canonical files;
- every device and writing-pattern classification is validated;
- canonical taxonomy terms use code formatting consistently;
- pending candidates are not presented as canonical;
- no canonical corpus data was changed while regenerating the analysis.
