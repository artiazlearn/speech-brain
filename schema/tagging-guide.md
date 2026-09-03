# Speech Corpus Tagging Guide

This guide defines how the canonical tags in `vocabulary.yaml` are interpreted and applied. Tags describe evidence in a speech; they should not be inferred solely from a speaker's identity, historical reputation, or presumed intent. Apply the most specific supported tag, and apply multiple tags when the evidence independently supports each one.

## Rhetorical devices

Rhetorical-device tags identify language-level techniques. They may describe a passage without defining the function of the larger section containing it.

### `antithesis`

- **Definition:** The balanced presentation of contrasting or opposing ideas.
- **Use when:** A passage places genuine opposites or alternatives against each other, often in corresponding grammatical forms.
- **Do not use when:** Phrases merely share a grammatical structure without expressing a meaningful contrast; use `parallelism` alone in that case.
- **Related tags:** `parallelism`, `contrast_alternatives`.
- **Example:** “We seek cooperation, not conflict.”

### `anaphora`

- **Definition:** Deliberate repetition at the beginning of successive clauses or sentences.
- **Use when:** The same opening word or phrase recurs across at least two adjacent or closely grouped units for rhetorical effect.
- **Do not use when:** Repeated language occurs elsewhere in the units or without a consistent initial position; use `repetition` instead.
- **Related tags:** `repetition`, `parallelism`, `build_to_climax`.
- **Example:** “We will work. We will endure. We will prevail.”

### `parallelism`

- **Definition:** The use of similar grammatical structures in coordinated words, phrases, clauses, or sentences.
- **Use when:** Corresponding units follow a recognizably similar syntactic pattern, whether or not their ideas contrast.
- **Do not use when:** The connection rests only on repeated vocabulary and there is no meaningful structural correspondence. Do not assume `antithesis` unless the ideas oppose each other.
- **Related tags:** `antithesis`, `anaphora`, `repetition`, `tricolon`.
- **Example:** “To serve with courage, to lead with honesty, to act with care.”

### `repetition`

- **Definition:** The broad, deliberate reuse of words, phrases, or structures for emphasis, cohesion, rhythm, or recall.
- **Use when:** Material recurs in a rhetorically meaningful way, including repeated language that does not occur at the beginnings of successive units.
- **Do not use when:** Recurrence is incidental, required by grammar, or too slight to carry rhetorical force. Use `anaphora` as the more specific tag when repetition occurs at successive beginnings; both may be applied when both levels of description are useful.
- **Related tags:** `anaphora`, `parallelism`, `build_to_climax`.
- **Example:** “The work is ours, and ours is the responsibility.”

### `tricolon`

- **Definition:** A sequence of three coordinated and usually parallel rhetorical units.
- **Use when:** Three words, phrases, or clauses are arranged as a deliberate set with rhetorical weight.
- **Do not use when:** A passage contains an incidental list of three items without a shaped rhetorical sequence, or contains only two coordinated units.
- **Related tags:** `parallelism`, `repetition`, `build_to_climax`.
- **Example:** “We will listen, we will learn, and we will lead.”

### `metaphor`

- **Definition:** A nonliteral comparison or conceptual framing in which one thing is described in terms of another.
- **Use when:** The transferred image or concept meaningfully shapes how an audience understands the subject.
- **Do not use when:** Language is literal, merely decorative without a comparison, or a conventional expression with no relevant figurative force in context.
- **Related tags:** `reframe_problem`, `raise_stakes`.
- **Example:** “The nation stands at a crossroads.”

### `simile`

- **Definition:** An explicit figurative comparison between unlike things, typically signaled by words such as "like" or "as."
- **Use when:** The comparison is explicitly stated rather than implied.
- **Do not use when:** One thing is directly described as another without an explicit comparison; use `metaphor` instead.

### `allusion`

