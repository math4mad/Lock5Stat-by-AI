# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q16_latenight.csv").write_text('# Phase 2, Q16: "Does late night eating impair concentration?"\n#\n# STUDY\n#   Spaeth AM, Dinges DF, Goel N (Unit for Experimental Psychiatry, Division\n#   of Sleep and Chronobiology, Perelman School of Medicine, University of\n#   Pennsylvania). Presented at SLEEP 2015, the 29th Annual Meeting of the\n#   Associated Professional Sleep Societies, Seattle WA, June 6-10, 2015.\n#   (The conference abstract PDF could not be retrieved - OUP Cloudflare\n#   block, Oct 2026.) Lock5 3e cites the press release (footnote 74 of\n#   exercise 1.110 "Late Night Eating", verified against the 3rd-edition\n#   textbook PDF, Oct 2026):\n#     University of Pennsylvania School of Medicine. "Eating less during late\n#     night hours may stave off some effects of sleep deprivation."\n#     ScienceDaily, June 4, 2015.\n#     https://www.sciencedaily.com/releases/2015/06/150604141905.htm\n#\n# DESIGN (facts from the press release)\n#   Randomized experiment. 44 healthy volunteers aged 21-50 had unlimited\n#   access to food and drink during the day but only 4 h of sleep per night\n#   (4:00-8:00 am) for three consecutive nights. On the fourth night (stay up\n#   to 4 am), participants were randomized: 20 kept unlimited food/drink\n#   access ("eat"), 24 received water only from 10 pm until 4 am ("fast").\n#   Every night at 2 am all subjects completed neurobehavioral tests measuring\n#   reaction time, attention lapses, working memory, sleepiness, stress, mood.\n#   Published findings:\n#     - Night 4: the fasting group performed significantly better on reaction\n#       time and had fewer attention lapses than the late-night-eating group.\n#     - Eaters were significantly slower and had more lapses on night 4 vs\n#       nights 1-3; fasters showed no such performance decline.\n#     - Sleep-restricted adults consume ~500 additional calories during\n#       late-night hours (Dinges quote).\n#\n# DATA SOURCE\n#   Lock5 distributes no dataset for this study (3rd-edition data page\n#   https://www.lock5stat.com/datapage3e.html checked Oct 2026; nearest\n#   matches LightatNight (mouse study), SleepCaffeine, SleepStudy,\n#   DietDepression - none is this experiment). Per-group means/SDs for the\n#   performance endpoints were not published anywhere retrievable (press\n#   release is qualitative), so this CSV is a documented reconstruction for\n#   method illustration only (same practice as q7_warmup.csv, q14_sleepfaces.csv).\n#\n# RECONSTRUCTION (seed 2026, numpy default_rng)\n#   - One row per participant (n = 44; group labels drawn by random shuffle,\n#     matching the published 20 eat / 24 fast split).\n#   - pvt_rt_n13_ms, pvt_rt_n4_ms: mean reaction time (ms) on the 2 a.m.\n#     psychomotor vigilance test, averaged over nights 1-3, and on night 4.\n#     Person-factor model: shared between-person vigilance factor across\n#     endpoints, night-to-night RT correlation 0.35 (between-person SD ~24 ms\n#     inside a total nightly SD ~40 ms). Columns affine-rescaled to the\n#     calibrated group moments below, then rounded to integer ms.\n#   - lapses_n13, lapses_n4: attention lapses (RT > 500 ms) per 10-min test.\n#     nights1-3 column = mean of three nightly integer counts (person latent +\n#     within-person nightly noise); night-4 column = one integer count.\n#   - Calibration anchors: published direction/significance of both findings\n#     plus PVT magnitudes typical of 4 h time-in-bed sleep restriction\n#     (Dinges et al. 1997, Sleep 20:267-277; Belenky et al. 2003, Sleep\n#     26:117-126): nights 1-3 both groups RT 330 +/- 40 ms, lapses ~4\n#     (randomized baseline); night 4 fast RT 333 +/- 40 ms / lapses ~4.1,\n#     eat RT 362 +/- 42 ms / lapses ~6.2.\n#   - Realized group stats (mean/SD): RT n13 eat 329.9/40.0, fast 330.1/40.1;\n#     RT n4 eat 361.9/42.0, fast 333.1/40.1; lapses n13 eat 4.13/1.94, fast\n#     4.51/2.95; lapses n4 eat 6.40/2.64, fast 4.33/2.43.\n#   - Realized analyses reproducing the published claims: Welch t on night 4\n#     (eat - fast): RT +28.9 ms, t(41.3)=2.32, p=.026; lapses +2.07, t(41.7)=\n#     2.68, p=.011. Paired night 4 vs nights 1-3, eaters: RT +32.0 ms, t(19)=\n#     3.08, p=.006; lapses +2.27, t(19)=3.66, p=.002. Fasters: n.s. (RT\n#     p=.68, lapses p=.74).\n#\n# CAVEAT: per-participant values are synthetic. Only the design facts and the\n#   direction/approximate magnitude of the effects are anchored to published\n#   material; analyses of this file illustrate the Lock5 inference pipeline\n#   and do not reproduce the study\'s exact (unpublished) statistics.\nsubject,group,pvt_rt_n13_ms,pvt_rt_n4_ms,lapses_n13,lapses_n4\n1,eat,322,317,5.00,8\n2,fast,358,355,1.67,4\n3,eat,344,350,1.33,3\n4,fast,334,305,9.67,10\n5,eat,412,364,5.00,10\n6,eat,408,356,6.00,7\n7,eat,363,385,1.33,8\n8,fast,364,392,1.00,3\n9,eat,296,337,6.33,7\n10,eat,346,385,1.00,8\n11,eat,325,353,6.33,9\n12,fast,339,313,5.33,4\n13,eat,312,292,2.33,0\n14,fast,333,326,6.67,5\n15,eat,363,429,6.67,7\n16,fast,288,296,4.33,3\n17,fast,278,341,5.00,5\n18,eat,304,385,5.00,8\n19,fast,286,313,3.33,4\n20,fast,235,290,0.67,0\n21,eat,284,358,3.00,2\n22,fast,391,383,3.00,6\n23,eat,299,324,4.33,6\n24,eat,326,284,0.67,6\n25,eat,300,382,3.67,8\n26,fast,382,359,1.67,8\n27,eat,255,318,4.33,5\n28,fast,337,395,7.67,6\n29,fast,374,288,2.33,3\n30,fast,309,344,9.67,6\n31,fast,334,330,3.00,1\n32,eat,365,445,4.67,10\n33,fast,343,374,10.33,7\n34,fast,333,338,3.00,6\n35,fast,348,298,5.67,2\n36,fast,338,368,7.00,6\n37,fast,367,345,1.33,5\n38,eat,291,395,6.00,3\n39,eat,335,398,6.00,7\n40,fast,366,393,6.00,5\n41,fast,344,328,2.00,3\n42,fast,263,272,6.67,2\n43,fast,278,248,1.33,0\n44,eat,348,382,3.67,6\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
"""Q16 (Phase 2): Does late night eating impair concentration?

Provenance
----------
Study: Spaeth AM, Dinges DF, Goel N (Unit for Experimental Psychiatry,
Division of Sleep and Chronobiology, Perelman School of Medicine, University
of Pennsylvania). Presented at SLEEP 2015, the 29th Annual Meeting of the
Associated Professional Sleep Societies, Seattle WA, June 6-10, 2015. Lock5 3e
cites it as (footnote 74 of exercise 1.110 "Late Night Eating"; verified
against the 3rd-edition textbook PDF, Oct 2026):

  University of Pennsylvania School of Medicine. "Eating less during late
  night hours may stave off some effects of sleep deprivation." ScienceDaily,
  June 4, 2015. https://www.sciencedaily.com/releases/2015/06/150604141905.htm

Design: randomized experiment. 44 healthy volunteers aged 21-50; unlimited
food/drink by day and only 4 h sleep/night (4:00-8:00 am) for 3 nights; on
night 4 randomized - 20 kept unlimited late-night food/drink access, 24 got
water only from 10 pm to 4 am; neurobehavioral tests (reaction time,
attention lapses, working memory, sleepiness, stress, mood) each night at 2 am.
Published headline findings (press release, qualitative):
  * Night 4: fasting group performed significantly better on reaction time and
    had fewer attention lapses than the late-night-eating group.
  * Eaters slowed significantly and had more lapses on night 4 vs nights 1-3;
    fasters showed no such decline.
  * Sleep-restricted adults consume ~500 additional late-night calories.

Data: Lock5 distributes no dataset for this study (3rd-edition data page
checked Oct 2026; nearest names are LightatNight - a mouse study -
SleepCaffeine, SleepStudy, DietDepression). Per-group means/SDs were never
published (conference abstract not retrievable), so
data/phase2/q16_latenight.csv is a documented reconstruction for method
illustration only: one row per participant, night-4 group labels randomized
(20 eat / 24 fast), RT and lapse values calibrated to the published direction
and literature-typical PVT magnitudes under 4 h time in bed. See the CSV
header for the full model and its realized statistics.

Analysis (Lock5 spirit)
-----------------------
  A. Night-4 between-group comparison (the randomized experiment):
     two-sample Welch t-test, 100,000-rep randomization (label-permutation)
     test, and 100,000-rep bootstrap percentile CI for the mean difference
     (eat - fast), for both endpoints (mean reaction time, attention lapses).
  B. Within-subject change (night 4 vs nights 1-3 average):
     paired t-tests per group and a difference-in-differences randomization
     test (group labels permuted on the change scores).

Caveat: participant-level values are synthetic; results illustrate the
inference pipeline for this study design, not the study's exact statistics.

Run from repo root: .venv/bin/python scripts/phase2/q16_latenight.py
Outputs: prints summary; writes scripts/phase2/out/q16_results.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = _os_cwd  # Kaggle override
CSV_PATH = REPO / "data" / "phase2" / "q16_latenight.csv"
OUT_PATH = REPO / "scripts" / "phase2" / "out" / "q16_results.json"

N_REPS = 100_000
SEED = 2026
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- load data
df = pd.read_csv(CSV_PATH, comment="#")
eat = df[df["group"] == "eat"]
fast = df[df["group"] == "fast"]
n_eat, n_fast = len(eat), len(fast)

ENDPOINTS = {
    "pvt_rt_n4_ms": ("mean reaction time night 4 (ms)", "pvt_rt_n13_ms"),
    "lapses_n4": ("attention lapses night 4 (count)", "lapses_n13"),
}


def two_sample(col):
    """Welch t + randomization + bootstrap CI for night-4 eat - fast."""
    x = df[col].to_numpy(float)
    a, b = x[df["group"] == "eat"], x[df["group"] == "fast"]
    obs = a.mean() - b.mean()
    welch = stats.ttest_ind(a, b, equal_var=False)
    v_a, v_b = a.var(ddof=1) / n_eat, b.var(ddof=1) / n_fast
    df_w = (v_a + v_b) ** 2 / (v_a**2 / (n_eat - 1) + v_b**2 / (n_fast - 1))

    pooled = np.concatenate([a, b])
    perm = np.empty(N_REPS)
    done = 0
    while done < N_REPS:
        m = min(5_000, N_REPS - done)
        idx = rng.random((m, pooled.size)).argsort(axis=1)
        s = pooled[idx]
        perm[done:done + m] = s[:, :n_eat].mean(axis=1) - s[:, n_eat:].mean(axis=1)
        done += m

    boot = np.empty(N_REPS)
    done = 0
    while done < N_REPS:
        m = min(10_000, N_REPS - done)
        ba = a[rng.integers(0, n_eat, (m, n_eat))].mean(axis=1)
        bb = b[rng.integers(0, n_fast, (m, n_fast))].mean(axis=1)
        boot[done:done + m] = ba - bb
        done += m
    ci = np.percentile(boot, [2.5, 97.5])

    return {
        "endpoint": ENDPOINTS[col][0],
        "data": {"eat": {"n": n_eat, "mean": a.mean(), "sd": a.std(ddof=1)},
                 "fast": {"n": n_fast, "mean": b.mean(), "sd": b.std(ddof=1)}},
        "diff_in_means_eat_minus_fast": obs,
        "welch_t": {"t": welch.statistic, "df": df_w, "p_two_sided": welch.pvalue,
                    "p_one_sided_eat_worse": float(stats.t.sf(welch.statistic, df_w))},
        "randomization": {"p_two_sided": float(np.mean(np.abs(perm) >= abs(obs))),
                          "p_one_sided_eat_worse": float(np.mean(perm >= obs))},
        "bootstrap": {"ci95_mean_diff": [float(ci[0]), float(ci[1])]},
    }


part_a = {name: two_sample(col) for col, (name, _) in ENDPOINTS.items()}

# --------------------------------------------------- Part B - within subject
def paired(sub):
    """Paired t: night 4 minus nights-1-3 average, per endpoint."""
    out = {}
    for col, (name, base) in ENDPOINTS.items():
        d = sub[col].to_numpy(float) - sub[base].to_numpy(float)
        t = stats.ttest_1samp(d, 0)
        out[name] = {"mean_change": d.mean(), "t": t.statistic,
                     "df": len(d) - 1, "p_two_sided": t.pvalue}
    return out


part_b = {"paired_eaters": paired(eat), "paired_fasters": paired(fast)}

# difference-in-differences on lapse change scores (group-label randomization);
# RT change is analyzed descriptively (randomization was applied on night 4)
d_lp_eat = (eat["lapses_n4"] - eat["lapses_n13"]).to_numpy(float)
d_lp_fast = (fast["lapses_n4"] - fast["lapses_n13"]).to_numpy(float)
did = d_lp_eat.mean() - d_lp_fast.mean()
pooled_ch = np.concatenate([d_lp_eat, d_lp_fast])
perm_did = np.empty(N_REPS)
done = 0
while done < N_REPS:
    m = min(5_000, N_REPS - done)
    idx = rng.random((m, pooled_ch.size)).argsort(axis=1)
    s = pooled_ch[idx]
    perm_did[done:done + m] = s[:, :n_eat].mean(axis=1) - s[:, n_eat:].mean(axis=1)
    done += m
part_b["diff_in_diff_lapses"] = {
    "did_eat_minus_fast": did,
    "randomization_p_two_sided": float(np.mean(np.abs(perm_did) >= abs(did))),
    "randomization_p_one_sided_eat_worse": float(np.mean(perm_did >= did)),
}

decision = {
    "question": "Does late night eating impair concentration?",
    "verdict": ("Yes - in this randomized experiment, the group kept awake with "
                "late-night food access had significantly slower reaction times "
                "and more attention lapses on night 4 than the group fasted from "
                "10 pm; the eaters also declined significantly from their nights "
                "1-3 level, while the fasting group did not decline."),
    "causality": ("Randomization of the night-4 condition supports a causal "
                  "conclusion: late-night eating (vs fasting) worsens some "
                  "effects of sleep restriction on vigilant attention."),
    "scope": ("Conclusions are about vigilance under acute sleep restriction "
              "(4 h/night); per-participant values in the CSV are a documented "
              "reconstruction, so numeric p-values illustrate the pipeline "
              "rather than replicate the unpublished study statistics."),
}

results = {
    "question": "Does late night eating impair concentration?",
    "provenance": {
        "study": "SLEEP 2015 conference presentation - Perelman School of Medicine, University of Pennsylvania",
        "citation": "Spaeth AM, Dinges DF, Goel N. Presented at SLEEP 2015 (29th Annual Meeting of the "
                    "Associated Professional Sleep Societies), Seattle WA, June 6-10, 2015. Lock5 3e cites: "
                    "University of Pennsylvania School of Medicine. 'Eating less during late night hours may "
                    "stave off some effects of sleep deprivation.' ScienceDaily, June 4, 2015.",
        "url": "https://www.sciencedaily.com/releases/2015/06/150604141905.htm",
        "lock5_location": "3rd-edition exercise 1.110 'Late Night Eating' (footnote 74)",
        "design": "Randomized experiment: 44 adults aged 21-50, 4 h sleep/night for 3 nights, night-4 "
                  "randomization to continued food access (n=20) vs water-only from 10 pm (n=24); "
                  "2 a.m. testing nightly.",
        "data_source": "No Lock5 dataset (3e data page checked Oct 2026). data/phase2/q16_latenight.csv is "
                       "a documented reconstruction (seed 2026) calibrated to the published direction of "
                       "effects and PVT magnitudes typical of 4 h time in bed; per-participant values are "
                       "synthetic.",
        "caution": "Published findings are qualitative (no group means/SDs released); the numeric results "
                   "here illustrate the analysis pipeline for this design.",
    },
    "methods": {"n_bootstrap": N_REPS, "n_randomization": N_REPS, "seed": SEED,
                "engine": "numpy/scipy/pandas"},
    "part_a_night4_between_groups": part_a,
    "part_b_within_subject_change": part_b,
    "decision": decision,
}

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ------------------------------------------------- human-readable summary
print("=" * 64)
print("Q16: Does late night eating impair concentration?")
print("Spaeth, Dinges & Goel, SLEEP 2015 (UPenn) - randomized experiment, n=44")
print("=" * 64)
print(f"\nGroups: eat n={n_eat}, fast n={n_fast} (night-4 randomization)")

for key, r in part_a.items():
    d = r["data"]
    print(f"\nPart A (night 4, eat - fast) - {key}")
    print(f"  eat : n={d['eat']['n']}  mean={d['eat']['mean']:.2f}  sd={d['eat']['sd']:.2f}")
    print(f"  fast: n={d['fast']['n']}  mean={d['fast']['mean']:.2f}  sd={d['fast']['sd']:.2f}")
    print(f"  diff = {r['diff_in_means_eat_minus_fast']:+.2f}")
    w = r["welch_t"]
    print(f"  Welch t = {w['t']:.2f}, df = {w['df']:.1f}, p(two) = {w['p_two_sided']:.4f}")
    print(f"  randomization p(two) = {r['randomization']['p_two_sided']:.5f}, "
          f"p(one, eat worse) = {r['randomization']['p_one_sided_eat_worse']:.5f}")
    ci = r["bootstrap"]["ci95_mean_diff"]
    print(f"  bootstrap 95% CI for diff: ({ci[0]:+.2f}, {ci[1]:+.2f})")

print("\nPart B (night 4 vs nights 1-3, paired)")
for label, block in (("eaters", part_b["paired_eaters"]), ("fasters", part_b["paired_fasters"])):
    for name, r in block.items():
        sig = "significant" if r["p_two_sided"] < 0.05 else "n.s."
        print(f"  {label:<7} {name:<36} change {r['mean_change']:+.2f}, "
              f"t({r['df']}) = {r['t']:.2f}, p = {r['p_two_sided']:.4f} ({sig})")
dd = part_b["diff_in_diff_lapses"]
print(f"  diff-in-diff (lapses, eat - fast) = {dd['did_eat_minus_fast']:+.2f}; "
      f"randomization p(two) = {dd['randomization_p_two_sided']:.5f}")

print("\nDecision: yes - late-night eating worsened vigilant attention under")
print("sleep restriction (randomized comparison; eaters declined, fasters did not).")
print(f"\nResults JSON written to {OUT_PATH.relative_to(REPO)}")
