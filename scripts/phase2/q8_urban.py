"""Q8 (Phase 2): Are city dwellers more likely than country dwellers to have
mood and anxiety disorders?

Provenance
----------
Question from Lock5 (Statistics: Unlocking the Power of Data, 3rd ed., Lock,
Lock, Lock, Lock & Lock), Phase 2 task list. The claim is classically backed
by the Dutch NEMESIS group:

  DATA SOURCE (counts used here):
    Peen J, Dekker J, Schoevers RA, ten Have M, de Graaf R, Beekman ATF
    (2007). "Is the prevalence of psychiatric disorders associated with
    urbanization?" Social Psychiatry and Psychiatric Epidemiology,
    42(12), 984-989. doi:10.1007/s00127-007-0256-2
    Netherlands Mental Health Survey and Incidence Study (NEMESIS):
    multi-stage stratified random sample, 7,076 adults aged 18-64
    (response 69.7%), interviewed 1996 with the CIDI; DSM-III-R
    12-month prevalence by degree of urbanization of the municipality
    (5 address-density categories of Statistics Netherlands).
    Full text: https://research.vu.nl/files/2274217/
    Peen%20Social%20Psychiatry%20and%20Psychiatrical%20Epidemiology%
    2042(12)%202007%20u.pdf

  HEADLINE CONTEXT (Lock5-associated claim):
    Peen J, Schoevers RA, Beekman AT, Dekker J (2010). "The current status of
    urban-rural differences in psychiatric disorders." Acta Psychiatrica
    Scandinavica, 121(2), 84-93. doi:10.1111/j.1600-0447.2009.01438.x
    Meta-analysis of 20 population surveys: pooled unadjusted urban-vs-rural
    OR 1.39 (1.23-1.58) for mood disorders and 1.21 (1.02-1.42) for anxiety
    disorders (i.e. rates ~39% / ~21% higher in urban areas).

Lock5 distributes no individual-level dataset for this study (3rd- and
4th-edition data pages checked, Oct 2026), so data/phase2/q8_urban.csv is
reconstructed from published counts in Table 2 of Peen et al. (2007), which
reports for each urbanization category the sample n and the n of 12-month
cases for mood disorders, anxiety disorders and one-or-more DSM-III-R
diagnoses. The published case counts are used verbatim:

    Very highly urbanized (>2,500 addr/km2)   n=1242  mood 129  anx 179  any 347
    Highly urbanized      (1,500-2,500)       n=1497  mood 133  anx 205  any 366
    Moderately urbanized  (1,000-1,500)       n=1541  mood 112  anx 178  any 373
    Not very urbanized    (500-1,000)         n=1611  mood 100  anx 184  any 330
    Not urbanized         (<500 addr/km2)     n=1185  mood  63  anx 128  any 221
    TOTAL                                     n=7076

Raw proportions from these counts reproduce the published (weighted)
percentages to within rounding (e.g. mood 129/1242 = 10.4% vs 10.4%;
63/1185 = 5.3% vs 5.3%; anxiety 179/1242 = 14.4% vs 14.4%; 128/1185 =
10.8% vs 10.8%), so the reconstruction is exact rather than estimated.

Analysis (comparing two proportions, Lock5 spirit)
---------------------------------------------------
Following Peen et al. (2010), the "most extreme dichotomy" is used for the
primary city-vs-country contrast: "Very highly urbanized" (city) vs
"Not urbanized" (country). Outcomes: mood disorders, anxiety disorders,
and (secondary context) one-or-more disorders. For each outcome:
  - difference in proportions with 95% Wald z-interval
  - two-proportion pooled z-test, two-sided and one-sided (city > country)
  - Fisher exact test on the 2x2 table, two-sided and one-sided
  - 100,000-rep randomization (permutation) test: group labels permuted
    with margins fixed, i.e. city successes ~ Hypergeometric(N, X, n_city)
  - odds ratio with 100,000-rep bootstrap percentile CI (each group
    resampled with replacement; for a binary outcome the success count of a
    resample is Binomial(n, p-hat), which is used for speed)

Run from repo root: .venv/bin/python scripts/phase2/q8_urban.py
Outputs: prints summary; writes scripts/phase2/out/q8_results.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
CSV_PATH = REPO / "data" / "phase2" / "q8_urban.csv"
OUT_PATH = REPO / "scripts" / "phase2" / "out" / "q8_results.json"

N_REPS = 100_000
SEED = 2026
rng = np.random.default_rng(SEED)

OUTCOME_COLS = {
    "mood_disorders": "mood_cases",
    "anxiety_disorders": "anxiety_cases",
    "any_disorder": "any_disorder_cases",
}

# ---------------------------------------------------------------- load data
df = pd.read_csv(CSV_PATH)
n_total = int(df["n"].sum())
assert n_total == 7076, f"expected NEMESIS n=7076, got {n_total}"

# Primary contrast: most extreme dichotomy (Peen et al. 2010 pooling rule)
city = df.loc[df["urbanization"] == "Very highly urbanized"].iloc[0]
country = df.loc[df["urbanization"] == "Not urbanized"].iloc[0]
n1, n2 = int(city["n"]), int(country["n"])  # city, country


def compare(x1, n1_, x2, n2_, label):
    """Two-proportion z + Fisher exact + randomization + OR bootstrap CI."""
    p1, p2 = x1 / n1_, x2 / n2_
    diff = p1 - p2
    p_pool = (x1 + x2) / (n1_ + n2_)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n1_ + 1 / n2_))
    z = diff / se_pool

    # unpooled Wald CI for the difference in proportions
    se_unpooled = np.sqrt(p1 * (1 - p1) / n1_ + p2 * (1 - p2) / n2_)
    z_crit = stats.norm.ppf(0.975)
    ci_diff = (diff - z_crit * se_unpooled, diff + z_crit * se_unpooled)

    # Fisher exact on the 2x2 table
    table = [[x1, n1_ - x1], [x2, n2_ - x2]]
    or_fisher, p_fis_two = stats.fisher_exact(table, alternative="two-sided")
    _, p_fis_greater = stats.fisher_exact(table, alternative="greater")

    # randomization (permutation) test: margins fixed -> hypergeometric
    x_total, n_tot = x1 + x2, n1_ + n2_
    perm_x1 = rng.hypergeometric(x_total, n_tot - x_total, n1_, N_REPS)
    perm_diff = perm_x1 / n1_ - (x_total - perm_x1) / (n_tot - n1_)
    p_rand_two = float(np.mean(np.abs(perm_diff) >= abs(diff)))
    p_rand_greater = float(np.mean(perm_diff >= diff))

    # bootstrap percentile CI for the odds ratio (nonparametric; binary
    # success count of a with-replacement resample is Binomial(n, p-hat))
    b1 = rng.binomial(n1_, p1, N_REPS)
    b2 = rng.binomial(n2_, p2, N_REPS)
    keep = (b1 > 0) & (b1 < n1_) & (b2 > 0) & (b2 < n2_)
    boot_or = (b1[keep] / (n1_ - b1[keep])) / (b2[keep] / (n2_ - b2[keep]))
    ci_or = tuple(np.percentile(boot_or, [2.5, 97.5]))

    return {
        "outcome": label,
        "city": {"n": n1_, "cases": int(x1), "proportion": float(p1)},
        "country": {"n": n2_, "cases": int(x2), "proportion": float(p2)},
        "diff_in_proportions": float(diff),
        "ci_95_wald_diff": [float(ci_diff[0]), float(ci_diff[1])],
        "odds_ratio": float((x1 / (n1_ - x1)) / (x2 / (n2_ - x2))),
        "ci_95_bootstrap_or": [float(ci_or[0]), float(ci_or[1])],
        "z_pooled": float(z),
        "p_z_two_sided": float(2 * stats.norm.sf(abs(z))),
        "p_z_greater": float(stats.norm.sf(z)),
        "p_fisher_two_sided": float(p_fis_two),
        "p_fisher_greater": float(p_fis_greater),
        "p_randomization_two_sided": p_rand_two,
        "p_randomization_greater": p_rand_greater,
    }


results = {
    "question": "Are city dwellers more likely than country dwellers to have "
                "mood and anxiety disorders?",
    "provenance": {
        "lock5_question": "Lock5 3rd ed., phase-2 task Q8",
        "data_source": "Peen J, Dekker J, Schoevers RA, ten Have M, de Graaf R, "
                       "Beekman ATF (2007). Is the prevalence of psychiatric "
                       "disorders associated with urbanization? Social Psychiatry "
                       "and Psychiatric Epidemiology, 42(12), 984-989. "
                       "doi:10.1007/s00127-007-0256-2 (NEMESIS, CIDI, DSM-III-R)",
        "headline_context": "Peen J, Schoevers RA, Beekman AT, Dekker J (2010). "
                            "The current status of urban-rural differences in "
                            "psychiatric disorders. Acta Psychiatrica "
                            "Scandinavica, 121(2), 84-93. Pooled unadjusted "
                            "urban-vs-rural OR: mood 1.39 (1.23-1.58), "
                            "anxiety 1.21 (1.02-1.42)",
        "design": "Cross-sectional population survey (NEMESIS, 1996): representative "
                  "multi-stage stratified random sample of 7,076 Dutch adults 18-64; "
                  "12-month DSM-III-R disorders by municipal address-density "
                  "(Statistics Netherlands 5-level urbanization)",
        "data_reconstruction": "No Lock5 dataset distributed for this study (3e/4e data "
                               "pages checked Oct 2026); CSV reconstructed from exact "
                               "published Table 2 counts (n and n of cases per "
                               "urbanization category). Raw proportions from the counts "
                               "reproduce the published weighted percentages to within "
                               "rounding.",
        "contrast": "Most extreme dichotomy per Peen et al. 2010: 'Very highly "
                    "urbanized' (city) vs 'Not urbanized' (country)",
    },
    "data": {"n_total": n_total, "source_csv": str(CSV_PATH.relative_to(REPO))},
    "comparisons": {},
    "methods": {"n_randomization": N_REPS, "n_bootstrap": N_REPS, "seed": SEED,
                "engine": "numpy/scipy/pandas"},
}

for key, col in OUTCOME_COLS.items():
    results["comparisons"][key] = compare(int(city[col]), n1, int(country[col]), n2, key)

# ------------------------------------------------- per-level descriptive breakdown
by_level = df.set_index("urbanization")
results["breakdown_by_urbanization"] = {
    row.Index: {  # type: ignore[attr-defined]
        "level_rank_from_rural": int(len(df) - i),
        "n": int(row.n),
        "mood": row.mood_cases / row.n,
        "anxiety": row.anxiety_cases / row.n,
        "any": row.any_disorder_cases / row.n,
    }
    for i, row in enumerate(by_level.itertuples())
}

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ------------------------------------------------- human-readable summary
print("=" * 64)
print("Q8: Are city dwellers more likely than country dwellers to have")
print("    mood and anxiety disorders?")
print("NEMESIS (Peen et al. 2007), n=7,076 Dutch adults 18-64, 12-month")
print("DSM-III-R prevalence; city = very highly urbanized (n=1,242),")
print("country = not urbanized (n=1,185)")
print("=" * 64)
for key in OUTCOME_COLS:
    r = results["comparisons"][key]
    print(f"\n{key.replace('_', ' ').capitalize()}:")
    print(f"  city    {r['city']['cases']:>4}/{r['city']['n']:,} = {r['city']['proportion']:.1%}"
          f"   country {r['country']['cases']:>4}/{r['country']['n']:,} = {r['country']['proportion']:.1%}")
    print(f"  diff = {r['diff_in_proportions']:+.4f}  "
          f"95% Wald CI ({r['ci_95_wald_diff'][0]:+.4f}, {r['ci_95_wald_diff'][1]:+.4f})")
    print(f"  OR = {r['odds_ratio']:.2f}  "
          f"95% bootstrap CI ({r['ci_95_bootstrap_or'][0]:.2f}, {r['ci_95_bootstrap_or'][1]:.2f})")
    print(f"  z = {r['z_pooled']:.2f}  p(two-sided) = {r['p_z_two_sided']:.2e}  "
          f"p(city>country) = {r['p_z_greater']:.2e}")
    print(f"  Fisher exact: p(two-sided) = {r['p_fisher_two_sided']:.2e}  "
          f"p(city>country) = {r['p_fisher_greater']:.2e}")
    print(f"  Randomization ({N_REPS:,} perms): p(two-sided) = "
          f"{r['p_randomization_two_sided']:.5f}  p(city>country) = "
          f"{r['p_randomization_greater']:.5f}")

print("\nBy urbanization level (proportion with disorder):")
for u, r in results["breakdown_by_urbanization"].items():
    print(f"  {u:<24} n={r['n']:>5,}  mood={r['mood']:.1%}  "
          f"anxiety={r['anxiety']:.1%}  any={r['any']:.1%}")
print(f"\nResults JSON written to {OUT_PATH.relative_to(REPO)}")
