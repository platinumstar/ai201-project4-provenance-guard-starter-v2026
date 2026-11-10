# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **Arrive.** A client sends `POST /submit` with JSON `{"text", "creator_id"}`. The route checks the input and rejects missing, empty or enormous text with a 400 instead of crashing.
2. **Signal one (model signal).** `detector.model_signal` runs the text through a local language model and measures perplexity (how predictable the text is). It converts that to a 0–1 score where higher means more likely AI.
3. **Signal two (style signal).** `stylometry.style_signal` measures the shape of the text (sentence-length spread and punctuation density) and returns a 0–1 score in the same direction.
4. **Combine.** `scoring.combine_signals` merges the two scores into one final score.
5. **Label.** `scoring.score_to_label` maps the final score to a guess (`ai` / `human` / `unsure`) and a plain-language label for the reader.
6. **Log.** `audit.log_decision` records the `content_id`, both signal scores, the final score and the label, and the route returns them as JSON.
7. **Appeal.** If the writer disagrees, they send `POST /appeal` with the `content_id` and their reasoning. The item moves to `under_review`.

### The false positive, traced

A student submits a plain, conventional essay they wrote themselves.

- The model signal gives it about 0.70, because plain prose is predictable.
- The style signal gives it about 0.60, because the sentences are even in length.
- The combined score is about 0.65. If the AI threshold were set low enough, the label would call this AI.
- To protect this writer, the "unsure" band has to be wide enough to catch 0.65, with wording that doesn't accuse. They can then send `POST /appeal` with their `content_id` and reasoning, and the item goes to `under_review`.

This scenario decides the thresholds in Milestone 4: an accusation should require a high score, and the middle band should be generous.

### Endpoint contracts

**`POST /submit`**

| | Field | Type | Notes |
|---|---|---|---|
| In | `text` | string | Required, non-empty, capped in length |
| In | `creator_id` | string | Identifies the submitter |
| Out | `content_id` | string | Needed later by `/appeal` |
| Out | `guess` | string | `ai`, `human` or `unsure` |
| Out | `confidence` | float 0–1 | The combined score |
| Out | `label` | string | The plain-language text the reader sees |
| Out | `model_score` | float 0–1 | Signal one, higher = more likely AI |
| Out | `style_score` | float 0–1 | Signal two, higher = more likely AI |

Errors: 400 for missing, empty or oversized `text`; 429 when rate limited.

**`POST /appeal`**

| | Field | Type | Notes |
|---|---|---|---|
| In | `content_id` | string | Must match an existing submission |
| In | `reasoning` | string | Why the writer thinks the result is wrong |
| Out | `content_id` | string | Echoed back |
| Out | `status` | string | `under_review` |

Errors: 400 for missing fields; 404 for an unknown `content_id`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a local language model (perplexity). Low perplexity means the model finds the text unsurprising. The score is scaled to 0–1, higher meaning more likely AI.

**Why that might differ between human and AI writing:** AI text is built from likely next words, so a language model finds it very predictable. Human writing tends to contain more surprising word choices.

**What it can't see:** Who wrote it. It measures predictability, not authorship. Plain, conventional human writing is also predictable and can score as AI, while formal or heavily edited AI text can score as human.

### Signal two — the style signal

**What it measures:** The shape of the text without reading it: how much sentence length varies (standard deviation over mean) and how much non-terminal punctuation is used (commas, semicolons, colons, dashes, parentheses, quotes, per word). Scaled to 0–1, higher meaning more likely AI. Both measures are averaged equally. `style_signal` returns 0.5, meaning no evidence, for text under 2 sentences or 15 words.

**A measure I built and dropped:** the type-token ratio (unique words over total words). On my five test texts it sat between 0.81 and 0.86 for human and AI writing alike, so it did not discriminate and only added noise. `stylometry.type_token_ratio` still exists but is not part of the score.

**Why that might differ between human and AI writing:** AI prose tends toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier, with a three-word sentence next to a forty-word one.

**What it can't see:** Meaning. It has no idea what the text says, so anything that changes the shape without changing the substance moves it: adding typos, breaking up sentences, or pasting in a quotation. That is cheap to do on purpose.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two scores. Where the signals disagree by more than a set gap, pull the average halfway toward 0.5, because two methods that split mean we do not know. Equal weights, since the two signals fail on different inputs and my five test texts did not show a clearly better one to favour: the model signal scored the AI texts as more human, and the style signal scored the plain forum comment as more AI.

**The numbers:** In `config.py`: `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`, `DISAGREEMENT_GAP = 0.30`, `DISAGREEMENT_PULL = 0.5`. That is, `combined = 0.5 * model + 0.5 * style`, then if `|model - style| > 0.30`, `combined += (0.5 - combined) * 0.5`.

**Where it lives:** `scoring.py::combine_signals`

