# Transcript Guide

Transcript Format Version: 1.0.0

## Purpose

Each `01-transcript.md` file contains two distinct layers:

1. standardized machine-readable provenance metadata;
2. a source-faithful transcript body with stable paragraph IDs.

Metadata may be normalized as source research improves. Once prepared, the transcript body beginning at `[p001]` must not be changed during metadata or container normalization.

## Standard File Shape

```yaml
---
transcript_format_version: 1.0.0
speech_id: <speech id>
title: <title>
speaker: <speaker>
date: YYYY-MM-DD
country: <country>
speech_type: <speech type>

# Optional when genuinely known:
venue: <venue>
common_title: <common title>

source:
  organization: <source organization>
  source_title: <source title>
  source_url: <plain URL>
  # Optional when genuinely known:
  document_reference: <source document reference>

# Optional only when verified:
rights:
  status: <rights status>
  license: <license>
  attribution: <attribution statement>
---

# <title>

## Transcript

[p001]
...
```

Optional fields must be omitted when unknown. Do not insert blank or null values, infer unverified rights, or convert source URLs into Markdown links.

## Required Metadata

Every transcript front matter must contain:

- `transcript_format_version`
- `speech_id`
- `title`
- `speaker`
- `date`
- `country`
- `speech_type`
- `source.organization`
- `source.source_title`
- `source.source_url`

The front matter must begin and end with `---`. Nested `source` and `rights` mappings must use valid YAML indentation.

## Document Structure

After the closing front-matter delimiter, the document must contain, in order:

1. an H1 heading that exactly matches the `title` value;
2. the H2 heading `Transcript`;
3. the paragraph entries, beginning with `[p001]`.

Do not place free-form metadata or commentary between these elements.

## Paragraph IDs and Source Text

Each transcript paragraph must have an ID on its own line immediately before the paragraph text. IDs use the three-digit, zero-padded form `[pNNN]`: begin with `[p001]` and increment by one without gaps or duplicates. Separate paragraph entries with a blank line.

Prepare the transcript faithfully from the cited source. Preserve its wording, spelling, capitalization, punctuation, quotation style, dashes, and paragraph divisions; do not silently correct or modernize the text. Do not add editorial commentary that is absent from the source.

## Transcript Immutability

Once the transcript body has been prepared, everything from `[p001]` through the end of the file must remain byte-for-byte unchanged during metadata or container normalization. This includes:

- paragraph wording and spelling;
- punctuation, quotation marks, and dashes;
- paragraph IDs and their order;
- line wrapping and paragraph boundaries;
- blank lines between paragraphs.

If a formatting preference conflicts with body preservation, preserve the body. Transcript Format Version is independent of schema, vocabulary, and analysis-template versions.

## Conformance Checklist

A conforming transcript meets these checks:

1. The front matter parses as YAML.
2. Every required metadata field exists and is nonempty.
3. The source URL is a plain YAML string.
4. The H1 heading exactly matches `title` and is followed by `## Transcript`.
5. Paragraph IDs use the required form, begin at `[p001]`, and remain sequential.
6. The transcript is source-faithful and contains no added editorial commentary.
7. During metadata or container normalization, the bytes from `[p001]` through EOF remain unchanged.
