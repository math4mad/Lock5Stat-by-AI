# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q5_aboveavg.csv").write_text('# Reconstructed counts from Cross, K. P. (1977), "Not can, but will college teaching\n# be improved?", New Directions for Higher Education, 1977(17), 1-15.\n# DOI: 10.1002/he.36919771703\n#\n# Published finding (from the article abstract): "more than 90 percent of faculty\n# members rate themselves as above-average teachers" and "two-thirds rate themselves\n# among the top quarter." The widely cited headline figures are 94% above average\n# (68% in the top quarter), surveying faculty during Cross\'s 1975-76 year as visiting\n# professor at the University of Nebraska-Lincoln.\n#\n# NOTE: Cross\'s exact sample size n is not documented in publicly accessible sources.\n# n = 250 is a documented reconstruction assumption chosen so that 235/250 = 94.0%\n# matches the cited headline proportion. Do not treat n as the true survey size.\nresponse,count\nAboveAverage,235\nNotAboveAverage,15\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
# Q5 (Phase 2): What percent of college professors consider themselves
# "above-average" teachers?
#
# Survey: Cross, K. P. (1977), "Not can, but will college teaching be improved?",
#   New Directions for Higher Education, 1977(17), 1-15. DOI 10.1002/he.36919771703.
#   Headline finding: 94% of faculty rated themselves above-average teachers
#   (68% ranked themselves in the top quarter).
# Data: reconstructed counts in data/phase2/q5_aboveavg.csv (235/250 = 94.0%).
#   Cross's exact n is not publicly documented; n = 250 is a documented
#   reconstruction assumption matching the cited headline proportion.
#
# One-proportion analysis: Wald 95% CI, z-test vs p0 = 0.5, exact binomial test,
# bootstrap percentile CI, and randomization (coin-flip) test.
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(2026)
P0 = 0.5

df = pd.read_csv("data/phase2/q5_aboveavg.csv", comment="#")
x = int(df.loc[df.response == "AboveAverage", "count"].iloc[0])
n = int(df["count"].sum())
p_hat = x / n
print(f"Q5: professors rating themselves 'above-average' teachers")
print(f"Data (reconstructed, Cross 1977): {x}/{n} = {p_hat:.1%}\n")

# 1) Parametric: Wald 95% CI and z-test vs p0 = 0.5
se_wald = np.sqrt(p_hat * (1 - p_hat) / n)
ci_wald = (p_hat - 1.96 * se_wald, p_hat + 1.96 * se_wald)
se_null = np.sqrt(P0 * (1 - P0) / n)
z = (p_hat - P0) / se_null
p_z = 2 * stats.norm.sf(abs(z))
p_exact = stats.binomtest(x, n, P0).pvalue
print(f"Wald 95% CI for p: ({ci_wald[0]:.4f}, {ci_wald[1]:.4f})")
print(f"z-test vs 0.50 (two-sided): z={z:.3f}, p={p_z:.6g}")
print(f"Exact binomial test vs 0.50 (two-sided): p={p_exact:.6g}\n")

# 2) Bootstrap 95% percentile CI (resample n from empirical distribution)
n_boot = 100_000
boot_p = rng.binomial(n, p_hat, size=n_boot) / n
ci_boot = np.percentile(boot_p, [2.5, 97.5])
print(f"Bootstrap 95% CI for p: ({ci_boot[0]:.4f}, {ci_boot[1]:.4f})")

# 3) Randomization (coin-flip) test under H0: p = 0.5, two-sided
n_rand = 100_000
rand_p = rng.binomial(n, P0, size=n_rand) / n
p_rand = (np.sum(np.abs(rand_p - P0) >= abs(p_hat - P0)) + 1) / (n_rand + 1)  # add-one so p > 0
print(f"Randomization test vs 0.50 (two-sided): p={p_rand:.6g}\n")

print("Conclusion: the proportion rating themselves above average is far above 50%,")
print("a classic better-than-average (illusory superiority) effect. Since n is a")
print("documented reconstruction assumption (Cross's exact n unavailable), the CI")
print("width is illustrative; the headline point estimate of 94% is the published figure.")

results = {
    "question": 'What percent of college professors consider themselves "above-average" teachers?',
    "citation": 'Cross, K. P. (1977). "Not can, but will college teaching be improved?" New Directions for Higher Education, 1977(17), 1-15. DOI 10.1002/he.36919771703',
    "data": {
        "file": "data/phase2/q5_aboveavg.csv",
        "provenance": "Reconstructed counts from Cross (1977); n=250 is a documented reconstruction assumption (exact n not published); 235/250 = 94.0% matches the cited headline.",
        "x_above_average": x,
        "n_total": n,
    },
    "p_hat": p_hat,
    "wald_ci_95": [float(ci_wald[0]), float(ci_wald[1])],
    "z_test_vs_50": {"z": float(z), "p_two_sided": float(p_z)},
    "exact_binomial_p_two_sided": float(p_exact),
    "bootstrap_ci_95": [float(ci_boot[0]), float(ci_boot[1])],
    "randomization_p_two_sided": float(p_rand),
    "conclusion": "94% of professors rated themselves above average, far above the 50% null; all methods (z-test, exact binomial, randomization) give p << 0.001. Strong better-than-average effect; CI width is illustrative due to assumed n.",
}
os.makedirs("scripts/phase2/out", exist_ok=True)
with open("scripts/phase2/out/q5_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("saved scripts/phase2/out/q5_results.json")
