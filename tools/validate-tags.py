#!/usr/bin/env python3
"""Validate speech-corpus structures and tags against the current taxonomy."""

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

SCHEMA_PATH = Path("schema/speech-schema.yaml")
VOCABULARY_PATH = Path("schema/vocabulary.yaml")
CANDIDATES_PATH = Path("review/candidate-tags.yaml")
SPEECHES_PATH = Path("speeches")

TRANSCRIPT_FILENAME = "01-transcript.md"
STRUCTURE_FILENAME = "02-structure.yaml"
TAGS_FILENAME = "03-tags.yaml"

CONFIDENCE_VALUES = {"high", "medium", "low"}
SPEECH_LEVEL_CATEGORIES = {"purposes", "themes", "tone"}
PURPOSE_PRIORITIES = {"primary", "secondary"}
PASSAGE_CATEGORIES = {"rhetorical_devices", "writing_patterns"}
CANDIDATE_STATUSES = {"pending_review", "approved", "rejected", "merged"}
CANDIDATE_CATEGORIES = {
    "purposes",
    "themes",
    "tone",
    "rhetorical_devices",
    "writing_patterns",
    "section_functions",
}
CANDIDATE_REQUIRED_FIELDS = {
    "candidate",
    "proposed_category",
    "speech",
    "section",
    "paragraphs",
    "reason",
    "possible_existing_tags",
    "status",
}
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
PARAGRAPH_MARKER_PATTERN = re.compile(r"^\[(p[^\]]*)\]\s*$", re.MULTILINE)
SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


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


def load_transcript(path: Path, errors: list[str]) -> list[str]:
    full_path = ROOT / path
    try:
        text = full_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        add_error(errors, path, "file not found")
        return []
    except OSError as exc:
        add_error(errors, path, f"could not read file: {exc}")
        return []

    raw_paragraph_ids = PARAGRAPH_MARKER_PATTERN.findall(text)
    paragraph_ids = PARAGRAPH_ID_PATTERN.findall(text)
    for paragraph_id in raw_paragraph_ids:
        if not re.fullmatch(r"p\d{3}", paragraph_id):
            add_error(
                errors,
                path,
                f"invalid paragraph ID {paragraph_id!r}; expected pNNN format",
            )
    for paragraph_id, count in Counter(paragraph_ids).items():
        if count > 1:
            add_error(errors, path, f"duplicate paragraph ID {paragraph_id!r}")
    if not paragraph_ids:
        add_error(errors, path, "no paragraph IDs found")
    else:
        expected_ids = [f"p{index:03d}" for index in range(1, len(paragraph_ids) + 1)]
        if paragraph_ids != expected_ids:
            mismatch_index = next(
                index
                for index, (actual, expected) in enumerate(
                    zip(paragraph_ids, expected_ids), start=1
                )
                if actual != expected
            )
            add_error(
                errors,
                path,
                "paragraph IDs must be sequential starting at p001; "
                f"expected {expected_ids[mismatch_index - 1]!r} but found "
                f"{paragraph_ids[mismatch_index - 1]!r} at position {mismatch_index}",
            )
    return paragraph_ids


def require_mapping(
    value: Any, path: Path, description: str, errors: list[str]
) -> dict[str, Any]:
    if not isinstance(value, dict):
        add_error(errors, path, f"{description} must be a mapping")
        return {}
    return value


def validate_versions(
    schema: dict[str, Any],
    vocabulary: dict[str, Any],
    structure: dict[str, Any],
    tags: dict[str, Any],
    structure_path: Path,
    tags_path: Path,
    errors: list[str],
) -> None:
    schema_version = schema.get("schema_version")
    vocabulary_version = vocabulary.get("vocabulary_version")
    if schema_version is None:
        add_error(errors, SCHEMA_PATH, "missing schema_version")
    if vocabulary_version is None:
        add_error(errors, VOCABULARY_PATH, "missing vocabulary_version")

    for document, path in ((structure, structure_path), (tags, tags_path)):
        for key, expected, source_path in (
            ("schema_version", schema_version, SCHEMA_PATH),
            ("vocabulary_version", vocabulary_version, VOCABULARY_PATH),
        ):
            actual = document.get(key)
            if actual is None:
                add_error(errors, path, f"missing {key}")
            elif expected is not None and actual != expected:
                add_error(
                    errors,
                    path,
                    f"{key} {actual!r} does not match "
                    f"{source_path.as_posix()} version {expected!r}",
                )


