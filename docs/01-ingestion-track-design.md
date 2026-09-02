---
date: 2026-09-02
version: 0.1
---

# Speech Refinery

## 1 Human documentation
- docs/refinery-runbook.md (source of truth, not written yet)
- docs/refinery-workflow.mmd (generated visual, not written yet)

## 2 Tracks

### 2.1 Ingestion

#### 2.1.1 Transcript Stage

##### 2.1.1.1 Codex inputs
- Source A
- schema/speech-refinery-skill.md (not written yet)
- schema/transcript-guide.md 
- tools/transcript-preflight.py (future) 
- tools/validate-transcript.py (future)

##### 2.1.1.2 Flow
```
Prompt X1
        │
        ▼
speech-refinery-skill.md
        │
        ▼
transcript-guide.md
        │
        ▼
source A
        │
        ▼
transcript-preflight.py      (future)
        │
        ▼
Create 01-transcript.md
        │
        ▼
validate-transcript.py       (future)
        │
        ▼
Human review
        │
        ▼
Git commit
```
#### 2.1.2 Structure Stage

##### 2.1.2.1 Codex inputs
- schema/speech-refinery-skill.md (not written yet)
- schema/structure-guide.md
- schema/speech-schema.yaml
- speeches/{{speech-id}}/01-transcript.md
- tools/structure-preflight.py (future)
- tools/validate-structure.py (future)

##### 2.1.2.2 Flow
```
Prompt X2
        │
        ▼
speech-refinery-skill.md
        │
        ▼
structure-guide.md
        │
        ├──────────────┐
        ▼              ▼
speech-schema.yaml   01-transcript.md
        │              │
        └──────┬───────┘
               ▼
structure-preflight.py      (future)
               │
               ▼
Create 02-structure.yaml
               │
               ▼
validate-structure.py       (future)
               │
               ▼
Human review
               │
               ▼
Git commit
```

#### 2.1.3 Tags Stage

##### 2.1.3.1 Codex Inputs
- schema/speech-refinery-skill.md (not written yet)
- schema/tags-guide.md
- schema/tagging-guide.md
- schema/speech-schema.yaml
- schema/vocabulary.yaml
- speeches/{{speech-id}}/01-transcript.md
- speeches/{{speech-id}}/02-structure.yaml
- tools/tags-preflight.py (future)
- tools/validate-tags.py

##### 2.1.3.2 Flow
```
Prompt X3
        │
        ▼
speech-refinery-skill.md
        │
        ▼
tags-guide.md
        │
        ├──────────────────────────────┐
        ▼                              ▼
tagging-guide.md                speech-schema.yaml
        │                              │
        ├──────────────┐               │
        ▼              ▼               ▼
vocabulary.yaml   01-transcript.md  02-structure.yaml
        │              │               │
        └──────────────┴───────┬───────┘
                               ▼
tags-preflight.py          (future)
                               │
                               ▼
Create 03-tags.yaml
                               │
                               ▼
validate-tags.py
                               │
                               ▼
pytest
                               │
                               ▼
Human review
                               │
                               ▼
Git commit
```


#### 2.1.4 Analysis Stage

##### 2.1.4.1 Codex Inputs
- schema/speech-refinery-skill.md (not written yet)
- schema/analysis-guide.md
- schema/speech-schema.yaml
- schema/vocabulary.yaml
- speeches/{{speech-id}}/01-transcript.md
- speeches/{{speech-id}}/02-structure.yaml
- speeches/{{speech-id}}/03-tags.yaml
- tools/analysis-preflight.py (future)
- tools/validate-analysis.py (future)
##### 2.1.4.2 Flow
```
Prompt X4
        │
        ▼
speech-refinery-skill.md
        │
        ▼
analysis-guide.md
        │
        ├──────────────────────────────┐
        ▼                              ▼
speech-schema.yaml             vocabulary.yaml
        │                              │
        ├──────────────┬───────────────┘
        ▼              ▼
01-transcript.md   02-structure.yaml
        │              │
        └──────┬───────┘
               ▼
        03-tags.yaml
               │
               ▼
analysis-preflight.py      (future)
               │
               ▼
Create 04-analysis.md
               │
               ▼
validate-analysis.py       (future)
               │
               ▼
Human review
               │
               ▼
Git commit
```

