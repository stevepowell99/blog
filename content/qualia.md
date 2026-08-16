---
title: QualiaInterviews
date: 2026-08-16
---

[QualiaInterviews](https://qualiainterviews.com) is an AI interviewer, the second piece of software I work on at [Causal Map Ltd](https://causalmap.app). You write the interview guide. It then interviews each respondent, following up where a human interviewer would, and gives you the transcripts.

The case for it is narrow and practical. A survey with closed questions is usually too thin to tell you why anything happened. Fifty face-to-face interviews cost more than most programmes will spend on their whole evaluation. Qualia covers the middle ground, where everybody gets interviewed and everybody gets follow-up questions.

## What it does

Respondents open a link and talk or type. The interviewer follows your guide, probing where you asked it to probe. What comes back is a transcript per respondent, ready to code.

Researchers who already have an account sign in at [manage.qualiainterviews.com](https://manage.qualiainterviews.com).

## Writing about it

- [What Qualia does](https://garden.causalmap.app/qualia), the background piece in the Causal Map Garden.
- [The potential of AI interviewing](https://garden.causalmap.app/qualia-potential), on what changes when the cost of a good interview falls.
- *A workflow for collecting and understanding stories at scale*, in *Evaluation* 31(3), 394 to 411 (2025), [summarised here](https://garden.causalmap.app/summary-eval2025). This is the argument for running the two tools as one pipeline, from AI interview to coded causal map.

There is more about how I think this kind of work should be done, and where I think it goes wrong, on [[ai-and-evaluation|AI for evaluation and social research]].

## In practice

DuocUC, a higher education institution in Chile, hired us to look at the gender gaps facing women in STEM careers at the university. Qualia ran the interviews in Spanish, on a guide we wrote with their quality assurance team over several rounds, asking about educational experiences, professional development and relationships. They sent the link to 50 people and got 32 interviews back, which we then coded into a causal map. [The case study](https://garden.causalmap.app/qualia-seamless-stories) walks through each step, including how they tracked who had replied without us ever holding a name.

At a European Evaluation Society webinar in February 2025 we made the demonstration the data. Over 90 participants spent a few minutes being interviewed about the problems facing the USA and the reasons behind them, at a mean of 13 messages each. We coded what they said into a map afterwards. It was a demo, plenty of people started and stopped, so treat the map as an example of the output rather than as social science. [What came out of it](https://garden.causalmap.app/qualia-usa).

The University of Bath used it in 2024 to gather [feedback on the learning experiences of doctoral students](https://causalmap.notion.site/dprp-qualia-cm). We demonstrated it again at a UK Evaluation Society webinar in December 2025.

## Two questions people ask

**Which languages?** Qualia switches language on request, mid-interview, so a respondent who would rather carry on in German can just say so. The languages best represented on the internet work well for both the interviewing and the voice transcription. Some quite widely spoken ones need dedicated services. There is also a trade-off between EU-only mode for GDPR and letting people speak instead of type. [The detail](https://garden.causalmap.app/qualia-multilingual), including how to send language-specific invitation links.

**Do people tell it the truth?** Often more of it than they tell a human, especially on sensitive or embarrassing topics. That is not an AI truth serum. It follows from having less need to manage the impression you make, no facial expressions to read, and time to think before answering. It cuts both ways: the same conditions invite over-disclosure and misplaced trust, which is the interviewer's problem to handle. [The mechanisms and the risks](https://garden.causalmap.app/qualia-candid).
