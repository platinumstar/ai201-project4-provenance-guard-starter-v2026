# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives

In each of three runs, no more than 1 of 20 human-written samples is labeled
high-confidence AI (`guess` = `"ai"`, i.e. combined score above
`AI_THRESHOLD`, currently 0.65 in `config.py`).

**Why this target:** A wrong AI accusation can have serious consequences for a
writer, while a missed detection costs the site little, so false positives
should be rare in every run, not just on average.

---

## 2. Score spread

In each of three runs, score 20 clearly AI-written and 20 clearly
human-written samples. The mean combined score (0.0–1.0) of the AI group must
be at least 0.20 higher than the mean of the human group.

**Why this target:** A consistent 0.20 gap shows the scores meaningfully
separate the two groups instead of clustering around 0.5.

---

## 3. Label coverage

In each of three runs, across the 40 samples from criterion 2 plus 5 samples I
judge borderline, at least one submission receives each label: `"human"`,
`"unsure"` and `"ai"`.

**Why this target:** This confirms that all three intended outcomes are
reachable in practice, not just on paper in `config.py`.

---

## 4. Appeal path

After I submit a text and receive a `content_id`, `POST /appeal` with that ID
and a reason returns a response whose status is `under_review`, and `GET /log`
then shows an entry with that `content_id`, `event` = `"appeal"` and `status` =
`"under_review"`. An appeal with an unknown `content_id` is refused (404) and
writes no appeal entry.

**Why this target:** An appeal has to be both acknowledged to the writer and
recorded, and a typo in the ID must not silently look like success.

---

## 5. Bad input

With `MAX_TEXT_LENGTH = 10000` set in `config.py`, `POST /submit` returns 400
for each of: missing `text`, empty `text`, and a 10,001-character `text`.
Immediately afterwards, a valid submission returns 200 with a decision. Each
rejected request leaves a `rejected` entry in the audit log.

**Why this target:** Specific test inputs make the error behavior
reproducible, and the final valid submission checks that the service remains
usable after bad requests.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
