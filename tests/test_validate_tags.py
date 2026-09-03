"""Synthetic rule tests and one real-corpus test for the tag validator."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import shutil
from types import ModuleType
from typing import Any

import pytest
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate-tags.py"
SCHEMA_PATH = Path("schema/speech-schema.yaml")
VOCABULARY_PATH = Path("schema/vocabulary.yaml")
CANDIDATES_PATH = Path("review/candidate-tags.yaml")
TRANSCRIPT_FILENAME = "01-transcript.md"
STRUCTURE_FILENAME = "02-structure.yaml"
TAGS_FILENAME = "03-tags.yaml"
SYNTHETIC_SPEECH_ID = "synthetic-speech"
SYNTHETIC_SPEECH_DIR = Path("speeches") / SYNTHETIC_SPEECH_ID
SYNTHETIC_TRANSCRIPT_PATH = SYNTHETIC_SPEECH_DIR / TRANSCRIPT_FILENAME
SYNTHETIC_STRUCTURE_PATH = SYNTHETIC_SPEECH_DIR / STRUCTURE_FILENAME
SYNTHETIC_TAGS_PATH = SYNTHETIC_SPEECH_DIR / TAGS_FILENAME


@pytest.fixture(scope="session")
def validator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "speech_corpus_validate_tags", VALIDATOR_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_yaml(corpus_root: Path, relative_path: Path) -> dict[str, Any]:
    with (corpus_root / relative_path).open(encoding="utf-8") as handle:
        document = yaml.safe_load(handle)
    assert isinstance(document, dict)
    return document


def write_yaml(
    corpus_root: Path, relative_path: Path, document: dict[str, Any]
) -> None:
    path = corpus_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(
            document,
            handle,
            allow_unicode=True,
            sort_keys=False,
            width=100,
        )


def tag_entry(tag: str, rationale: str = "Synthetic rationale.") -> dict[str, str]:
    return {"tag": tag, "rationale": rationale, "confidence": "high"}


def candidate_record(
    corpus_root: Path,
    candidate: str = "freedom",
    category: str = "themes",
    status: str = "pending_review",
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "candidate": candidate,
        "proposed_category": category,
        "speech": SYNTHETIC_SPEECH_ID,
        "section": "s01",
        "paragraphs": ["p001"],
        "reason": "Synthetic candidate rationale.",
        "possible_existing_tags": [],
        "status": status,
    }
    if status == "approved":
        vocabulary = read_yaml(corpus_root, VOCABULARY_PATH)
        record["approved_in_vocabulary_version"] = vocabulary["vocabulary_version"]
    return record


@pytest.fixture
def corpus_root(tmp_path: Path) -> Path:
    corpus_root = tmp_path / "synthetic-corpus"
    for schema_file in (SCHEMA_PATH, VOCABULARY_PATH):
        destination = corpus_root / schema_file
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROJECT_ROOT / schema_file, destination)

    write_yaml(corpus_root, CANDIDATES_PATH, {"candidate_tags": []})

    speech_dir = corpus_root / SYNTHETIC_SPEECH_DIR
    speech_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = speech_dir / TRANSCRIPT_FILENAME
    transcript_path.write_text(
        "# A Generic Speech\n\n"
        "[p001]\n\n"
        "Friends, today we begin a shared task.\n\n"
        "[p002]\n\n"
        "The task will ask patience from everyone.\n\n"
        "[p003]\n\n"
        "Let us work together, and let us finish it.\n",
        encoding="utf-8",
    )

    schema = read_yaml(corpus_root, SCHEMA_PATH)
    vocabulary = read_yaml(corpus_root, VOCABULARY_PATH)
    versions = {
        "schema_version": schema["schema_version"],
        "vocabulary_version": vocabulary["vocabulary_version"],
    }

    write_yaml(
        corpus_root,
        SYNTHETIC_STRUCTURE_PATH,
        {
            "speech_id": SYNTHETIC_SPEECH_ID,
            **versions,
            "sections": [
                {
                    "id": "s01",
                    "paragraphs": ["p001", "p002"],
                    "functions": ["opening"],
                    "rationale": "The speech opens by addressing its audience.",
                },
                {
                    "id": "s02",
                    "paragraphs": ["p003"],
                    "functions": ["call_to_action", "closing"],
                    "rationale": "The speech closes with a simple shared action.",
                },
            ],
        },
    )
    write_yaml(
        corpus_root,
        SYNTHETIC_TAGS_PATH,
        {
            "speech_id": SYNTHETIC_SPEECH_ID,
            **versions,
            "speech_level": {
                "purposes": {
                    "primary": [tag_entry("inspire")],
                    "secondary": [tag_entry("inform")],
                },
                "themes": [tag_entry("freedom")],
                "tone": [tag_entry("formal")],
            },
            "passage_annotations": [
                {
                    "id": "a001",
                    "category": "rhetorical_devices",
                    "tag": "direct_address",
                    "section": "s01",
                    "paragraphs": ["p001"],
                    "evidence": "Friends",
                    "rationale": "The opening explicitly addresses the audience.",
                    "confidence": "high",
                },
                {
                    "id": "a002",
                    "category": "rhetorical_devices",
                    "tag": "repetition",
                    "section": "s02",
                    "paragraphs": ["p003"],
                    "evidence": "Let us ... let us",
                    "rationale": "The closing repeats its inclusive opening phrase.",
                    "confidence": "high",
                },
            ],
        },
    )
    return corpus_root


def run_validator(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> tuple[int, str]:
    monkeypatch.setattr(validator_module, "PROJECT_ROOT", corpus_root)
    result = validator_module.main()
    output = capsys.readouterr().out
    return result, output


def assert_validation_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    expected_message: str,
) -> None:
    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )
    assert result == 1, output
    assert expected_message in output


def test_valid_current_corpus_passes_and_discovers_speeches(
    validator_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    discovered_count = sum(
        path.is_dir() for path in (PROJECT_ROOT / "speeches").iterdir()
    )
    assert discovered_count > 0

    result, output = run_validator(
        validator_module, PROJECT_ROOT, monkeypatch, capsys
    )

    assert result == 0, output
    assert "Validation passed." in output
    assert f"speeches validated: {discovered_count}" in output


def test_valid_synthetic_corpus_passes(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )
    assert result == 0, output
    assert "Validation passed." in output


def test_unknown_canonical_tag_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][0]["tag"] = "invented_device"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "unknown rhetorical_devices tag 'invented_device'",
    )


def test_wrong_category_tag_pairing_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][0]["category"] = "writing_patterns"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "unknown writing_patterns tag 'direct_address'",
    )


def test_missing_tags_top_level_field_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    del tags["speech_id"]
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "missing required top-level field 'speech_id'",
    )


def test_unexpected_tags_top_level_field_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["candidate_tags"] = []
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "unexpected top-level field 'candidate_tags'",
    )


def test_invalid_confidence_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["speech_level"]["purposes"]["primary"][0]["confidence"] = "maybe"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "invalid confidence 'maybe'",
    )


def test_zero_primary_purposes_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["speech_level"]["purposes"]["primary"] = []
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "at least 1 primary purpose is required",
    )


def test_unknown_paragraph_reference_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][0]["paragraphs"] = ["p999"]
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "references unknown paragraph 'p999'",
    )


def test_unknown_section_reference_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][0]["section"] = "s999"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "references unknown section 's999'",
    )


def test_paragraph_outside_referenced_section_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][0]["paragraphs"] = ["p003"]
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "paragraph 'p003', which does not belong to section 's01'",
    )


def test_duplicate_annotation_id_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][1]["id"] = "a001"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "duplicate passage annotation ID 'a001'",
    )


def test_non_sequential_annotation_ids_pass(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][1]["id"] = "a099"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )
    assert result == 0, output
    assert "Validation passed." in output


def test_invalid_annotation_id_format_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][0]["id"] = "annotation-1"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "invalid annotation ID 'annotation-1'; expected aNNN format",
    )


def test_too_many_primary_purposes_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    primary = tags["speech_level"]["purposes"]["primary"]
    primary.extend(
        tag_entry(tag) for tag in ("persuade", "reassure", "warn", "unify")
    )
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "no more than 4 primary purposes are allowed",
    )


def test_primary_secondary_overlap_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    purposes = tags["speech_level"]["purposes"]
    purposes["secondary"].append(copy.deepcopy(purposes["primary"][0]))
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "cannot be both primary and secondary",
    )


def test_duplicate_section_membership_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH)
    structure["sections"][1]["paragraphs"].append("p001")
    write_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH, structure)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "transcript paragraph 'p001' appears multiple times in sections",
    )


def test_missing_section_membership_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH)
    structure["sections"][0]["paragraphs"].remove("p002")
    write_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH, structure)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "transcript paragraph 'p002' belongs to no section",
    )


def test_unknown_section_function_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH)
    structure["sections"][0]["functions"] = ["invented_function"]
    write_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH, structure)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "unknown section function 'invented_function'",
    )


def test_unexpected_structure_top_level_field_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH)
    structure["candidate_section_functions"] = []
    write_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH, structure)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "unexpected top-level field 'candidate_section_functions'",
    )


@pytest.mark.parametrize(
    ("field", "source"),
    [
        ("schema_version", "schema/speech-schema.yaml"),
        ("vocabulary_version", "schema/vocabulary.yaml"),
    ],
)
def test_wrong_tags_version_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    field: str,
    source: str,
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags[field] = "9.9.9"
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        f"{field} '9.9.9' does not match {source}",
    )


def test_approved_candidate_missing_from_vocabulary_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidates = read_yaml(corpus_root, CANDIDATES_PATH)
    candidates["candidate_tags"].append(
        candidate_record(
            corpus_root,
            candidate="invented_theme",
            status="approved",
        )
    )
    write_yaml(corpus_root, CANDIDATES_PATH, candidates)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "approved candidate 'invented_theme' does not exist",
    )


def test_empty_speech_level_rationale_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["speech_level"]["purposes"]["primary"][0]["rationale"] = ""
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "speech_level.purposes.primary[1] has no usable rationale",
    )


def test_missing_passage_annotation_field_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    del tags["passage_annotations"][0]["evidence"]
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "passage_annotations[1] is missing: evidence",
    )


@pytest.mark.parametrize("field", ["evidence", "rationale"])
def test_empty_passage_annotation_text_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    field: str,
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][0][field] = "  "
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        f"passage_annotations[1] has no usable {field}",
    )


def test_duplicate_speech_level_tag_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    themes = tags["speech_level"]["themes"]
    themes.append(copy.deepcopy(themes[0]))
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "speech_level.themes has duplicate tag 'freedom'",
    )


def test_missing_section_rationale_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH)
    del structure["sections"][0]["rationale"]
    write_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH, structure)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "section 's01' has no usable rationale",
    )


def test_non_sequential_paragraph_ids_fail(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    transcript_path = corpus_root / SYNTHETIC_TRANSCRIPT_PATH
    transcript = transcript_path.read_text(encoding="utf-8")
    transcript_path.write_text(
        transcript.replace("[p003]", "[p004]"), encoding="utf-8"
    )

    structure = read_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH)
    structure["sections"][1]["paragraphs"] = ["p004"]
    write_yaml(corpus_root, SYNTHETIC_STRUCTURE_PATH, structure)

    tags = read_yaml(corpus_root, SYNTHETIC_TAGS_PATH)
    tags["passage_annotations"][1]["paragraphs"] = ["p004"]
    write_yaml(corpus_root, SYNTHETIC_TAGS_PATH, tags)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "paragraph IDs must be sequential starting at p001",
    )


def test_malformed_pending_candidate_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidates = read_yaml(corpus_root, CANDIDATES_PATH)
    candidate = candidate_record(corpus_root)
    candidate.update(
        {
            "proposed_category": "invented_category",
            "speech": "missing-speech",
            "section": "s999",
            "paragraphs": ["p999"],
            "reason": "",
        }
    )
    candidates["candidate_tags"].append(candidate)
    write_yaml(corpus_root, CANDIDATES_PATH, candidates)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "candidate_tags[1] has invalid proposed_category 'invented_category'",
    )


def test_invalid_approved_vocabulary_version_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidates = read_yaml(corpus_root, CANDIDATES_PATH)
    candidate = candidate_record(corpus_root, status="approved")
    candidate["approved_in_vocabulary_version"] = "banana"
    candidates["candidate_tags"].append(candidate)
    write_yaml(corpus_root, CANDIDATES_PATH, candidates)
    assert_validation_fails(
        validator_module,
        corpus_root,
        monkeypatch,
        capsys,
        "invalid approved_in_vocabulary_version 'banana'",
    )
