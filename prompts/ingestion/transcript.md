# Transcript Stage Launcher

stage: Transcript
speech_id: {{speech_id}}
source: {{source_path}}
target_output: speeches/{{speech_id}}/01-transcript.md
speech_specific_cautions: {{speech_specific_cautions}}

Use `None` when there are no speech-specific cautions. Include only cautions genuinely specific to this speech or source; do not place reusable rules here.

Authoritative references:

- `skills/speech-refinery/SKILL.md`
- `schema/transcript-guide.md`

Follow the refinery skill and stage-specific authoritative files. Do not treat this prompt as permission to redefine, supplement, or override reusable framework rules. If this prompt conflicts with an authoritative repository instruction, report the conflict instead of silently resolving it.

Stop after the Transcript-stage gate.
Do not proceed to Structure.