def validate_structure(
    structure: dict[str, Any],
    vocabulary: dict[str, Any],
    transcript_paragraphs: list[str],
    structure_path: Path,
    errors: list[str],
) -> tuple[int, dict[str, set[str]]]:
    canonical_functions = vocabulary.get("section_functions", [])
    if not isinstance(canonical_functions, list):
        add_error(errors, VOCABULARY_PATH, "section_functions must be a list")
        canonical_functions = []
    canonical_function_set = set(canonical_functions)

    sections = structure.get("sections", [])
    if not isinstance(sections, list):
        add_error(errors, structure_path, "sections must be a list")
        return 0, {}

    transcript_set = set(transcript_paragraphs)
    section_ids: set[str] = set()
    section_paragraphs: dict[str, set[str]] = defaultdict(set)
    paragraph_memberships: dict[str, list[str]] = defaultdict(list)

    for index, raw_section in enumerate(sections, start=1):
        location = f"sections[{index}]"
        if not isinstance(raw_section, dict):
            add_error(errors, structure_path, f"{location} must be a mapping")
            continue

        section_id = raw_section.get("id")
        if not isinstance(section_id, str) or not section_id:
            add_error(errors, structure_path, f"{location} has no valid id")
            section_id = f"<section {index}>"
        elif section_id in section_ids:
            add_error(errors, structure_path, f"duplicate section ID {section_id!r}")
        else:
            section_ids.add(section_id)

        rationale = raw_section.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            add_error(
                errors,
                structure_path,
                f"section {section_id!r} has no usable rationale",
            )

        paragraphs = raw_section.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            add_error(
                errors,
                structure_path,
                f"section {section_id!r} must have a non-empty paragraphs list",
            )
            paragraphs = []

        for paragraph_id in paragraphs:
            if paragraph_id not in transcript_set:
                add_error(
                    errors,
                    structure_path,
                    f"section {section_id!r} references unknown paragraph "
                    f"{paragraph_id!r}",
                )
            paragraph_memberships[paragraph_id].append(section_id)
            section_paragraphs[section_id].add(paragraph_id)

        functions = raw_section.get("functions")
        if not isinstance(functions, list) or not functions:
            add_error(
                errors,
                structure_path,
                f"section {section_id!r} must have a non-empty functions list",
            )
            functions = []
        for function in functions:
            if function not in canonical_function_set:
                add_error(
                    errors,
                    structure_path,
                    f"section {section_id!r} has unknown section function "
                    f"{function!r}",
                )

    for paragraph_id in transcript_paragraphs:
        memberships = paragraph_memberships.get(paragraph_id, [])
        if not memberships:
            add_error(
                errors,
                structure_path,
                f"transcript paragraph {paragraph_id!r} belongs to no section",
            )
        elif len(memberships) > 1:
            add_error(
                errors,
                structure_path,
                f"transcript paragraph {paragraph_id!r} appears multiple times "
                f"in sections: {', '.join(memberships)}",
            )

    return len(sections), dict(section_paragraphs)


