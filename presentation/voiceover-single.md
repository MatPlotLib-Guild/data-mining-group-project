# Single-speaker voiceover — short slide descriptions

One short English line per slide. Read sequentially.

---

**Slide 1 — Title**
A CRISP-DM project that predicts pull request merge outcomes from public GitHub events.

**Slide 2 — At a glance**
We turned 9.27 million events into 195 thousand pull request lifecycles and built a triage-grade ranking model.

**Slide 3 — CRISP-DM map**
Six phases, in strict order: Business, Data Understanding, Preparation, Modeling, Evaluation, Deployment.

**Slide 4 — Phase 1 divider**
Phase one. Business Understanding.

**Slide 5 — Business Understanding**
Goal: rank newly opened pull requests by merge likelihood — before maintainers spend a minute reviewing them.

**Slide 6 — Phase 2 divider**
Phase two. Data Understanding.

**Slide 7 — Data Understanding**
The dataset is an event stream — 9.27 million records, fourteen event types, 470 thousand pull request events.

**Slide 8 — Phase 3 divider**
Phase three. Data Preparation.

**Slide 9 — Data Preparation**
A leakage-aware pipeline: 26 features over 195 thousand rows, with no closure-time fields and no same-day future events.

**Slide 10 — Phase 4 divider**
Phase four. Modeling.

**Slide 11 — Modeling**
Histogram Gradient Boosting wins, and repository workflow context dominates raw pull request size.

**Slide 12 — Phase 5 divider**
Phase five. Evaluation.

**Slide 13 — Evaluation**
At the top one percent of risk, non-merge precision reaches ninety-nine percent — about seven times the baseline.

**Slide 14 — Phase 6 divider**
Phase six. Deployment.

**Slide 15 — Deployment & Conclusions**
A maintainer dashboard for prioritization, never an automated decision system.

**Slide 16 — End**
Thank you. Questions welcome.
