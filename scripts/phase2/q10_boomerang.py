#!/usr/bin/env python3
"""Lock5 Phase 2, Q10: "What percent of young adults in the US move back in with their parents?"

Pew Research Center analysis of Census Bureau Current Population Survey (CPS) monthly
files: 52% of U.S. 18- to 29-year-olds (26.6 million) lived with a parent in July 2020,
up from 47% in February 2020 (pre-pandemic) -- a 2.6 million increase. The previous
all-time high was 48% in the 1940 census.

Citation: Fry, R., Passel, J. S., & Cohn, D. V. (September 4, 2020), "A majority of
young adults in the U.S. live with their parents for the first time since the Great
Depression", Pew Research Center. Lock5 3e ships no dataset for this question (checked
lock5stat.com/datapage3e.html), so data/phase2/q10_boomerang.csv holds documented
count reconstructions from the published percentages (provenance in the CSV header).

Analysis: one-proportion Wald + bootstrap CIs and tests of the July 2020 share against
meaningful historical nulls (Feb 2020 pre-pandemic baseline p0=0.47; 1940 previous
record p0=0.48), plus two-proportion comparisons across subgroups (men vs women,
ages 18-24 vs 25-29) with Wald/bootstrap CIs, pooled z-tests, randomization tests
and Fisher exact. numpy/scipy/pandas only; seed 2026; 100k replicates.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data" / "phase2" / "q10_boomerang.csv"
OUT = REPO / "scripts" / "phase2" / "out" / "q10_results.json"

GROUP_LABEL = {
    "overall": "All 18- to 29-year-olds",
    "men": "Men 18-29",
    "women": "Women 18-29",
    "age_18_24": "Ages 18-24",
    "age_25_29": "Ages 25-29",
}

rng = np.random.default_rng(2026)
B = 100_000  # bootstrap / randomization iterations

df = pd.read_csv(DATA, comment="#")
wide = df.pivot_table(index=["group", "period"], columns="response", values="count",
                      aggfunc="sum")[["with_parent", "not_with_parent"]]
print("Question: What percent of young adults in the US move back in with their parents?")
print("Outcome: share of 18- to 29-year-olds residing with at least one parent\n")
print("Reconstructed counts (data/phase2/q10_boomerang.csv):")
print(wide, "\n")

counts = {(g, t): (int(r["with_parent"]), int(r["not_with_parent"]))
          for (g, t), r in wide.iterrows()}

# --- 1) One-proportion analysis of the July 2020 overall share -------------------
def one_prop(group, period, p0, p0_label):
    yes, no = counts[(group, period)]
    n = yes + no
    p = yes / n
    se = np.sqrt(p * (1 - p) / n)
    wald = (p - 1.96 * se, p + 1.96 * se)
    boot = rng.binomial(n, p, B) / n
    boot_ci = np.percentile(boot, [2.5, 97.5])
    null = rng.binomial(n, p0, B) / n  # randomization under H0: p = p0
    p_rand = np.mean(np.abs(null - p0) >= abs(p - p0) - 1e-12)
    z = (p - p0) / np.sqrt(p0 * (1 - p0) / n)
    p_z = 2 * stats.norm.sf(abs(z))
    print(f"--- {GROUP_LABEL[group]}, {period}: {yes:,}/{n:,} = {p:.3f}")
    print(f"    95% CI (Wald):        ({wald[0]:.4f}, {wald[1]:.4f})")
    print(f"    95% CI (bootstrap):   ({boot_ci[0]:.4f}, {boot_ci[1]:.4f})")
    print(f"    Test H0 p={p0} ({p0_label}): z={z:.2f}, normal p={p_z:.2e}, "
          f"randomization p={p_rand:.2e} ({B} shuffles)\n")
    return {
        "group": group, "label": GROUP_LABEL[group], "period": period,
        "with_parent": yes, "n": n, "phat": round(p, 4),
        "wald_ci95": [round(wald[0], 4), round(wald[1], 4)],
        "bootstrap_ci95": [round(boot_ci[0], 4), round(boot_ci[1], 4)],
        "test_h0": {"p0": p0, "null_label": p0_label, "z": round(float(z), 3),
                    "p_normal": float(f"{p_z:.2e}"),
                    "p_randomization": float(f"{p_rand:.2e}")},
    }

feb_overall = counts[("overall", "feb_2020")]
feb_p = feb_overall[0] / sum(feb_overall)
print(f"--- Baseline (descriptive): overall, feb_2020 (pre-pandemic): "
      f"{feb_overall[0]:,}/{sum(feb_overall):,} = {feb_p:.3f}\n")

jul_feb = one_prop("overall", "jul_2020", round(feb_p, 2),
                   "Feb 2020 pre-pandemic baseline")
jul_1940 = one_prop("overall", "jul_2020", 0.48,
                    "1940 census, previous all-time high")

# --- 2) Two-proportion comparisons across subgroups (July 2020) ------------------
def two_prop(group_a, group_b):
    ya, noa = counts[(group_a, "jul_2020")]
    yb, nob = counts[(group_b, "jul_2020")]
    na_, nb = ya + noa, yb + nob
    pa, pb = ya / na_, yb / nb
    diff = pa - pb
    se_un = np.sqrt(pa * (1 - pa) / na_ + pb * (1 - pb) / nb)
    wald = (diff - 1.96 * se_un, diff + 1.96 * se_un)
    pooled = (ya + yb) / (na_ + nb)
    se_p = np.sqrt(pooled * (1 - pooled) * (1 / na_ + 1 / nb))
    z = diff / se_p
    p_z = 2 * stats.norm.sf(abs(z))
    # Randomization test: shuffling group labels -> hypergeometric #yes in group A
    yes_tot, no_tot = ya + yb, noa + nob
    k = rng.hypergeometric(yes_tot, no_tot, na_, B)
    stat_perm = np.abs(k / na_ - (yes_tot - k) / nb)
    p_rand = np.mean(stat_perm >= abs(diff) - 1e-12)
    _, p_fisher = stats.fisher_exact([[ya, noa], [yb, nob]])
    # Bootstrap CI for the difference (resample each group separately)
    boot = rng.binomial(na_, pa, B) / na_ - rng.binomial(nb, pb, B) / nb
    boot_ci = np.percentile(boot, [2.5, 97.5])
    res = {
        "group_a": {"group": group_a, "label": GROUP_LABEL[group_a],
                    "with_parent": ya, "n": na_, "phat": round(pa, 4)},
        "group_b": {"group": group_b, "label": GROUP_LABEL[group_b],
                    "with_parent": yb, "n": nb, "phat": round(pb, 4)},
        "diff_phat": round(diff, 4),
        "wald_ci95_diff": [round(wald[0], 4), round(wald[1], 4)],
        "bootstrap_ci95_diff": [round(boot_ci[0], 4), round(boot_ci[1], 4)],
        "test_equal_p": {"z": round(float(z), 3), "p_normal": float(f"{p_z:.2e}"),
                         "p_randomization": float(f"{p_rand:.2e}"),
                         "p_fisher_exact": float(f"{p_fisher:.2e}")},
    }
    print(f"--- {GROUP_LABEL[group_a]} ({pa:.3f}) vs {GROUP_LABEL[group_b]} ({pb:.3f})")
    print(f"    diff = {diff:.4f}")
    print(f"    95% CI (Wald):      ({wald[0]:.4f}, {wald[1]:.4f})")
    print(f"    95% CI (bootstrap): ({boot_ci[0]:.4f}, {boot_ci[1]:.4f})")
    print(f"    z={z:.2f}, normal p={p_z:.2e}, randomization p={p_rand:.2e}, "
          f"Fisher exact p={p_fisher:.2e}\n")
    return res

print("--- Two-proportion comparisons, July 2020 (difference in share living with a parent)")
mw = two_prop("men", "women")
ages = two_prop("age_18_24", "age_25_29")

# --- 3) Conclusion + results JSON ------------------------------------------------
print("Conclusion:")
print(f"  In July 2020, {jul_feb['phat']:.0%} of U.S. 18- to 29-year-olds lived with a")
print("  parent (26.6 million) -- the first majority since the Great Depression era,")
print("  exceeding even the 1940 record of 48% and the Feb 2020 pre-pandemic share of")
print(f"  {feb_p:.0%}. With n = 51.2 million, both nulls are rejected overwhelmingly")
print("  (p < 1e-15). Young men exceed young women (55% vs 49%) and the youngest")
print("  adults dominate the increase (ages 18-24: 71% vs 28% for ages 25-29), all")
print("  differences significant at any conventional level.")

results = {
    "question": "What percent of young adults in the US move back in with their parents?",
    "outcome": ("Share of U.S. 18- to 29-year-olds residing with at least one parent "
                "(co-residence, incl. COVID-era 'boomerang' moves), CPS monthly files."),
    "citation": (
        "Fry, R., Passel, J. S., & Cohn, D. V. (September 4, 2020), 'A majority of "
        "young adults in the U.S. live with their parents for the first time since the "
        "Great Depression', Pew Research Center. Underlying data: U.S. Census Bureau "
        "Current Population Survey monthly files (IPUMS); historical series from "
        "decennial censuses 1900-1990 and CPS annual averages 2000-2019."
    ),
    "dataset": {
        "path": "data/phase2/q10_boomerang.csv",
        "note": ("Lock5 3e ships no dataset for this question (checked "
                 "lock5stat.com/datapage3e.html). Counts are documented reconstructions "
                 "from the published percentages; provenance and denominator choices "
                 "in CSV header comments."),
    },
    "one_proportion": {
        "overall_feb_2020_baseline": {"phat": round(feb_p, 4),
                                      "with_parent": feb_overall[0],
                                      "n": sum(feb_overall)},
        "overall_jul_2020_vs_feb2020": jul_feb,
        "overall_jul_2020_vs_1940": jul_1940,
    },
    "two_proportion": {
        "men_vs_women_jul_2020": mw,
        "age_18_24_vs_25_29_jul_2020": ages,
    },
    "conclusion": (
        "52% of U.S. 18- to 29-year-olds (26.6 million of ~51.2 million) lived with a "
        "parent in July 2020, up from 47% in February 2020 (+2.6 million) and above the "
        "1940 census record of 48% -- first majority since the Great Depression. Both "
        "nulls rejected (p < 1e-15). Men > women (55% vs 49%) and ages 18-24 far above "
        "ages 25-29 (71% vs 28%), all p < 1e-15."
    ),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, indent=2) + "\n")
print(f"\nSaved results to {OUT}")