def validate_tag_entries(
    entries: Any,
    category: str,
    location: str,
    vocabulary: dict[str, Any],
    tags_path: Path,
    errors: list[str],
) -> list[str]:
    if not isinstance(entries, list):
        add_error(errors, tags_path, f"{location} must be a list")
        return []

    canonical_tags = vocabulary.get(category, [])
    if not isinstance(canonical_tags, list):
        add_error(errors, VOCABULARY_PATH, f"{category} must be a list")
        canonical_tags = []
    canonical_set = set(canonical_tags)
    found_tags: list[str] = []

    for index, entry in enumerate(entries, start=1):
        entry_location = f"{location}[{index}]"
        if not isinstance(entry, dict):
            add_error(errors, tags_path, f"{entry_location} must be a mapping")
            continue
        missing = SPEECH_TAG_REQUIRED_FIELDS - set(entry)
        if missing:
            add_error(
                errors,
                tags_path,
                f"{entry_location} is missing: {', '.join(sorted(missing))}",
            )
        tag = entry.get("tag")
        if not isinstance(tag, str) or not tag.strip():
            add_error(errors, tags_path, f"{entry_location} has no usable tag")
        elif tag not in canonical_set:
            add_error(
                errors,
                tags_path,
                f"{entry_location} has unknown {category} tag {tag!r}",
            )
        else:
            found_tags.append(tag)

        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            add_error(
                errors,
                tags_path,
                f"{entry_location} has no usable rationale",
            )
        confidence = entry.get("confidence")
        if confidence not in CONFIDENCE_VALUES:
            add_error(
                errors,
                tags_path,
                f"{entry_location} has invalid confidence {confidence!r}",
            )

    for tag, count in Counter(found_tags).items():
        if count > 1:
            add_error(
                errors,
                tags_path,
                f"{location} has duplicate tag {tag!r}",
            )

    return found_tags


def validate_speech_level_tags(
    tags: dict[str, Any],
    vocabulary: dict[str, Any],
    tags_path: Path,
    errors: list[str],
) -> tuple[int, int, int]:
    speech_level = tags.get("speech_level")
    if not isinstance(speech_level, dict):
        add_error(errors, tags_path, "speech_level must be a mapping")
        return 0, 0, 0

    actual_categories = set(speech_level)
    for category in sorted(actual_categories - SPEECH_LEVEL_CATEGORIES):
        add_error(errors, tags_path, f"unknown speech-level category {category!r}")
    for category in sorted(SPEECH_LEVEL_CATEGORIES - actual_categories):
        add_error(errors, tags_path, f"missing speech-level category {category!r}")

    purposes = speech_level.get("purposes")
    if not isinstance(purposes, dict):
        add_error(errors, tags_path, "speech_level.purposes must be a mapping")
        purposes = {}
    actual_priorities = set(purposes)
    for priority in sorted(actual_priorities - PURPOSE_PRIORITIES):
        add_error(errors, tags_path, f"unknown purpose priority {priority!r}")
    for priority in sorted(PURPOSE_PRIORITIES - actual_priorities):
        add_error(errors, tags_path, f"missing purpose priority {priority!r}")

    primary_tags = validate_tag_entries(
        purposes.get("primary", []),
        "purposes",
        "speech_level.purposes.primary",
        vocabulary,
        tags_path,
        errors,
    )
    secondary_tags = validate_tag_entries(
        purposes.get("secondary", []),
        "purposes",
        "speech_level.purposes.secondary",
        vocabulary,
        tags_path,
        errors,
    )
    if not primary_tags:
        add_error(errors, tags_path, "at least 1 primary purpose is required")
    if len(primary_tags) > 4:
        add_error(errors, tags_path, "no more than 4 primary purposes are allowed")
    overlap = set(primary_tags) & set(secondary_tags)
    if overlap:
        add_error(
            errors,
            tags_path,
            "purposes cannot be both primary and secondary: "
            f"{', '.join(sorted(overlap))}",
        )

    theme_tags = validate_tag_entries(
        speech_level.get("themes", []),
        "themes",
        "speech_level.themes",
        vocabulary,
        tags_path,
        errors,
    )
    tone_tags = validate_tag_entries(
        speech_level.get("tone", []),
        "tone",
        "speech_level.tone",
        vocabulary,
        tags_path,
        errors,
    )

    total = len(primary_tags) + len(secondary_tags) + len(theme_tags) + len(tone_tags)
    return total, len(primary_tags), len(secondary_tags)


