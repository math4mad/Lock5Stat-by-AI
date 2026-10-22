"""Generate one quarto note per Phase 2 question (phase2/qNN-slug.qmd).

Run from the repo root:  python3 scripts/phase2/build_notes.py
Numbers are baked from the retrieved Kaggle results JSONs (seed 2026);
EDA plots execute live against data/phase2/q*.csv at render time.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "phase2"

TEMPLATE = '''---
title: "@@TITLE@@"
subtitle: "@@SUBTITLE@@"
author: "Lock5Stat-by-AI"
date: today
jupyter: python3
---

```{python}
#| include: false
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# run from the repo root so data/... paths resolve regardless of note location
_root = Path.cwd()
while not (_root / "_quarto.yml").exists():
    _root = _root.parent
os.chdir(_root)

sns.set_theme(style="whitegrid")
df = pd.read_csv("@@CSV@@", comment="#")
```

# Question

@@QUESTION@@

## Data source

@@DATA@@

# Exploratory analysis

```{python}
#| echo: false
#| fig-cap: "@@FIGCAP@@"
@@PLOT@@
```

# Methods & results

@@METHODS@@

@@TESTS@@

# Decision

@@DECISION@@

*Reproduce:* `scripts/phase2/@@SCRIPT@@` → retrieved output in
`scripts/phase2/kaggle_results/@@RESDIR@@/` (seed 2026; randomization /
bootstrap with 100,000 replicates run on Kaggle).
'''

Q = []

Q.append(dict(
    num=1, slug="handwashing", resdir="q1-handwashing", script="q1_handwashing.py",
    title="What Proportion of People Wash Their Hands?",
    subtitle="Q1 · Harris Interactive / ASM & SDA (2005)",
    csv="data/phase2/q1_handwashing.csv",
    question=("**What proportion of people using a public restroom wash their hands?** "
              "Harris Interactive, for the American Society for Microbiology (ASM) and the "
              "Soap & Detergent Association (SDA), had observers discreetly record the "
              "handwashing behaviour of 6,336 adults in public restrooms at six major U.S. "
              "attractions (Aug 2005), and separately asked people by telephone whether "
              "they *always* wash."),
    data=("Constructed CSV from the published per-venue, per-sex counts (Harris Interactive "
          "for ASM/SDA, *A Survey of Hand Washing Behavior — 2005 Findings*). No Lock5 "
          "dataset ships for this study. Press headline: 83%; the exact counts give 82.0%."),
    figcap="Observed handwashing proportion by venue (dashed line: 91% self-reported rate)",
    plot='''v = df.groupby("venue", as_index=False)[["n", "washed"]].sum()
v["prop"] = v["washed"] / v["n"]
v = v.sort_values("prop")
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.barh(v["venue"], v["prop"], color="#4c72b0")
ax.axvline(0.91, ls="--", color="#c44e52")
ax.text(0.905, 0.1, "self-report 91%", color="#c44e52", ha="right", fontsize=9)
ax.set_xlim(0, 1)
ax.set_xlabel("Observed handwashing proportion")
plt.tight_layout()
plt.show()''',
    methods=("One-proportion inference on p̂ with the Wald interval; parametric z-tests "
             "against H₀: p = 0.5 (majority) and H₀: p = 0.91 (self-report), each "
             "validated with 100k-replicate randomization and bootstrap."),
    tests='''| Quantity | Value |
|---|---|
| Observed proportion p̂ | **82.0%** (5,195 / 6,336) |
| 95% CI (Wald / bootstrap) | (81.0%, 82.9%) / (81.0%, 82.9%) |
| z vs 50% (majority) | z = 50.9, p < 1e-15 (randomization p < 1e-5) |
| z vs 91% self-report | z = −25.1, p ≈ 8e-139 (randomization p < 1e-5) |
| Female vs male | 89.5% vs 74.6% |''',
    decision=("**Most people do wash their hands** — but the observed 82% sits dramatically "
              "below the 91% self-reported rate. Self-reports of hygiene are inflated by "
              "roughly 9 percentage points, and the gap is largest among men "
              "(89.5% vs 74.6%). A classic case of social-desirability bias made measurable."),
))

Q.append(dict(
    num=2, slug="turnback", resdir="q2-turnback", script="q2_turnback.py",
    title="Would Parents Choose Children Again?",
    subtitle="Q2 · Ann Landers (1976) vs Newsday / Kansas City Star random samples",
    csv="data/phase2/q2_turnback.csv",
    question=("**If parents could turn back time, would they still choose to have children?** "
              "In 1976 advice columnist Ann Landers posed this question to her readers and "
              "received ≈10,000 responses — about 70% said \"no.\" Lock⁵ contrasts this "
              "famous result with contemporary random-sample polls of parents."),
    data=("Counts compiled in Lock⁵ (Lock et al. 2021): Landers voluntary column (n = 10,000), "
          "Newsday nationwide random sample (n = 1,373), Kansas City Star random sample of "
          "KC parents (n = 409). No Lock5 dataset file; Newsday counts reconstructed from "
          "the published 91% figure."),
    figcap="Would do it again — by sampling method (voluntary column vs random samples)",
    plot='''w = df.pivot_table(index=["study", "method"], columns="response",
                   values="count", aggfunc="sum")
w["phat"] = w["yes"] / (w["yes"] + w["no"])
labels = {"landers_1976": "Ann Landers\\n(voluntary column)",
          "newsday_1976": "Newsday\\n(random sample)",
          "kc_star_1976": "KC Star\\n(random sample)"}
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.bar([labels[s] for s in w.index.get_level_values("study")], w["phat"],
       color=["#c76c6c", "#8fbf8f", "#8fbf8f"])
ax.set_ylim(0, 1)
ax.set_ylabel("Proportion answering \\"yes\\"")
for x, p in enumerate(w["phat"]):
    ax.text(x, p + 0.02, f"{p:.0%}", ha="center")
plt.tight_layout()
plt.show()''',
    methods=("One-proportion CIs for each sample; two-proportion z-tests with pooled SE "
             "for the three pairwise contrasts, each validated with 100k-replicate "
             "randomization and bootstrap."),
    tests='''| Sample | Method | "Yes" share |
|---|---|---|
| Ann Landers 1976 | voluntary column | **30.0%** (3,000 / 10,000) |
| Newsday 1976 | random, US parents | 91.0% (1,250 / 1,373) |
| Kansas City Star 1976 | random, KC parents | 93.9% (384 / 409) |

| Comparison | Diff | Test |
|---|---|---|
| Newsday − Landers | +61.0 pp | z = 43.8, p ≈ 0 (randomization p < 1e-5) |
| KC Star − Landers | +63.9 pp | p ≈ 0 |
| KC Star − Newsday | +2.9 pp | p = 0.067 (not significant) |''',
    decision=("The infamous \"70% wouldn't do it again\" was pure **voluntary-response "
              "bias**: aggrieved readers self-select into writing in. Random samples agree "
              "at ~91–94%, and the two random samples are statistically indistinguishable "
              "from each other — a textbook demonstration of why sampling method dominates "
              "sample size."),
))

Q.append(dict(
    num=3, slug="spider", resdir="q3-spider", script="q3_spider.py",
    title="Why Do Adolescent Spiders Engage in Foreplay?",
    subtitle="Q3 · Pruitt, Burghardt & Riechert (2012), *Anelosimus studiosus*",
    csv="data/phase2/q3_spider.csv",
    question=("**Why do adolescent spiders engage in foreplay?** Pruitt, Burghardt & "
              "Riechert (2012, *Ethology*) observed nonconceptive courtship (\"foreplay\") "
              "in *Anelosimus studiosus* males before sperm transfer. One hypothesis: "
              "courtship play is a costly signal — aggressive, high-play males pay a price "
              "in mating outcomes."),
    data=("Calibrated reconstruction (n = 45 males) matching the paper's published "
          "statistics (play bouts by personality; kept-female rates). Raw per-male data "
          "were never published; reconstruction check: LR χ² = 13.9 vs paper's 15.9 for "
          "personality."),
    figcap="Proportion of males that kept the female, high-play vs low-play",
    plot='''med = df["play_bouts"].median()
df["grp"] = np.where(df["play_bouts"] > med, "high play", "low play")
p = df.groupby("grp")["kept_female"].mean().reindex(["low play", "high play"])
fig, ax = plt.subplots(figsize=(5.5, 4))
ax.bar(p.index, p.values, color=["#8fbf8f", "#c76c6c"])
ax.set_ylim(0, 0.55)
ax.set_ylabel("Proportion that kept the female")
for x, v in enumerate(p.values):
    ax.text(x, v + 0.01, f"{v:.0%}", ha="center")
plt.tight_layout()
plt.show()''',
    methods=("Two-proportion z (one-sided: high-play keeps less), Fisher exact, "
             "100k-replicate randomization, and 10k-resample bootstrap CI of the "
             "difference; personality–play link via logistic regression LR χ²."),
    tests='''| Method | Result |
|---|---|
| High-play vs low-play kept rate | 15% (3/20) vs 40% (10/25), diff = −25 pp |
| Two-proportion z (one-sided) | z = −1.84, **p = 0.033** |
| Fisher exact (one-sided) | OR = 0.26, p = 0.064 |
| Randomization (100k) | p = 0.063 |
| Bootstrap 95% CI of diff | (−0.50, +0.01) — touches 0 |
| Personality → play bouts (LR χ²) | χ² = 13.9 vs paper's 15.9 (p < 0.001) |''',
    decision=("**Suggestive but not decisive.** High-play (aggressive) males are less likely "
              "to end up with the female, consistent with courtship play as a *cost* paid "
              "mainly by aggressive phenotypes. With n = 45 the bootstrap CI touches zero — "
              "direction is credible (randomized-style design), magnitude is uncertain."),
))

Q.append(dict(
    num=4, slug="intergen", resdir="q4-intergen", script="q4_intergen.py",
    title="Do Parents' Experiences Affect Future Children?",
    subtitle="Q4 · Ng et al. (2010, *Nature*) — paternal high-fat diet",
    csv="data/phase2/q4_intergen.csv",
    question=("**How broadly do experiences of parents affect their future children?** "
              "Ng et al. (2010, *Nature*) put founder male rats on a high-fat diet, mated "
              "them, and raised the F1 daughters on standard chow — isolating the paternal "
              "*pre-conception* environment from anything postnatal."),
    data=("Seeded rescale (n = 34 rows) to the paper's published mean ± SEM group summaries; "
          "per-animal raw data are not public, so p-values approximate the paper's. "
          "Fathers: 8 control vs 9 high-fat."),
    figcap="Daughter insulinogenic index (6 wk) by father's diet",
    plot='''off = df[df["cohort"] == "offspring"]
fig, ax = plt.subplots(figsize=(5.5, 4))
sns.boxplot(data=off, x="father_diet", y="insulinogenic_index",
            hue="father_diet", palette=["#8fbf8f", "#c76c6c"], legend=False, ax=ax)
sns.stripplot(data=off, x="father_diet", y="insulinogenic_index",
              color="0.25", size=4, ax=ax)
ax.set_xlabel("Father's diet")
ax.set_ylabel("Insulinogenic index (daughter, 6 wk)")
plt.tight_layout()
plt.show()''',
    methods=("Welch t-tests for father manipulation checks; two-sample comparisons with "
             "Cohen's d, 100k-replicate randomization and bootstrap CIs for offspring "
             "endpoints."),
    tests='''| Endpoint | Result |
|---|---|
| Fathers: body weight (manipulation check) | 705 g vs 550 g, d = −3.45, p ≈ 3.6e-6 |
| Daughter insulinogenic index | 38.7 vs 86.8 (halved), d = 2.58, randomization p = 0.0004 |
| Daughter glucose peak (6 wk) | impaired, p = 0.023 |
| Islet gene expression | 56 / 77 genes down-regulated, p = 6.6e-05 |
| Daughter body weight (12 wk) | unaffected, p = 0.47 |''',
    decision=("Paternal high-fat diet **reprograms daughter β-cell function without "
              "obesity** — the effect is specific (insulin secretion / glucose tolerance), "
              "not a generalized growth effect. A clean experimental demonstration of "
              "intergenerational metabolic programming (reconstruction caveat applies)."),
))

Q.append(dict(
    num=5, slug="aboveavg", resdir="q5-aboveavg", script="q5_aboveavg.py",
    title="Are Professors “Above-Average” Teachers?",
    subtitle="Q5 · Cross (1977) faculty self-ratings",
    csv="data/phase2/q5_aboveavg.csv",
    question=("**What percent of college professors consider themselves \"above-average\" "
              "teachers?** Cross (1977, \"Not can, but will: college teaching\") reported "
              "faculty self-ratings across U.S. colleges."),
    data=("Reconstructed counts (n = 250) calibrated to the published 94% headline figure; "
          "the original per-institution breakdown is not available."),
    figcap="Self-rated above-average vs the statistical ceiling",
    plot='''fig, ax = plt.subplots(figsize=(5.5, 4))
ax.bar(["Self-rated above\\naverage", "Statistically\\npossible"], [0.94, 0.50],
       color=["#c76c6c", "#999999"])
ax.axhline(0.5, ls="--", color="k", lw=0.8)
ax.set_ylim(0, 1)
ax.set_ylabel("Proportion")
for x, v in enumerate([0.94, 0.50]):
    ax.text(x, v + 0.02, f"{v:.0%}", ha="center")
plt.tight_layout()
plt.show()''',
    methods=("One-proportion z vs H₀: p = 0.5, exact binomial, 100k-replicate "
             "randomization, and Wald + bootstrap CIs."),
    tests='''| Method | Result |
|---|---|
| Point estimate | p̂ = **94%** above average (235 / 250) |
| 95% CI (Wald / bootstrap) | (91.1%, 96.9%) / (90.8%, 96.8%) |
| z vs 50% | z = 13.9, p ≈ 5e-44 |
| Exact binomial (two-sided) | p ≈ 5e-52 |
| Randomization (100k) | p < 1e-5 |''',
    decision=("Statistically **impossible** for 94% to be above average — at most ~50% plus "
              "sampling noise can exceed the median. A textbook better-than-average effect "
              "(illusory superiority), rivalling the famous 93% of drivers who rate "
              "themselves above average."),
))

Q.append(dict(
    num=6, slug="highfives", resdir="highfives", script="q6_highfives.py",
    title="Do High Fives Help Teams Win?",
    subtitle="Q6 · Kraus, Huang & Keltner (2010), NBA touch study",
    csv="data/phase2/q6_highfives.csv",
    question=("**Does giving lots of high fives to teammates help sports teams win?** "
              "Kraus, Huang & Keltner (2010, *Emotion*) had two independent coder teams "
              "record celebratory teammate touch — high fives, fist bumps, chest bumps, "
              "hugs, huddles — for 294 players across all 30 NBA teams in the first two "
              "months of the 2008–09 season, then asked whether early-season touch "
              "predicted later performance."),
    data=("`win_pct` = real 2008–09 final standings (public record); per-player touch "
          "seconds were never published, so that column is a seeded (2026) reconstruction "
          "calibrated to the paper's 1.80 s mean and to Boston / L.A. being the touchiest "
          "teams. Results characterise the documented reconstruction, not a literal "
          "replication of the paper's statistics."),
    figcap="Early-season celebratory touch vs final win percentage, 2008–09 NBA",
    plot='''fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.scatter(df["touch_sec_per_player"], df["win_pct"], s=42,
           color="#4c72b0", alpha=0.85)
b, a = np.polyfit(df["touch_sec_per_player"], df["win_pct"], 1)
xs = np.linspace(df["touch_sec_per_player"].min(),
                 df["touch_sec_per_player"].max(), 50)
ax.plot(xs, a + b * xs, color="#c44e52")
ax.set_xlabel("Touch seconds per player (first 2 months)")
ax.set_ylabel("Final win percentage")
plt.tight_layout()
plt.show()''',
    methods=("Pearson correlation with Fisher-z CI (parametric), 100k-permutation "
             "randomization test, and 100k-resample percentile bootstrap."),
    tests='''| Quantity | Value |
|---|---|
| Teams (n) | 30 |
| Pearson r | **0.750** |
| R² | 0.562 |
| Parametric p (t) | 1.9e-06 |
| Randomization p (100k) | < 1e-05 |
| Fisher-z 95% CI | (0.534, 0.874) |
| Bootstrap 95% CI | (0.553, 0.896) |''',
    decision=("**Reject H₀: teams whose players touch more win more** — touch alone "
              "explains 56% of the variance in final win percentage. Direction matches the "
              "paper's cooperation interpretation; caveats: reconstructed touch column, "
              "and observational association (winning may also cause celebration)."),
))

Q.append(dict(
    num=7, slug="warmup", resdir="warmup", script="q7_warmup.py",
    title="Short Mild vs Long Intense Warm-Up?",
    subtitle="Q7 · Neiva et al. (2015), randomized crossover in swimmers",
    csv="data/phase2/q7_warmup.csv",
    question=("**Which is better for peak performance: a short mild warm-up or a long "
              "intense warm-up?** Neiva et al. (2015, *J Strength Cond Res*) had 11 elite "
              "swimmers complete a randomized crossover of a 600 m (short, mild) vs 1,800 m "
              "(long, intense) warm-up before 100 m time trials."),
    data=("Reconstruction of the published group means/SDs (n = 11; SWU 59.38 ± 2.18 s, "
          "LWU 60.18 ± 2.46 s). Within-swimmer pairing assumed r = 0.50, with a documented "
          "sensitivity analysis across r = 0.3–0.9."),
    figcap="Individual 100 m times under each warm-up (grey: swimmers; colour: means)",
    plot='''fig, ax = plt.subplots(figsize=(5.5, 4))
for _, r in df.iterrows():
    ax.plot([0, 1], [r["swu_100m_s"], r["lwu_100m_s"]],
            marker="o", color="grey", alpha=0.45, lw=0.9)
ax.plot([0, 1], [df["swu_100m_s"].mean()] * 2, marker="o", lw=3,
        color="#8fbf8f", label="mean (short mild)")
ax.plot([0, 1], [df["lwu_100m_s"].mean()] * 2, marker="o", lw=3,
        color="#c76c6c", label="mean (long intense)")
ax.set_xticks([0, 1], ["Short mild\\n(600 m)", "Long intense\\n(1,800 m)"])
ax.set_ylabel("100 m time (s)")
ax.legend()
plt.tight_layout()
plt.show()''',
    methods=("Paired t-test (pairing assumption r = 0.5), sign-flip randomization "
             "(100k), bootstrap CI of the mean difference, plus Welch unpaired test and "
             "a pairing-correlation sensitivity analysis."),
    tests='''| Method | Result |
|---|---|
| Mean 100 m time | 59.38 s (SWU) vs 60.18 s (LWU), diff = −0.80 s |
| Paired t (r = 0.5 assumption) | t(10) = −1.14, p = 0.282 |
| Sign-flip randomization | p = 0.282 |
| Bootstrap 95% CI | (−2.13, +0.48) s |
| Welch (unpaired) | t = −0.81, p = 0.429 |
| Sensitivity (r = 0.9) | p = 0.033 |''',
    decision=("**Not significant at the assumed pairing.** With n = 11 the study cannot "
              "rule out a meaningful effect; the direction favours the short mild warm-up, "
              "consistent with the paper's caution that a long intense warm-up *may* "
              "impair 100 m performance. Only under near-perfect pairing (r = 0.9) would "
              "significance emerge — an honest example of small-sample ambiguity."),
))

Q.append(dict(
    num=8, slug="urban", resdir="urban", script="q8_urban.py",
    title="Are City Dwellers More Anxious and Depressed?",
    subtitle="Q8 · Peen et al. (2007), NEMESIS (n = 7,076 Dutch adults)",
    csv="data/phase2/q8_urban.csv",
    question=("**Are city dwellers more likely than country dwellers to have mood and "
              "anxiety disorders?** Peen, Dekker, Schoevers & ten Have (2007) analysed the "
              "NEMESIS population survey across five urbanization levels; Lock⁵'s phase-2 "
              "question contrasts the most vs least urbanized."),
    data=("Published Table 2 counts from NEMESIS-1 (Peen et al. 2007) — near-exact "
          "reconstruction. Headline context: Peen, Schoevers, Beekman & Dekker (2010) "
          "meta-analysis."),
    figcap="Mood and anxiety disorder rates by urbanization level (NEMESIS)",
    plot='''u = df.assign(mood=df["mood_cases"] / df["n"],
              anx=df["anxiety_cases"] / df["n"])
x = np.arange(len(u))
w = 0.38
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(x - w / 2, u["mood"], w, label="Mood disorders", color="#c76c6c")
ax.bar(x + w / 2, u["anx"], w, label="Anxiety disorders", color="#4c72b0")
ax.set_xticks(x, [s.replace(" ", "\\n") for s in u["urbanization"]], fontsize=8)
ax.set_ylabel("Prevalence")
ax.legend()
plt.tight_layout()
plt.show()''',
    methods=("Two-proportion z (pooled) and Fisher exact for city vs country contrasts on "
             "each outcome, odds ratios with bootstrap CIs, and 100k-replicate "
             "randomization tests."),
    tests='''| Outcome | City vs country | OR | p |
|---|---|---|---|
| Mood disorders | 10.4% vs 5.3% (+5.1 pp) | 2.06 (bootstrap CI excludes 1) | z p = 3.7e-6 · Fisher p = 3.8e-6 · rand. p < 1e-5 |
| Anxiety disorders | 14.4% vs 10.8% (+3.6 pp) | 1.39 | z p = 0.0075 · rand. p = 0.008 |''',
    decision=("**Reject H₀ for both outcomes** — urbanicity is significantly associated "
              "with mood and anxiety disorders, matching the Peen et al. (2010) "
              "meta-analysis headline. Observational: urbanicity may proxy for other risk "
              "factors (social drift, crowding, pollution), so the causal pathway is open."),
))

Q.append(dict(
    num=9, slug="beautysleep", resdir="beautysleep", script="q9_beautysleep.py",
    title="Is There Truth to “Beauty Sleep”?",
    subtitle="Q9 · Axelsson et al. (2010, *BMJ*) sleep-deprivation photos",
    csv="data/phase2/q9_beautysleep.csv",
    question=('**Is there truth to the saying "beauty sleep"?** Axelsson et al. (2010, '
              "*BMJ*) photographed 23 adults after a normal 8 h sleep and again after "
              "31 h of sleep deprivation; independent observers (65 in the paper) rated "
              "the photos on 0–100 mm visual analogue scales."),
    data=("Reconstruction of per-participant ratings calibrated to the published condition "
          "means (health, tiredness, attractiveness); n = 23 participants."),
    figcap="Attractiveness ratings: 8 h sleep vs 31 h sleep deprivation (paired)",
    plot='''fig, ax = plt.subplots(figsize=(5.5, 4))
for _, r in df.iterrows():
    ax.plot([0, 1], [r["attract_normal"], r["attract_deprived"]],
            marker="o", color="grey", alpha=0.45, lw=0.9)
ax.plot([0, 1], [df["attract_normal"].mean()] * 2, marker="o", lw=3,
        color="#4c72b0", label="mean")
ax.set_xticks([0, 1], ["After 8 h sleep", "After 31 h awake"])
ax.set_ylabel("Attractiveness rating (0–100)")
ax.legend()
plt.tight_layout()
plt.show()''',
    methods=("Paired t-tests on each outcome, sign-flip randomization on the paired "
             "differences (100k), and percentile bootstrap CIs of the mean differences."),
    tests='''| Outcome (deprived − normal) | Mean diff | Paired t p | Randomization p |
|---|---|---|---|
| Health | −5.0 | 9e-08 | ≤ 1e-5 |
| Tiredness | +9.0 | < 1e-13 | ≤ 1e-5 |
| Attractiveness | −2.0 | 4e-04 | ≤ 1e-5 |''',
    decision=("**Sleep-deprived faces are rated less healthy, more tired, and less "
              "attractive** — all three outcomes move in the expected direction with "
              "randomization p ≤ 1e-5. The saying holds up experimentally."),
))

Q.append(dict(
    num=10, slug="boomerang", resdir="q10-boomerang", script="q10_boomerang.py",
    title="Moving Back in With Mom and Dad?",
    subtitle="Q10 · Pew Research Center (Fry, Passel & Cohn 2020), CPS counts",
    csv="data/phase2/q10_boomerang.csv",
    question=("**What percent of young adults in the US move back in with their parents?** "
              "Pew Research Center tracked CPS counts of 18–29-year-olds living with "
              "parents through the COVID-19 pandemic (Fry, Passel & Cohn, Sept 2020)."),
    data=("Published percentages / counts from the Pew report (CPS Feb & Jul 2020); "
          "subgroup denominators documented constructions."),
    figcap="Share of 18–29-year-olds living with parents, July 2020 (dashed: Feb 2020 overall)",
    plot='''g = df.pivot_table(index=["group", "period"], columns="response",
                   values="count", aggfunc="sum").reset_index()
g["share"] = g["with_parent"] / (g["with_parent"] + g["not_with_parent"])
jul = g[g["period"] == "jul_2020"].sort_values("share")
feb_overall = g[(g["period"] == "feb_2020") &
                (g["group"] == "overall")]["share"].iloc[0]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.barh(jul["group"], jul["share"], color="#4c72b0")
ax.axvline(feb_overall, ls="--", color="#c44e52")
ax.text(feb_overall + 0.005, 0.1, "Feb 2020 overall", color="#c44e52", fontsize=8)
ax.set_xlim(0, 0.85)
ax.set_xlabel("Share living with parents (Jul 2020)")
plt.tight_layout()
plt.show()''',
    methods=("One-proportion Wald + bootstrap CIs; two-proportion z for Feb-vs-Jul and "
             "demographic contrasts, validated with 100k-replicate randomization."),
    tests='''| Comparison | Result |
|---|---|
| All 18–29 y/o, Jul 2020 | **52.0%** with parents (26.6 M) — record since 1940 |
| vs Feb 2020 (47.0%) | diff +5.0 pp, p < 1e-15 |
| Men vs women (Jul) | 55% vs 49% |
| Ages 18–24 vs 25–29 (Jul) | 71% vs 28% |''',
    decision=("The pandemic \"boomerang\" pushed a **majority of young adults back home** "
              "for the first time since the Great Depression era; the steep age gradient "
              "shows the effect concentrates among the youngest adults."),
))

Q.append(dict(
    num=11, slug="barmusic", resdir="barmusic", script="q11_barmusic.py",
    title="Does Loud Bar Music Make People Drink More?",
    subtitle="Q11 · Guéguen, Jacob, Le Guellec, Lourel & Pascual (2008)",
    csv="data/phase2/q11_barmusic.csv",
    question=("**Does turning up the music in a bar cause people to drink more beer?** "
              "Guéguen et al. (2008, *Alcoholism: Clin Exp Res*) observed 40 male beer "
              "patrons in a bar on nights with the sound level at 88 vs 72 dB, recording "
              "glasses consumed and time per glass."),
    data=("Group means reproduced exactly from the paper; the 20/20 per-patron split and "
          "SDs are a documented reconstruction. Naturalistic field experiment — sound "
          "level varied by night, not randomized per patron."),
    figcap="Glasses of beer consumed per patron by sound level",
    plot='''fig, ax = plt.subplots(figsize=(5.5, 4))
sns.boxplot(data=df, x="condition", y="glasses", hue="condition",
            palette=["#8fbf8f", "#c76c6c"], legend=False, ax=ax)
sns.stripplot(data=df, x="condition", y="glasses", color="0.25", size=4, ax=ax)
ax.set_xlabel("Sound level")
ax.set_ylabel("Glasses consumed")
plt.tight_layout()
plt.show()''',
    methods=("Welch two-mean tests on both outcomes, normal approximation and "
             "100k-replicate randomization, bootstrap CIs of the differences."),
    tests='''| Outcome | 88 dB vs 72 dB | Test |
|---|---|---|
| Glasses consumed | +0.80 glasses | Welch t(37.8) = 2.97, **p = 0.005**; randomization p = 0.009 |
| Time per glass | −3.06 min | Welch t ≈ −4.9, **p < 1e-4**; randomization p < 1e-4 |''',
    decision=("**Louder music → faster drinking**: patrons drank more glasses because each "
              "glass took less time. Effect small but reliable; the causal reading is "
              "suggestive since patrons were not individually randomized to sound levels."),
))

Q.append(dict(
    num=12, slug="nose", resdir="nose", script="q12_nose.py",
    title="Is Your Nose Getting Bigger?",
    subtitle="Q12 · Sforza et al. (2011), digital anthropometry, 859 Italians",
    csv="data/phase2/q12_nose.csv",
    question=("**Is your nose getting bigger?** Sforza et al. (2011, *Forensic Sci Int*) "
              "measured external nose dimensions by digital anthropometry in Italians aged "
              "4–80; here the 519 men of published Table 1 (grouped means by age)."),
    data=("Published Table 1 grouped means by age (men); the women's table was "
          "inaccessible, so the analysis covers men only."),
    figcap="Mean nasal height and width by age (men, 4–80)",
    plot='''m = df[df["sex"] == "men"]
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.scatter(m["age_mid"], m["height_mean_mm"], label="Nasal height", color="#4c72b0")
ax.scatter(m["age_mid"], m["width_mean_mm"], label="Nasal width", color="#c76c6c")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Mean dimension (mm)")
ax.legend()
plt.tight_layout()
plt.show()''',
    methods=("Pearson correlations of each dimension with age (full span and adults-only), "
             "validated with 100k-replicate randomization tests."),
    tests='''| Association with age | r | Randomization p |
|---|---|---|
| Nasal height, ages 4–80 | 0.78 | 1.5e-4 |
| Nasal width, ages 4–80 | 0.92 | < 1e-4 |
| Nasal height, adults 18–80 | plateaus | — |
| Nasal width, adults 18–80 | **0.99** | 0.008 |''',
    decision=("**Yes — the nose keeps growing throughout adulthood**, and it is mainly the "
              "*width* (cartilage growth + gravity), while height plateaus after "
              "adolescence."),
))

Q.append(dict(
    num=13, slug="catvideos", resdir="catvideos", script="q13_catvideos.py",
    title="Do Cat Videos Improve Mood?",
    subtitle="Q13 · Myrick (2015), N = 6,795 retrospective pre/post ratings",
    csv="data/phase2/q13_catvideos.csv",
    question=("**Does watching cat videos improve mood?** Myrick (2015, *Computers in "
              "Human Behavior*) surveyed 6,795 respondents about cat-video viewing and "
              "rated 11 emotion scales before vs after (retrospective pre/post)."),
    data=("Published Table 2 aggregates (means/SDs, published t); the analytic paired t "
          "from these moments reproduces the published t within Δ ≈ 0.34."),
    figcap="Mean emotion change (after − before) across the 11 scales",
    plot='''d = df.assign(change=df["mean_after"] - df["mean_prior"]).sort_values("change")
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.barh(d["label"], d["change"],
        color=np.where(d["change"] > 0, "#8fbf8f", "#c76c6c"))
ax.axvline(0, color="k", lw=0.8)
ax.set_xlabel("Mean change (after − before), 1–5 scale")
plt.tight_layout()
plt.show()''',
    methods=("Analytic paired t-tests from published moments for all 11 scales; for the "
             "two composites, per-person paired data simulated (seed 2026) for "
             "sign-flip randomization (100k) and bootstrap CIs."),
    tests='''| Composite | Mean change | Paired t | Randomization p | Bootstrap 95% CI |
|---|---|---|---|---|
| Positive emotions | +0.77 | t = 51.1 | < 1e-5 | (0.74, 0.80) |
| Negative emotions | −0.74 | t = −60.1 | < 1e-5 | (−0.77, −0.71) |''',
    decision=("**Mood improves substantially after cat videos** — all 11 emotion scales "
              "move favourably (|t| ≥ 26). But this is a within-person retrospective "
              "association (recall and mood-congruent biases possible), not a causal "
              "experiment."),
))

Q.append(dict(
    num=14, slug="sleepfaces", resdir="sleepfaces", script="q14_sleepfaces.py",
    title="Does Sleep Deprivation Blur Emotional Faces?",
    subtitle="Q14 · Killgore et al., 54-participant within-subject study",
    csv="data/phase2/q14_sleepfaces.csv",
    question=("**Does sleep deprivation hurt one's ability to interpret facial "
              "expressions?** Killgore, Balkin, Yarnell & Capaldi had 54 healthy adults "
              "recognize Ekman morphed faces after a rested night vs 23.5 h awake "
              "(within-subject)."),
    data=("Reconstruction of per-participant percent-correct (20 trials per emotion) "
          "calibrated to means digitized from the paper's Fig. 3; paired-SD calibration "
          "documented."),
    figcap="Mean recognition difference (deprived − rested) by emotion",
    plot='''emotions = ["happiness", "sadness", "surprise", "fear", "disgust", "anger"]
diffs = [(df[f"{e}_deprived"] - df[f"{e}_rested"]).mean() for e in emotions]
sig = [e in ("happiness", "sadness") for e in emotions]
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.bar(emotions, diffs,
       color=["#c76c6c" if s else "#999999" for s in sig])
ax.axhline(0, color="k", lw=0.8)
ax.set_ylabel("Mean difference (deprived − rested), % correct")
plt.tight_layout()
plt.show()''',
    methods=("Paired t-tests per emotion, sign-flip randomization on paired differences "
             "(100k), and percentile bootstrap CIs; overall average also tested."),
    tests='''| Emotion | Mean diff (deprived − rested) | Randomization p |
|---|---|---|
| Happiness | −1.30 | **0.0050** |
| Sadness | −2.59 | **0.0047** |
| Surprise | −0.46 | 0.78 |
| Fear / disgust / anger | ≈ 0 | n.s. |
| Overall average | ≈ 0 | 0.86 |''',
    decision=("The deficit is **emotion-specific**: recognition of happiness and sadness "
              "is impaired while the average across emotions looks null (p = 0.86). "
              "Averaging would have masked the effect entirely — a nice argument against "
              "blindly collapsing multi-outcome experiments."),
))

Q.append(dict(
    num=15, slug="sweetener", resdir="sweetener", script="q15_sweetener.py",
    title="Do Artificial Sweeteners Cause Weight Gain?",
    subtitle="Q15 · Fowler et al. (2008, *Obesity*), San Antonio Heart Study",
    csv="data/phase2/q15_sweetener.csv",
    question=("**Do artificial sweeteners cause weight gain?** Fowler et al. (2008, "
              "*Obesity*) followed 3,682 San Antonio Heart Study participants for 7–8 "
              "years, comparing diet-soda users with non-users on BMI change and "
              "overweight/obesity incidence."),
    data=("Baseline 2×2 back-calculated from the published figures; ΔBMI SDs derived from "
          "published CIs. Observational cohort — users vs non-users were not randomized."),
    figcap="Mean BMI change over 7–8 years by diet-soda consumption",
    plot='''d = df[df["metric"] == "mean_dbmi_kg_m2"].sort_values("value")
fig, ax = plt.subplots(figsize=(6.5, 3.6))
ax.barh(d["group"], d["value"], color="#4c72b0")
ax.set_xlabel("Mean ΔBMI (kg/m² over follow-up)")
plt.tight_layout()
plt.show()''',
    methods=("Two-proportion z and Fisher exact for the overweight/obesity contrast, odds "
             "ratio with bootstrap CI, 100k-replicate randomization; published incidence "
             "ORs and adjusted ΔBMI reported alongside."),
    tests='''| Analysis | Result |
|---|---|
| Overweight/obesity, user vs non-user | OR = 1.38, z = 4.44, p = 8.9e-6 · Fisher p = 1.0e-5 · rand. p = 2e-5 |
| ΔBMI over 7–8 y | users +1.48 vs non-users +1.01 kg/m² (+47%, published p < 0.0001) |
| Published incidence ORs | 1.93 (overweight), 2.03 (obesity) |''',
    decision=("A **strong observational association** — consistent in the cross-section "
              "and the incidence analyses. But causation is unproven: reverse causality "
              "(overweight people switching to diet soda) and confounding by baseline "
              "adiposity remain live alternatives."),
))

Q.append(dict(
    num=16, slug="latenight", resdir="latenight", script="q16_latenight.py",
    title="Does Late-Night Eating Impair Concentration?",
    subtitle="Q16 · Spaeth, Dinges & Goel (SLEEP 2015), UPenn sleep-restriction lab",
    csv="data/phase2/q16_latenight.csv",
    question=("**Does late-night eating impair concentration?** Spaeth, Dinges & Goel "
              "(SLEEP 2015) studied 44 adults during a week of sleep restriction (4 h/night); "
              "some were allowed to eat at night, others fasted — a randomized experiment "
              "with PVT reaction time and attention lapses as endpoints."),
    data=("Reconstruction calibrated to the published qualitative claims (the conference "
          "abstract reports no numeric tables). Lock⁵ 3e exercise 1.110 \"Late Night "
          "Bites.\""),
    figcap="Change in PVT reaction time (night 4 − night 1) by group",
    plot='''df["rt_change"] = df["pvt_rt_n4_ms"] - df["pvt_rt_n13_ms"]
fig, ax = plt.subplots(figsize=(5.5, 4))
sns.boxplot(data=df, x="group", y="rt_change", hue="group",
            palette=["#c76c6c", "#8fbf8f"], legend=False, ax=ax)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel("Group")
ax.set_ylabel("Δ reaction time night 4 − night 1 (ms)")
plt.tight_layout()
plt.show()''',
    methods=("Welch two-mean tests at night 4, 100k-replicate randomization and bootstrap "
             "CIs; within-subject change and a difference-in-differences comparison with "
             "randomization p-values."),
    tests='''| Endpoint (night 4) | Eaters vs fasters | p |
|---|---|---|
| PVT reaction time | +28.9 ms worse | 0.026 |
| Attention lapses | +2.1 more | 0.011 |
| Within-subject decline (diff-in-diff, lapses) | eaters declined, fasters stable | rand. p = 0.0025 |''',
    decision=("**Consistent with the published claim**: allowing late-night eating did not "
              "protect — eaters showed worse reaction times and more lapses than fasters "
              "by night 4. Caveat: reconstruction calibrated to qualitative claims, so "
              "magnitudes are approximate."),
))

Q.append(dict(
    num=17, slug="organic", resdir="organic", script="q17_organic.py",
    title="Does Eating Organic Food Improve Your Health?",
    subtitle="Q17 · Magnér et al. (2015, IVL/Coop Sweden) — Lock⁵ dataset OrganicEffect",
    csv="data/phase2/q17_organic.csv",
    question=("**Does eating organic food improve your health?** In the IVL/Coop Sweden "
              "within-family pilot (Magnér et al. 2015), one family switched from a "
              "conventional to an organic diet for two weeks; urinary pesticide "
              "concentrations were measured before, during and after. Lock⁵ ships the "
              "raw data as *OrganicEffect* (160 paired measurements)."),
    data=("REAL Lock5 dataset (`OrganicEffect`) — exact, verbatim. n = 5 family members × "
          "8 pesticides, paired conventional vs organic measurements. Endpoint is "
          "*exposure*, not a clinical health outcome; single family, diet order not "
          "randomized."),
    figcap="Urinary pesticide concentration, conventional vs organic diet (paired)",
    plot='''fig, ax = plt.subplots(figsize=(5.5, 4))
ax.boxplot([df["NonOrganic"], df["Organic"]], tick_labels=["Conventional", "Organic"])
ax.set_ylabel("Urinary pesticide (µg/g creatinine)")
plt.tight_layout()
plt.show()''',
    methods=("Paired t-test, Wilcoxon signed-rank (non-parametric), sign-flip "
             "randomization (100k), bootstrap CI of the mean difference, Cohen's d and "
             "percent reduction."),
    tests='''| Method | Result |
|---|---|
| Mean concentration | 38.76 → 2.83 µg/g creatinine (**−92.7%**) |
| Mean diff | +35.93 (bootstrap CI excludes 0), d = 0.37 |
| Paired t | t(159) = 4.71, **p = 5.3e-6** |
| Wilcoxon signed-rank | p = 3.7e-22 |
| Sign-flip randomization (100k) | p < 1e-5 |''',
    decision=("**Switching to an organic diet dramatically cut pesticide exposure within "
              "days** — the cleanest experimental evidence in this whole question set. "
              "But the endpoint is exposure rather than a health outcome, and with a "
              "single family and non-randomized diet order, generalization is limited."),
))


def main():
    OUT.mkdir(exist_ok=True)
    for q in Q:
        body = (
            TEMPLATE.replace("@@TITLE@@", q["title"])
            .replace("@@SUBTITLE@@", q["subtitle"])
            .replace("@@CSV@@", q["csv"])
            .replace("@@QUESTION@@", q["question"])
            .replace("@@DATA@@", q["data"])
            .replace("@@FIGCAP@@", q["figcap"])
            .replace("@@PLOT@@", q["plot"])
            .replace("@@METHODS@@", q["methods"])
            .replace("@@TESTS@@", q["tests"])
            .replace("@@DECISION@@", q["decision"])
            .replace("@@SCRIPT@@", q["script"])
            .replace("@@RESDIR@@", q["resdir"])
        )
        path = OUT / f"q{q['num']:02d}-{q['slug']}.qmd"
        path.write_text(body)
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
