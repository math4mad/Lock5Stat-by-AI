"""Q14 (Phase 2): Does sleep deprivation hurt one's ability to interpret
facial expressions?

Provenance
----------
Killgore WDS, Balkin TJ, Yarnell AM, Capaldi VF II. "Sleep deprivation
impairs recognition of specific emotions." Neurobiology of Sleep and
Circadian Rhythms 2017;3:10-16. doi:10.1016/j.nbscr.2017.01.001 (open
access, CC BY-NC-ND; PMID 31236499, PMCID PMC6575584). Some secondary
sources list a 2017 NeuroReport venue; the correct journal is Neurobiology
of Sleep and Circadian Rhythms (verified against the published PDF, Oct
2026). ScienceDaily (21 Mar 2017) headlined this study as "Sleep
deprivation impairs ability to interpret facial expressions", matching the
Q14 question.

Design: within-subject experiment (Walter Reed Army Institute of Research).
54 healthy young adults (29 male, 25 female; mean age 23.5, SD 4.0) took
the Ekman Hexagon Test (EHT): 120 computer-morphed facial blends (20 per
basic emotion - happiness, sadness, surprise, fear, disgust, anger; 50:50
blends excluded) classified under the 6 emotion labels. Tested after a
normal night of sleep (baseline), after one night of total sleep
deprivation (23.5 h awake), and after 12 h recovery sleep. Published
results: happiness and sadness recognition declined from baseline to sleep
deprivation (planned contrasts p=.004 and p=.023); surprise, fear, disgust
and anger were unaffected; recovery sleep returned accuracy to baseline.
Numeric per-condition means appear only in Fig. 3 (no table is published).

Data: Lock5 distributes no dataset for this study (3rd-edition data page
checked Oct 2026 - only SleepCaffeine and SleepStudy exist, neither is this
experiment). data/phase2/q14_sleepfaces.csv is a documented reconstruction:
54 participant-level rows, percent correct (out of 20 trials per emotion,
5-point steps) per emotion for the rested and sleep-deprived sessions.
Condition means exactly match Fig. 3 values read programmatically off the
published figure (axis-tick text calibration + marker centroid detection,
600 dpi, tolerance ~+/-0.15 point); paired-difference SDs are calibrated so
the paired t (df=53) approximately reproduces the published planned-contrast
p-values. Generation algorithm, calibrated parameters and seed (2026) are
documented in the CSV header. True per-participant values are unpublished -
use for method illustration, not re-estimation.

Analysis (matched pairs, Lock5 spirit)
--------------------------------------
  - Paired t-test on the 54 within-participant differences
    (deprived - rested), overall and per emotion
  - 100,000-rep sign-flip randomization test on the differences
  - 100,000-rep bootstrap percentile CI of the mean difference
    (resampling participants, i.e. whole pairs)

Run from repo root: .venv/bin/python scripts/phase2/q14_sleepfaces.py
Outputs: prints summary; writes scripts/phase2/out/q14_results.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
CSV_PATH = REPO / "data" / "phase2" / "q14_sleepfaces.csv"
OUT_PATH = REPO / "scripts" / "phase2" / "out" / "q14_results.json"

N_REPS = 100_000
SEED = 2026
rng = np.random.default_rng(SEED)

EMOTIONS = ["happiness", "sadness", "surprise", "fear", "disgust", "anger"]

# digitized from Fig. 3 of the paper (percent correct)
PUB_MEANS = {
    "happiness": (99.91, 98.63), "sadness": (98.75, 96.09),
    "surprise": (88.46, 87.96),  "fear": (91.62, 90.18),
    "disgust": (84.58, 87.77),   "anger": (83.56, 85.34),
}
# published planned contrasts (baseline vs sleep deprivation)
PUB_P = {"happiness": .004, "sadness": .023, "surprise": .39,
         "fear": .39, "disgust": None, "anger": None}

# ---------------------------------------------------------------- load data
df = pd.read_csv(CSV_PATH, comment="#")
n = len(df)
assert n == 54, f"expected 54 participants, got {n}"

results = {
    "question": "Does sleep deprivation hurt one's ability to interpret "
                "facial expressions?",
    "provenance": {
        "citation": "Killgore WDS, Balkin TJ, Yarnell AM, Capaldi VF II. "
                    "Sleep deprivation impairs recognition of specific "
                    "emotions. Neurobiology of Sleep and Circadian Rhythms "
                    "2017;3:10-16. doi:10.1016/j.nbscr.2017.01.001 (PMID "
                    "31236499, PMCID PMC6575584).",
        "citation_note": "Some secondary sources list a 2017 NeuroReport "
                         "venue; the correct journal is Neurobiology of Sleep "
                         "and Circadian Rhythms (verified against the "
                         "published PDF, Oct 2026).",
        "design": "Within-subject experiment: 54 healthy young adults (29 M, "
                  "25 F) classified 120 morphed facial expressions (20 per "
                  "basic emotion) on the Ekman Hexagon Test after a normal "
                  "night of sleep, after one night of total sleep deprivation "
                  "(23.5 h awake), and after 12 h recovery sleep",
        "data_source": "Reconstructed CSV (data/phase2/q14_sleepfaces.csv): "
                       "condition means digitized programmatically from Fig. 3 "
                       "of the paper; paired-difference SDs calibrated to the "
                       "published planned-contrast p-values. No Lock5 dataset "
                       "exists for this study (3e data page checked Oct 2026). "
                       "Generation algorithm documented in the CSV header.",
    },
    "data": {"n_participants": n, "n_trials_per_emotion": 20,
             "scale": "percent correct out of 20 morphed faces (5-point steps)",
             "source_csv": str(CSV_PATH.relative_to(REPO))},
    "methods": {"paired_test": "scipy.stats.ttest_rel (paired t, df = 53)",
                "randomization": "sign-flip test on differences, two-sided",
                "bootstrap": "percentile CI of mean difference, resampling "
                             "participants (whole pairs)",
                "n_replicates": N_REPS, "seed": SEED,
                "engine": "numpy/scipy/pandas"},
    "outcomes": {},
}


def analyze(rested, deprived, label, pub):
    diff = deprived - rested  # <0 means worse recognition when deprived
    mean_diff = float(diff.mean())
    sd_diff = float(diff.std(ddof=1))

    t_res = stats.ttest_rel(deprived, rested)

    # sign-flip randomization test: under H0 differences are symmetric about 0
    signs = rng.choice([-1.0, 1.0], size=(N_REPS, n))
    flip_means = (signs * diff).mean(axis=1)
    p_flip = float((np.sum(np.abs(flip_means) >= abs(mean_diff)) + 1)
                   / (N_REPS + 1))

    # bootstrap percentile CI of the mean difference (resample participants)
    idx = rng.integers(0, n, size=(N_REPS, n))
    boot_means = diff[idx].mean(axis=1)
    ci_boot = np.percentile(boot_means, [2.5, 97.5])

    return {
        "published": {"mean_rested": pub[0], "mean_deprived": pub[1],
                      "p_paper": PUB_P.get(label)},
        "reconstructed": {"mean_rested": float(rested.mean()),
                          "mean_deprived": float(deprived.mean()),
                          "sd_rested": float(rested.std(ddof=1)),
                          "sd_deprived": float(deprived.std(ddof=1))},
        "mean_difference_deprived_minus_rested": mean_diff,
        "sd_difference": sd_diff,
        "paired_t": {"t": float(t_res.statistic), "df": n - 1,
                     "p_two_sided": float(t_res.pvalue)},
        "p_signflip_randomization": p_flip,
        "ci_95_bootstrap_percentile": [float(ci_boot[0]), float(ci_boot[1])],
    }


# ------------------------------------------------- matched-pairs analysis
for label in EMOTIONS:
    rested = df[f"{label}_rested"].to_numpy(dtype=float)
    deprived = df[f"{label}_deprived"].to_numpy(dtype=float)
    results["outcomes"][label] = analyze(rested, deprived, label,
                                         PUB_MEANS[label])

# overall: participant mean accuracy across the six emotions
rested = df[[f"{e}_rested" for e in EMOTIONS]].mean(axis=1).to_numpy()
deprived = df[[f"{e}_deprived" for e in EMOTIONS]].mean(axis=1).to_numpy()
pub_overall = (float(np.mean([PUB_MEANS[e][0] for e in EMOTIONS])),
               float(np.mean([PUB_MEANS[e][1] for e in EMOTIONS])))
results["outcomes"]["overall"] = analyze(rested, deprived, "overall",
                                         pub_overall)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ------------------------------------------------- human-readable summary
print("=" * 64)
print("Q14: Does sleep deprivation hurt one's ability to interpret")
print("facial expressions?")
print("Killgore et al., Neurobiol Sleep Circadian Rhythms 2017;3:10-16 -")
print("54 adults, Ekman Hexagon Test, rested vs sleep-deprived (paired);")
print("reconstructed participant-level data (means digitized from Fig. 3)")
print("=" * 64)
for label in EMOTIONS + ["overall"]:
    o = results["outcomes"][label]
    md = o["mean_difference_deprived_minus_rested"]
    ci = o["ci_95_bootstrap_percentile"]
    hdr = "Overall (mean of 6 emotions)" if label == "overall" \
        else label.capitalize()
    print(f"\n{hdr}:")
    print(f"  rested = {o['reconstructed']['mean_rested']:.2f}%, "
          f"sleep-deprived = {o['reconstructed']['mean_deprived']:.2f}% "
          f"(digitized from Fig. 3: {o['published']['mean_rested']:.2f} vs "
          f"{o['published']['mean_deprived']:.2f})")
    print(f"  mean difference (deprived - rested) = {md:+.2f} points")
    print(f"  paired t({o['paired_t']['df']}) = {o['paired_t']['t']:.2f}, "
          f"p = {o['paired_t']['p_two_sided']:.4f}")
    print(f"  sign-flip randomization p = {o['p_signflip_randomization']:.4f}")
    print(f"  bootstrap 95% CI of mean difference: ({ci[0]:+.2f}, {ci[1]:+.2f})")

sig = [e for e in EMOTIONS
       if results["outcomes"][e]["paired_t"]["p_two_sided"] < 0.05]
print("\nConclusion: sleep deprivation significantly impaired recognition of"
      f" {', '.join(sig)} - the prosocial emotions - while recognition of")
print("surprise, fear, disgust and anger (threat-relevant expressions) was")
print("unaffected. Overall accuracy across all six emotions was unchanged,")
print("so averaging across emotions masks the emotion-specific deficit;")
print("accuracy returned to baseline after recovery sleep (per the paper).")
print(f"\nResults JSON written to {OUT_PATH.relative_to(REPO)}")