def validate_passage_annotations(
    tags: dict[str, Any],
    vocabulary: dict[str, Any],
    transcript_paragraphs: list[str],
    section_paragraphs: dict[str, set[str]],
    transcript_path: Path,
    tags_path: Path,
    errors: list[str],
) -> int:
    annotations = tags.get("passage_annotations")
    if not isinstance(annotations, list):
        add_error(errors, tags_path, "passage_annotations must be a list")
        return 0

    transcript_set = set(transcript_paragraphs)
    annotation_ids: set[str] = set()

    for index, annotation in enumerate(annotations, start=1):
        location = f"passage_annotations[{index}]"
        if not isinstance(annotation, dict):
            add_error(errors, tags_path, f"{location} must be a mapping")
            continue

        missing = PASSAGE_REQUIRED_FIELDS - set(annotation)
        if missing:
            add_error(
                errors,
                tags_path,
                f"{location} is missing: {', '.join(sorted(missing))}",
            )

        annotation_id = annotation.get("id")
        if not isinstance(annotation_id, str) or not annotation_id:
            add_error(errors, tags_path, f"{location} has no valid id")
        elif annotation_id in annotation_ids:
            add_error(errors, tags_path, f"duplicate passage annotation ID {annotation_id!r}")
        else:
            annotation_ids.add(annotation_id)

        category = annotation.get("category")
        if category not in PASSAGE_CATEGORIES:
            add_error(errors, tags_path, f"{location} has invalid category {category!r}")
        else:
            canonical_tags = vocabulary.get(category, [])
            if not isinstance(canonical_tags, list):
                add_error(errors, VOCABULARY_PATH, f"{category} must be a list")
                canonical_tags = []
            tag = annotation.get("tag")
            if tag not in set(canonical_tags):
                add_error(
                    errors,
                    tags_path,
                    f"{location} has unknown {category} tag {tag!r}",
                )

        confidence = annotation.get("confidence")
        if confidence not in CONFIDENCE_VALUES:
            add_error(errors, tags_path, f"{location} has invalid confidence {confidence!r}")

        for text_field in ("evidence", "rationale"):
            value = annotation.get(text_field)
            if not isinstance(value, str) or not value.strip():
                add_error(errors, tags_path, f"{location} has no usable {text_field}")

        section_id = annotation.get("section")
        if section_id not in section_paragraphs:
            add_error(errors, tags_path, f"{location} references unknown section {section_id!r}")

        paragraphs = annotation.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            add_error(errors, tags_path, f"{location} must have a non-empty paragraphs list")
            paragraphs = []

        for paragraph_id in paragraphs:
            if paragraph_id not in transcript_set:
                add_error(
                    errors,
                    transcript_path,
                    f"{location} references unknown paragraph {paragraph_id!r}",
                )
            elif (
                section_id in section_paragraphs
                and paragraph_id not in section_paragraphs[section_id]
            ):
                add_error(
                    errors,
                    tags_path,
                    f"{location} references paragraph {paragraph_id!r}, which "
                    f"does not belong to section {section_id!r}",
                )

    return len(annotations)