| Test text | Words | Perplexity | Model | Style | Combined |
|---|---|---|---|---|---|
| clearly AI (houseplant care, chatbot-style) | 99 | 53.7 | 0.43 | 0.79 | 0.55 |
| AI-style descriptive paragraph (bakery) | 85 | 55.6 | 0.42 | 0.85 | 0.57 |
| clearly human (forum post, short) | 61 | 27.8 | 0.68 | 0.25 | 0.48 |
| human opening + AI-sounding ending | 124 | 29.7 | 0.66 | 0.51 | 0.58 |
| plain human (forum comment, begonias) | 129 | 33.3 | 0.62 | 0.63 | 0.62 |

These come from five short texts (61-129 words), so they are indicative only. Run from a script file: quotes inside a shell argument cut my first runs short, which made two rows wrong until I caught it.

**A case where my two signals split, and what my rule does with it:** The houseplant text, which I treat as clearly AI. The model signal reads it as 0.43, leaning human. The style signal reads it as 0.79, because the sentences are even and the punctuation is plain. They differ by 0.36, over the 0.30 gap, so the average of 0.61 is pulled to 0.55, in the unsure range. Neither signal's mistake alone decides it.

**What the rule cannot fix:**
- **The model signal runs backwards on my samples.** The two AI texts have higher perplexity (54-56) than the three human texts (28-33), so they score as more human. My guess is that GPT-2, trained on web text, finds casual internet writing predictable and clean chatbot prose less so. I have not tested that beyond five texts.
- **The style signal carries the separation.** It gives the AI texts 0.79-0.85 and the short human text 0.25, but reads the plain forum comment as 0.63.
- **Clearly-AI and clearly-human do not separate well.** The AI texts combine to 0.55-0.57, the human texts to 0.48-0.62. The plain human comment (0.62) scores higher than both AI texts and sits just under the 0.65 AI threshold. That is the Milestone 1 false-positive case, and no combining rule can fix two signals that are wrong together.
- **Weights do not repair it.** Moving to 0.3 model / 0.7 style lifts the AI texts to 0.59-0.61 and lowers the short human text to 0.44, but the plain human comment stays at 0.62. I kept 0.5 / 0.5.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.50 | We think this was probably written by a person. |
| unsure | 0.50 – 0.65 | Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal. |
| high-confidence AI | 0.65 – 1.00 | This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

My first version ended "that says nothing bad about you or your work." Read as a writer, that sounded like a polite suspicion, and it left the reader not knowing whether anything would happen to them. It also didn't mention appeals, which only the AI label did. The current wording says what the system could not do ("couldn't tell"), calls the result "only a guess, not a finding", and gives the appeal option so a writer who gets it always has somewhere to go.

**Thresholds and why:** `HUMAN_THRESHOLD = 0.50`, `AI_THRESHOLD = 0.65` in `config.py`. A false "human" costs less than a false accusation, so I lowered only the human side. My first setting of 0.35 left "human" unreachable: my combined scores for realistic texts ran from 0.48 to 0.62, so everything was "unsure".

**Reachability test:** each label produced by a real submission to `/submit`.

| Text | Combined | Guess | Label |
|---|---|---|---|
| Generic textbook-style paragraph about exercise (52 words) | 0.94 | ai | "This looks like it may have been written with an AI tool…" |
| Chatbot-style paragraph about houseplants (99 words) | 0.55 | unsure | "Our checks couldn't tell…" |
| Short human forum post (61 words) | 0.48 | human | "We think this was probably written by a person." |

Five generic, repetitive texts all reached the AI label (0.82 to 0.99). My richer AI-written texts (houseplants, bakery) and my plain human forum comment (begonias, 0.62) all landed in "unsure".

**What this tells me about the signals:**
- The AI label is reached by text that is simple and predictable ("Regular exercise is important for good health. It helps to improve your mood…"). The model signal measures predictability, not authorship.
- Plain, honest writing, such as a student's or a non-native English writer's, is also simple and predictable, so it can get the AI label. This is the false-positive risk from my Milestone 1 scenario, and I have not tested it with real human samples of that kind.
- Polished AI prose with richer vocabulary lands in "unsure", so it gets through.
- The "human" label rests on one 61-word sample, so it is weakly supported.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

```bash
$ curl -s -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The dopamine hit is definitely more of a thing. When people comment on my posts, I get a nice warm glow. And when last night, just before I went to bed, I saw that my previous post was #1 on the front page of HN, I took a screenshot and posted it to my Fellow Geeks WhatsApp group with the caption.", "creator_id": "writer-2"}'
```

```json
{
  "confidence": 0.494691393442623,
  "content_id": "02de0977-733b-4a13-9e97-7cf182df52ac",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.6427,
  "style_score": 0.33606557377049184
}
```

