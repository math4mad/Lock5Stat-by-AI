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

REPO = Path(__file__).resolve().parents[2]
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