- **Definition:** A reference to a recognizable literary, historical, cultural, religious, or other prior source that draws meaning from the audience's recognition of that reference.
- **Use when:** The passage invokes a prior text, person, event, tradition, or cultural source so that its associations contribute to the present message.
- **Do not use when:** A speaker merely reports a historical fact, explains a past event, or uses language that resembles another source without a meaningful reference.
- **Related tags:** `metaphor`, `simile`, `establish_shared_values`. Unlike an ordinary historical reference, an allusion depends on the prior source's associations to add rhetorical meaning.

### `rhetorical_question`

- **Definition:** A question posed primarily to make a point, frame an issue, or prompt reflection rather than obtain an answer.
- **Use when:** The context supplies or implies the answer, or the speaker proceeds without expecting an audience response.
- **Do not use when:** The speaker is genuinely requesting information or explicitly soliciting an answer.
- **Related tags:** `direct_address`, `personalize_responsibility`, `call_to_action`.
- **Example:** “What kind of future will we choose?”

### `imperative`

- **Definition:** Command or directive language that tells an audience or another party to do, consider, or refrain from something.
- **Use when:** The grammar or clear force of the expression is directive, including an understood subject such as “you.”
- **Do not use when:** A passage merely describes desirable action or states a goal. `imperative` is a language-level device; `call_to_action` is a section function in which a larger passage urges action, and the two are not interchangeable.
- **Related tags:** `call_to_action`, `mobilize`, `direct_address`.
- **Example:** “Stand together and defend the truth.”

### `direct_address`

- **Definition:** Language in which the speaker explicitly speaks to or names a person, group, institution, or audience.
- **Use when:** Vocatives, second-person references, or explicit audience naming create a direct speaker-to-audience relationship.
- **Do not use when:** A group is merely discussed in the third person. `direct_address` marks a rhetorical device in particular language; `address_audience_group` marks the function of a larger section.
- **Related tags:** `address_audience_group`, `address_audience_groups`, `address_adversary`, `imperative`.
- **Example:** “Friends and fellow citizens, this choice belongs to you.”

## Section functions

Section-function tags identify the rhetorical roles performed by a coherent section. They operate at a larger structural level than individual rhetorical devices.

### `opening`

- **Definition:** The section that begins the speech and establishes the initial relationship, setting, or direction.
- **Use when:** A passage performs the speech's entry function, such as greeting the audience, acknowledging the occasion, or introducing the central concern.
- **Do not use when:** A later section restarts an argument or introduces a new topic but does not begin the speech.
- **Related tags:** `reframe_occasion`, `establish_values`.
- **Example:** An initial greeting followed by a concise statement of why the gathering matters.

### `reframe_occasion`

- **Definition:** A section that interprets the event or moment as meaning something different, broader, or more consequential than its surface purpose.
- **Use when:** The section explicitly recasts what the audience is witnessing or why the occasion matters.
- **Do not use when:** It merely describes the event, offers background, or changes the framing of a problem rather than the occasion; use `reframe_problem` for the latter.
- **Related tags:** `opening`, `reframe_problem`, `reframe_occasion` in writing patterns.
- **Example:** Presenting a ceremony not as a routine transition but as a renewal of public commitments.

### `commemorate`

- **Definition:** A section whose rhetorical job is substantially to honor or preserve the memory of people, sacrifice, achievement, or loss.
- **Use when:** A coherent passage recalls character, service, achievement, or sacrifice in order to lead remembrance or pay tribute.
- **Do not use when:** A person or past event is merely mentioned, or admirable qualities are stated principally to establish standards for later judgment; use `establish_values` for the latter function.
- **Related tags:** `establish_values`, `closing`, `commemorate` in purposes. Commemoration centers memory and honor, whereas `establish_values` centers the principles that orient an argument or course of conduct.

### `console`

- **Definition:** A section whose rhetorical job is substantially to acknowledge suffering, shock, or grief and offer comfort, solidarity, meaning, or emotional orientation.
- **Use when:** A passage directly responds to people experiencing pain or irreversible loss and helps them bear or interpret that experience.
- **Do not use when:** A passage is merely grave or sympathetic, or chiefly reduces fear, uncertainty, or doubt by supplying grounds for confidence.
- **Related tags:** `address_audience_group`, `reframe_problem`, `console` and `reassure` in purposes. Consolation addresses suffering that cannot simply be undone; reassurance addresses uncertainty or fear that confidence may reduce.