The two signals disagree here (model 0.64 leans AI, style 0.34 leans human) by 0.31, just over the 0.30 gap, so the combining rule pulled the average (0.489) up to 0.495, which is still under the 0.50 human threshold. This is a borderline result: a small change in wording could move it into "unsure".

**Bad input (empty body)**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{}'
```

```json
{
  "error": "missing_or_empty_text",
  "message": "`text` is required and can't be empty."
}
```

**An appeal**

```bash
$ curl -s -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "02de0977-733b-4a13-9e97-7cf182df52ac", "reasoning": "I wrote this myself."}'
```

```json
{
  "content_id": "02de0977-733b-4a13-9e97-7cf182df52ac",
  "message": "Thanks. Your appeal has been recorded and this result is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.494691393442623,
      "content_id": "02de0977-733b-4a13-9e97-7cf182df52ac",
      "creator_id": "writer-2",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6427,
      "status": "decided",
      "style_score": 0.33606557377049184,
      "timestamp": "2026-11-03T04:45:55+00:00"
    },
    {
      "content_id": "02de0977-733b-4a13-9e97-7cf182df52ac",
      "creator_id": "writer-2",
      "event": "appeal",
      "reasoning": "I wrote this myself.",
      "status": "under_review",
      "timestamp": "2026-11-03T04:48:58+00:00"
    }
  ]
}
```

The original decision stays in the log unchanged and the appeal sits after it, with the same `content_id`.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I ran my forum comment through the model and style signals with a python -c one-liner, and asked Claude whether the scores looked right. The begonias comment came back 0.35 model and 1.0 style, and the short dopamine text came back 0.66 and 0.36.
- *What came back:* Claude re-ran all five texts from a script file and found the numbers didn't match. The straight quotes inside my texts ("difficult diva", "Fellow Geeks") had ended the shell argument early, so Python only received a fragment of the text. The begonias result was really 0.62 model and 0.63 style.
- *What I changed:* I stopped passing texts on the command line, used the full texts, and replaced the table in Signals and Scoring with the corrected numbers. I also removed the quotes from my curl examples.

**Moment 2**

- *What I asked for:* I asked Claude to read my three labels as the writer who receives them, saying what I'd think and do next, without rewriting them.
- *What came back:* Claude said my "unsure" label ("that says nothing bad about you or your work") sounded like a polite suspicion, and that it didn't tell the writer whether anything would happen to them or mention the appeal option, which only the AI label did.
- *What I changed:* I rewrote "unsure" to say what the system couldn't do, called the result "only a guess, not a finding", and added the appeal option. I also noted my reasoning in Label Variants.

**Moment 3 (unit 8)**

- *What I asked for:* I asked Claude to turn my five criteria into runnable tests and run them three times each, and to draft the 20 AI-style and 20 casual human-style texts for the score-spread and label-coverage criteria. I wrote the 20 texts for the false-positive criterion myself.
- *What came back:* The third trial of one group returned HTTP 429 on all 20 requests. Claude traced it to `run_eval.py`, which builds each `creator_id` from the first 12 characters of the scenario name, so two of my scenarios ("score spread AI group" and "score spread human group") shared the same 20 IDs and hit my own rate limit of 5 per minute per creator. It also first reported a 0/20 audit-log result that was its own script's bug (it filtered on an `event` field that decision entries do not have).
- *What I changed:* I renamed the scenarios so their IDs differ, waited out the limit and reran for clean results. I discarded the earlier runs and fixed the audit-log check to match on `status: "decided"`.

**Moment 4 (unit 8)**

- *What I asked for:* I asked Claude to explain why criteria 1, 2 and 3 missed and to write the diagnoses.
- *What came back:* Its first diagnosis said the model signal never scored AI text above 0.80. When I checked the results file, the AI group's model score reached 0.93, so that claim was wrong. The real mechanism was that the style signal returns 0.5 on every single-sentence text and the disagreement pull then drags strong AI scores back toward 0.5.
- *What I changed:* I rewrote the diagnoses from the recorded scores, and used the same numbers to test a weight change offline before touching the service. I chose 0.65 / 0.35 and kept the other settings the same, so the effect could be read.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 100 per day

**Why those numbers and not others:**
I chose 5 submissions per minute and 100 per day to allow a writer to submit and revise work while slowing down scripts that send many variations to probe the detector’s thresholds. The limits reduce excessive requests, though they don’t guarantee the service can’t fail.

**What a caller counts as:** per creator_id.


**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

`run_attacks.py --set attack_set --label before`, 56 attacks, `HUMAN_THRESHOLD = 0.50` / `AI_THRESHOLD = 0.65`. MF02 and RQ07 are auto-marked BROKE (5xx); every other verdict is mine.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `6d3eea48-399c-4820-9e5f-e2775b87a359` | unsure | 0.511 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `3e8a2ee6-f1a8-4fb7-a8b8-d5dcbedc0279` | human | 0.492 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8f5da756-850c-473f-adcd-216fc1d98f36` | unsure | 0.649 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `7c06ff8e-ff4c-4331-9be4-6644100cf79d` | ai | 0.733 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `74f2649a-c75f-4d59-8444-7ed7db055a2c` | human | 0.356 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `82a35f17-c9b2-4c5e-8aa1-2008fb085f7b` | human | 0.496 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `6a717881-2800-4836-bfc5-4fc6ea6939f5` | unsure | 0.543 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `d1e1fb3b-6ef1-4eae-aa61-6e95d20965be` | human | 0.373 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `dca562a0-2401-4f98-bfc1-03d60b03be70` | ai | 0.673 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `897bc78f-2d8b-4096-b445-f466ee6be620` | ai | 0.909 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `380ddb5f-3abe-48e5-9b3a-f8a4e9456e2e` | ai | 0.677 | BROKE |
| FP02 | false_positive | human writing in a formal register | 200 | `3afe78eb-0897-4d73-8a4e-9873b6e5e0d7` | ai | 0.836 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `7287f954-91b1-4e58-a2ba-9db9b65c2f28` | ai | 0.849 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `cc927cd2-5059-41d5-bd6d-e5a6c5d16b81` | ai | 0.829 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `b389b19e-ad77-475f-be6e-09d5e0092e9b` | ai | 0.832 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `1afe49d8-618a-40c0-9f7a-a853e475157e` | ai | 0.788 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `fe40eae0-68ed-433d-aeb5-0fc10cab3601` | unsure | 0.589 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `7de55e38-9dbd-41aa-bdaf-dd486f37cacc` | human | 0.411 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `540981dd-bcf5-4992-9ce1-af6fb10af894` | unsure | 0.538 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `5334e0e8-ae24-4acc-9ce3-8d8d30b67960` | human | 0.429 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `078ecc0d-c3df-4ee1-9b32-c64bd9e08745` | ai | 0.669 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `a4ca3a15-d4a0-4f61-a028-8545a81ae995` | unsure | 0.570 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `38bc5662-6d25-4af3-9697-f868c090ec33` | human | 0.478 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b30e5cea-9997-42b5-83d4-8aa5b6f23e94` | ai | 0.655 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `ef009f07-4c32-4631-890b-d4669a9d6bcd` | human | 0.375 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `634620de-19c4-45df-9429-cbe7ff7a2cce` | human | 0.378 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `dd083371-888f-40f4-9fb9-7f0cb46c321f` | unsure | 0.624 | HELD |
| MF06 | malformed | text is emoji only | 200 | `9da72931-a63d-4a9c-8176-7cf10796795c` | unsure | 0.624 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `b5ab861f-3b77-44c2-aba1-f91be9105e2c` | unsure | 0.602 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `9b343e24-6a42-4da4-8464-69c0cdefa476` | human | 0.370 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `949d8291-3920-43b4-a148-0c67e46d1d41` | human | 0.387 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5022dcac-cc92-4688-a149-1b83779ba930` | human | 0.382 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6b72855e-01de-4828-8c74-3cb4288239c1` | human | 0.382 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `85119d3a-81f1-43dd-87ce-26419f9949e3` | human | 0.382 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f8096c38-0d6f-4848-b99e-69f887993dbe` | human | 0.382 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fab07416-ae18-42b0-9eb6-121f25984274` | human | 0.382 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**By family:** evasion 6 held / 4 broke (EV02, EV05, EV06, EV08 — all three exploited the style-signal's 0.5 fallback or a low-perplexity/short-text gap); false_positive 2 held / 6 broke (every formal, rubric-written, or non-native-register human sample landed on the AI label); prompt_injection 6 held / 0 broke (the detector only scores shape and perplexity, so there was nothing for an embedded instruction to act on); malformed 15 held / 5 broke (MF02 and RQ07 crash outright; MF03, MF04 and RQ06 don't crash but still misbehave — see below); flood_same_creator 12 held / 0 broke (exactly 5 through, 7 rejected, matching `RATE_LIMIT_PER_MINUTE = 5`).

Two things worth flagging rather than hiding in a clean HELD/BROKE split: RQ10 and RQ11 both came back 429 instead of exercising their actual malformed-body handling — reproducible on a second, independent run of the full set, so it looks like a request with no extractable `creator_id` falls back to a shared rate-limit key and gets swept up by the other malformed attacks landing in the same minute, rather than being a timing fluke. And RQ02 (missing `creator_id`) I called HELD because the endpoint contract above only marks `text` as required, not `creator_id`.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
[
  {
    "combined_score": 0.8360904330495595,
    "content_id": "3afe78eb-0897-4d73-8a4e-9873b6e5e0d7",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.7387,
    "status": "decided",
    "style_score": 0.9334808660991191,
    "timestamp": "2026-11-07T22:16:06+00:00"
  },
  {
    "combined_score": 0.849137967149837,
    "content_id": "7287f954-91b1-4e58-a2ba-9db9b65c2f28",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "label": "This looks like it may have been written with an AI tool. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.893175934299674,
    "timestamp": "2026-11-07T22:16:06+00:00"
  },
  {
    "combined_score": 0.49220494505494505,
    "content_id": "3e8a2ee6-f1a8-4fb7-a8b8-d5dcbedc0279",
    "creator_id": "attacker_EV02",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.5943,
    "status": "decided",
    "style_score": 0.3901098901098901,
    "timestamp": "2026-11-07T22:16:06+00:00"
  },
  {
    "combined_score": 0.4955891304347826,
    "content_id": "82a35f17-c9b2-4c5e-8aa1-2008fb085f7b",
    "creator_id": "attacker_EV06",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.5727,
    "status": "decided",
    "style_score": 0.41847826086956524,
    "timestamp": "2026-11-07T22:16:06+00:00"
  },
  {
    "combined_score": 0.3726,
    "content_id": "d1e1fb3b-6ef1-4eae-aa61-6e95d20965be",
    "creator_id": "attacker_EV08",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.2452,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-07T22:16:06+00:00"
  },
  {
    "combined_score": 0.47848239150186844,
    "content_id": "38bc5662-6d25-4af3-9697-f868c090ec33",
    "creator_id": "attacker_PI05",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.6401,
    "status": "decided",
    "style_score": 0.27382956600747366,
    "timestamp": "2026-11-07T22:16:07+00:00"
  },
  {
    "combined_score": 0.375,
    "content_id": "ef009f07-4c32-4631-890b-d4669a9d6bcd",
    "creator_id": "attacker_MF03",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-07T22:16:07+00:00"
  },
  {
    "combined_score": 0.3778,
    "content_id": "634620de-19c4-45df-9429-cbe7ff7a2cce",
    "creator_id": "attacker_MF04",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0112,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-07T22:16:07+00:00"
  },
  {
    "combined_score": 0.3873,
    "content_id": "949d8291-3920-43b4-a148-0c67e46d1d41",
    "creator_id": {
      "id": "x"
    },
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0492,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-07T22:16:07+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "limit": "5 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-07T22:16:07+00:00"
  }
]
```

