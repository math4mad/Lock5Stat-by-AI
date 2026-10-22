# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q9_beautysleep.csv").write_text('# Q9 (Phase 2): Is there truth to the saying "beauty sleep"?\n#\n# STUDY\n#   Axelsson J, Sundelin T, Ingre M, Van Someren EJW, Olsson A, Lekander M.\n#   "Beauty sleep: experimental study on the perceived health and attractiveness\n#   of sleep deprived people." BMJ 2010;341:c6614. doi:10.1136/bmj.c6614\n#   (published 14 Dec 2010; PMID 21156746, PMCID PMC3001961).\n#   NOTE: some secondary sources cite this as 341:c6611; the correct eLocator\n#   is c6614 (verified against PubMed and bmj.com citation records, Oct 2026).\n#\n# DESIGN\n#   Within-participant experiment in a Stockholm sleep laboratory. 23 healthy\n#   adults (age 18-31) were photographed after a normal night\'s sleep (8 hours)\n#   and again after sleep deprivation (31 hours of wakefulness after a night of\n#   reduced sleep). The 46 photographs were presented in randomised,\n#   counterbalanced order to 65 untrained observers (age 18-61), who rated each\n#   face on 100-mm visual analogue scales (0-100) for perceived health,\n#   tiredness, and attractiveness.\n#\n# PUBLISHED RESULTS (mixed model; abstract of the paper)\n#   Health:         63 (SE 2) sleep deprived vs 68 (SE 2) normal sleep, P<0.001\n#   Tiredness:      53 (SE 3) sleep deprived vs 44 (SE 3) normal sleep, P<0.001\n#   Attractiveness: 38 (SE 2) sleep deprived vs 40 (SE 2) normal sleep, P<0.001\n#\n# RECONSTRUCTION (Lock5 distributes no dataset for this study; 3e data page\n#   checked Oct 2026 - only SleepCaffeine and SleepStudy exist, neither is this\n#   experiment. So each cell below is a reconstructed participant-level mean\n#   observer rating that exactly reproduces the published condition means, with\n#   documented assumptions for the unpublished dispersion):\n#   - Unit: one row per participant; each value is that participant\'s mean\n#     rating (over the ~65 observers, cf. Fig 1 of the paper) for the\n#     corresponding photograph, on the 0-100 mm VAS.\n#   - Condition means: exactly the published values (68/63 health, 44/53\n#     tiredness, 40/38 attractiveness).\n#   - Condition SDs: published SE interpreted as the SE of the condition mean\n#     across the 23 participants, so SD = SE*sqrt(23) = 9.59 (health,\n#     attractiveness) and 14.39 (tiredness); sample SDs match exactly.\n#   - Within-participant correlation between the two condition ratings:\n#     rho = 0.97, the value implied by the paper\'s own precision (P<0.001 for\n#     the 2-point attractiveness difference with n=23 requires an SD of paired\n#     differences of about 2.5). Same face, same observer pool, so base\n#     attractiveness dominates and near-identical cross-condition ratings are\n#     expected; realized sample r = 0.95/0.99/0.97.\n#   - Generation algorithm (reproducible, seed 2026, numpy default_rng):\n#       for outcome in (health, tiredness, attractiveness):   # in this order\n#           a = rng.standard_normal(23); b = rng.standard_normal(23)\n#           d_raw = 0.97*a + sqrt(1-0.97^2)*b\n#           normal   = m_normal    + SD*(a - mean(a))/sd(a, ddof=1)\n#           deprived = m_deprived + SD*(d_raw - mean(d_raw))/sd(d_raw, ddof=1)\n#     values rounded to one decimal (VAS readings were reported to the mm).\n#   - The true per-participant values are not published; use these data for\n#     method illustration only, not to re-estimate the study\'s effect sizes.\nparticipant,health_normal,health_deprived,tired_normal,tired_deprived,attract_normal,attract_deprived\n1,58.5,52.0,65.9,73.8,25.7,27.6\n2,72.4,68.8,32.8,38.2,30.3,26.2\n3,43.6,43.6,70.0,75.5,42.8,41.5\n4,88.0,80.0,76.6,89.1,59.8,57.5\n5,77.8,76.7,59.7,66.1,38.3,36.8\n6,65.2,55.1,50.9,62.4,44.0,43.3\n7,65.0,59.7,34.5,45.4,32.3,29.4\n8,73.3,63.5,52.8,60.8,32.4,29.0\n9,65.6,64.3,36.9,44.8,24.3,25.1\n10,66.1,63.1,41.6,54.1,41.5,40.2\n11,78.9,77.1,38.6,47.6,50.2,49.6\n12,76.1,67.3,44.9,57.9,38.6,36.5\n13,68.3,64.8,56.0,62.4,54.2,53.7\n14,68.0,60.4,35.7,45.5,43.5,40.0\n15,71.3,64.0,30.9,42.2,41.4,36.5\n16,60.9,56.7,30.8,41.7,46.3,39.0\n17,63.7,60.8,31.1,38.0,46.1,40.7\n18,76.6,71.5,26.0,34.7,51.9,50.0\n19,67.4,59.4,31.7,41.2,34.6,29.4\n20,50.6,41.7,56.1,62.1,21.4,19.3\n21,62.7,61.7,35.3,46.7,42.8,44.2\n22,78.0,74.3,44.7,55.2,36.3,35.7\n23,66.0,62.6,28.4,33.6,41.5,42.4\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
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

REPO = _os_cwd  # Kaggle override
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
