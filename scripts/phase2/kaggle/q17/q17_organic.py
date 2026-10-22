# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q17_organic.csv").write_text('Person,Pesticide,Day,NonOrganic,Organic,Diff\nFather,24D,Day1,0,0.2,-0.2\nFather,24D,Day3,1.2,0.3,0.9\nFather,24D,Day4,0.7,0.3,0.4\nFather,24D,Day6,0.3,0.3,0\nMother,24D,Day1,0.5,0.5,0\nMother,24D,Day3,0.9,0.2,0.7\nMother,24D,Day4,1,0.3,0.7\nMother,24D,Day6,0.6,0.6,0\nGirlA,24D,Day1,20.7,0.3,20.4\nGirlA,24D,Day3,29.5,4.1,25.4\nGirlA,24D,Day4,29.2,0.5,28.7\nGirlA,24D,Day6,2,0.9,1.1\nGirlB,24D,Day1,2.8,1.1,1.7\nGirlB,24D,Day3,6,1.7,4.3\nGirlB,24D,Day4,1.9,1,0.9\nGirlB,24D,Day6,2,1.7,0.3\nBoy,24D,Day1,4.4,1,3.4\nBoy,24D,Day3,7.2,0.7,6.5\nBoy,24D,Day4,16,2.4,13.6\nBoy,24D,Day6,2.2,0.7,1.5\nFather,3-PBA,Day1,5.7,0.8,4.9\nFather,3-PBA,Day3,5.5,1.3,4.2\nFather,3-PBA,Day4,16,1.5,14.5\nFather,3-PBA,Day6,15,1.2,13.8\nMother,3-PBA,Day1,6.5,2.4,4.1\nMother,3-PBA,Day3,39,0.8,38.2\nMother,3-PBA,Day4,22,1.3,20.7\nMother,3-PBA,Day6,56,2.9,53.1\nGirlA,3-PBA,Day1,23,1.7,21.3\nGirlA,3-PBA,Day3,36,1.6,34.4\nGirlA,3-PBA,Day4,28,2.3,25.7\nGirlA,3-PBA,Day6,12,1,11\nGirlB,3-PBA,Day1,20,1.3,18.7\nGirlB,3-PBA,Day3,32,1.5,30.5\nGirlB,3-PBA,Day4,25,4.9,20.1\nGirlB,3-PBA,Day6,24,1.1,22.9\nBoy,3-PBA,Day1,6.4,4.6,1.8\nBoy,3-PBA,Day3,55,3.2,51.8\nBoy,3-PBA,Day4,63,12,51\nBoy,3-PBA,Day6,51,3.3,47.7\nFather,35DC,Day1,4.1,0.3,3.8\nFather,35DC,Day3,22,0.5,21.5\nFather,35DC,Day4,1.3,0.6,0.7\nFather,35DC,Day6,1.4,0.5,0.9\nMother,35DC,Day1,40,0.9,39.1\nMother,35DC,Day3,21,0.3,20.7\nMother,35DC,Day4,49,0.5,48.5\nMother,35DC,Day6,69,1.1,67.9\nGirlA,35DC,Day1,34,0.6,33.4\nGirlA,35DC,Day3,60,0.6,59.4\nGirlA,35DC,Day4,8.8,0.9,7.9\nGirlA,35DC,Day6,1.5,0.4,1.1\nGirlB,35DC,Day1,0.5,0.5,0\nGirlB,35DC,Day3,1.3,0.6,0.7\nGirlB,35DC,Day4,1.4,1.9,-0.5\nGirlB,35DC,Day6,0.7,0.4,0.3\nBoy,35DC,Day1,20,1.8,18.2\nBoy,35DC,Day3,18,1.2,16.8\nBoy,35DC,Day4,27,4.5,22.5\nBoy,35DC,Day6,1.4,1.3,0.1\nFather,CCC,Day1,0.6,0.8,-0.2\nFather,CCC,Day3,2.9,1.3,1.6\nFather,CCC,Day4,25,1.6,23.4\nFather,CCC,Day6,10,1.3,8.7\nMother,CCC,Day1,88,2.5,85.5\nMother,CCC,Day3,4.3,0.8,3.5\nMother,CCC,Day4,404,1.3,402.7\nMother,CCC,Day6,323,3,320\nGirlA,CCC,Day1,241,9.3,231.7\nGirlA,CCC,Day3,57,15,42\nGirlA,CCC,Day4,468,2.5,465.5\nGirlA,CCC,Day6,14,1.1,12.9\nGirlB,CCC,Day1,6.7,1.3,5.4\nGirlB,CCC,Day3,11,1.6,9.4\nGirlB,CCC,Day4,16,5.1,10.9\nGirlB,CCC,Day6,13,1.2,11.8\nBoy,CCC,Day1,627,4.9,622.1\nBoy,CCC,Day3,375,3.4,371.6\nBoy,CCC,Day4,248,12,236\nBoy,CCC,Day6,654,3.5,650.5\nFather,ETU,Day1,0.3,0.4,-0.1\nFather,ETU,Day3,0.5,0.6,-0.1\nFather,ETU,Day4,1.6,0.7,0.9\nFather,ETU,Day6,12.2,0.6,11.6\nMother,ETU,Day1,1,1.2,-0.2\nMother,ETU,Day3,1.9,0.4,1.5\nMother,ETU,Day4,2.3,0.6,1.7\nMother,ETU,Day6,16.5,1.4,15.1\nGirlA,ETU,Day1,1.9,0.8,1.1\nGirlA,ETU,Day3,1.9,0.8,1.1\nGirlA,ETU,Day4,2.8,1.1,1.7\nGirlA,ETU,Day6,0.6,0.5,0.1\nGirlB,ETU,Day1,0.6,0.6,0\nGirlB,ETU,Day3,1.6,0.7,0.9\nGirlB,ETU,Day4,0.8,2.3,-1.5\nGirlB,ETU,Day6,0.9,0.5,0.4\nBoy,ETU,Day1,3,2.2,0.8\nBoy,ETU,Day3,2.5,1.5,1\nBoy,ETU,Day4,3.4,5.5,-2.1\nBoy,ETU,Day6,1.8,1.6,0.2\nFather,Mepiquat,Day1,2,5.2,-3.2\nFather,Mepiquat,Day3,7.4,3.5,3.9\nFather,Mepiquat,Day4,15,5.5,9.5\nFather,Mepiquat,Day6,4.8,2.7,2.1\nMother,Mepiquat,Day1,23,15,8\nMother,Mepiquat,Day3,36,2.4,33.6\nMother,Mepiquat,Day4,211,13,198\nMother,Mepiquat,Day6,48,25,23\nGirlA,Mepiquat,Day1,13,3.6,9.4\nGirlA,Mepiquat,Day3,8.5,1.3,7.2\nGirlA,Mepiquat,Day4,60,1.9,58.1\nGirlA,Mepiquat,Day6,3.4,0.8,2.6\nGirlB,Mepiquat,Day1,2.7,1,1.7\nGirlB,Mepiquat,Day3,3.1,1.2,1.9\nGirlB,Mepiquat,Day4,2.9,4,-1.1\nGirlB,Mepiquat,Day6,2.1,0.9,1.2\nBoy,Mepiquat,Day1,36,3.8,32.2\nBoy,Mepiquat,Day3,95,8.5,86.5\nBoy,Mepiquat,Day4,33,9.5,23.5\nBoy,Mepiquat,Day6,77,2.7,74.3\nFather,Propamocarb,Day1,0,0,0\nFather,Propamocarb,Day3,0,0,0\nFather,Propamocarb,Day4,0.3,0,0.3\nFather,Propamocarb,Day6,7.6,0,7.6\nMother,Propamocarb,Day1,0.2,0.2,0\nMother,Propamocarb,Day3,0.4,0,0.4\nMother,Propamocarb,Day4,0.5,0,0.5\nMother,Propamocarb,Day6,6.8,0.3,6.5\nGirlA,Propamocarb,Day1,2.1,0.2,1.9\nGirlA,Propamocarb,Day3,0.4,0.2,0.2\nGirlA,Propamocarb,Day4,0.6,0.2,0.4\nGirlA,Propamocarb,Day6,2.5,0,2.5\nGirlB,Propamocarb,Day1,0.1,0,0.1\nGirlB,Propamocarb,Day3,0.3,0.5,-0.2\nGirlB,Propamocarb,Day4,0.2,0.5,-0.3\nGirlB,Propamocarb,Day6,5.2,0.6,4.6\nBoy,Propamocarb,Day1,0.6,0.4,0.2\nBoy,Propamocarb,Day3,5.6,0.3,5.3\nBoy,Propamocarb,Day4,0.7,1.1,-0.4\nBoy,Propamocarb,Day6,8,0.3,7.7\nFather,TCP,Day1,9.7,14,-4.3\nFather,TCP,Day3,5.9,20,-14.1\nFather,TCP,Day4,15,34,-19\nFather,TCP,Day6,13,12,1\nMother,TCP,Day1,32,15,17\nMother,TCP,Day3,40,6.4,33.6\nMother,TCP,Day4,18,1.4,16.6\nMother,TCP,Day6,66,3.3,62.7\nGirlA,TCP,Day1,44,1.9,42.1\nGirlA,TCP,Day3,63,1.9,61.1\nGirlA,TCP,Day4,91,2.7,88.3\nGirlA,TCP,Day6,16,1.2,14.8\nGirlB,TCP,Day1,12,1.4,10.6\nGirlB,TCP,Day3,17,1.7,15.3\nGirlB,TCP,Day4,18,5.6,12.4\nGirlB,TCP,Day6,30,1.3,28.7\nBoy,TCP,Day1,31,5.3,25.7\nBoy,TCP,Day3,89,3.7,85.3\nBoy,TCP,Day4,116,13,103\nBoy,TCP,Day6,50,3.8,46.2\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
"""Q17 (Phase 2): Does eating organic food improve your health?

Provenance
----------
Dataset: "OrganicEffect" from Lock5 Statistics: Unlocking the Power of Data
(3rd ed., also 4th ed.) - 160 observations, 6 variables:
Person (Father, Mother, GirlA, GirlB, Boy), Pesticide (8 compounds),
Day (Day1/Day3/Day4/Day6), NonOrganic, Organic, Diff (= NonOrganic - Organic).
Lock5 3e/4e data pages checked Oct 2026; no dataset named "OrganicFood"
exists. Downloaded verbatim from
https://www.lock5stat.com/datasets3e/OrganicEffect.csv
to data/phase2/q17_organic.csv (NOT reconstructed - this is the real file).

Primary source: Magner J, Wallberg P, Sandberg J, Cousins AP (2015).
"Human exposure to pesticides from food: A pilot study" (Report U 5080),
IVL Swedish Environmental Research Institute, commissioned by Coop Sverige
AB, January 2015.
https://www.coop.se/PageFiles/429812/Coop%20Ekoeffekten_Report%20ENG.pdf

Design: within-family before/after (matched-pairs) pilot study. A Swedish
family of five (2 adults, 3 children) that normally ate a conventional diet
ate conventional food first, then ate only organic food for two weeks.
Concentrations of 8 pesticides (2,4-D, 3-PBA, 3,5-DCCA, CCC, ETU, mepiquat,
propamocarb, TCP) were measured in morning urine (micrograms/g creatinine)
on 4 days under each diet, giving 5 x 8 x 4 = 160 paired observations.

Question framing: the endpoint the study actually measures is urinary
pesticide-metabolite concentration - a health-relevant EXPOSURE biomarker,
not a clinical health outcome. Reduced exposure is the mechanism by which
"eating organic" could improve health, so this is the best available data
shape. Alternatives without Lock5 datasets: Smith-Spangler et al. 2012
(Ann Intern Med 157:348-366) systematic review (no health-outcome
differences reported) and the Norwegian MoBa pregnancy cohort (Torjusen et
al. 2012, BMC Public Health 12:612); neither is distributed by Lock5.

Published headline statistic (IVL report, not re-derived here):
  Pesticide-residue concentrations in urine decreased on average by a
  factor of 6.7 when the family ate organic food; children in particular
  had lower concentrations, and measured levels were estimated to be below
  the acceptable daily intake (ADI) by a good margin.

Analysis (Lock5 spirit, matched pairs -> one-mean inference on the diffs)
-------------------------------------------------------------------------
  Primary endpoint: d = NonOrganic - Organic per row (positive = organic
  diet lowers the pesticide level).
  - paired t-test (one-mean t on the differences), two- and one-sided
  - Wilcoxon signed-rank test (sensitivity; data are strongly right-skewed)
  - 100,000-rep randomization test (random sign-flip of the differences)
  - 100,000-rep bootstrap percentile CIs for the mean difference, the
    percent reduction, and Cohen's d (effect size)
  - descriptive breakdowns by person and by pesticide

Caveats: single family (n = 5 subjects, 160 paired measurements);
diet order was not randomized (conventional first, then organic);
the 4 days within a person x pesticide are repeated measures, so rows are
not fully independent (Lock5 exercises treat them as paired observations);
exposure reduction does not by itself establish a health benefit.

Run from repo root: .venv/bin/python scripts/phase2/q17_organic.py
Outputs: prints summary; writes scripts/phase2/out/q17_results.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = _os_cwd  # Kaggle override
CSV_PATH = REPO / "data" / "phase2" / "q17_organic.csv"
OUT_PATH = REPO / "scripts" / "phase2" / "out" / "q17_results.json"

N_REPS = 100_000
SEED = 2026
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- load data
df = pd.read_csv(CSV_PATH)
assert len(df) == 160, f"expected 160 paired observations, got {len(df)}"

non = df["NonOrganic"].to_numpy(float)
org = df["Organic"].to_numpy(float)
d = non - org
# integrity check against the Diff column shipped with the Lock5 file
assert np.allclose(d, df["Diff"].to_numpy(float), atol=0.005), \
    "Diff column disagrees with NonOrganic - Organic"

n = len(d)
mean_non, mean_org = non.mean(), org.mean()
mean_d, sd_d, med_d = d.mean(), d.std(ddof=1), np.median(d)

results = {
    "question": "Does eating organic food improve your health?",
    "provenance": {
        "dataset": "Lock5Data: OrganicEffect (160 obs, 6 vars) - real Lock5 dataset",
        "data_source": "Downloaded verbatim from "
                       "https://www.lock5stat.com/datasets3e/OrganicEffect.csv "
                       "to data/phase2/q17_organic.csv (Lock5 3e/4e data pages "
                       "checked Oct 2026; no dataset named 'OrganicFood' exists).",
        "citation": "Magner J, Wallberg P, Sandberg J, Cousins AP (2015). "
                    "Human exposure to pesticides from food: A pilot study "
                    "(Report U 5080). IVL Swedish Environmental Research "
                    "Institute, for Coop Sverige AB, January 2015.",
        "report_url": "https://www.coop.se/PageFiles/429812/"
                      "Coop%20Ekoeffekten_Report%20ENG.pdf",
        "design": "Within-family before/after pilot: Swedish family of five "
                  "(2 adults, 3 children) ate a conventional diet, then only "
                  "organic food for two weeks; 8 pesticides measured in "
                  "morning urine (micrograms/g creatinine) on 4 days per "
                  "diet -> 5 x 8 x 4 = 160 paired observations",
        "endpoint_note": "Endpoint is urinary pesticide concentration - a "
                         "health-relevant exposure biomarker, not a clinical "
                         "health outcome. Smith-Spangler et al. 2012 (Ann "
                         "Intern Med 157:348-366) and the Norwegian MoBa "
                         "cohort (Torjusen et al. 2012, BMC Public Health "
                         "12:612) have no Lock5 dataset.",
        "caution": "Single family (n=5); diet order not randomized; repeated "
                   "days within person x pesticide are not fully independent; "
                   "reduced exposure does not by itself establish a health "
                   "benefit (measured levels were below the ADI).",
    },
    "published_headlines": {
        "ivl_report": {
            "statement": "Urinary pesticide-residue concentrations decreased "
                         "on average by a factor of 6.7 on the organic diet",
            "extra": "Children in particular had lower concentrations; "
                     "levels of most, but not all, pesticides fell in adults; "
                     "measured levels estimated below the ADI by a good margin.",
        },
    },
    "methods": {"n_bootstrap": N_REPS, "n_randomization": N_REPS, "seed": SEED,
                "engine": "numpy/scipy/pandas"},
}

# =================================================================
# Matched-pairs analysis: one-mean inference on d = NonOrganic - Organic
# =================================================================
t_stat, p_t_two = stats.ttest_1samp(d, 0.0)
p_t_greater = stats.t.sf(t_stat, n - 1)
se_d = sd_d / np.sqrt(n)
ci_t = (mean_d - stats.t.ppf(0.975, n - 1) * se_d,
        mean_d + stats.t.ppf(0.975, n - 1) * se_d)

# Wilcoxon signed-rank (sensitivity for skew; zero diffs are dropped)
w_res = stats.wilcoxon(d)

# randomization test: randomly flip the sign of each difference
# (equivalent to d coming from a symmetric distribution centered at 0)
rand_mean = np.empty(N_REPS)
done = 0
while done < N_REPS:
    m = min(10_000, N_REPS - done)
    flips = rng.integers(0, 2, (m, n)) * 2 - 1
    rand_mean[done:done + m] = (d * flips).mean(axis=1)
    done += m
p_rand_greater = float(np.mean(rand_mean >= mean_d))
p_rand_two = float(np.mean(np.abs(rand_mean) >= abs(mean_d)))

# effect sizes
cohen_d = mean_d / sd_d
percent_reduction = (1 - mean_org / mean_non) * 100
ratio_of_means = mean_non / mean_org

# bootstrap percentile CIs (resample the 160 pairs with replacement)
boot_mean = np.empty(N_REPS)
boot_red = np.empty(N_REPS)
boot_cohen = np.empty(N_REPS)
done = 0
while done < N_REPS:
    m = min(10_000, N_REPS - done)
    idx = rng.integers(0, n, (m, n))
    b_d = d[idx]
    b_non, b_org = non[idx], org[idx]
    boot_mean[done:done + m] = b_d.mean(axis=1)
    boot_red[done:done + m] = (1 - b_org.mean(axis=1) / b_non.mean(axis=1)) * 100
    boot_cohen[done:done + m] = b_d.mean(axis=1) / b_d.std(axis=1, ddof=1)
    done += m
mean_ci = tuple(np.percentile(boot_mean, [2.5, 97.5]))
red_ci = tuple(np.percentile(boot_red, [2.5, 97.5]))
cohen_ci = tuple(np.percentile(boot_cohen, [2.5, 97.5]))

results["part_paired"] = {
    "endpoint": "urinary pesticide concentration (micrograms/g creatinine); "
                "d = NonOrganic - Organic per person x pesticide x day",
    "data": {
        "n_pairs": n,
        "n_subjects": int(df["Person"].nunique()),
        "n_pesticides": int(df["Pesticide"].nunique()),
        "mean_nonorganic": float(mean_non),
        "mean_organic": float(mean_org),
        "mean_diff": float(mean_d),
        "sd_diff": float(sd_d),
        "median_diff": float(med_d),
    },
    "effect_size": {
        "mean_diff_units_ug_per_g_creatinine": float(mean_d),
        "percent_reduction": float(percent_reduction),
        "ratio_of_means_non_over_org": float(ratio_of_means),
        "cohens_d": float(cohen_d),
    },
    "paired_t_test": {
        "t": float(t_stat), "df": n - 1,
        "p_two_sided": float(p_t_two),
        "p_one_sided_organic_lower": float(p_t_greater),
        "ci95_theory_mean_diff": [float(ci_t[0]), float(ci_t[1])],
    },
    "wilcoxon_signed_rank": {"statistic": float(w_res.statistic),
                             "p_two_sided": float(w_res.pvalue)},
    "randomization": {"p_two_sided": p_rand_two,
                      "p_one_sided_organic_lower": p_rand_greater},
    "bootstrap": {
        "ci95_mean_diff": [float(mean_ci[0]), float(mean_ci[1])],
        "ci95_percent_reduction": [float(red_ci[0]), float(red_ci[1])],
        "ci95_cohens_d": [float(cohen_ci[0]), float(cohen_ci[1])],
    },
    "by_person": [
        {"person": p,
         "mean_nonorganic": float(g["NonOrganic"].mean()),
         "mean_organic": float(g["Organic"].mean()),
         "mean_diff": float((g["NonOrganic"] - g["Organic"]).mean()),
         "percent_reduction": float(100 * (1 - g["Organic"].mean()
                                           / g["NonOrganic"].mean())),
         "n": len(g)}
        for p, g in df.groupby("Person", sort=False)
    ],
    "by_pesticide": [
        {"pesticide": p,
         "mean_nonorganic": float(g["NonOrganic"].mean()),
         "mean_organic": float(g["Organic"].mean()),
         "mean_diff": float((g["NonOrganic"] - g["Organic"]).mean()),
         "percent_reduction": float(100 * (1 - g["Organic"].mean()
                                           / g["NonOrganic"].mean())),
         "n": len(g)}
        for p, g in df.groupby("Pesticide", sort=False)
    ],
}

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ------------------------------------------------- human-readable summary
print("=" * 64)
print("Q17: Does eating organic food improve your health?")
print("Lock5 OrganicEffect - Magner et al. 2015, IVL Report U 5080 (Coop)")
print("=" * 64)
print("\nPublished headline (IVL report):")
print("  urinary pesticide concentrations decreased on average by a")
print("  factor of 6.7 on the organic diet; levels below the ADI")

print(f"\nMatched-pairs analysis (n = {n} pairs: 5 persons x 8 pesticides x 4 days)")
print(f"  mean NonOrganic = {mean_non:.2f}   mean Organic = {mean_org:.2f} "
      f"(micrograms/g creatinine)")
print(f"  mean diff = {mean_d:+.2f}  (median {med_d:+.2f}, SD {sd_d:.2f})")
print(f"  percent reduction = {percent_reduction:.1f}%  "
      f"(factor {ratio_of_means:.1f} lower; IVL headline: factor 6.7)")
print(f"  Cohen's d = {cohen_d:.3f}")
print(f"  paired t = {t_stat:.2f}, df = {n - 1}, "
      f"p(two-sided) = {p_t_two:.2e}, p(one-sided) = {p_t_greater:.2e}")
print(f"  theory 95% CI for mean diff: ({ci_t[0]:.2f}, {ci_t[1]:.2f})")
print(f"  Wilcoxon signed-rank p(two-sided) = {w_res.pvalue:.2e}")
print(f"  randomization p(two) = {p_rand_two:.5f}, "
      f"p(one, organic lower) = {p_rand_greater:.5f}")
print(f"  bootstrap 95% CI mean diff: ({mean_ci[0]:.2f}, {mean_ci[1]:.2f})")
print(f"  bootstrap 95% CI percent reduction: ({red_ci[0]:.1f}%, {red_ci[1]:.1f}%)")
print(f"  bootstrap 95% CI Cohen's d: ({cohen_ci[0]:.3f}, {cohen_ci[1]:.3f})")

print("\nBy person:")
for r in results["part_paired"]["by_person"]:
    print(f"  {r['person']:<6} Non = {r['mean_nonorganic']:>7.2f}  "
          f"Org = {r['mean_organic']:>6.2f}  "
          f"reduction = {r['percent_reduction']:>5.1f}%")
print("By pesticide:")
for r in results["part_paired"]["by_pesticide"]:
    print(f"  {r['pesticide']:<11} Non = {r['mean_nonorganic']:>7.2f}  "
          f"Org = {r['mean_organic']:>6.2f}  "
          f"reduction = {r['percent_reduction']:>5.1f}%")

print("\n  Caution: single family, diet order not randomized; exposure")
print("  biomarker, not a clinical health outcome; levels below the ADI.")
print(f"\nResults JSON written to {OUT_PATH.relative_to(REPO)}")