### `establish_values`

- **Definition:** A section that states or grounds the principles by which the speech's argument, choices, or actions should be judged.
- **Use when:** The section's main function is to articulate values that orient the rest of the speech.
- **Do not use when:** Values are mentioned only incidentally or a recurring technique invokes common ground without forming the section's primary function. `establish_values` is a section function; `establish_shared_values` is a reusable writing pattern.
- **Related tags:** `establish_shared_values`, `freedom`, `civic_duty`, `responsibility`.
- **Example:** A section declaring dignity and equal treatment to be the standards for future policy.

### `address_audience_group`

- **Definition:** A section organized around speaking to the concerns, duties, or relationship of a particular audience group.
- **Use when:** A substantial section turns toward one named constituency and tailors its message to that group.
- **Do not use when:** A group receives only a brief salutation or isolated second-person reference. `address_audience_group` is structural; `direct_address` is a rhetorical device in the wording.
- **Related tags:** `direct_address`, `address_audience_groups`, `address_adversary`.
- **Example:** A full passage directed to workers about their role in a national program.

### `address_adversary`

- **Definition:** A section directed toward, or explicitly framing a message for, an opponent or potentially hostile party.
- **Use when:** The speaker presents warnings, terms, appeals, boundaries, or opportunities specifically for an adversary.
- **Do not use when:** The speech only mentions opposition, criticizes an idea, or describes a threat without directing a sustained message toward the opposing party.
- **Related tags:** `address_audience_group`, `direct_address`, `warn`, `conciliatory`.
- **Example:** A section offering negotiations to a rival while stating limits that will be defended.

### `explain_problem`

- **Definition:** A section that describes the nature, causes, scope, or consequences of a problem.
- **Use when:** The section primarily helps the audience understand what is wrong and how the problem operates.
- **Do not use when:** It only announces that a problem exists, focuses chiefly on the consequences of failure, or changes the audience's interpretation of the problem.
- **Related tags:** `define_stakes`, `reframe_problem`, `raise_stakes`.
- **Example:** A passage tracing how institutional failures produced a continuing public crisis.

### `define_stakes`

- **Definition:** A section that identifies what may be gained, lost, protected, or endangered by the situation or choice.
- **Use when:** The section makes the consequences and significance of action or inaction its main focus.
- **Do not use when:** It merely explains the mechanics of a problem or adds intensity without clearly identifying consequences.
- **Related tags:** `raise_stakes`, `warn`, `define_stakes` in purposes.
- **Example:** A section explaining that the decision will affect both present security and the opportunities of future generations.

### `reframe_problem`

- **Definition:** A section that changes how the audience is asked to understand the nature, cause, scale, or ownership of a problem.
- **Use when:** The section replaces or significantly revises an existing interpretation of the problem.
- **Do not use when:** It only supplies more detail under the existing interpretation, or recasts the ceremonial occasion rather than the problem.
- **Related tags:** `explain_problem`, `reframe_occasion`, `personalize_responsibility`.
- **Example:** Recasting an economic difficulty from a temporary shortage into a question of institutional fairness.

### `personalize_responsibility`

- **Definition:** Translate an abstract, institutional, national, or collective issue into a responsibility personally borne by the audience or listener.
- **Use when:** The speaker makes listeners personally responsible for an outcome, decision, duty, or course of action.
- **Do not use when:** The speaker merely identifies a named person as responsible for causing an event, assigns blame, or describes someone's individual actions.
- **Related tags:** `personalize_responsibility` in writing patterns, `transfer_responsibility_to_audience`, `civic_duty`, `responsibility`.
- **Example:** A passage moving from national goals to the choices each citizen must make.

### `climax`

