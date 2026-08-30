# Transcript Guide

Transcript Format Version: 1.0.0

## Purpose

Each `01-transcript.md` file contains two distinct layers:

1. standardized machine-readable provenance metadata;
2. the immutable primary-source transcript.

Metadata may be normalized as source research improves. The transcript beginning at `[p001]` is primary-source data and must not be changed during metadata normalization.

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

The front matter must begin and end with `---`. Nested `source` and `rights` mappings must use valid YAML indentation. No free-form metadata may appear between the closing delimiter and the title.

## Transcript Immutability

Everything from the existing `[p001]` marker through the end of the file must remain byte-for-byte unchanged during metadata or container normalization. This includes:

- paragraph wording and spelling;
- punctuation, quotation marks, and dashes;
- paragraph IDs and their order;
- line wrapping and paragraph boundaries;
- blank lines between paragraphs.

If a formatting preference conflicts with body preservation, preserve the body. Transcript Format Version is independent of schema, vocabulary, and analysis-template versions.

## Verification Checklist

Before completing a normalization pass:

1. Parse the front matter as YAML.
2. Confirm every required metadata field exists and is nonempty.
3. Confirm source URLs are plain YAML strings.
4. Confirm paragraph IDs begin at p001 and remain sequential.
5. Compare the bytes from `[p001]` through EOF with the pre-edit snapshot.
6. Confirm that only authorized transcript containers and this guide changed.
