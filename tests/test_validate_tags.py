"""End-to-end tests for the speech-corpus tag validator."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import re
import shutil
from types import ModuleType
from typing import Any

import pytest
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate-tags.py"
CORPUS_DIRECTORIES = ("schema", "review", "speeches")
CHURCHILL_TAGS = Path("speeches/churchill-1940-fight-on-beaches/03-tags.yaml")
CHURCHILL_STRUCTURE = Path(
    "speeches/churchill-1940-fight-on-beaches/02-structure.yaml"
)
JFK_TRANSCRIPT = Path("speeches/jfk-1961-inaugural/01-transcript.md")
JFK_STRUCTURE = Path("speeches/jfk-1961-inaugural/02-structure.yaml")
JFK_TAGS = Path("speeches/jfk-1961-inaugural/03-tags.yaml")
CANDIDATES = Path("review/candidate-tags.yaml")
PARAGRAPH_MARKER = re.compile(r"^\[(p\d{3})\]\s*$", re.MULTILINE)


@pytest.fixture(scope="session")
def validator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "speech_corpus_validate_tags", VALIDATOR_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def corpus_root(tmp_path: Path) -> Path:
    root = tmp_path / "corpus"
    root.mkdir()
    for directory in CORPUS_DIRECTORIES:
        shutil.copytree(PROJECT_ROOT / directory, root / directory)
    return root


def read_yaml(root: Path, relative_path: Path) -> dict[str, Any]:
    with (root / relative_path).open(encoding="utf-8") as handle:
        document = yaml.safe_load(handle)
    assert isinstance(document, dict)
    return document


def write_yaml(root: Path, relative_path: Path, document: dict[str, Any]) -> None:
    with (root / relative_path).open("w", encoding="utf-8") as handle:
        yaml.safe_dump(
            document,
            handle,
            allow_unicode=True,
            sort_keys=False,
            width=100,
        )


def run_validator(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> tuple[int, str]:
    monkeypatch.setattr(validator_module, "ROOT", corpus_root)
    result = validator_module.main()
    output = capsys.readouterr().out
    return result, output


def find_annotation(
    tags: dict[str, Any], category: str, tag: str
) -> dict[str, Any]:
    for annotation in tags["passage_annotations"]:
        if annotation["category"] == category and annotation["tag"] == tag:
            return annotation
    raise AssertionError(f"No {category} annotation found for {tag}")


def test_valid_current_corpus_passes(
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
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    annotation = find_annotation(tags, "rhetorical_devices", "antithesis")
    annotation["tag"] = "beautiful_contrast"
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "unknown rhetorical_devices tag 'beautiful_contrast'" in output


def test_invalid_confidence_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    tags["speech_level"]["purposes"]["primary"][0]["confidence"] = "maybe"
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "invalid confidence 'maybe'" in output


def test_unknown_paragraph_reference_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    tags["passage_annotations"][0]["paragraphs"][0] = "p999"
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "references unknown paragraph 'p999'" in output


def test_unknown_section_reference_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    tags["passage_annotations"][0]["section"] = "s999"
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "references unknown section 's999'" in output


def test_too_many_primary_purposes_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    purposes = tags["speech_level"]["purposes"]
    purposes["primary"].append(purposes["secondary"].pop(0))
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "no more than 4 primary purposes are allowed" in output


def test_primary_secondary_overlap_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    purposes = tags["speech_level"]["purposes"]
    purposes["secondary"].append(copy.deepcopy(purposes["primary"][0]))
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "cannot be both primary and secondary" in output


def test_duplicate_section_membership_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, CHURCHILL_STRUCTURE)
    duplicate = structure["sections"][0]["paragraphs"][0]
    structure["sections"][1]["paragraphs"].append(duplicate)
    write_yaml(corpus_root, CHURCHILL_STRUCTURE, structure)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "appears multiple times in sections" in output


def test_missing_section_membership_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, CHURCHILL_STRUCTURE)
    missing = structure["sections"][0]["paragraphs"].pop(0)
    write_yaml(corpus_root, CHURCHILL_STRUCTURE, structure)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert f"transcript paragraph '{missing}' belongs to no section" in output


def test_unknown_section_function_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, CHURCHILL_STRUCTURE)
    structure["sections"][0]["functions"][0] = "explain_magic"
    write_yaml(corpus_root, CHURCHILL_STRUCTURE, structure)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "unknown section function 'explain_magic'" in output


def test_unexpected_structure_top_level_field_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure_path = next(
        path.relative_to(corpus_root)
        for path in (corpus_root / "speeches").glob("*/02-structure.yaml")
    )
    structure = read_yaml(corpus_root, structure_path)
    structure["candidate_section_functions"] = []
    write_yaml(corpus_root, structure_path, structure)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "unexpected top-level field 'candidate_section_functions'" in output


def test_wrong_schema_version_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    tags["schema_version"] = "9.9.9"
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "schema_version '9.9.9' does not match" in output


def test_approved_candidate_missing_from_vocabulary_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidates = read_yaml(corpus_root, CANDIDATES)
    candidates["candidate_tags"].append(
        {
            "candidate": "missing_canonical_theme",
            "proposed_category": "themes",
            "speech": "churchill-1940-fight-on-beaches",
            "section": "s01",
            "paragraphs": ["p001"],
            "reason": "A deliberately invalid approved candidate for validation.",
            "possible_existing_tags": [],
            "status": "approved",
            "approved_in_vocabulary_version": "0.2.0",
        }
    )
    write_yaml(corpus_root, CANDIDATES, candidates)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "approved candidate 'missing_canonical_theme' does not exist" in output


def test_empty_speech_level_rationale_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    tags["speech_level"]["purposes"]["primary"][0]["rationale"] = ""
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "rationale" in output.lower()


def test_duplicate_speech_level_tag_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tags = read_yaml(corpus_root, CHURCHILL_TAGS)
    themes = tags["speech_level"]["themes"]
    themes.append(copy.deepcopy(themes[0]))
    write_yaml(corpus_root, CHURCHILL_TAGS, tags)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "duplicate" in output.lower()


def test_missing_section_rationale_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    structure = read_yaml(corpus_root, CHURCHILL_STRUCTURE)
    del structure["sections"][0]["rationale"]
    write_yaml(corpus_root, CHURCHILL_STRUCTURE, structure)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "rationale" in output.lower()


def test_non_sequential_paragraph_ids_fail(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    transcript_path = corpus_root / JFK_TRANSCRIPT
    transcript = transcript_path.read_text(encoding="utf-8")
    paragraph_ids = PARAGRAPH_MARKER.findall(transcript)
    assert len(paragraph_ids) >= 3

    shifted_ids = {
        paragraph_id: f"p{int(paragraph_id[1:]) + 1:03d}"
        for paragraph_id in paragraph_ids[2:]
    }
    transcript = PARAGRAPH_MARKER.sub(
        lambda match: f"[{shifted_ids.get(match.group(1), match.group(1))}]",
        transcript,
    )
    transcript_path.write_text(transcript, encoding="utf-8")

    structure = read_yaml(corpus_root, JFK_STRUCTURE)
    for section in structure["sections"]:
        section["paragraphs"] = [
            shifted_ids.get(paragraph, paragraph)
            for paragraph in section["paragraphs"]
        ]
    write_yaml(corpus_root, JFK_STRUCTURE, structure)

    tags = read_yaml(corpus_root, JFK_TAGS)
    for annotation in tags["passage_annotations"]:
        annotation["paragraphs"] = [
            shifted_ids.get(paragraph, paragraph)
            for paragraph in annotation["paragraphs"]
        ]
    write_yaml(corpus_root, JFK_TAGS, tags)

    candidates = read_yaml(corpus_root, CANDIDATES)
    for candidate in candidates["candidate_tags"]:
        if candidate.get("speech") == "jfk-1961-inaugural":
            candidate["paragraphs"] = [
                shifted_ids.get(paragraph, paragraph)
                for paragraph in candidate["paragraphs"]
            ]
    write_yaml(corpus_root, CANDIDATES, candidates)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "sequential" in output.lower()


def test_malformed_pending_candidate_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidates = read_yaml(corpus_root, CANDIDATES)
    candidates["candidate_tags"].append(
        {
            "candidate": "malformed_candidate",
            "proposed_category": "imaginary_category",
            "speech": "nonexistent-speech",
            "section": "s999",
            "paragraphs": ["p999"],
            "reason": "",
            "possible_existing_tags": [],
            "status": "pending_review",
        }
    )
    write_yaml(corpus_root, CANDIDATES, candidates)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "candidate" in output.lower()


def test_invalid_approved_vocabulary_version_fails(
    validator_module: ModuleType,
    corpus_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidates = read_yaml(corpus_root, CANDIDATES)
    approved = next(
        candidate
        for candidate in candidates["candidate_tags"]
        if candidate["status"] == "approved"
    )
    approved["approved_in_vocabulary_version"] = "banana"
    write_yaml(corpus_root, CANDIDATES, candidates)

    result, output = run_validator(
        validator_module, corpus_root, monkeypatch, capsys
    )

    assert result == 1, output
    assert "approved_in_vocabulary_version" in output