def validate_candidates(
    candidates: dict[str, Any],
    vocabulary: dict[str, Any],
    speech_contexts: dict[str, dict[str, Any]],
    errors: list[str],
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

        missing = CANDIDATE_REQUIRED_FIELDS - set(record)
        if missing:
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} is missing: {', '.join(sorted(missing))}",
            )

        candidate = record.get("candidate")
        if not isinstance(candidate, str) or not candidate.strip():
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} has no usable candidate",
            )

        category = record.get("proposed_category")
        category_is_valid = (
            isinstance(category, str) and category in CANDIDATE_CATEGORIES
        )
        if not category_is_valid:
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} has invalid proposed_category {category!r}",
            )

        speech_id = record.get("speech")
        speech_context = None
        if not isinstance(speech_id, str) or not speech_id.strip():
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} has no usable speech",
            )
        elif speech_id not in speech_contexts:
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} references nonexistent speech {speech_id!r}",
            )
        else:
            speech_context = speech_contexts[speech_id]

        section_id = record.get("section")
        section_paragraphs: set[str] | None = None
        if not isinstance(section_id, str) or not section_id.strip():
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} has no usable section",
            )
        elif speech_context is not None:
            sections = speech_context["sections"]
            if section_id not in sections:
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"{location} references nonexistent section {section_id!r} "
                    f"in speech {speech_id!r}",
                )
            else:
                section_paragraphs = sections[section_id]

        paragraphs = record.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} must have a non-empty paragraphs list",
            )
            paragraphs = []
        for paragraph_id in paragraphs:
            if not isinstance(paragraph_id, str) or not paragraph_id.strip():
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"{location} has invalid paragraph {paragraph_id!r}",
                )
            elif (
                speech_context is not None
                and paragraph_id not in speech_context["paragraphs"]
            ):
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"{location} references nonexistent paragraph "
                    f"{paragraph_id!r} in speech {speech_id!r}",
                )
            elif section_paragraphs is not None and paragraph_id not in section_paragraphs:
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"{location} references paragraph {paragraph_id!r}, which "
                    f"does not belong to section {section_id!r}",
                )

        reason = record.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} has no usable reason",
            )

        possible_existing_tags = record.get("possible_existing_tags")
        if not isinstance(possible_existing_tags, list):
            add_error(
                errors,
                CANDIDATES_PATH,
                f"{location} possible_existing_tags must be a list",
            )
            possible_existing_tags = []
        if category_is_valid:
            canonical_tags = vocabulary.get(category)
            if not isinstance(canonical_tags, list):
                add_error(
                    errors,
                    VOCABULARY_PATH,
                    f"{category} must be a list",
                )
                canonical_tags = []
            canonical_set = set(canonical_tags)
            for possible_tag in possible_existing_tags:
                if (
                    not isinstance(possible_tag, str)
                    or possible_tag not in canonical_set
                ):
                    add_error(
                        errors,
                        CANDIDATES_PATH,
                        f"{location} has unknown possible_existing_tag "
                        f"{possible_tag!r} for category {category!r}",
                    )

        status = record.get("status")
        if not isinstance(status, str) or not status.strip():
            add_error(errors, CANDIDATES_PATH, f"{location} has no usable status")
        elif status not in CANDIDATE_STATUSES:
            add_error(errors, CANDIDATES_PATH, f"{location} has invalid status {status!r}")

        if status == "approved":
            approved_version = record.get("approved_in_vocabulary_version")
            if (
                not isinstance(approved_version, str)
                or not approved_version.strip()
                or not SEMANTIC_VERSION_PATTERN.fullmatch(approved_version)
            ):
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"{location} has invalid approved_in_vocabulary_version "
                    f"{approved_version!r}; expected semantic version X.Y.Z",
                )

            canonical_tags = vocabulary.get(category)
            if not isinstance(canonical_tags, list) or candidate not in canonical_tags:
                add_error(
                    errors,
                    CANDIDATES_PATH,
                    f"approved candidate {candidate!r} does not exist in "
                    f"canonical vocabulary category {category!r}",
                )


def discover_speech_directories(errors: list[str]) -> list[Path]:
    full_speeches_path = ROOT / SPEECHES_PATH
    try:
        directories = sorted(path for path in full_speeches_path.iterdir() if path.is_dir())
    except FileNotFoundError:
        add_error(errors, SPEECHES_PATH, "directory not found")
        return []
    except OSError as exc:
        add_error(errors, SPEECHES_PATH, f"could not list directory: {exc}")
        return []
    if not directories:
        add_error(errors, SPEECHES_PATH, "no speech directories found")
    return [path.relative_to(ROOT) for path in directories]


