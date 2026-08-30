#!/usr/bin/env python3
"""Validate the current speech-corpus pilot files."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "ERROR tools/validate-tags.py: PyYAML is required. "
        "Install PyYAML and run the validator again.",
        file=sys.stderr,
    )
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]

VOCABULARY_PATH = Path("schema/vocabulary.yaml")
TRANSCRIPT_PATH = Path("speeches/jfk-1961-inaugural/01-transcript.md")
STRUCTURE_PATH = Path("speeches/jfk-1961-inaugural/02-structure.yaml")
TAGS_PATH = Path("speeches/jfk-1961-inaugural/03-tags.yaml")
CANDIDATES_PATH = Path("review/candidate-tags.yaml")

CONFIDENCE_VALUES = {"high", "medium", "low"}
SPEECH_LEVEL_CATEGORIES = {"purposes", "themes", "tone"}
PASSAGE_CATEGORIES = {"rhetorical_devices", "writing_patterns"}
CANDIDATE_STATUSES = {"pending_review", "approved", "rejected", "merged"}
PASSAGE_REQUIRED_FIELDS = {
    "id",
    "category",
    "tag",
    "section",
    "paragraphs",
    "evidence",
    "rationale",
    "confidence",
}
SPEECH_TAG_REQUIRED_FIELDS = {"tag", "rationale", "confidence"}
PARAGRAPH_ID_PATTERN = re.compile(r"^\[(p\d{3})\]\s*$", re.MULTILINE)


def add_error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"ERROR {path.as_posix()}: {message}")


def load_yaml(path: Path, errors: list[str]) -> Any:
    full_path = ROOT / path
    try:
        with full_path.open(encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except FileNotFoundError:
        add_error(errors, path, "file not found")
    except yaml.YAMLError as exc:
        add_error(errors, path, f"invalid YAML: {exc}")
    except OSError as exc:
        add_error(errors, path, f"could not read file: {exc}")
    return None


def load_transcript(errors: list[str]) -> list[str]:
    full_path = ROOT / TRANSCRIPT_PATH
    try:
        text = full_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        add_error(errors, TRANSCRIPT_PATH, "file not found")
        return []
    except OSError as exc:
        add_error(errors, TRANSCRIPT_PATH, f"could not read file: {exc}")
        return []

    paragraph_ids = PARAGRAPH_ID_PATTERN.findall(text)
    for paragraph_id, count in Counter(paragraph_ids).items():
        if count > 1:
            add_error(
                errors,
                TRANSCRIPT_PATH,
                f"duplicate paragraph ID {paragraph_id!r}",
            )
    if not paragraph_ids:
        add_error(errors, TRANSCRIPT_PATH, "no paragraph IDs found")
    return paragraph_ids


def require_mapping(
    value: Any, path: Path, description: str, errors: list[str]
) -> dict[str, Any]:
    if not isinstance(value, dict):
        add_error(errors, path, f"{description} must be a mapping")
        return {}
    return value


def validate_versions(
    vocabulary: dict[str, Any],
    structure: dict[str, Any],
    tags: dict[str, Any],
    errors: list[str],
) -> None:
    vocabulary_version = vocabulary.get("vocabulary_version")
    if vocabulary_version is None:
        add_error(errors, VOCABULARY_PATH, "missing vocabulary_version")

    for key in ("schema_version", "vocabulary_version"):
        if key not in structure:
            add_error(errors, STRUCTURE_PATH, f"missing {key}")
        if key not in tags:
            add_error(errors, TAGS_PATH, f"missing {key}")

    tags_vocabulary_version = tags.get("vocabulary_version")
    if (
        vocabulary_version is not None
        and tags_vocabulary_version is not None
        and tags_vocabulary_version != vocabulary_version
    ):
        add_error(
            errors,
            TAGS_PATH,
            "vocabulary_version "
            f"{tags_vocabulary_version!r} does not match "
            f"{VOCABULARY_PATH.as_posix()} version {vocabulary_version!r}",
        )

    structure_schema_version = structure.get("schema_version")
    tags_schema_version = tags.get("schema_version")
    if (
        structure_schema_version is not None
        and tags_schema_version is not None
        and structure_schema_version != tags_schema_version
    ):
        add_error(
            errors,
            TAGS_PATH,
            "schema_version "
            f"{tags_schema_version!r} does not match "
            f"{STRUCTURE_PATH.as_posix()} version {structure_schema_version!r}",
        )


def validate_structure(
    structure: dict[str, Any],
    vocabulary: dict[str, Any],
    transcript_paragraphs: list[str],
    errors: list[str],
) -> tuple[int, dict[str, set[str]]]:
    canonical_functions = vocabulary.get("section_functions", [])
    if not isinstance(canonical_functions, list):
        add_error(
            errors,
            VOCABULARY_PATH,
            "section_functions must be a list",
        )
        canonical_functions = []
    canonical_function_set = set(canonical_functions)

    sections = structure.get("sections", [])
    if not isinstance(sections, list):
        add_error(errors, STRUCTURE_PATH, "sections must be a list")
        return 0, {}

    transcript_set = set(transcript_paragraphs)
    section_ids: set[str] = set()
    section_paragraphs: dict[str, set[str]] = defaultdict(set)
    paragraph_memberships: dict[str, list[str]] = defaultdict(list)

    for index, raw_section in enumerate(sections, start=1):
        location = f"sections[{index}]"
        if not isinstance(raw_section, dict):
            add_error(errors, STRUCTURE_PATH, f"{location} must be a mapping")
            continue

        section_id = raw_section.get("id")
        if not isinstance(section_id, str) or not section_id:
            add_error(errors, STRUCTURE_PATH, f"{location} has no valid id")
            section_id = f"<section {index}>"
        elif section_id in section_ids:
            add_error(
                errors,
                STRUCTURE_PATH,
                f"duplicate section ID {section_id!r}",
            )
        else:
            section_ids.add(section_id)

        paragraphs = raw_section.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            add_error(
                errors,
                STRUCTURE_PATH,
                f"section {section_id!r} must have a non-empty paragraphs list",
            )
            paragraphs = []

        for paragraph_id in paragraphs:
            if paragraph_id not in transcript_set:
                add_error(
                    errors,
                    STRUCTURE_PATH,
                    f"section {section_id!r} references unknown paragraph "
                    f"{paragraph_id!r}",
                )
            paragraph_memberships[paragraph_id].append(section_id)
            section_paragraphs[section_id].add(paragraph_id)

        functions = raw_section.get("functions")
        if not isinstance(functions, list) or not functions:
            add_error(
                errors,
                STRUCTURE_PATH,
                f"section {section_id!r} must have a non-empty functions list",
            )
            functions = []
        for function in functions:
            if function not in canonical_function_set:
                add_error(
                    errors,
                    STRUCTURE_PATH,
                    f"section {section_id!r} has unknown section function "
                    f"{function!r}",
                )

    for paragraph_id in transcript_paragraphs:
        memberships = paragraph_memberships.get(paragraph_id, [])
        if not memberships:
            add_error(
                errors,
                STRUCTURE_PATH,
                f"transcript paragraph {paragraph_id!r} belongs to no section",
            )
        elif len(memberships) > 1:
            add_error(
                errors,
                STRUCTURE_PATH,
                f"transcript paragraph {paragraph_id!r} appears multiple times "
                f"in sections: {', '.join(memberships)}",
            )

    return len(sections), dict(section_paragraphs)


def validate_speech_level_tags(
    tags: dict[str, Any], vocabulary: dict[str, Any], errors: list[str]
) -> int:
    speech_level = tags.get("speech_level")
    if not isinstance(speech_level, dict):
        add_error(errors, TAGS_PATH, "speech_level must be a mapping")
        return 0

    actual_categories = set(speech_level)
    for category in sorted(actual_categories - SPEECH_LEVEL_CATEGORIES):
        add_error(
            errors,
            TAGS_PATH,
            f"unknown speech-level category {category!r}",
        )
    for category in sorted(SPEECH_LEVEL_CATEGORIES - actual_categories):
        add_error(
            errors,
            TAGS_PATH,
            f"missing speech-level category {category!r}",
        )

    tag_count = 0
    for category in sorted(SPEECH_LEVEL_CATEGORIES):
        entries = speech_level.get(category, [])
        if not isinstance(entries, list):
            add_error(
                errors,
                TAGS_PATH,
                f"speech_level.{category} must be a list",
            )
            continue

        canonical_tags = vocabulary.get(category, [])
        if not isinstance(canonical_tags, list):
            add_error(errors, VOCABULARY_PATH, f"{category} must be a list")
            canonical_tags = []
        canonical_set = set(canonical_tags)

        for index, entry in enumerate(entries, start=1):
            tag_count += 1
            location = f"speech_level.{category}[{index}]"
            if not isinstance(entry, dict):
                add_error(errors, TAGS_PATH, f"{location} must be a mapping")
                continue
            missing = SPEECH_TAG_REQUIRED_FIELDS - set(entry)
            if missing:
                add_error(
                    errors,
                    TAGS_PATH,
                    f"{location} is missing: {', '.join(sorted(missing))}",
                )
            tag = entry.get("tag")
            if tag not in canonical_set:
                add_error(
                    errors,
                    TAGS_PATH,
                    f"{location} has unknown {category} tag {tag!r}",
                )
            confidence = entry.get("confidence")
            if confidence not in CONFIDENCE_VALUES:
                add_error(
                    errors,
                    TAGS_PATH,
                    f"{location} has invalid confidence {confidence!r}",
                )

    return tag_count


def validate_passage_annotations(
    tags: dict[str, Any],
    vocabulary: dict[str, Any],
    transcript_paragraphs: list[str],
    section_paragraphs: dict[str, set[str]],
    errors: list[str],
) -> int:
    annotations = tags.get("passage_annotations")
    if not isinstance(annotations, list):
        add_error(errors, TAGS_PATH, "passage_annotations must be a list")
        return 0

    transcript_set = set(transcript_paragraphs)
    annotation_ids: set[str] = set()

    for index, annotation in enumerate(annotations, start=1):
        location = f"passage_annotations[{index}]"
        if not isinstance(annotation, dict):
            add_error(errors, TAGS_PATH, f"{location} must be a mapping")
            continue

        missing = PASSAGE_REQUIRED_FIELDS - set(annotation)
        if missing:
            add_error(
                errors,
                TAGS_PATH,
                f"{location} is missing: {', '.join(sorted(missing))}",
            )

        annotation_id = annotation.get("id")
        if not isinstance(annotation_id, str) or not annotation_id:
            add_error(errors, TAGS_PATH, f"{location} has no valid id")
        elif annotation_id in annotation_ids:
            add_error(
                errors,
                TAGS_PATH,
                f"duplicate passage annotation ID {annotation_id!r}",
            )
        else:
            annotation_ids.add(annotation_id)

        category = annotation.get("category")
        if category not in PASSAGE_CATEGORIES:
            add_error(
                errors,
                TAGS_PATH,
                f"{location} has invalid category {category!r}",
            )
        else:
            canonical_tags = vocabulary.get(category, [])
            if not isinstance(canonical_tags, list):
                add_error(errors, VOCABULARY_PATH, f"{category} must be a list")
                canonical_tags = []
            tag = annotation.get("tag")
            if tag not in set(canonical_tags):
                add_error(
                    errors,
                    TAGS_PATH,
                    f"{location} has unknown {category} tag {tag!r}",
                )

        confidence = annotation.get("confidence")
        if confidence not in CONFIDENCE_VALUES:
            add_error(
                errors,
                TAGS_PATH,
                f"{location} has invalid confidence {confidence!r}",
            )

        for text_field in ("evidence", "rationale"):
            value = annotation.get(text_field)
            if not isinstance(value, str) or not value.strip():
                add_error(
                    errors,
                    TAGS_PATH,
                    f"{location} has no usable {text_field}",
                )

        section_id = annotation.get("section")
        if section_id not in section_paragraphs:
            add_error(
                errors,
                TAGS_PATH,
                f"{location} references unknown section {section_id!r}",
            )

        paragraphs = annotation.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            add_error(
                errors,
                TAGS_PATH,
                f"{location} must have a non-empty paragraphs list",
            )
            paragraphs = []

        for paragraph_id in paragraphs:
            if paragraph_id not in transcript_set:
                add_error(
                    errors,
                    TAGS_PATH,
                    f"{location} references unknown paragraph {paragraph_id!r}",
                )
            elif (
                section_id in section_paragraphs
                and paragraph_id not in section_paragraphs[section_id]
            ):
                add_error(
                    errors,
                    TAGS_PATH,
                    f"{location} references paragraph {paragraph_id!r}, which "
                    f"does not belong to section {section_id!r}",
                )

    return len(annotations)


def validate_candidates(
    candidates: dict[str, Any], vocabulary: dict[str, Any], errors: list[str]
) -> None:
    records = candidates.get("candidate_tags")
    if not isinstance(records, list):
        add_error(errors, CANDIDATES_PATH, "candidate_tags must be a list")
        return

    for index, record in enumerate(records, start=1):
        location = f"candidate_tags[{index}]"
        if not isinstance(record, dict):
            add_error(errors, CANDIDATES_PATH, f"{location} must be a mapping")
            continue

        status = record.get("status")
        if status is None:
            add_error(errors, CANDIDATES_PATH, f"{location} is missing status")
            continue
        if status not in CANDIDATE_STATUSES:
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} has invalid status {status!r}",
            )

        if status == "approved":
            approved_version = record.get("approved_in_vocabulary_version")
            if approved_version is None:
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"{location} is approved but missing "
                    "approved_in_vocabulary_version",
                )

            candidate = record.get("candidate")
            category = record.get("proposed_category")
            canonical_tags = vocabulary.get(category)
            if not isinstance(canonical_tags, list) or candidate not in canonical_tags:
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"approved candidate {candidate!r} does not exist in "
                    f"canonical vocabulary category {category!r}",
                )


def print_result(
    errors: list[str],
    paragraph_count: int,
    section_count: int,
    speech_tag_count: int,
    annotation_count: int,
) -> int:
    print("Speech corpus validation")
    print()
    if errors:
        for message in errors:
            print(message)
        print()
        print(f"Validation failed with {len(errors)} error(s).")
        return 1

    print(f"✓ transcript paragraphs: {paragraph_count}")
    print(f"✓ rhetorical sections: {section_count}")
    print(f"✓ speech-level tags: {speech_tag_count}")
    print(f"✓ passage annotations: {annotation_count}")
    print("✓ all canonical tags valid")
    print("✓ paragraph references valid")
    print("✓ section references valid")
    print("✓ versions consistent")
    print("✓ candidate-tag records valid")
    print()
    print("Validation passed.")
    return 0


def main() -> int:
    errors: list[str] = []
    transcript_paragraphs = load_transcript(errors)
    vocabulary = require_mapping(
        load_yaml(VOCABULARY_PATH, errors),
        VOCABULARY_PATH,
        "document root",
        errors,
    )
    structure = require_mapping(
        load_yaml(STRUCTURE_PATH, errors),
        STRUCTURE_PATH,
        "document root",
        errors,
    )
    tags = require_mapping(
        load_yaml(TAGS_PATH, errors), TAGS_PATH, "document root", errors
    )
    candidates = require_mapping(
        load_yaml(CANDIDATES_PATH, errors),
        CANDIDATES_PATH,
        "document root",
        errors,
    )

    validate_versions(vocabulary, structure, tags, errors)
    section_count, section_paragraphs = validate_structure(
        structure, vocabulary, transcript_paragraphs, errors
    )
    speech_tag_count = validate_speech_level_tags(tags, vocabulary, errors)
    annotation_count = validate_passage_annotations(
        tags,
        vocabulary,
        transcript_paragraphs,
        section_paragraphs,
        errors,
    )
    validate_candidates(candidates, vocabulary, errors)

    return print_result(
        errors,
        len(transcript_paragraphs),
        section_count,
        speech_tag_count,
        annotation_count,
    )


if __name__ == "__main__":
    sys.exit(main())
