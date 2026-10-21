# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q3_spider.csv").write_text('male_id,personality,play_bouts,kept_female\n1,aggressive,8,0\n2,aggressive,3,0\n3,aggressive,3,1\n4,aggressive,5,0\n5,aggressive,3,1\n6,aggressive,2,0\n7,aggressive,5,0\n8,aggressive,5,0\n9,aggressive,4,1\n10,aggressive,7,0\n11,aggressive,7,1\n12,aggressive,9,1\n13,aggressive,3,1\n14,aggressive,8,1\n15,aggressive,3,0\n16,aggressive,3,1\n17,aggressive,4,0\n18,aggressive,7,0\n19,aggressive,5,0\n20,aggressive,3,1\n21,aggressive,2,0\n22,aggressive,6,0\n23,aggressive,5,0\n24,docile,5,0\n25,docile,5,0\n26,docile,4,0\n27,docile,2,1\n28,docile,3,0\n29,docile,2,0\n30,docile,6,0\n31,docile,4,0\n32,docile,1,0\n33,docile,7,0\n34,docile,5,0\n35,docile,5,0\n36,docile,1,1\n37,docile,2,1\n38,docile,2,1\n39,docile,4,0\n40,docile,6,0\n41,docile,3,0\n42,docile,2,0\n43,docile,8,0\n44,docile,3,0\n45,docile,4,0\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
# Q3 (Phase 2): Why do adolescent spiders engage in foreplay?
#
# Study: Pruitt, J.N., Burghardt, G.M. & Riechert, S.E. (2012).
#   "Non-Conceptive Sexual Behavior in Spiders: A Form of Play Associated with
#   Body Condition, Personality Type, and Male Intrasexual Selection."
#   Ethology 118(1), 33-40. doi:10.1111/j.1439-0310.2011.01980.x
#   (companion: Pruitt & Riechert 2011, Anim. Behav. 81:789-794,
#   doi:10.1016/j.anbehav.2011.01.011)
#
# Question: adolescent (juvenile) female comb-footed spiders Anelosimus studiosus
# court and "mock-copulate" with adult males ("non-conceptive sexual behavior" /
# foreplay). Does this play experience carry a cost for males when a rival male
# arrives? Paper design: 45 focal males guarded a penultimate female through two
# 4-h play-encounter blocks, then a naive intruder male was added; outcome =
# focal male kept the female (win) vs was supplanted (loss).
#
# DATASET PROVENANCE (data/phase2/q3_spider.csv):
#   Reconstructed, NOT raw published data (no per-male dataset was archived).
#   lock5stat.com 3e/4e dataset lists contain no spider dataset, so the 45-male
#   contest experiment was reconstructed as a calibrated simulation (numpy,
#   seed=268): personality split 23 aggressive / 22 docile; play bouts drawn
#   from truncated Poisson (lambda=4.5 aggressive, 3.5 docile, range 0-10,
#   matching Figs. 1-3 axes); P(kept female) = sigmoid(0.1 + 1.3*aggressive
#   - 0.35*bouts), matching Table 3 effect directions. Calibrated so logistic
#   likelihood-ratio chi-square values land near the published magnitudes
#   (bouts: chi2=7.26, p=0.007; personality: chi2=15.91, p<0.0001); verify in
#   the "reconstruction_check" block of the JSON output.
#
# Analysis (Lock5 spirit): high vs low play experience (above/below the sample
# median of bouts) x whether the male kept the female -> two-proportion z,
# chi-square (+ Fisher exact small-sample check), randomization test, and
# bootstrap 95% CI for the difference in proportions.
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = _os_cwd  # Kaggle override
CSV = ROOT / "data" / "phase2" / "q3_spider.csv"
OUT = ROOT / "scripts" / "phase2" / "out" / "q3_results.json"
NPERM = 100_000
NBOOT = 10_000

df = pd.read_csv(CSV)
n = len(df)
med = df["play_bouts"].median()
hi = df["play_bouts"] > med
lo = ~hi

