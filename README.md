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
3. **Signal two (style signal).** `stylometry.style_signal` measures the shape of the text (sentence-length spread, type-token ratio, punctuation density) and returns a 0–1 score in the same direction.
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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