- **Definition:** The section that forms the speech's principal rhetorical, emotional, or argumentative high point.
- **Use when:** The speech's accumulated force culminates in a clearly heightened and pivotal passage.
- **Do not use when:** A passage is merely emphatic, memorable, or late in the speech. `climax` identifies the high-point section; `build_to_climax` describes the writing pattern that creates escalation toward it.
- **Related tags:** `build_to_climax`, `call_to_action`, `tricolon`, `anaphora`.
- **Example:** The speech's strongest synthesis of its central claim immediately before the final appeal.

### `call_to_action`

- **Definition:** A section whose main function is to urge the audience or another party toward a specific action, commitment, or course of conduct.
- **Use when:** The section moves beyond approval or reflection and asks for action, whether immediate or sustained.
- **Do not use when:** Directive wording is isolated or incidental, or the passage only expresses hope. `call_to_action` is a structural function; `imperative` is a linguistic device and may occur outside a call-to-action section.
- **Related tags:** `imperative`, `mobilize`, `transfer_responsibility_to_audience`, `call_to_action` in purposes.
- **Example:** A concluding passage asking citizens to volunteer, vote, or organize.

### `closing`

- **Definition:** The final section that completes the speech through summary, resolution, farewell, blessing, final appeal, or a combination of these.
- **Use when:** A passage performs the speech's terminal function and supplies a sense of completion.
- **Do not use when:** A section merely contains a strong line near the end but is followed by substantial new argument.
- **Related tags:** `climax`, `call_to_action`, `reassure`.
- **Example:** A final restatement of commitment followed by a brief farewell.

## Writing patterns

Writing-pattern tags identify reusable compositional strategies that may operate across one or more sections. They describe how a speech is built, not merely what one section is called.

### `narrative_reconstruction`

- **Definition:** Reconstructing a sequence of past events in chronological or causal order so the audience can understand how the present situation developed.
- **Use when:** The speaker substantially organizes past events into a sequence that establishes context, causality, credibility, or interpretation.
- **Do not use when:** The speech merely mentions historical facts, examples, or isolated anecdotes without reconstructing a meaningful sequence.

### `reframe_occasion`

- **Definition:** A compositional strategy that turns the immediate event into a broader symbolic, moral, historical, or political moment.
- **Use when:** The speech deliberately uses a new interpretation of the occasion to support its larger message.
- **Do not use when:** The occasion is simply acknowledged or described. When labeling the primary function of a specific section, use `reframe_occasion` in section functions.
- **Related tags:** `reframe_occasion` in section functions, `reframe_problem`, `establish_shared_values`.
- **Example:** Using an anniversary as a lens through which to renew unfinished commitments.

### `establish_shared_values`

- **Definition:** A compositional strategy that creates common ground by invoking principles the speaker presents as shared with the audience.
- **Use when:** Shared beliefs are used to build identification, authorize an argument, or bridge differences.
- **Do not use when:** The speaker merely states personal beliefs or names a value without presenting it as common ground. `establish_shared_values` is a writing pattern; `establish_values` is the primary function of a section.
- **Related tags:** `establish_values`, `unify`, `national_unity`.
- **Example:** Beginning a contested proposal from a principle that both sides publicly affirm.

### `address_audience_groups`

- **Definition:** A compositional strategy that organizes successive parts of a speech around messages to multiple distinct constituencies.
- **Use when:** The speech systematically moves from one audience group to another, adapting the appeal or commitment for each.
- **Do not use when:** Only one constituency is addressed, groups are merely listed, or direct address occurs sporadically. A single section serving one group may take `address_audience_group` as its section function.
- **Related tags:** `address_audience_group`, `address_adversary`, `direct_address`.
- **Example:** Separate passages directed in turn to citizens, allies, rivals, and future generations.

### `contrast_alternatives`

- **Definition:** A compositional strategy that clarifies a choice by placing competing paths, outcomes, values, or positions beside each other.
- **Use when:** Contrast structures the audience's understanding of the available options and their consequences.
- **Do not use when:** A passage contains a local verbal opposition with no larger role in shaping alternatives; that may be `antithesis` alone.
- **Related tags:** `antithesis`, `define_stakes`, `raise_stakes`, `persuade`.
- **Example:** Developing one future under cooperation and another under continued division.