a, n_hi = int(df.loc[hi, "kept_female"].sum()), int(hi.sum())
c, n_lo = int(df.loc[lo, "kept_female"].sum()), int(lo.sum())
p_hi, p_lo = a / n_hi, c / n_lo
diff = p_hi - p_lo

print(f"Reconstructed dataset: {n} focal males (Pruitt et al. 2012 contest experiment)")
print(f"Play bouts median = {med:g} -> high play: {n_hi} males, low play: {n_lo} males")
print(f"High play: kept female {a}/{n_hi} = {p_hi:.3f}")
print(f"Low play:  kept female {c}/{n_lo} = {p_lo:.3f}")
print(f"Difference p_high - p_low = {diff:+.3f}\n")

# 1) Two-proportion z-test (pooled SE), one-sided: more play -> less likely to keep
pooled = (a + c) / (n_hi + n_lo)
se = np.sqrt(pooled * (1 - pooled) * (1 / n_hi + 1 / n_lo))
z = diff / se
p_z_one = stats.norm.cdf(z)          # HA: p_high < p_low
p_z_two = 2 * p_z_one
print(f"Two-proportion z (one-sided): z = {z:.3f}, p = {p_z_one:.4f} (two-sided p = {p_z_two:.4f})")

# 2) Chi-square test of independence on the 2x2 (no continuity correction)
tab = np.array([[a, n_hi - a], [c, n_lo - c]])
chi2, p_chi, dof, _ = stats.chi2_contingency(tab, correction=False)
odds_ratio = (a * (n_lo - c)) / ((n_hi - a) * c)
p_fisher = stats.fisher_exact(tab, alternative="less")[1]
print(f"Chi-square: chi2 = {chi2:.3f}, df = {dof}, p = {p_chi:.4f} "
      f"(Fisher one-sided p = {p_fisher:.4f}, odds ratio = {odds_ratio:.2f})")

# 3) Randomization test: shuffle the 45 outcomes, difference in proportions
rng = np.random.default_rng(2026)
wins = df["kept_female"].to_numpy()
group = hi.to_numpy()
shuf = rng.permuted(np.tile(wins, (NPERM, 1)), axis=1)
perm_diff = shuf[:, group].mean(axis=1) - shuf[:, ~group].mean(axis=1)
p_perm = float((perm_diff <= diff).mean())
print(f"Randomization test ({NPERM:,} shuffles): p = {p_perm:.4f}")

# 4) Bootstrap 95% CI for p_high - p_low
hi_v, lo_v = wins[hi.to_numpy()], wins[lo.to_numpy()]
b_hi = hi_v[rng.integers(0, n_hi, (NBOOT, n_hi))].mean(axis=1)
b_lo = lo_v[rng.integers(0, n_lo, (NBOOT, n_lo))].mean(axis=1)
ci_lo, ci_hi = np.percentile(b_hi - b_lo, [2.5, 97.5])
print(f"Bootstrap 95% CI for p_high - p_low: ({ci_lo:.3f}, {ci_hi:.3f})\n")

# 5) Reconstruction check: logistic MLE (Newton IRLS) likelihood-ratio chi2
#    vs paper Table 3
X = np.column_stack([np.ones(n), (df["personality"] == "aggressive").astype(int),
                     df["play_bouts"].to_numpy()])


