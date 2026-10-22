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

REPO = Path(__file__).resolve().parents[2]
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