### `raise_stakes`

- **Definition:** A compositional strategy that progressively increases the perceived urgency, scale, consequence, or moral weight of an issue.
- **Use when:** Later material deliberately makes the issue matter more than it appeared to earlier in the speech.
- **Do not use when:** Consequences are stated once without escalation, or the section simply identifies what is at risk; use `define_stakes` for that structural function.
- **Related tags:** `define_stakes`, `warn`, `build_to_climax`.
- **Example:** Moving from a local cost, to national stability, to the welfare of future generations.

### `personalize_responsibility`

- **Definition:** Translate an abstract, institutional, national, or collective issue into a responsibility personally borne by the audience or listener.
- **Use when:** The speaker makes listeners personally responsible for an outcome, decision, duty, or course of action.
- **Do not use when:** The speaker merely identifies a named person as responsible for causing an event, assigns blame, or describes someone's individual actions.
- **Related tags:** `personalize_responsibility` in section functions, `transfer_responsibility_to_audience`, `responsibility`, `civic_duty`.
- **Example:** Moving from “the nation must change” to the specific conduct expected of every listener.

### `build_to_climax`

- **Definition:** A compositional strategy that arranges language, claims, images, or appeals in increasing intensity toward a high point.
- **Use when:** Multiple preceding units create discernible escalation and prepare a later culmination.
- **Do not use when:** A strong passage appears without meaningful preparation, or when labeling the high-point section itself. `build_to_climax` describes the ascent; `climax` identifies the high point.
- **Related tags:** `climax`, `raise_stakes`, `anaphora`, `tricolon`.
- **Example:** A series of increasingly consequential commitments culminating in the speech's central demand.

### `transfer_responsibility_to_audience`

- **Definition:** A compositional strategy that shifts agency, duty, or the burden of the outcome from the speaker or institutions to the audience.
- **Use when:** The speech explicitly makes listeners responsible for carrying forward the argument, work, choice, or commitment.
- **Do not use when:** The audience is only praised, addressed, or invited to agree, or when responsibility is personalized to someone other than the audience.
- **Related tags:** `personalize_responsibility`, `call_to_action`, `imperative`, `civic_duty`.
- **Example:** Concluding that success now depends on what listeners choose to do after the speech.

## Purposes

Purpose tags describe intended outcomes supported by the speech as a whole or by a substantial passage.

### Primary purposes

A primary purpose should satisfy most of these tests:

- It is central to why the speech was delivered.
- It is sustained across substantial parts of the speech.
- Removing it would materially change the reason the speech exists.
- It represents a major audience outcome the speaker is seeking.

Rules:

- A speech must have at least 1 primary purpose.
- Use no more than 4 primary purposes.
- Classify a purpose as primary only when it satisfies the tests above.

### Secondary purposes

A secondary purpose:

- meaningfully supports the speech,
- may occur strongly in only part of the speech,
- but is not one of the main reasons the speech exists.

A purpose cannot appear in both primary and secondary.

### `inform`

- **Definition:** The speech substantially reports, explains, or clarifies facts, events, circumstances, or a situation so the audience understands what has happened or what is happening.
- **Use when:** Providing understanding or situational awareness is an important purpose of the speech.
- **Do not use when:** The speech merely contains factual details in support of another purpose.

### `inspire`

- **Definition:** Elevate confidence, hope, courage, aspiration, or commitment.
- **Use when:** The speech seeks to make the audience feel capable of or devoted to a worthy effort.
- **Do not use when:** The passage is merely positive, ceremonial, or complimentary without an elevating aim.

### `persuade`

- **Definition:** Move the audience toward accepting a claim, judgment, policy, or course of action.
- **Use when:** Reasons, framing, evidence, or appeals are used to change or reinforce a position.
- **Do not use when:** The speech only informs, commemorates, or expresses a view without seeking audience assent.

### `reassure`

