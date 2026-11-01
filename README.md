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

**What it measures:** The shape of the text without reading it: how much sentence length varies, how much vocabulary repeats (type-token ratio), and how much punctuation is used. Scaled to 0–1, higher meaning more likely AI.

**Why that might differ between human and AI writing:** AI prose tends toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier, with a three-word sentence next to a forty-word one.

**What it can't see:** Meaning. It has no idea what the text says, so anything that changes the shape without changing the substance moves it: adding typos, breaking up sentences, or pasting in a quotation. That is cheap to do on purpose.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I went to the store this morning and bought some bread. It was a nice day, so I walked home slowly.", "creator_id": "me"}'
```

```json
{
  "confidence": 0.5,
  "content_id": "e0aef3f1-2aa0-432d-8249-e2d9ce3dc80e",
  "guess": "unsure",
  "label": "PLACEHOLDER",
  "model_score": 0.7867,
  "style_score": null
}
```

Milestone 3 only has the first signal, so `style_score` is `null` and `confidence` and `label` are placeholders. Milestones 4 and 5 fill them in.

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

**What the log shows**

```bash
$ curl http://127.0.0.1:5000/log
```

```json
{
  "count": 2,
  "entries": [
    {
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "missing_or_empty_text",
      "status": "rejected",
      "timestamp": "2026-10-31T23:52:19+00:00"
    },
    {
      "combined_score": 0.5,
      "content_id": "e0aef3f1-2aa0-432d-8249-e2d9ce3dc80e",
      "creator_id": "me",
      "guess": "unsure",
      "label": "PLACEHOLDER",
      "model_score": 0.7867,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-01T00:19:01+00:00"
    }
  ]
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

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
