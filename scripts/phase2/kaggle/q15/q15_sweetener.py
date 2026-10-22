# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q15_sweetener.csv").write_text('table,group,n,metric,value,ci95_low,ci95_high\ndelta_bmi,0 per week (none),1819,mean_dbmi_kg_m2,1.01,0.88,1.14\ndelta_bmi,<3 per week,420,mean_dbmi_kg_m2,1.11,0.85,1.38\ndelta_bmi,3-10 per week,422,mean_dbmi_kg_m2,1.46,1.20,1.73\ndelta_bmi,11-21 per week,401,mean_dbmi_kg_m2,1.50,1.23,1.78\ndelta_bmi,22+ per week,403,mean_dbmi_kg_m2,1.78,1.51,2.06\nbaseline_status,nonuser,1767,ow_or_obese,1064,,\nbaseline_status,nonuser,1767,obese,408,,\nbaseline_status,user,1604,ow_or_obese,1084,,\nbaseline_status,user,1604,obese,446,,\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
"""Q15 (Phase 2): Do artificial sweeteners cause weight gain?

Provenance
----------
Primary source: Fowler SP, Williams K, Resendez RG, Hunt KJ, Hazuda HP,
Stern MP. "Fueling the Obesity Epidemic? Artificially Sweetened Beverage Use
and Long-term Weight Gain." Obesity (Silver Spring) 2008;16(8):1894-1900.
doi:10.1038/oby.2008.284 (PMID 18535548).
https://onlinelibrary.wiley.com/doi/10.1038/oby.2008.284

Design: prospective observational cohort - the San Antonio Heart Study.
5,158 adults (25-64 y, San Antonio, TX) enrolled 1979-1988; 3,682 (74% of
survivors) re-examined 7-8 years later. Adjusted models use the 3,371
participants with complete covariate data; the change-in-BMI (DBMI) figure
analysis reports n = 3,465 (participants with baseline ASB dose and
follow-up BMI).

Source-study choice: the question asks about weight gain, so the best match
is this human prospective cohort rather than Suez et al. (2014, Nature
514:181-186), whose human/experimental evidence concerns glucose
intolerance and gut microbiota. Lock5 distributes no dataset for either
study (3rd-edition data page checked Oct 2026; only an unrelated
"DietDepression" file matches soda/sweet keywords), so
data/phase2/q15_sweetener.csv is reconstructed from numbers published in
Fowler et al. (2008):

  Table "delta_bmi" - 7-8 y change in BMI (kg/m2) by baseline artificially
  sweetened beverage (ASB) consumption:
    * group n's are printed on the x-axis of Figure 2a:
        None 1,819 | <3/week 420 | 3-10/week 422 | 11-21/week 401 | 22+/week 403
    * adjusted group means and 95% CIs are quoted in the Results text:
        1.01 (0.88, 1.14) | 1.11 (0.85, 1.38) | 1.46 (1.20, 1.73)
        1.50 (1.23, 1.78) | 1.78 (1.51, 2.06)

  Table "baseline_status" - baseline overweight/obesity by self-reported AS
  use (Table 1 of the paper: nonusers n = 1,767, users n = 1,604). Counts
  are back-calculated from the published percentages (60.2% vs 67.6%
  overweight-or-obese; 23.1% vs 27.8% obese) and rounded to the nearest
  integer:
        nonuser 1,064/1,767 OW/OB (60.2%), 408/1,767 obese (23.1%)
        user    1,084/1,604 OW/OB (67.6%), 446/1,604 obese (27.8%)

  Published headline statistics quoted (not re-derived here):
    * OW/OB incidence: >21 ASBs/week (22+) vs none -> adjusted OR = 1.93
      (95% CI 1.20-3.11, P = 0.007) among the 1,250 baseline normal-weight
      participants, of whom 428 (34.0%) became overweight/obese.
    * Obesity incidence: 22+ vs none -> adjusted OR = 2.03
      (95% CI 1.36-3.03, P = 0.0005) among the 2,571 with baseline
      BMI < 30, of whom 390 (15.2%) became obese.
    * Overall adjusted DBMI: users +1.48 vs nonusers +1.01 kg/m2 (47%
      greater, P < 0.0001).

Analysis (Lock5 spirit, two data shapes)
----------------------------------------
  A. Two-proportion analysis of the baseline 2x2 (ASB user vs nonuser,
     overweight/obese at baseline):
       - two-proportion z-test (pooled SE), two- and one-sided
       - Fisher's exact test
       - 100,000-rep randomization test (label shuffling = hypergeometric)
       - risk ratio and odds ratio with 100,000-rep bootstrap percentile CIs
  B. Group-mean comparison of DBMI (None vs 22+ per week primary contrast):
       - within-group SDs reconstructed from the published 95% CIs
         (SE = width/3.92, SD = SE*sqrt(n)) - these are ANCOVA-adjusted
         intervals, so theory-based tests are approximations
       - Welch t-test (from published summary stats) and one-way ANOVA
         across all five consumption groups
       - 100,000-rep bootstrap percentile CI for the mean difference
       - 100,000-rep randomization (label-permutation) test
       - linear trend across consumption categories (Pearson r)

Caveat: observational study - association does not establish causation
(reverse causation is plausible: heavier individuals may switch to diet
drinks). The paper's own adjusted models partially address confounding.

Run from repo root: .venv/bin/python scripts/phase2/q15_sweetener.py
Outputs: prints summary; writes scripts/phase2/out/q15_results.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = _os_cwd  # Kaggle override
CSV_PATH = REPO / "data" / "phase2" / "q15_sweetener.csv"
OUT_PATH = REPO / "scripts" / "phase2" / "out" / "q15_results.json"

N_REPS = 100_000
SEED = 2026
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- load data
df = pd.read_csv(CSV_PATH)
dbmi = df[df["table"] == "delta_bmi"].copy()
base = df[df["table"] == "baseline_status"].copy()

groups = dbmi["group"].tolist()
n_g = dbmi["n"].to_numpy(int)
mean_g = dbmi["value"].to_numpy(float)
lo_g = dbmi["ci95_low"].to_numpy(float)
hi_g = dbmi["ci95_high"].to_numpy(float)
# SD reconstructed from published 95% CI of the (adjusted) group mean
se_g = (hi_g - lo_g) / (2 * stats.norm.ppf(0.975))
sd_g = se_g * np.sqrt(n_g)

# baseline 2x2: ASB user vs nonuser, overweight/obese (BMI >= 25) at baseline
owob = base[base["metric"] == "ow_or_obese"].set_index("group")
n_non = int(owob.loc["nonuser", "n"])
n_usr = int(owob.loc["user", "n"])
x_non = int(owob.loc["nonuser", "value"])   # OW/OB among nonusers
x_usr = int(owob.loc["user", "value"])      # OW/OB among users

p_non, p_usr = x_non / n_non, x_usr / n_usr
n_tot, x_tot = n_non + n_usr, x_non + x_usr
p_pool = x_tot / n_tot

results = {
    "question": "Do artificial sweeteners cause weight gain?",
    "provenance": {
        "study": "San Antonio Heart Study - prospective observational cohort",
        "citation": "Fowler SP, Williams K, Resendez RG, Hunt KJ, Hazuda HP, Stern MP. "
                    "Fueling the Obesity Epidemic? Artificially Sweetened Beverage Use and "
                    "Long-term Weight Gain. Obesity (Silver Spring) 2008;16(8):1894-1900.",
        "doi": "10.1038/oby.2008.284",
        "pmid": "18535548",
        "url": "https://onlinelibrary.wiley.com/doi/10.1038/oby.2008.284",
        "design": "5,158 adults enrolled 1979-1988; 3,682 re-examined after 7-8 years; "
                  "3,371 with complete covariates for adjusted models (3,465 in the DBMI figure analysis)",
        "data_source": "Reconstructed CSV: group n's from Figure 2a axis labels; adjusted group "
                       "means and 95% CIs from the Results text; baseline counts back-calculated "
                       "from Table 1 percentages. No Lock5 dataset exists for this study "
                       "(3e data page checked Oct 2026).",
        "related_study": "Suez et al. 2014 (Nature 514:181-186) covers glucose intolerance/gut "
                         "microbiota, not weight gain, so Fowler et al. 2008 is the better match.",
        "caution": "Observational study: association does not establish causation; reverse "
                   "causation (heavier people choosing diet drinks) is plausible.",
    },
    "published_headlines": {
        "or_owob_incidence_22plus_vs_none": {"or": 1.93, "ci95": [1.20, 3.11], "p": 0.007,
                                             "context": "1,250 baseline normal-weight participants; "
                                                        "428 (34.0%) became overweight/obese"},
        "or_obese_incidence_22plus_vs_none": {"or": 2.03, "ci95": [1.36, 3.03], "p": 0.0005,
                                              "context": "2,571 with baseline BMI < 30; "
                                                         "390 (15.2%) became obese"},
        "adjusted_dbmi_users_vs_nonusers": {"users": 1.48, "nonusers": 1.01,
                                            "percent_greater": 47, "p": "<0.0001"},
    },
    "methods": {"n_bootstrap": N_REPS, "n_randomization": N_REPS, "seed": SEED,
                "engine": "numpy/scipy/pandas"},
}

# =================================================================
# Part A - two-proportion analysis: baseline OW/OB by ASB use (2x2)
# =================================================================
diff = p_usr - p_non
se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_non + 1 / n_usr))
z_two = diff / se_pool
p_z_two = 2 * stats.norm.sf(abs(z_two))
p_z_greater = stats.norm.sf(z_two)

or_table = np.array([[x_usr, n_usr - x_usr], [x_non, n_non - x_non]])
p_fisher = stats.fisher_exact(or_table)

# risk ratio and odds ratio (point estimates)
rr = p_usr / p_non
odds_usr, odds_non = p_usr / (1 - p_usr), p_non / (1 - p_non)
orr = odds_usr / odds_non

# randomization test: shuffle the OW/OB labels between the two groups
# (equivalent to assigning x_tot OW/OB cases to groups of size n_usr: hypergeometric)
rand_usr = rng.hypergeometric(x_tot, n_tot - x_tot, n_usr, N_REPS)
rand_diff = rand_usr / n_usr - (x_tot - rand_usr) / n_non
p_rand_greater = float(np.mean(rand_diff >= diff))
p_rand_two = float(np.mean(np.abs(rand_diff) >= abs(diff)))

# bootstrap percentile CIs for RR and OR (binomial resampling within groups)
b_usr = rng.binomial(n_usr, p_usr, N_REPS)
b_non = rng.binomial(n_non, p_non, N_REPS)
boot_rr = (b_usr / n_usr) / (b_non / n_non)
boot_or = (b_usr / (n_usr - b_usr)) / (b_non / (n_non - b_non))
rr_ci = tuple(np.percentile(boot_rr, [2.5, 97.5]))
or_ci = tuple(np.percentile(boot_or, [2.5, 97.5]))

results["part_a_two_proportion"] = {
    "endpoint": "overweight/obese (BMI >= 25) at baseline, by self-reported artificial-sweetener use",
    "data": {"nonuser": {"n": n_non, "ow_obese": x_non, "proportion": p_non},
             "user": {"n": n_usr, "ow_obese": x_usr, "proportion": p_usr}},
    "diff_in_proportions": diff,
    "z_test": {"z": float(z_two), "p_two_sided": float(p_z_two),
               "p_one_sided_user_greater": float(p_z_greater)},
    "fisher_exact": {"p_two_sided": float(p_fisher.pvalue),
                     "odds_ratio": float(p_fisher.statistic)},
    "randomization": {"p_two_sided": p_rand_two, "p_one_sided_user_greater": p_rand_greater},
    "risk_ratio": {"estimate": float(rr), "ci95_bootstrap": [float(rr_ci[0]), float(rr_ci[1])]},
    "odds_ratio": {"estimate": float(orr), "ci95_bootstrap": [float(or_ci[0]), float(or_ci[1])]},
}

# =================================================================
# Part B - group-mean comparison of 7-8 y BMI change (DBMI)
# =================================================================
i_none = groups.index("0 per week (none)")
i_high = groups.index("22+ per week")

# theory-based tests from published summary statistics
t_welch = stats.ttest_ind_from_stats(mean_g[i_high], sd_g[i_high], n_g[i_high],
                                     mean_g[i_none], sd_g[i_none], n_g[i_none],
                                     equal_var=False)
v_hi, v_lo = sd_g[i_high] ** 2 / n_g[i_high], sd_g[i_none] ** 2 / n_g[i_none]
df_welch = (v_hi + v_lo) ** 2 / (v_hi ** 2 / (n_g[i_high] - 1) + v_lo ** 2 / (n_g[i_none] - 1))
diff_dbmi = mean_g[i_high] - mean_g[i_none]

# individual-level values simulated from published group means/SDs (seed 2026)
sim = [rng.normal(mean_g[i], sd_g[i], n_g[i]) for i in range(len(groups))]
f_anova = stats.f_oneway(*sim)

# bootstrap percentile CI for the mean difference (22+ minus None), chunked
hi_vals, lo_vals = sim[i_high], sim[i_none]
boot_diff = np.empty(N_REPS)
done = 0
while done < N_REPS:
    m = min(10_000, N_REPS - done)
    s_hi = hi_vals[rng.integers(0, n_g[i_high], (m, n_g[i_high]))].mean(axis=1)
    s_lo = lo_vals[rng.integers(0, n_g[i_none], (m, n_g[i_none]))].mean(axis=1)
    boot_diff[done:done + m] = s_hi - s_lo
    done += m
dbmi_ci = tuple(np.percentile(boot_diff, [2.5, 97.5]))

# randomization (label-permutation) test on the pooled simulated values
pooled = np.concatenate([hi_vals, lo_vals])
n_hi = n_g[i_high]
perm_diff = np.empty(N_REPS)
done = 0
while done < N_REPS:
    m = min(5_000, N_REPS - done)
    order = rng.random((m, pooled.size)).argsort(axis=1)
    perm = pooled[order]
    perm_diff[done:done + m] = perm[:, :n_hi].mean(axis=1) - perm[:, n_hi:].mean(axis=1)
    done += m
p_perm = float(np.mean(np.abs(perm_diff) >= abs(diff_dbmi)))

# linear trend across consumption categories (ordinal 0..4) on simulated values
all_vals = np.concatenate(sim)
cat = np.concatenate([np.full(n_g[i], i) for i in range(len(groups))])
r_trend = stats.pearsonr(cat, all_vals)

results["part_b_group_means"] = {
    "endpoint": "change in BMI (kg/m2) over 7-8 years, by baseline ASB consumption (adjusted means)",
    "groups": [{"group": groups[i], "n": int(n_g[i]), "mean_dbmi": float(mean_g[i]),
                "ci95_published": [float(lo_g[i]), float(hi_g[i])],
                "sd_reconstructed": float(sd_g[i])} for i in range(len(groups))],
    "contrast": "22+ per week minus None",
    "diff_in_means": float(diff_dbmi),
    "percent_greater_than_nonusers": float(diff_dbmi / mean_g[i_none] * 100),
    "welch_t_test": {"t": float(t_welch.statistic), "df": float(df_welch),
                     "p_two_sided": float(t_welch.pvalue)},
    "anova_omnibus": {"F": float(f_anova.statistic), "p": float(f_anova.pvalue)},
    "bootstrap": {"ci95_mean_diff": [float(dbmi_ci[0]), float(dbmi_ci[1])]},
    "randomization": {"p_two_sided": p_perm},
    "linear_trend": {"pearson_r": float(r_trend.statistic), "p": float(r_trend.pvalue)},
}

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ------------------------------------------------- human-readable summary
print("=" * 64)
print("Q15: Do artificial sweeteners cause weight gain?")
print("Fowler et al. 2008, Obesity 16(8):1894-1900 - San Antonio Heart Study")
print("=" * 64)
print("\nPublished headline statistics (adjusted models):")
print("  OR overweight/obesity incidence, 22+ ASBs/wk vs none: 1.93 (1.20-3.11), P=0.007")
print("  OR obesity incidence,            22+ ASBs/wk vs none: 2.03 (1.36-3.03), P=0.0005")
print("  Adjusted DBMI: users +1.48 vs nonusers +1.01 kg/m2 (+47%, P<0.0001)")

print(f"\nPart A - baseline overweight/obesity by AS use (2x2, n={n_tot:,})")
print(f"  nonusers: {x_non:,}/{n_non:,} = {p_non:.1%}   users: {x_usr:,}/{n_usr:,} = {p_usr:.1%}")
print(f"  diff = {diff:+.4f};  z = {z_two:.2f}, p(two-sided) = {p_z_two:.2e}")
print(f"  Fisher exact p = {p_fisher.pvalue:.2e};  "
      f"randomization p(two) = {p_rand_two:.5f}, p(one) = {p_rand_greater:.5f}")
print(f"  risk ratio = {rr:.3f}  (95% bootstrap CI {rr_ci[0]:.3f} to {rr_ci[1]:.3f})")
print(f"  odds ratio = {orr:.3f}  (95% bootstrap CI {or_ci[0]:.3f} to {or_ci[1]:.3f})")

print(f"\nPart B - 7-8 y BMI change by baseline ASB consumption")
for i, g in enumerate(groups):
    print(f"  {g:<14} n={n_g[i]:>5,}  DBMI = {mean_g[i]:.2f} kg/m2  "
          f"(95% CI {lo_g[i]:.2f}-{hi_g[i]:.2f}; SD~{sd_g[i]:.2f})")
print(f"  None vs 22+/wk: diff = {diff_dbmi:+.2f} kg/m2 "
      f"({diff_dbmi / mean_g[i_none] * 100:.0f}% greater than nonusers)")
print(f"  Welch t = {t_welch.statistic:.2f}, df = {df_welch:.0f}, p = {t_welch.pvalue:.2e}")
print(f"  ANOVA F(4,{len(all_vals) - 5:.0f}) = {f_anova.statistic:.2f}, p = {f_anova.pvalue:.2e}")
print(f"  bootstrap 95% CI for diff: ({dbmi_ci[0]:.3f}, {dbmi_ci[1]:.3f})")
print(f"  randomization p(two-sided) = {p_perm:.5f}")
print(f"  linear trend: r = {r_trend.statistic:.3f}, p = {r_trend.pvalue:.2e}")
print("\n  Caution: observational - association does not establish causation.")
print(f"\nResults JSON written to {OUT_PATH.relative_to(REPO)}")
