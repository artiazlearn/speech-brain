# Analysis Stage Launcher

stage: Analysis
speech_id: {{speech_id}}
inputs:

- speeches/{{speech_id}}/01-transcript.md
- speeches/{{speech_id}}/02-structure.yaml
- speeches/{{speech_id}}/03-tags.yaml

target_output: speeches/{{speech_id}}/04-analysis.md
speech_specific_cautions: {{speech_specific_cautions}}

Use `None` when there are no speech-specific cautions. Include only cautions genuinely specific to this speech or source; do not place reusable rules here.

Authoritative references:

- `skills/speech-refinery/SKILL.md`
- `schema/analysis-guide.md`

Follow the refinery skill and stage-specific authoritative files. Do not treat this prompt as permission to redefine, supplement, or override reusable framework rules. If this prompt conflicts with an authoritative repository instruction, report the conflict instead of silently resolving it.

Stop after the Analysis-stage gate.
Do not proceed to another track.