Why these ten, in order: FP02 and FP03 (human formal / non-native writing scored 0.84–0.85, labeled AI, both signals agreeing); EV02, EV06 and EV08 (AI text pushed to "human" by sentence-length tricks and by being under the token window, where style_score falls back to exactly 0.5); PI05 (an injection attempt in the text that was scored as plain content); MF03 and MF04 (control characters and pure punctuation got model_score of 0.0 and a confident "human" instead of a rejection); the `creator_id` object entry (RQ06 logged a dict, not a string); and a rate_limited rejection. MF02 and RQ07 returned 500 and have **no** audit entry at all, because they crashed before anything was logged.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03: a non-native English speaker writing carefully got the high-confidence AI label at 0.849, the highest score of any false-positive attack. It's not just a wrong guess — it's a confident accusation ("This looks like it may have been written with an AI tool") against exactly the kind of writer who already gets disproportionately flagged by AI detectors, because writing carefully in a second language produces the same plain, even, predictable prose both of my signals read as machine-made. FP02 (formal register, 0.836) fails for the same reason. There is no appeal-after-the-fact that undoes having been told your own writing isn't yours.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | ≤ 1 of 20 flagged AI | 3/20 | 3/20 | 3/20 | MISSED |
| 2. Score spread | AI mean ≥ 0.20 above human mean | 0.169 | 0.169 | 0.169 | MISSED |
| 3. Label coverage | Human, unsure and AI all appear | 2/3 | 2/3 | 2/3 | MISSED |
| 4. Appeal path | under_review, logged, 404 on unknown ID | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input | 400 × 3, then 200 | pass | pass | pass | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json
// Criterion 2 and 3 — AI-style text, from run_eval.py via app.py::submit (trial 1, results/run_2026-11-09_2034_before5.md)
{"status": 200, "guess": "unsure", "confidence": 0.6193, "model_score": 0.7386, "style_score": 0.5,
 "label": "Our checks couldn't tell whether this was written by a person or with an AI tool. This is only a guess, not a finding. If you'd like someone to look at it, you can appeal.",
 "sent": "In today's rapidly evolving digital landscape, it is essential for org"}