- **Definition:** Reduce fear, doubt, uncertainty, or mistrust by offering confidence or stability.
- **Use when:** The speech directly responds to actual or anticipated concern and seeks to calm it.
- **Do not use when:** Optimistic language does not address a concern or source of anxiety.

### `commemorate`

- **Definition:** Honor and preserve the memory of a person, group, event, or sacrifice, especially by recalling character, service, achievement, or loss.
- **Use when:** Remembrance or honoring the dead or past is a central intended audience outcome of the speech.
- **Do not use when:** A speech merely mentions a historical person or event, or invokes admirable principles chiefly to guide judgment or conduct.
- **Related tags:** `establish_values`, `inspire`, `commemorate` in section functions. Commemoration seeks remembrance and honor; `establish_values` seeks to articulate a guiding value framework.

### `console`

- **Definition:** Respond to grief, suffering, shock, or irreversible loss by acknowledging pain and offering comfort, solidarity, meaning, or emotional orientation.
- **Use when:** Helping an audience bear or interpret suffering is a substantial intended outcome of the speech.
- **Do not use when:** The speech chiefly reduces fear, uncertainty, doubt, or mistrust by offering grounds for confidence; use `reassure` for that outcome.
- **Related tags:** `reassure`, `unify`, `console` in section functions. A speech may both console an audience about irreversible loss and reassure it about what remains stable or possible.

### `warn`

- **Definition:** Alert the audience or another party to danger, harmful consequences, or unacceptable conduct.
- **Use when:** The speech makes a threat, risk, boundary, or consequence salient so it can be avoided or heeded.
- **Do not use when:** It neutrally describes risk or retrospectively recounts harm without an alerting purpose.

### `unify`

- **Definition:** Reduce division and strengthen a sense of common identity, interest, or commitment.
- **Use when:** The speech actively brings groups together or places shared bonds above differences.
- **Do not use when:** Inclusive pronouns appear without a substantive unifying appeal.

### `mobilize`

- **Definition:** Generate coordinated readiness, participation, or sustained collective effort.
- **Use when:** The speech seeks to activate people or institutions around a shared undertaking.
- **Do not use when:** It asks only for private agreement, reflection, or a single isolated act with no collective effort.

### `call_to_action`

- **Definition:** Urge an audience or another party to take a specific action or adopt a course of conduct.
- **Use when:** Producing action is an intended outcome of the speech or a substantial passage.
- **Do not use when:** Action is merely mentioned or directive language serves another local rhetorical role without an action-seeking purpose.

### `establish_values`

- **Definition:** Articulate the principles that should guide judgment, identity, policy, or conduct.
- **Use when:** Establishing or reaffirming a value framework is an intended outcome.
- **Do not use when:** A value is only a topic, incidental reference, or assumed premise.

### `define_stakes`

- **Definition:** Clarify what may be gained, lost, protected, or endangered.
- **Use when:** Making the significance and consequences of a choice or situation clear is an intended outcome.
- **Do not use when:** The speech describes a problem without clarifying why its outcome matters.

## Themes

Theme tags identify substantive ideas developed with meaningful emphasis, not every subject briefly mentioned.

### `freedom`

- **Definition:** Liberty from domination or constraint, or the capacity to exercise rights and agency.
- **Use when:** Freedom is a sustained subject, governing principle, or central object of protection or pursuit.
- **Do not use when:** The term appears incidentally or only as part of a conventional phrase.

### `civic_duty`

- **Definition:** Obligations people hold by virtue of citizenship or membership in a political community.
- **Use when:** The speech develops what citizens owe their community, institutions, or one another.
- **Do not use when:** It discusses responsibility that is purely personal, professional, or unrelated to civic membership.

### `responsibility`

- **Definition:** Accountability or obligation for choices, conduct, duties, or outcomes.
- **Use when:** The speech substantially develops who must answer for or undertake something.
- **Do not use when:** Duty or blame receives only a passing reference with no thematic development.

### `sacrifice`

- **Definition:** Willing acceptance of cost, loss, hardship, or self-denial for a larger purpose.
- **Use when:** The speech meaningfully presents giving something up or enduring hardship as necessary or honorable.
- **Do not use when:** It refers only to effort, inconvenience, or suffering not framed as serving a larger purpose.

