# Speech Analysis Guide

Analysis Template Version: 1.0.0

## Purpose and Authority

Each `04-analysis.md` file is a derived, human-readable artifact intended for study, comparison, and teaching. Its canonical inputs are `01-transcript.md`, `02-structure.yaml`, and `03-tags.yaml`. The transcript governs wording, paragraph order, and textual evidence; the structure file governs section boundaries, paragraph membership, and section functions; and the tags file governs speech-level classifications and passage annotations.

The analysis synthesizes those inputs but does not create or alter canonical transcript, structure, or tag data. If analysis prose conflicts with a canonical input, the canonical input governs and the analysis must be corrected. Do not silently resolve the conflict by changing canonical meaning in prose. `04-analysis.md` is downstream of all three inputs and must not be used as an input to create or revise an earlier Ingestion artifact.

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

Follow the front matter with one descriptive H1 title for the speech and analysis.

## Required H2 Structure

Every analysis must use these H2 sections, in this order:

1. `## Speech at a Glance`
2. `## Rhetorical Structure`
3. `## Rhetorical Progression`
4. `## Rhetorical Devices`
5. `## Reusable Writing Patterns`
6. `## Speech-Specific Analysis`
7. `## Climax and Closing`
8. `## Speechwriting Blueprint`
9. `## Questions for Study`
10. `## Taxonomy Notes`

Use the unnumbered headings above for new or regenerated analyses. Earlier analyses using the same headings with numeric prefixes follow the same 1.0.0 semantic template; heading numbering alone does not define a different template version.

Do not add, remove, rename, or reorder the shared H2 sections. Material unique to a speech may appear under descriptively named H3 subsections within Speech-Specific Analysis. These H3 subsections are optional, and their names and number depend on the speech. Do not create one merely to fill space.

## Section Requirements

### 1. Speech at a Glance

Cover the validated primary purposes, secondary purposes, themes, and tone recorded in `03-tags.yaml`, without filling an empty collection by inference. Briefly explain how the primary purposes define the speech's central work and how any secondary purposes support it. End with a concise architecture summary grounded in the transcript and canonical structure.

### 2. Rhetorical Structure

Cover every canonical section in order without changing its segmentation, paragraph membership, or functions. For each section, provide its section ID, a human-readable title, paragraph span, canonical section functions, rhetorical job, and connection to surrounding sections. The title, explanation of the rhetorical job, and discussion of connections are interpretive prose, not new canonical fields or functions.

### 3. Rhetorical Progression

Describe the speech's beginning-to-end movement, momentum, and major transitions in analytical prose. Ground the account in transcript order and the canonical sections. The progression should be specific to the speech and must not be presented as a sequence of canonical functions or patterns unless those classifications are explicitly validated in the corresponding canonical input.

### 4. Rhetorical Devices

Discuss a representative selection of rhetorical-device annotations present in `03-tags.yaml`; no device or number of examples is required. For each selected annotation, provide the canonical tag, paragraph location, faithful brief evidence, effect, and explanation of why the placement matters. If no rhetorical-device annotations are validated, say so rather than inventing one.

### 5. Reusable Writing Patterns

Discuss a representative selection of canonical writing-pattern annotations present in `03-tags.yaml`; no pattern or number of examples is required. Explain each selected pattern in plain English, locate it, explain how it works in this speech, and derive a cautious speechwriting principle. If no writing-pattern annotations are validated, say so rather than inventing one.

### 6. Speech-Specific Analysis

Develop distinctive material that deserves greater depth. Optional H3 subsections may organize this material, but their subjects and number must emerge from the speech. Interpretations not represented in the canonical inputs may be discussed as ordinary prose when they are supported by transcript evidence and do not masquerade as canonical tags, section functions, annotations, or schema fields.

### 7. Climax and Closing

Discuss canonical `climax` and `closing` functions when they are present and explain whether they coincide or differ. The shared heading does not require every speech to contain a section tagged `climax`. If no climax is validated, do not invent one; describe the speech's strongest emphasis and ending in ordinary analytical prose without assigning a canonical function. Ground claims in the transcript, canonical structure, and validated annotations rather than assuming that the most famous or final line is automatically the climax.

### 8. Speechwriting Blueprint

Extract a concise numbered sequence from the speech's actual progression. State clearly that the blueprint is derived from this speech and is not a universal formula. Do not introduce steps unsupported by the canonical inputs and analysis.

### 9. Questions for Study

Provide a useful set of close-reading questions grounded in the speech. Cover relevant dimensions such as structure, purposes, audience, stakes, devices, writing patterns, ending, and distinctive rhetorical work, but do not force a question about a classification or feature the canonical inputs do not contain.

### 10. Taxonomy Notes

Record where the canonical distinctions were especially useful and where the available vocabulary did not fully capture an evidence-supported interpretive nuance. Describe any such gap as a noncanonical analytical observation. An already-known candidate concept may be mentioned when it helps explain the boundary, but it must remain explicitly noncanonical. This section does not create, approve, reject, or modify taxonomy candidates, and it does not prescribe a review or migration workflow.

## Formatting Convention

In analysis files, validated canonical taxonomy terms use Markdown code formatting, such as `inspire`, `console`, `antithesis`, and `build_to_climax`. Ordinary analytical concepts remain normal prose. Bold may provide ordinary emphasis, but it is not the convention for canonical tags. Paragraph and section IDs normally remain plain text.

An interpretive or candidate concept absent from the canonical inputs must remain visibly noncanonical. Do not format or label it in a way that implies canonical status.

## Grounding Rules

1. Treat `01-transcript.md`, `02-structure.yaml`, and `03-tags.yaml` as canonical inputs within their respective areas of authority.
2. Support quotations, paragraph references, and claims about wording with the transcript.
3. Preserve the structure file's section boundaries, paragraph membership, and section functions exactly in the analysis.
4. Do not invent canonical tags, section functions, annotations, paragraph references, quotations, or claims of canonical status.
5. Higher-level interpretations are permitted in ordinary prose when supported by evidence and clearly distinguished from canonical data.
6. If an interpretation exposes a possible canonical-data issue, report the distinction; do not silently override the canonical artifact in prose.
7. Do not claim universality from a single speech or force a particular structure, device, pattern, climax shape, or observation onto every speech.
8. Keep `04-analysis.md` downstream: it must not become evidence for `01-transcript.md`, `02-structure.yaml`, or `03-tags.yaml`.
9. Prefer analytical precision and representative examples over exhaustive commentary.

## Consistency Checklist

Before completion, verify that:

- the front matter contains all four required fields;
- the ten H2 sections match this guide and appear in order, using the current unnumbered heading convention;
- any speech-specific H3 subsections occur only in Speech-Specific Analysis and are justified by the speech;
- section and paragraph references, section boundaries, functions, and quotations match the canonical inputs;
- every canonical device and writing-pattern classification is validated in `03-tags.yaml`;
- canonical taxonomy terms use code formatting consistently;
- interpretive prose and candidate concepts are not presented as canonical data;
- any absence of a validated climax, device, or writing pattern is handled without invention;
- the analysis neither overrides canonical meaning nor serves as an input to an earlier Ingestion artifact;
- no canonical corpus data was changed while creating or regenerating the analysis.