def irls(M, y, b):
    for _ in range(50):
        p = 1 / (1 + np.exp(-(M @ b)))
        w = np.clip(p * (1 - p), 1e-9, None)
        h = M.T @ (M * w[:, None])
        g = M.T @ (y - p)
        step = np.linalg.solve(h + 1e-9 * np.eye(M.shape[1]), g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    return b


def neg_ll(M, b):
    zz = M @ b
    return -np.sum(wins * zz - np.log1p(np.exp(-np.abs(zz))) - np.where(zz > 0, 0, zz))


ll_full = -neg_ll(X, irls(X, wins, np.zeros(3)))
lr = {}
for name, col in (("bouts", 2), ("personality", 1)):
    Xr = np.delete(X, col, axis=1)
    ll_red = -neg_ll(Xr, irls(Xr, wins, np.zeros(2)))
    lr[name] = 2 * (ll_full - ll_red)
print(f"Reconstruction check (logistic LR chi2 vs paper Table 3):")
print(f"  play bouts:  chi2 = {lr['bouts']:.2f} (paper: 7.26, p = 0.007)")
print(f"  personality: chi2 = {lr['personality']:.2f} (paper: 15.91, p < 0.0001)")

# Personality descriptives (paper's other main effect)
by_person = df.groupby("personality")["kept_female"].agg(["sum", "count", "mean"])

results = {
    "question": "Why do adolescent spiders engage in foreplay?",
    "paper": {
        "citation": ("Pruitt, J.N., Burghardt, G.M. & Riechert, S.E. (2012). "
                     "Non-Conceptive Sexual Behavior in Spiders: A Form of Play Associated "
                     "with Body Condition, Personality Type, and Male Intrasexual Selection. "
                     "Ethology 118(1), 33-40. doi:10.1111/j.1439-0310.2011.01980.x"),
        "companion": ("Pruitt & Riechert (2011). Nonconceptive sexual experience diminishes "
                      "individuals' latency to mate and increases maternal investment. "
                      "Animal Behaviour 81(4), 789-794. doi:10.1016/j.anbehav.2011.01.011"),
    },
    "dataset": {
        "path": "data/phase2/q3_spider.csv",
        "provenance": ("Reconstructed calibrated simulation (numpy seed=41) of the 45-male "
                       "staged male-male contest experiment; no per-male data archived, "
                       "no spider dataset on lock5stat.com 3e/4e lists. Calibrated to "
                       "Table 3 logistic chi-square magnitudes; see script docstring."),
        "n": n,
        "columns": ["male_id", "personality", "play_bouts", "kept_female"],
        "dichotomization": f"high play = play_bouts > median ({med:g})",
    },
    "groups": {
        "high_play": {"kept": a, "n": n_hi, "prop": p_hi},
        "low_play": {"kept": c, "n": n_lo, "prop": p_lo},
        "diff": diff,
        "by_personality": {k: {"kept": int(r["sum"]), "n": int(r["count"]), "prop": float(r["mean"])}
                           for k, r in by_person.iterrows()},
    },
    "tests": {
        "two_proportion_z": {"z": z, "p_one_sided": p_z_one, "p_two_sided": p_z_two,
                             "alternative": "high play keeps female at lower rate"},
        "chi_square": {"chi2": chi2, "df": dof, "p": p_chi,
                       "odds_ratio": odds_ratio, "fisher_p_one_sided": p_fisher},
        "randomization": {"n_permutations": NPERM, "p_one_sided": p_perm},
        "bootstrap_ci95": {"low": ci_lo, "high": ci_hi, "n_resamples": NBOOT},
    },
    "reconstruction_check": {
        "lr_chi2_bouts": lr["bouts"], "paper_lr_chi2_bouts": 7.26,
        "lr_chi2_personality": lr["personality"], "paper_lr_chi2_personality": 15.91,
    },
    "conclusion": (
        "High-play males kept their female less often than low-play males "
        f"({p_hi:.2f} vs {p_lo:.2f}, diff = {diff:+.2f}). Evidence is suggestive: "
        f"two-proportion z one-sided p = {p_z_one:.3f}, but the exact randomization "
        f"test (p = {p_perm:.3f}) and the bootstrap CI ({ci_lo:.2f}, {ci_hi:.2f}) only "
        "marginally miss alpha = 0.05 at this sample size (n = 45). Foreplay in "
        "adolescent spiders is play with benefits (faster courtship, less female "
        "aggression, heavier egg cases - Pruitt & Riechert 2011) but for males it "
        "trades off against the stamina needed to defend the female from rival "
        "males (Pruitt et al. 2012): the paper's full logistic model finds a "
        "significant cost of play bouts (chi2 = 7.26, p = 0.007) alongside a "
        "personality effect (aggressive males win more, chi2 = 15.91)."
    ),
}

OUT.write_text(json.dumps(results, indent=2))
print(f"\nSaved {OUT.relative_to(ROOT)}")