### `peace`

- **Definition:** The prevention or ending of violent conflict and the creation or preservation of nonviolent relations.
- **Use when:** Peace is a sustained objective, condition, process, or subject of argument.
- **Do not use when:** It appears only as a greeting, general expression of goodwill, or incidental contrast with war.

### `national_unity`

- **Definition:** Cohesion, solidarity, or common purpose among the people or parts of a nation.
- **Use when:** The speech substantially addresses overcoming internal divisions or strengthening national togetherness.
- **Do not use when:** It invokes the nation without developing unity as an idea.

### `international_cooperation`

- **Definition:** Collaboration among nations or international institutions toward shared aims.
- **Use when:** The speech develops joint action, mutual commitments, alliances, negotiation, or multilateral problem-solving.
- **Do not use when:** It merely names other countries or discusses foreign affairs without a meaningful cooperative dimension.

### `poverty`

- **Definition:** Material deprivation, economic hardship, or lack of resources affecting individuals or populations.
- **Use when:** Poverty, deprivation, economic hardship, or unmet material needs are a substantive subject of the speech.
- **Do not use when:** The speech merely refers generally to struggle, sacrifice, inequality, or hardship without materially discussing poverty or deprivation.

## Tone

Tone tags describe sustained qualities of attitude or emotional character in the speech, not its subject or intended outcome. Apply them when the quality is supported across a meaningful portion of the speech; do not infer tone solely from the occasion, speaker, or an isolated phrase.

### `formal`

- **Definition:** A controlled, ceremonious, institutional, or elevated public register.
- **Use when:** Diction, syntax, forms of address, or measured presentation consistently give the speech an official or ceremonially serious character.
- **Do not use when:** The speech is merely delivered in an official setting or contains occasional polite language. `formal` describes register, whereas `sombre` describes emotional gravity.

### `idealistic`

- **Definition:** An aspirational attitude oriented toward principles, moral possibility, or a better future.
- **Use when:** The speech repeatedly reaches beyond immediate circumstances to present ideals as guides for collective judgment, identity, or action.
- **Do not use when:** The speech is merely optimistic, complimentary, or hopeful. `idealistic` describes the speech's outlook; `inspire` describes an intended audience outcome.

### `resolute`

- **Definition:** A firm, determined attitude marked by commitment despite difficulty, loss, doubt, or opposition.
- **Use when:** The speech repeatedly affirms that a duty, course, or undertaking will be sustained and not abandoned.
- **Do not use when:** The speech contains only isolated certainty or forceful wording. `resolute` emphasizes commitment; `challenging` emphasizes pressure placed on an audience, opponent, or assumption.

### `challenging`

- **Definition:** A demanding or confrontational attitude that presses others to meet a standard, reconsider an assumption, or face an unwelcome choice or difficulty.
- **Use when:** The speech persistently tests, rebukes, confronts, or makes exacting demands of an audience, institution, or adversary.
- **Do not use when:** The subject itself is difficult or the speaker merely states a firm position. A speech may be `resolute` without directing a challenge toward others.

### `conciliatory`

- **Definition:** An accommodating attitude that seeks common ground, reduced hostility, negotiation, or repaired relations across disagreement.
- **Use when:** The speech offers cooperation, mutual restraint, or a credible path toward agreement while acknowledging division or conflict.
- **Do not use when:** The language is merely courteous or the speech invokes unity without addressing disagreement. `conciliatory` describes the manner of approaching division; `unify` describes an intended outcome.

### `sombre`

- **Definition:** A grave, mournful, or emotionally weighty attitude shaped by loss, danger, suffering, or tragic consequence.
- **Use when:** The speech sustains gravity through mourning, acknowledgment of suffering, or serious contemplation of destructive stakes.
- **Do not use when:** The speech is merely formal or discusses a serious subject without a sustained grave emotional character. A `sombre` tone does not by itself imply the purpose `console`.
