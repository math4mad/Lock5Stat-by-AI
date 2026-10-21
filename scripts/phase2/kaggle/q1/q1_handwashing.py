# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q1_handwashing.csv").write_text('venue,sex,n,washed\nTurner Field (Atlanta),male,778,493\nTurner Field (Atlanta),female,810,682\nMuseum of Science and Industry (Chicago),male,375,304\nMuseum of Science and Industry (Chicago),female,380,353\nShedd Aquarium (Chicago),male,375,318\nShedd Aquarium (Chicago),female,379,354\nGrand Central Station (New York City),male,410,273\nGrand Central Station (New York City),female,461,411\nPenn Station (New York City),male,342,218\nPenn Station (New York City),female,290,268\nFerry Terminal Farmers Market (San Francisco),male,926,787\nFerry Terminal Farmers Market (San Francisco),female,810,734\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
"""Q1 (Phase 2): What proportion of people using a public restroom wash their hands?

Provenance
----------
Observational study by Harris Interactive for the American Society for
Microbiology (ASM) and the Soap and Detergent Association (SDA), "A Survey of
Hand Washing Behavior (2005 Findings)", September 2005. On August 18-21, 2005,
trained observers discreetly watched 6,336 adults in public restrooms at six
major U.S. public attractions (Turner Field, Atlanta; Museum of Science and
Industry and Shedd Aquarium, Chicago; Grand Central Station and Penn Station,
New York City; Ferry Terminal Farmers Market, San Francisco) and recorded
whether each washed their hands after using the facilities.

Lock5 distributes no individual-level dataset for this study (3rd- and
4th-edition data pages checked, Oct 2026), so data/phase2/q1_handwashing.csv
is constructed from the published per-venue, per-sex counts (n and successes,
p. 6 of the report):

    Atlanta: Turner Field                M 493/778   F 682/810
    Chicago: Museum of Science & Industry M 304/375  F 353/380
    Chicago: Shedd Aquarium               M 318/375  F 354/379
    NYC: Grand Central Station            M 273/410  F 411/461
    NYC: Penn Station                     M 218/342  F 268/290
    SF: Ferry Terminal Farmers Market     M 787/926  F 734/810
    TOTAL observed 6,336; 5,195 washed (82.0%; press fact sheet rounds to 83%)

    Report PDF: https://www.pacificjanisystems.com/_files/ugd/d694e3_52e0fc4abb67e4f3744ee9d083db3a92.pdf
    Fact sheet: https://www.cleaninginstitute.org/sites/default/files/assets/1/AssetManager/2005%20Hand%20Hygiene%20Survey%20Key%20Findings.pdf

Analysis (one proportion, Lock5 spirit)
---------------------------------------
  - 95% theory-based (Wald) z-interval for p
  - z-test H0: p = 0.5 vs Ha: p > 0.5 (majority wash?), exact binomial check
  - z-test H0: p = 0.91 vs Ha: p < 0.91 (observed rate vs the 91% of adults
    who claim they always wash after using a public restroom)
  - 100,000-rep bootstrap percentile CI (resampling individual outcomes)
  - 100,000-rep randomization (simulation) tests under each null

Run from repo root: .venv/bin/python scripts/phase2/q1_handwashing.py
Outputs: prints summary; writes scripts/phase2/out/q1_results.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = _os_cwd  # Kaggle override
CSV_PATH = REPO / "data" / "phase2" / "q1_handwashing.csv"
OUT_PATH = REPO / "scripts" / "phase2" / "out" / "q1_results.json"

N_REPS = 100_000
SEED = 2026
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- load data
cells = pd.read_csv(CSV_PATH)
x = int(cells["washed"].sum())
n = int(cells["n"].sum())
p_hat = x / n

# Individual-level binary outcomes expanded from the published cell counts
# (row order within cells is arbitrary; counts are exactly as published).
ind = pd.DataFrame({
    "venue": np.repeat(cells["venue"], cells["n"]),
    "sex": np.repeat(cells["sex"], cells["n"]),
    "washed": np.concatenate([np.repeat([1, 0], [w, c_w - w])
                              for w, c_w in zip(cells["washed"], cells["n"])]),
})
assert len(ind) == n and ind["washed"].sum() == x, "expansion mismatch"

results = {
    "question": "What proportion of people using a public restroom wash their hands?",
    "provenance": {
        "study": "Harris Interactive for the American Society for Microbiology (ASM) "
                 "and the Soap and Detergent Association (SDA)",
        "report": "A Survey of Hand Washing Behavior (2005 Findings), September 2005",
        "design": "Observational: observers recorded handwashing by 6,336 adults in "
                  "public restrooms at six major U.S. public attractions, Aug 18-21, 2005",
        "data_source": "Constructed CSV from published per-venue/per-sex counts (n and successes); "
                       "no Lock5 dataset distributed for this study (3e/4e data pages checked)",
        "note": "Press fact sheet headline says 83%; the published counts give 82.0%",
    },
    "data": {"n": n, "washed": x, "not_washed": n - x, "source_csv": str(CSV_PATH.relative_to(REPO))},
    "point_estimate": {"proportion": p_hat, "se_wald": float(np.sqrt(p_hat * (1 - p_hat) / n))},
}

# ------------------------------------------------- 95% theory-based (Wald) CI
se = np.sqrt(p_hat * (1 - p_hat) / n)
z_crit = stats.norm.ppf(0.975)
ci_wald = (p_hat - z_crit * se, p_hat + z_crit * se)
results["ci_95_wald"] = [float(ci_wald[0]), float(ci_wald[1])]

# ------------------------------------------------- hypothesis tests (normal + exact)
def z_test(x, n, p0, alternative):
    z = (x / n - p0) / np.sqrt(p0 * (1 - p0) / n)
    if alternative == "greater":
        p_norm = stats.norm.sf(z)
        p_exact = stats.binomtest(x, n, p0, alternative="greater").pvalue
    else:  # less
        z = -abs(z)
        p_norm = stats.norm.cdf(z)
        p_exact = stats.binomtest(x, n, p0, alternative="less").pvalue
    return float(z), float(p_norm), float(p_exact)

z_majority, p_majority, p_majority_exact = z_test(x, n, 0.5, "greater")
z_selfrep, p_selfrep, _ = z_test(x, n, 0.91, "less")

# ------------------------------------------------- randomization (simulation) tests
rand_majority = rng.binomial(n, 0.5, N_REPS) / n
rand_selfrep = rng.binomial(n, 0.91, N_REPS) / n
p_rand_majority = float(np.mean(rand_majority >= p_hat))
p_rand_selfrep = float(np.mean(rand_selfrep <= p_hat))

# ------------------------------------------------- bootstrap percentile CI
boot = ind["washed"].to_numpy()[rng.integers(0, n, (N_REPS, n))].mean(axis=1)
ci_boot = tuple(np.percentile(boot, [2.5, 97.5]))
results["ci_95_bootstrap_percentile"] = [float(ci_boot[0]), float(ci_boot[1])]

results["tests"] = {
    "majority": {"null": 0.5, "alternative": "greater", "z": z_majority,
                 "p_normal": p_majority, "p_exact_binomial": p_majority_exact,
                 "p_randomization": p_rand_majority},
    "vs_self_report": {"null": 0.91, "alternative": "less",
                       "self_report_context": "91% of U.S. adults say they always wash after "
                                              "using a public restroom (telephone survey, same study)",
                       "z": z_selfrep, "p_normal": p_selfrep, "p_randomization": p_rand_selfrep},
}
results["methods"] = {"n_bootstrap": N_REPS, "n_randomization": N_REPS, "seed": SEED,
                      "engine": "numpy/scipy/pandas"}

# ------------------------------------------------- descriptives
by_sex = ind.groupby("sex")["washed"].agg(["count", "sum"])
by_venue = ind.groupby("venue")["washed"].agg(["count", "sum"])
results["breakdown"] = {
    "by_sex": {s: {"n": int(r["count"]), "washed": int(r["sum"]),
                   "proportion": float(r["sum"] / r["count"])} for s, r in by_sex.iterrows()},
    "by_venue": {v: {"n": int(r["count"]), "washed": int(r["sum"]),
                     "proportion": float(r["sum"] / r["count"])} for v, r in by_venue.iterrows()},
}

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ------------------------------------------------- human-readable summary
print("=" * 64)
print("Q1: What proportion of people using a public restroom wash their hands?")
print("Harris Interactive / ASM & SDA observational study, Aug 18-21, 2005")
print("=" * 64)
print(f"n = {n:,} adults observed; washed = {x:,}  ->  p-hat = {p_hat:.4f} ({p_hat:.1%})")
print(f"\n95% CI (Wald z):        ({ci_wald[0]:.4f}, {ci_wald[1]:.4f})")
print(f"95% CI (bootstrap):     ({ci_boot[0]:.4f}, {ci_boot[1]:.4f})")
print(f"\nTest 1  H0: p = 0.50 vs Ha: p > 0.50")
print(f"        z = {z_majority:.2f}, normal p = {p_majority:.2e}, "
      f"exact binomial p = {p_majority_exact:.2e}, randomization p = {p_rand_majority:.5f}")
print(f"Test 2  H0: p = 0.91 vs Ha: p < 0.91   (vs 91% who SAY they always wash)")
print(f"        z = {z_selfrep:.2f}, normal p = {p_selfrep:.2e}, "
      f"randomization p = {p_rand_selfrep:.5f}")
print("\nBy sex:")
for s, r in by_sex.iterrows():
    print(f"  {s:<6} {int(r['sum']):>5,}/{int(r['count']):>5,} = {r['sum'] / r['count']:.1%}")
print("\nBy venue:")
for v, r in by_venue.sort_values("sum", ascending=False).iterrows():
    print(f"  {v:<46} {int(r['sum']):>5,}/{int(r['count']):>5,} = {r['sum'] / r['count']:.1%}")
print(f"\nResults JSON written to {OUT_PATH.relative_to(REPO)}")