// Criterion 2 — casual human-style text, same file and function
{"status": 200, "guess": "human", "confidence": 0.48212093671242084, "model_score": 0.298, "style_score": 0.6304837468496833,
 "label": "We think this was probably written by a person.",
 "sent": "ok so my sister called at 6am again about the cat. he's fine. he was j"}

// Criterion 4 — test_appeal.py, app.py::appeal
{"content_id": "b3d8e552-8916-4be3-b396-e42bc17c8b10", "message": "Thanks. Your appeal has been recorded and this result is now under review.", "status": "under_review"}
// unknown id (app.py::appeal): 404 {"error": "unknown_content_id", "message": "No submission has that `content_id`."}

// Criterion 5 — app.py::submit, 10,001-character text, then a valid follow-up
{"status": 400, "guess": null, "confidence": null, "sent": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
{"status": 200, "guess": "human", "confidence": 0.40725, "model_score": 0.129, "style_score": 0.5, "sent": "This is a normal sentence about my morning walk."}

// Audit log entry — audit.py::log_decision (logs/audit.jsonl), from test_audit.py, 20/20 found in all three runs
{"timestamp": "2026-11-10T01:06:50+00:00", "content_id": "eb7ff8d5-597c-40e3-9c15-76a97f9a2b3e", "creator_id": "eval_audit_1", "guess": "human", "model_score": 0.2864, "style_score": 0.5, "combined_score": 0.3932, "label": "We think this was probably written by a person.", "status": "decided"}
```

Criterion 1 came from `run_eval.py --label before6` (20 of my own texts, results/run_2026-11-09_2215_before6.md); criteria 2, 3 and 5 came from `run_eval.py --label before5` (three trials, identical every time). Criterion 4 came from `test_appeal.py` and the audit-log check from `test_audit.py`, each run three times by hand. All three trials matched, so nothing in the pipeline was unstable. One mistake along the way: two scenarios shared a `creator_id` prefix, so the rate limiter (5 per minute per creator) returned 429 on a trial. I renamed the scenarios and reran; the numbers above are from the clean run.

**Diagnoses**

**Criterion 1, false positives (MISSED: 3 of 20 of my own texts labelled `ai` in every trial, target at most 1).** The first 10 texts I tested were single sentences, so the style signal returned its 0.5 fallback and none was flagged (0 of 10). My other 10 are two sentences each, and three of them were flagged: "A representative gave me a report…" (model 0.63, style 1.0, combined 0.657), "I told my boss via text…" (0.71, 1.0, 0.855) and "I found that I could not understand a lot of text in a table…" (0.65, 1.0, 0.662). The stage that fails is signal two. `stylometry.py::style_signal` scores plain, short, evenly sized sentences with little punctuation at 1.0 (most AI-like), which is how ordinary human writing looks. With equal weights, a style score of 1.0 plus a model score near 0.65 pushes the average over `AI_THRESHOLD` (0.65). The 0.5 fallback was hiding this problem on the first 10 texts.

**Criterion 2, score spread (MISSED: 0.169 against a target of 0.20).** The AI group averaged 0.583 and the human group 0.414. The failure is in signal two and the combining rule, not signal one. `stylometry.py::style_signal` returns exactly 0.5 ("no evidence") for any text with fewer than two sentences or under `MIN_WORDS` (15). All 20 of my AI texts are single sentences, so all 20 have `style_score` 0.5 (the human group: 14 of 20). The model signal does separate the groups (AI texts up to 0.93, human texts at most 0.60), but each AI text is then averaged with 0.5, which halves its distance from 0.5.

**Criterion 3, label coverage (MISSED: no `ai` label in 45 texts).** The `ai` label needs a combined score above `AI_THRESHOLD` (0.65). The highest combined score was about 0.64. A second step in `scoring.py::combine_signals` makes it worse: when the signals differ by more than `DISAGREEMENT_GAP` (0.30), the average is pulled halfway back toward 0.5. A strong AI text such as model 0.93 and style 0.5 averages to 0.72, but the gap of 0.43 triggers the pull, giving about 0.61, which is `unsure`. So the signal that is working (model) is cancelled by the signal that has no evidence (style = 0.5), twice. Three of my 20 AI texts were also labelled `human`, which is a model-signal miss.

**Criteria 4 and 5 (MET), and how I decided.** Criterion 4: in all three runs, 5 of 5 appeals returned `under_review`, each had an `event: "appeal"` entry in `GET /log`, and the unknown `content_id` got a 404 with no new entry, so no run fell short of the target. Criterion 5: in all three trials the empty, missing and 10,001-character texts each returned 400 and the valid follow-up returned 200. I read each verdict against the original target line in `criteria.md` and checked every trial, not the best one.

**Broken attacks (from the "Attack Run — Before" table), grouped by cause.**

- **FP01-FP06, six human texts called `ai`** (plain, formal, rubric-written, non-native, technical, template-style). Stages: signal one, signal two and the combining rule. Both signals read plain, even, predictable prose as machine-made (FP02: model 0.74, style 0.93; FP03: model 0.81, style 0.89). Because the signals agree, `combine_signals` has no disagreement to soften, so the average clears `AI_THRESHOLD` and the label mapping issues the high-confidence `ai` label. This is the same mechanism as my criterion 1 miss.
- **EV02, EV06 (style evasion).** Stage: signal two. EV02 inserts short sentences ("Really.") between long ones and EV06 hides one very long sentence in the text. Both raise the sentence-length spread, which `style_signal` reads as human (EV02 style 0.39), and equal weights let that drag the average down to a `human` label (0.49 and 0.50).
- **EV05, EV08 (heavy editing, short text).** EV05 is AI text after a heavy human edit, and both signals went low (model 0.32, style 0.39), so no combining rule could catch it. EV08 is only 10 words, under `MIN_WORDS` (15), so `style_signal` returned its 0.5 fallback and the model signal alone scored 0.25. Stage: signal two (the fallback) and signal one on short text.
- **MF02 (a single character) returned 500.** Stage: the route and signal one. `detector.model_signal` raises `ValueError("Text is too short to score")`, and `app.py::submit` does not catch it, so Flask returns an HTML error page. The route needs to check minimum length, or catch the error and return a 400.
- **MF03 and MF04 (control characters, punctuation only) got a `human` decision.** Stage: the route. `submit` only checks that text is non-empty after `strip()`, so text with no real words is accepted and scored as if it were writing. It should be rejected like empty text.
- **RQ06 (`creator_id` is an object) and RQ07 (body is a JSON array).** Stage: the route. `submit` never checks the type of `creator_id`, so an object goes straight into the audit log (RQ06). For a JSON array, `payload.get` is called on a list, which raises and returns 500 (RQ07; this is from reading the code, since `or {}` only guards an empty body). Both need a check that the body is an object and `creator_id` is a string.

**Pattern:** Two patterns. The three criteria misses and the EV02, EV06 and EV08 attacks trace to `style_signal` in `stylometry.py`, and the FP attacks add signal one to it; the six malformed-request breaks (MF02-MF04, RQ06, RQ07) trace to one thing, the route doing too little input validation. For the criteria misses, `style_signal` on short single-sentence text returns 0.5, which hides the model signal (criteria 2 and 3). On short two-sentence plain text it returns 1.0, which wrongly accuses human writing (criterion 1). The fix I will try is to ignore the style signal, and skip the disagreement pull, when the style signal has no evidence (returns exactly 0.5), so the model score is used alone. That alone will not fix criterion 1, because there the style signal is confidently wrong, so its scaling (`SPREAD_RANGE`, `PUNCT_RANGE`) also needs recalibrating on short human text. I'm not lowering either target in `criteria.md`.



---

## The Improvement

**What I changed:** One thing, in `config.py`: the signal weights, from `WEIGHT_MODEL_SIGNAL = 0.5` / `WEIGHT_STYLE_SIGNAL = 0.5` to `0.65` / `0.35`. Nothing else changed (thresholds, the disagreement pull, the signals and the route are as before). Before choosing 0.65 I recomputed my recorded scores under several weights without touching the service: 0.6 gave a score spread of 0.19999 (just under 0.20), 0.65 gave 0.216, and every weight I tried left the six false-positive attacks broken.

**Which diagnosis pointed at it:** Criteria 2 and 3. Every one of my AI texts has `style_score` 0.5 ("no evidence"), so an equal-weight average cut each AI text's distance from 0.5 in half and the model signal, which does separate the groups, was diluted. Weighting the model signal more should widen the spread and let strong AI scores reach `ai`. I predicted it would not fix criterion 1 or the false-positive attacks, because there both signals are wrong together.

### Attack Run — After

`run_attacks.py --set attack_set --label after`, same 56 attacks and thresholds (`HUMAN_THRESHOLD` 0.50 / `AI_THRESHOLD` 0.65), weights 0.65 / 0.35. Full table: `results/attack_run_2026-11-09_2246_after.md`. Nine attacks changed outcome; the other 47 are identical to the before run.

| ID | Family | Before | After | Verdict change |
|---|---|---|---|---|
| EV01 | evasion (typos) | unsure 0.511 | human 0.458 | HELD → **BROKE** (regression) |
| EV02 | evasion (broken-up sentences) | human 0.492 | unsure 0.523 | BROKE → HELD |
| EV03 | evasion (pasted quotation) | unsure 0.649 | ai 0.654 | HELD → HELD (now caught outright) |
| EV06 | evasion (long + short sentence) | human 0.496 | unsure 0.519 | BROKE → HELD |
| PI03 | prompt injection | ai 0.669 | unsure 0.647 | HELD → HELD |
| PI05 | prompt injection (audit log) | human 0.478 | unsure 0.506 | HELD → HELD |
| PI06 | prompt injection | ai 0.655 | unsure 0.626 | HELD → HELD |
| MF05 | malformed (one very long word) | unsure 0.624 | ai 0.662 | HELD → **BROKE** (my judgment) |
| MF06 | malformed (emoji only) | unsure 0.624 | ai 0.661 | HELD → **BROKE** (my judgment) |

By family, broken attacks before → after: evasion 4 → 3 (EV02 and EV06 fixed, EV01 newly broken; EV05 and EV08 still broken), false positives 6 → 6 (unchanged), prompt injection 0 → 0, malformed 5 → 7 (MF02, MF03, MF04, RQ06, RQ07 as before, plus MF05 and MF06 now called `ai`), flood 0 → 0. I marked MF05 and MF06 BROKE because a confident AI accusation on a single long word or on emoji is not a decision the signals can support; that is my judgment, not an automatic mark.

**Five criteria, before and after (three trials each, identical across trials):**

| Criterion | Target | Before (Run 1 / 2 / 3) | After (Run 1 / 2 / 3) | Verdict after |
|---|---|---|---|---|
| 1. False positives | ≤ 1 of 20 flagged `ai` | 3/20, 3/20, 3/20 | 2/20, 2/20, 2/20 | MISSED (improved) |
| 2. Score spread | AI mean ≥ 0.20 above human mean | 0.169 ×3 | 0.216 ×3 | **MET** |
| 3. Label coverage | `human`, `unsure`, `ai` all appear | 2/3 ×3 | 3/3 ×3 | **MET** |
| 4. Appeal path | `under_review`, logged, 404 on unknown ID | 5/5 ×3 | not rerun (weights do not touch it) | MET |
| 5. Bad input | 400 ×3, then 200 | pass ×3 | pass ×3 | MET |

**Did it help, and how do I know:** Partly. It fixed what I aimed at: criteria 2 and 3 went from MISSED to MET in all three trials (spread 0.169 → 0.216; the `ai` label is now reachable, six of my 20 AI texts get it where none did), and criterion 1 improved from 3/20 to 2/20 but is still MISSED against a target of at most 1. It also fixed two evasions (EV02, EV06). The costs are on the other side. The set of my own texts that are flagged changed rather than just shrinking: "I saw a homeless person on the street…" is now labelled `ai` (it has a high model score, 0.75, which now counts for more), while "A representative gave me a report…" and "I found that I could not understand…" dropped back to `unsure`. EV01 (typos) went from held to broken, and MF05 and MF06 are now confidently called `ai`. The six false-positive attacks are unchanged because both signals score formal and careful human writing as machine-made, so no weighting between them can separate it. In one sentence: reweighting toward the model signal made the detector separate AI from human text better, but it moved the false accusations around instead of removing them.

---

## What's Still Broken

**Criterion 1, false positives (2 of 20 of my own texts still labelled `ai`, target at most 1).** The style signal gives short, plain, evenly sized sentences a score near 1.0, and the model signal scores some of my everyday sentences high too (0.75 for "I saw a homeless person…"). I'd recalibrate `SPREAD_RANGE` and `PUNCT_RANGE` in `stylometry.py` on a set of plain human texts, so ordinary writing stops reading as machine-made. I stopped because that is a second change, and this milestone allows one so the result can be read.

**The six false-positive attacks (FP01-FP06).** Careful, formal or rubric-written human prose scores high on both signals, so changing the weights between them cannot help. Fixing this needs a signal that measures something else, or a wider `unsure` band, which would let more AI text through. I stopped because neither was in scope for one change.

**Evasions EV01, EV05 and EV08.** EV01 (typos) newly broke with the new weights, EV05 (heavy human editing) fools both signals at once, and EV08 is 10 words, under `MIN_WORDS`, so the style signal has nothing to say. I'd lower `MIN_WORDS` or refuse to label text that is too short to judge. I stopped because each of these is a separate change.

**Malformed requests: MF02, MF03, MF04, MF05, MF06, RQ06 and RQ07.** These all come from the route doing too little input validation, and my change made MF05 and MF06 worse. I'd add checks to `app.py::submit` before the signals run: the body must be a JSON object, `creator_id` must be a string, and the text needs a minimum number of real words (this also stops MF02 crashing with a 500, and rejects control-character and punctuation-only text). I stopped because the weights fix and the validation fix are different changes, and I wanted to measure one.

**Not tested:** Criterion 4 (the appeal path) was not rerun after the weights change, because the weights do not touch it. Criterion 1 is tested on 20 texts I wrote myself, and criteria 2 and 3 use 20 AI and 20 human-style texts written with Claude's help, so the results are indicative, not a measure of real-world accuracy.

**The trade I'd make if this ran for real:**

If this ran for real I would keep the `unsure` band wide and move `AI_THRESHOLD` up, accepting that more AI text would pass as `unsure` or `human`. The cost of getting this wrong falls on the writers: a plain-spoken person or a non-native English speaker who is told "this may have been written with an AI tool" has to prove their own work is theirs, while the cost of missed AI text falls on the site, which is smaller. My own numbers show who pays today, because the false accusations land on short plain sentences and careful formal writing, which is how many real people write.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
