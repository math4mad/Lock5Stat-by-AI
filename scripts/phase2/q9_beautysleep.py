"""Q9 (Phase 2): Is there truth to the saying "beauty sleep"?

Provenance
----------
Axelsson J, Sundelin T, Ingre M, Van Someren EJW, Olsson A, Lekander M.
"Beauty sleep: experimental study on the perceived health and attractiveness
of sleep deprived people." BMJ 2010;341:c6614, doi:10.1136/bmj.c6614 (PMID
21156746, PMCID PMC3001961; published 14 Dec 2010). Note: some secondary
sources cite this as 341:c6611; the correct eLocator is c6614 (verified
against PubMed and bmj.com citation records, Oct 2026).

Design: within-participant experiment in a Stockholm sleep laboratory. 23
healthy adults (age 18-31) were photographed after a normal night's sleep
(eight hours) and again after sleep deprivation (31 hours of wakefulness
after a night of reduced sleep). The 46 photographs were shown in randomised,
counterbalanced order to 65 untrained observers (age 18-61), who rated each
face on 100-mm visual analogue scales (0-100) for perceived health,
tiredness, and attractiveness.

Published headline results (mixed model, article abstract): sleep-deprived
faces were rated less healthy (mean 63, SE 2 vs 68, SE 2, P<0.001), more
tired (53, SE 3 vs 44, SE 3, P<0.001), and less attractive (38, SE 2 vs 40,
SE 2, P<0.001) than after a normal night's sleep.

Data: Lock5 distributes no dataset for this study (3rd-edition data page
checked Oct 2026 - only SleepCaffeine and SleepStudy exist, neither is this
experiment). data/phase2/q9_beautysleep.csv is a documented reconstruction:
23 participant-level pairs matching the published condition means exactly,
with SD = published SE * sqrt(23) and within-participant correlation
rho = 0.97 (the value implied by the paper's own precision); the seeded
generation algorithm is documented in the CSV header. True per-participant
values are unpublished - use for method illustration, not re-estimation.

Analysis (matched pairs, Lock5 spirit)
--------------------------------------
  - Paired t-test on the 23 within-participant differences
  - 100,000-rep sign-flip randomization test on the differences
  - 100,000-rep bootstrap percentile CI of the mean difference
    (resampling participants, i.e. whole pairs)
  - repeated for each rated outcome: health, tiredness, attractiveness

Run from repo root: .venv/bin/python scripts/phase2/q9_beautysleep.py
Outputs: prints summary; writes scripts/phase2/out/q9_results.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
CSV_PATH = REPO / "data" / "phase2" / "q9_beautysleep.csv"
OUT_PATH = REPO / "scripts" / "phase2" / "out" / "q9_results.json"

N_REPS = 100_000
SEED = 2026
rng = np.random.default_rng(SEED)

# outcome label, (normal-sleep col, sleep-deprived col, published mean normal,
# published mean deprived, published SE per condition)
OUTCOMES = [
    ("health", "health_normal", "health_deprived", 68.0, 63.0, 2.0),
    ("tiredness", "tired_normal", "tired_deprived", 44.0, 53.0, 3.0),
    ("attractiveness", "attract_normal", "attract_deprived", 40.0, 38.0, 2.0),
]

# ---------------------------------------------------------------- load data
df = pd.read_csv(CSV_PATH, comment="#")
n = len(df)
assert n == 23, f"expected 23 participants, got {n}"

results = {
    "question": 'Is there truth to the saying "beauty sleep"?',
    "provenance": {
        "citation": "Axelsson J, Sundelin T, Ingre M, Van Someren EJW, Olsson A, "
                    "Lekander M. Beauty sleep: experimental study on the perceived "
                    "health and attractiveness of sleep deprived people. "
                    "BMJ 2010;341:c6614. doi:10.1136/bmj.c6614 (PMID 21156746, "
                    "PMCID PMC3001961).",
        "citation_note": "Some secondary sources cite 341:c6611; the correct "
                         "eLocator is c6614 (verified via PubMed/bmj.com, Oct 2026).",
        "design": "Within-participant experiment: 23 adults photographed after a "
                  "normal night's sleep (8h) and after sleep deprivation (31h "
                  "awake); 46 photos rated in randomised order by 65 untrained "
                  "observers on 100-mm VAS for health, tiredness, attractiveness",
        "data_source": "Reconstructed CSV (data/phase2/q9_beautysleep.csv) from the "
                       "published condition means/SEs; no Lock5 dataset exists for "
                       "this study (3e data page checked Oct 2026). Generation "
                       "algorithm and assumptions documented in the CSV header.",
    },
    "data": {"n_participants": n, "n_observers_published": 65,
             "scale": "0-100 mm visual analogue scale",
             "source_csv": str(CSV_PATH.relative_to(REPO))},
    "methods": {"paired_test": "scipy.stats.ttest_rel (paired t, df = 22)",
                "randomization": "sign-flip test on differences, two-sided",
                "bootstrap": "percentile CI of mean difference, resampling pairs",
                "n_replicates": N_REPS, "seed": SEED, "engine": "numpy/scipy/pandas"},
    "outcomes": {},
}

# ------------------------------------------------- matched-pairs analysis
for label, col_n, col_d, pub_m_n, pub_m_d, pub_se in OUTCOMES:
    normal = df[col_n].to_numpy(dtype=float)
    deprived = df[col_d].to_numpy(dtype=float)
    diff = deprived - normal  # >0 means worse (higher) rating when deprived

    mean_diff = float(diff.mean())
    sd_diff = float(diff.std(ddof=1))
    se_diff = sd_diff / np.sqrt(n)

    # paired t-test
    t_res = stats.ttest_rel(deprived, normal)

    # sign-flip randomization test: under H0 differences are symmetric about 0
    signs = rng.choice([-1.0, 1.0], size=(N_REPS, n))
    flip_means = (signs * diff).mean(axis=1)
    p_flip = float((np.sum(np.abs(flip_means) >= abs(mean_diff)) + 1) / (N_REPS + 1))

    # bootstrap percentile CI of the mean difference (resample whole pairs)
    idx = rng.integers(0, n, size=(N_REPS, n))
    boot_means = diff[idx].mean(axis=1)
    ci_boot = np.percentile(boot_means, [2.5, 97.5])

    results["outcomes"][label] = {
        "published": {"mean_normal": pub_m_n, "mean_deprived": pub_m_d,
                      "se_per_condition": pub_se, "p_paper": "<0.001"},
        "reconstructed": {
            "mean_normal": float(normal.mean()), "mean_deprived": float(deprived.mean()),
            "sd_normal": float(normal.std(ddof=1)), "sd_deprived": float(deprived.std(ddof=1)),
            "within_participant_corr": float(np.corrcoef(normal, deprived)[0, 1]),
        },
        "mean_difference_deprived_minus_normal": mean_diff,
        "sd_difference": sd_diff, "se_difference": float(se_diff),
        "paired_t": {"t": float(t_res.statistic), "df": n - 1,
                     "p_two_sided": float(t_res.pvalue)},
        "p_signflip_randomization": p_flip,
        "ci_95_bootstrap_percentile": [float(ci_boot[0]), float(ci_boot[1])],
    }

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ------------------------------------------------- human-readable summary
print("=" * 64)
print('Q9: Is there truth to the saying "beauty sleep"?')
print("Axelsson et al., BMJ 2010;341:c6614 - 23 faces x 2 conditions,")
print("rated by 65 observers (0-100 mm VAS); reconstructed paired data")
print("=" * 64)
for label, _, _, _, _, _ in OUTCOMES:
    o = results["outcomes"][label]
    md = o["mean_difference_deprived_minus_normal"]
    ci = o["ci_95_bootstrap_percentile"]
    direction = "less" if md < 0 else "more"
    print(f"\n{label.capitalize()}:")
    print(f"  normal sleep mean = {o['reconstructed']['mean_normal']:.1f}, "
          f"sleep-deprived mean = {o['reconstructed']['mean_deprived']:.1f} "
          f"(published: {o['published']['mean_normal']:.0f} vs "
          f"{o['published']['mean_deprived']:.0f})")
    print(f"  mean difference (deprived - normal) = {md:+.2f} points "
          f"(rated {direction} when sleep deprived)")
    print(f"  paired t({o['paired_t']['df']}) = {o['paired_t']['t']:.2f}, "
          f"p = {o['paired_t']['p_two_sided']:.2e}")
    print(f"  sign-flip randomization p = {o['p_signflip_randomization']:.5f}")
    print(f"  bootstrap 95% CI of mean difference: ({ci[0]:+.2f}, {ci[1]:+.2f})")
sig = all(o["paired_t"]["p_two_sided"] < 0.001 for o in results["outcomes"].values())
print("\nConclusion: sleep-deprived faces are rated significantly "
      f"{'(all p < 0.001) ' if sig else ''}less healthy, less attractive, and")
print("more tired than the same faces after a normal night's sleep -")
print('the saying "beauty sleep" holds up in this experiment.')
print(f"\nResults JSON written to {OUT_PATH.relative_to(REPO)}")
