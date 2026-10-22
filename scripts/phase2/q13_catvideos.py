#!/usr/bin/env python3
"""Lock5 Phase 2, Q13: "Does watching cat videos improve mood?"

Myrick (2015) surveyed Internet users who watch cat videos/photos online
(final N = 6,795; 88.4% female; snowball sample via Facebook/Twitter and Lil
BUB's channels). Respondents retrospectively rated 24 discrete emotions on
1 ("not at all") to 7 ("very much") scales for how they felt BEFORE and AFTER
their most recent online cat viewing. Paired t-tests (paper Table 2, p. 172):
positive-emotion composite rose 3.99 -> 4.76 (t(6604) = -51.27 for prior -
after), negative-emotion composite fell 2.19 -> 1.46 (t(6593) = 58.95), energy
rose 3.27 -> 3.78 (t(6615) = -30.93) while depletion, anxiety, annoyance,
sadness and guilt all fell (|t| = 26.7 to 78.8, all p < .001). Design caveat:
within-subject retrospective survey comparison, not a randomized experiment.

Citation: Myrick, J. G. (2015). Emotion regulation, procrastination, and
watching cat videos online: Who watches Internet cats, why, and to what
effect? Computers in Human Behavior, 52, 168-176.
https://doi.org/10.1016/j.chb.2015.06.001 Lock5 3e ships no dataset for this
question (checked lock5stat.com/datapage3e.html), so
data/phase2/q13_catvideos.csv reconstructs the published aggregate summary
statistics from paper Table 2 (provenance in the CSV header).

Analysis: paired comparison per data shape. For all 11 scales, an analytic
paired t computed from the published moments (mean change, s_d via pre/post
SDs and correlation) is verified against the published t. For the two primary
composites (positive and negative mood), individual pre/post pairs are
reconstructed from the published moments (seeded bivariate normal, documented)
and analyzed with scipy's paired t, a sign-flip randomization test (H0: the
difference distribution is symmetric about 0) and a percentile bootstrap CI
for the mean change. numpy/scipy/pandas only; seed 2026; 100k replicates.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data" / "phase2" / "q13_catvideos.csv"
OUT = REPO / "scripts" / "phase2" / "out" / "q13_results.json"

rng = np.random.default_rng(2026)
B = 100_000  # randomization / bootstrap iterations
CHUNK = 5_000  # rows per allocation to bound memory (5k x ~6.6k pairs)

df = pd.read_csv(DATA, comment="#")
print("Question: Does watching cat videos improve mood?")
print("Outcome: pre -> post change in self-reported emotions (1-7 scales) around")
print("the most recent online cat video/photo viewing (Myrick 2015, N = 6,795)\n")
print("Reconstructed summary statistics (data/phase2/q13_catvideos.csv, paper Table 2):")
print(df[["variable", "n", "mean_prior", "mean_after", "r_prior_after",
          "t_published"]].to_string(index=False), "\n")

# --- 1) Analytic paired t from published moments (all 11 scales) ------------------
analytic = []
max_dt = 0.0
print("--- Analytic paired t from published moments (change = after - prior)")
for r in df.itertuples():
    n = int(r.n)
    d_bar = r.mean_after - r.mean_prior
    s_d = np.sqrt(r.sd_prior**2 + r.sd_after**2
                  - 2 * r.r_prior_after * r.sd_prior * r.sd_after)
    se = s_d / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, n - 1)
    # Table 2 reports t for prior - after; match that direction for verification
    t_analytic = (r.mean_prior - r.mean_after) / se
    p_t = 2 * stats.t.sf(abs(t_analytic), n - 1)
    dt = t_analytic - r.t_published
    max_dt = max(max_dt, abs(dt))
    analytic.append({
        "variable": r.variable, "label": r.label, "n": n,
        "mean_prior": r.mean_prior, "mean_after": r.mean_after,
        "mean_change": round(d_bar, 3),
        "sd_diff_reconstructed": round(float(s_d), 3),
        "cohens_dz": round(d_bar / s_d, 3),
        "ci95_mean_change": [round(d_bar - t_crit * se, 3),
                             round(d_bar + t_crit * se, 3)],
        "t_analytic_prior_minus_after": round(float(t_analytic), 2),
        "t_published": r.t_published, "delta_t_vs_published": round(float(dt), 2),
        "df": n - 1, "p_two_sided": float(f"{p_t:.2e}"),
    })
    print(f"    {r.variable:<18} n={n}  change={d_bar:+.2f}  t({n - 1})={t_analytic:.2f}"
          f"  (published {r.t_published:+.2f}, d={dt:+.2f})  p<1e-20")
print(f"    max |t_analytic - t_published| = {max_dt:.2f} "
      "(agreement to rounding of the published means/SDs/r)\n")

# --- 2) Reconstructed pairs + full battery on the two primary composites ----------
def reconstruct_pairs(r):
    """Reconstruct n (prior, after) pairs from the published moments via a seeded
    bivariate normal (Cholesky: post = M2 + s2*(r*z1 + sqrt(1-r^2)*z2)). The
    published Table 2 moments, not the simulated microdata, are the source of
    truth; microdata only enable resampling-based inference."""
    z = rng.standard_normal((int(r.n), 2))
    prior = r.mean_prior + r.sd_prior * z[:, 0]
    after = r.mean_after + r.sd_after * (r.r_prior_after * z[:, 0]
                                         + np.sqrt(1 - r.r_prior_after**2) * z[:, 1])
    return prior, after

def battery(r):
    prior, after = reconstruct_pairs(r)
    diff = after - prior
    n = len(diff)
    t_paired, p_paired = stats.ttest_rel(after, prior)  # t for after - prior
    fidelity = {
        "mean_prior": [round(float(prior.mean()), 3), r.mean_prior],
        "mean_after": [round(float(after.mean()), 3), r.mean_after],
        "sd_prior": [round(float(prior.std(ddof=1)), 3), r.sd_prior],
        "sd_after": [round(float(after.std(ddof=1)), 3), r.sd_after],
        "r_prior_after": [round(float(np.corrcoef(prior, after)[0, 1]), 3),
                          r.r_prior_after],
    }
    # Sign-flip randomization: H0 = difference distribution symmetric about 0
    obs = diff.mean()
    null = np.empty(B)
    for i in range(0, B, CHUNK):
        k = min(CHUNK, B - i)
        flips = rng.choice([-1.0, 1.0], size=(k, n))
        null[i:i + k] = (flips * diff).mean(axis=1)
    p_rand = float(np.mean(np.abs(null) >= abs(obs) - 1e-12))
    # Percentile bootstrap CI for the mean change (resample respondents)
    boots = np.empty(B)
    for i in range(0, B, CHUNK):
        k = min(CHUNK, B - i)
        idx = rng.integers(0, n, size=(k, n))
        boots[i:i + k] = diff[idx].mean(axis=1)
    boot_ci = np.percentile(boots, [2.5, 97.5])
    print(f"--- {r.label}: reconstructed pairs (n = {n:,})")
    print(f"    paired t (after - prior): t({n - 1}) = {t_paired:.2f}, "
          f"p = {p_paired:.2e}  [published t = {r.t_published:+.2f} for prior - after]")
    print(f"    mean change = {obs:+.3f} points on 1-7 scale")
    print(f"    sign-flip randomization ({B:,} flips): p = {p_rand:.2e}")
    print(f"    bootstrap 95% CI ({B:,} resamples): ({boot_ci[0]:+.3f}, {boot_ci[1]:+.3f})")
    print(f"    reconstruction fidelity [simulated vs published]: {fidelity}\n")
    return {
        "n": n, "mean_change": round(float(obs), 3),
        "paired_t_after_minus_prior": round(float(t_paired), 2),
        "p_paired_t": float(f"{p_paired:.2e}"),
        "t_published_prior_minus_after": r.t_published,
        "p_signflip_randomization": p_rand,
        "randomization_replicates": B,
        "bootstrap_ci95_mean_change": [round(float(boot_ci[0]), 3),
                                       round(float(boot_ci[1]), 3)],
        "bootstrap_replicates": B,
        "reconstruction_fidelity_simulated_vs_published": fidelity,
    }

print("--- Full battery (paired t + sign-flip randomization + bootstrap) on the")
print("    two primary composites, pairs reconstructed from published moments\n")
pos = battery(df[df.variable == "positive_combined"].iloc[0])
neg = battery(df[df.variable == "negative_combined"].iloc[0])

# --- 3) Conclusion + results JSON ------------------------------------------------
happy = next(a for a in analytic if a["variable"] == "happy")
energy = next(a for a in analytic if a["variable"] == "energetic")
print("Conclusion:")
print("  Yes -- mood improves after watching cat videos. The positive-emotion")
print(f"  composite rose {pos['mean_change']:+.2f} points (3.99 -> 4.76) and the negative-")
print(f"  emotion composite fell {-neg['mean_change']:.2f} points (2.19 -> 1.46); both")
print(f"  nulls are rejected with t ~ 50-60 (df ~ 6,600), sign-flip p < 1e-5, and")
print(f"  bootstrap CIs far from 0. Happiest single emotion: +{happy['mean_change']:.2f}")
print(f"  (4.08 -> 5.22); viewers also felt more energetic (+{energy['mean_change']:.2f})")
print("  and less depleted, anxious, annoyed, sad and guilty (all |t| >= 26.7,")
print("  p < .001). Caveats: retrospective self-report, no control group, and a")
print("  self-selected snowball sample (88.4% female) -- so 'improves mood' is")
print("  supported as a within-person association around real viewing episodes,")
print("  not as a causal effect of an assigned treatment.")

results = {
    "question": "Does watching cat videos improve mood?",
    "outcome": ("Change in self-reported emotions (1 = not at all to 7 = very much) "
                "from before to after the respondent's most recent viewing of online "
                "cat videos and/or photos; positive vs negative emotion composites "
                "plus 7 discrete emotions and 2 arousal measures."),
    "citation": ("Myrick, J. G. (2015). Emotion regulation, procrastination, and "
                 "watching cat videos online: Who watches Internet cats, why, and to "
                 "what effect? Computers in Human Behavior, 52, 168-176. "
                 "https://doi.org/10.1016/j.chb.2015.06.001"),
    "design_note": ("Cross-sectional online survey (Qualtrics, snowball via "
                    "Facebook/Twitter and Lil BUB's channels), final N = 6,795 "
                    "(11,083 began, 6,827 completed, 32 removed); 88.4% female; mean "
                    "age 38.74. Retrospective within-subject pre/post comparison, not "
                    "a randomized experiment."),
    "dataset": {
        "path": "data/phase2/q13_catvideos.csv",
        "note": ("Lock5 3e ships no dataset for this question (checked "
                 "lock5stat.com/datapage3e.html). The CSV reconstructs the published "
                 "aggregate summary statistics from paper Table 2 (p. 172) -- not raw "
                 "respondent records; provenance in CSV header comments."),
    },
    "methods": {
        "analytic": ("Paired t from published moments: d_bar = M_after - M_prior, "
                     "s_d = sqrt(s1^2 + s2^2 - 2*r*s1*s2); verified against the "
                     "published Table 2 t values (max |delta t| = "
                     + f"{max_dt:.2f}" + ")."),
        "simulation": ("For the two composites, (prior, after) pairs reconstructed "
                       "from the published moments via seeded bivariate normal, then "
                       "scipy paired t + sign-flip randomization + percentile "
                       "bootstrap CI for the mean change."),
        "seed": 2026, "replicates": B,
    },
    "analytic_paired_t_all_scales": analytic,
    "simulation_battery": {
        "positive_emotions_composite": pos,
        "negative_emotions_composite": neg,
    },
    "conclusion": (
        "Mood improves after watching cat videos: positive-emotion composite "
        "3.99 -> 4.76 (+0.77, t(6604) = 51.3, sign-flip p < 1e-5, bootstrap CI "
        f"[{pos['bootstrap_ci95_mean_change'][0]:+.2f}, "
        f"{pos['bootstrap_ci95_mean_change'][1]:+.2f}]) and negative-emotion "
        "composite 2.19 -> 1.46 (-0.73, t(6593) = 59.0, sign-flip p < 1e-5, "
        f"bootstrap CI [{neg['bootstrap_ci95_mean_change'][0]:+.2f}, "
        f"{neg['bootstrap_ci95_mean_change'][1]:+.2f}]). All 7 discrete emotions "
        "move in the mood-beneficial direction (|t| = 26.7-78.8, p < .001); energy "
        "rises (+0.51) and depletion falls (-1.38). Retrospective self-report, no "
        "control group, self-selected snowball sample (88.4% female): supported as "
        "a within-person association, not a causal effect."
    ),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, indent=2) + "\n")
print(f"\nSaved results to {OUT}")