def print_result(results: list[dict[str, Any]], global_errors: list[str]) -> int:
    print("Speech corpus validation")
    print()

    all_errors = list(global_errors)
    for result in results:
        print(result["name"])
        if result["errors"]:
            all_errors.extend(result["errors"])
            for message in result["errors"]:
                print(message)
        else:
            print(f"✓ transcript paragraphs: {result['paragraph_count']}")
            print(f"✓ rhetorical sections: {result['section_count']}")
            print(f"✓ primary purposes: {result['primary_count']}")
            print(f"✓ secondary purposes: {result['secondary_count']}")
            print(f"✓ speech-level tags: {result['speech_tag_count']}")
            print(f"✓ passage annotations: {result['annotation_count']}")
            print("✓ canonical tags and references valid")
            print("✓ versions consistent")
        print()

    if global_errors:
        print("Corpus-level errors")
        for message in global_errors:
            print(message)
        print()

    print("Overall:")
    if all_errors:
        print(f"✗ speeches checked: {len(results)}")
        print(f"✗ validation errors: {len(all_errors)}")
        print()
        print("Validation failed.")
        return 1

    print(f"✓ speeches validated: {len(results)}")
    print("✓ all canonical tags valid")
    print("✓ versions consistent")
    print("✓ candidate-tag records valid")
    print()
    print("Validation passed.")
    return 0


def main() -> int:
    global_errors: list[str] = []
    schema = require_mapping(
        load_yaml(SCHEMA_PATH, global_errors),
        SCHEMA_PATH,
        "document root",
        global_errors,
    )
    vocabulary = require_mapping(
        load_yaml(VOCABULARY_PATH, global_errors),
        VOCABULARY_PATH,
        "document root",
        global_errors,
    )
    candidates = require_mapping(
        load_yaml(CANDIDATES_PATH, global_errors),
        CANDIDATES_PATH,
        "document root",
        global_errors,
    )

    results: list[dict[str, Any]] = []
    speech_contexts: dict[str, dict[str, Any]] = {}
    for speech_directory in discover_speech_directories(global_errors):
        errors: list[str] = []
        transcript_path = speech_directory / TRANSCRIPT_FILENAME
        structure_path = speech_directory / STRUCTURE_FILENAME
        tags_path = speech_directory / TAGS_FILENAME

        transcript_paragraphs = load_transcript(transcript_path, errors)
        structure = require_mapping(
            load_yaml(structure_path, errors),
            structure_path,
            "document root",
            errors,
        )
        tags = require_mapping(
            load_yaml(tags_path, errors), tags_path, "document root", errors
        )

        validate_versions(
            schema,
            vocabulary,
            structure,
            tags,
            structure_path,
            tags_path,
            errors,
        )
        section_count, section_paragraphs = validate_structure(
            structure,
            vocabulary,
            transcript_paragraphs,
            structure_path,
            errors,
        )
        speech_tag_count, primary_count, secondary_count = validate_speech_level_tags(
            tags, vocabulary, tags_path, errors
        )
        annotation_count = validate_passage_annotations(
            tags,
            vocabulary,
            transcript_paragraphs,
            section_paragraphs,
            transcript_path,
            tags_path,
            errors,
        )

        speech_contexts[speech_directory.name] = {
            "paragraphs": set(transcript_paragraphs),
            "sections": section_paragraphs,
        }

        results.append(
            {
                "name": tags.get("speech_id", speech_directory.name),
                "errors": errors,
                "paragraph_count": len(transcript_paragraphs),
                "section_count": section_count,
                "primary_count": primary_count,
                "secondary_count": secondary_count,
                "speech_tag_count": speech_tag_count,
                "annotation_count": annotation_count,
            }
        )

    validate_candidates(candidates, vocabulary, speech_contexts, global_errors)

    return print_result(results, global_errors)


if __name__ == "__main__":
    sys.exit(main())
