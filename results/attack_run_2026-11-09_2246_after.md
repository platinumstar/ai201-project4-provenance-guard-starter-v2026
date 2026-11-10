# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 22:46
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `d85e7ebf-82b2-48aa-8766-b1bc31f49617` | human | 0.458 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b9c0ea52-a92b-4cdb-9359-5f0e229abd06` | unsure | 0.523 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d1460d4f-309b-4150-ab7a-e474d63257dc` | ai | 0.654 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `3617b3c0-5d8f-4a79-ad19-5a3a5f2e1bdd` | ai | 0.697 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ca14dc18-c01e-4c43-8864-d7751f723839` | human | 0.345 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `eeeea100-76f0-430e-8bae-e07b2662f317` | unsure | 0.519 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `2f26c06f-7860-44ae-8076-487af460eeb4` | unsure | 0.556 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `7091afe0-a54e-470e-8ffd-c220a8a40551` | human | 0.334 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `12b3831b-cee7-40bc-9fb9-693ebf2763e7` | ai | 0.682 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `b16b6009-8fe7-4d60-954a-bce3187f8c80` | ai | 0.930 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c8da88a0-f949-4ef3-971b-cd52eb4c3a8b` | ai | 0.659 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `ece22f68-462b-4655-9161-f458b321e063` | ai | 0.807 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `6f763e13-0eb7-4354-9d4d-5ac3246e84c9` | ai | 0.836 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `08da3f63-cd49-4806-9b02-ee560c171ad9` | ai | 0.830 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `a492197e-3cfb-43a6-836f-a99d89e840fa` | ai | 0.823 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `7781834c-cff5-4cf9-816e-d953d889f3cd` | ai | 0.816 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3af6970f-478f-44f8-b5c0-72a25d5b4378` | unsure | 0.619 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `7cef6843-a485-4abd-8c78-3d91a3bdec6c` | human | 0.384 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `668eb633-2612-4573-89bc-6e4f82efbe59` | unsure | 0.516 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `06746c67-a77a-4953-9d27-c024d57fa34d` | human | 0.406 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `bf16d309-b01b-4bd4-99d5-48046fcc4970` | unsure | 0.647 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `83f993ad-4d07-4f88-8254-7ac3d08131b1` | unsure | 0.549 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `937f558f-e284-4b23-9c54-dd54a4b0575e` | unsure | 0.506 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `94abba8a-de1c-4b84-834d-878c7a4c4ae9` | unsure | 0.626 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `9f7c281f-9765-4e3b-85e6-0599528d83f1` | human | 0.338 |  |
| MF04 | malformed | text is only punctuation | 200 | `b76d69dd-7aab-4068-b5b3-2e03650a51dc` | human | 0.341 |  |
| MF05 | malformed | text is a very long single word | 200 | `4c482e51-b3db-4d35-9795-bbe2c47d8f5c` | ai | 0.662 |  |
| MF06 | malformed | text is emoji only | 200 | `64e49379-9f88-431e-a2e2-934b6f1e431b` | ai | 0.661 |  |
| MF07 | malformed | text is right-to-left script | 200 | `36291fd4-ddf4-497e-aac4-1051f5cc96bd` | unsure | 0.632 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `3bc81753-b196-453d-aa12-61b3b876d147` | human | 0.331 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `df1c3234-fc53-4ea1-b637-76c3381dbab0` | human | 0.353 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `33c7fdef-71eb-41b7-bb27-b7f1b34eac5a` | human | 0.347 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `062cd007-cfc0-46fe-b97f-59e81425ed6a` | human | 0.347 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `38de6f72-8bf1-488a-bb29-2de102190d0d` | human | 0.347 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3149bdec-d868-42e9-a04c-ed42f7da5218` | human | 0.347 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d6e17bd4-0207-4a8b-be16-7d21134a9a6e` | human | 0.347 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "d85e7ebf-82b2-48aa-8766-b1bc31f49617",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.4575492647058823,
  "model_score": 0.1635,
  "style_score": 0.8823529411764706,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "b9c0ea52-a92b-4cdb-9359-5f0e229abd06",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5228334615384616,
  "model_score": 0.5943,
  "style_score": 0.3901098901098901,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "d1460d4f-309b-4150-ab7a-e474d63257dc",
  "creator_id": "attacker_EV03",
  "guess": "ai",
  "confidence": 0.6542622696360648,
  "model_score": 0.6662,
  "style_score": 0.6320921989601851,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "3617b3c0-5d8f-4a79-ad19-5a3a5f2e1bdd",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6965379069767441,
  "model_score": 0.6114,
  "style_score": 0.8546511627906976,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "ca14dc18-c01e-4c43-8864-d7751f723839",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3454668345541669,
  "model_score": 0.3212,
  "style_score": 0.39053381301190543,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "eeeea100-76f0-430e-8bae-e07b2662f317",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5187223913043478,
  "model_score": 0.5727,
  "style_score": 0.41847826086956524,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "2f26c06f-7860-44ae-8076-487af460eeb4",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.55603,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "7091afe0-a54e-470e-8ffd-c220a8a40551",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.33438,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "12b3831b-cee7-40bc-9fb9-693ebf2763e7",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.6824012756260773,
  "model_score": 0.7042,
  "style_score": 0.6419179303602209,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "b16b6009-8fe7-4d60-954a-bce3187f8c80",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9299244012070935,
  "model_score": 0.9792,
  "style_score": 0.8384125748774099,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c8da88a0-f949-4ef3-971b-cd52eb4c3a8b",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.6592792974887727,
  "model_score": 0.6175,
  "style_score": 0.7368694213964933,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "ece22f68-462b-4655-9161-f458b321e063",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8068733031346917,
  "model_score": 0.7387,
  "style_score": 0.9334808660991191,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "6f763e13-0eb7-4354-9d4d-5ac3246e84c9",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.835926577004886,
  "model_score": 0.8051,
  "style_score": 0.893175934299674,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "08da3f63-cd49-4806-9b02-ee560c171ad9",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8299025282878851,
  "model_score": 0.8329,
  "style_score": 0.8243357951082434,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "a492197e-3cfb-43a6-836f-a99d89e840fa",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8228994902216298,
  "model_score": 0.8005,
  "style_score": 0.8644985434903709,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "7781834c-cff5-4cf9-816e-d953d889f3cd",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.8161486274988893,
  "model_score": 0.8814,
  "style_score": 0.6949675071396836,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "3af6970f-478f-44f8-b5c0-72a25d5b4378",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6192647145154686,
  "model_score": 0.8816,
  "style_score": 0.47282694008839193,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "7cef6843-a485-4abd-8c78-3d91a3bdec6c",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.384495,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "668eb633-2612-4573-89bc-6e4f82efbe59",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5156840767143906,
  "model_score": 0.4625,
  "style_score": 0.6144545048982588,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "06746c67-a77a-4953-9d27-c024d57fa34d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.4060929489654864,
  "model_score": 0.2044,
  "style_score": 0.5123597083742082,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "bf16d309-b01b-4bd4-99d5-48046fcc4970",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6468436849630361,
  "model_score": 0.5943,
  "style_score": 0.744424814180103,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "83f993ad-4d07-4f88-8254-7ac3d08131b1",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5488700693480887,
  "model_score": 0.4998,
  "style_score": 0.6400001981373962,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "937f558f-e284-4b23-9c54-dd54a4b0575e",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5059526740513078,
  "model_score": 0.6401,
  "style_score": 0.27382956600747366,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "94abba8a-de1c-4b84-834d-878c7a4c4ae9",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6258237623721191,
  "model_score": 0.5583,
  "style_score": 0.7512250353489118,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "9f7c281f-9765-4e3b-85e6-0599528d83f1",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3375,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "b76d69dd-7aab-4068-b5b3-2e03650a51dc",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.34114,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "4c482e51-b3db-4d35-9795-bbe2c47d8f5c",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.66172,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "64e49379-9f88-431e-a2e2-934b6f1e431b",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.6614925,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "36291fd4-ddf4-497e-aac4-1051f5cc96bd",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.63208,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "3bc81753-b196-453d-aa12-61b3b876d147",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.330675,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "df1c3234-fc53-4ea1-b637-76c3381dbab0",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.35348999999999997,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "33c7fdef-71eb-41b7-bb27-b7f1b34eac5a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34682749999999996,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "062cd007-cfc0-46fe-b97f-59e81425ed6a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34682749999999996,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "38de6f72-8bf1-488a-bb29-2de102190d0d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34682749999999996,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "3149bdec-d868-42e9-a04c-ed42f7da5218",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34682749999999996,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "d6e17bd4-0207-4a8b-be16-7d21134a9a6e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.34682749999999996,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
