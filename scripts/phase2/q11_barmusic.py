#!/usr/bin/env python3
"""Lock5 Phase 2, Q11: "Does turning up the music in a bar cause people to drink more beer?"

Gueguen, N., Jacob, C., Le Guellec, H., Morineau, T., & Lourel, M. (2008), "Sound level
of environmental music and drinking behavior: A field experiment with beer drinkers",
Alcoholism: Clinical and Experimental Research, 32(10), 1795-1798
(DOI 10.1111/j.1530-0277.2008.00764.x). Naturalistic field experiment: 40 male beer
drinkers (18-25) observed in 2 bars in western France over 3 Saturday nights; the
bars' usual top-40 music was randomly set to the normal level (72 dB) or a high level
(88 dB). Published headline results: loud music increased the mean number of drinks
ordered (2.6 -> 3.4 glasses) and cut the mean time to drink a glass (14.51 -> 11.45
min, ~3 min faster); both differences significant.

Lock5 3e ships no dataset for this question (checked lock5stat.com/datapage3e.html;
only "beer" match is PumpkinBeer, unrelated), so data/phase2/q11_barmusic.csv holds a
documented reconstruction from the published group means: balanced 20/20 assignment
assumed; per-patron values reproduce the published condition means exactly (2.6 / 3.4
glasses; 14.51 / 11.45 min) while per-patron spread is a documented assumption
(provenance in the CSV header).

Analysis: two-mean comparisons (glasses consumed; time per glass) of high vs normal
music with Welch t (+ normal-approximation z), randomization tests (100k label
permutations) and bootstrap CIs for the difference in means (100k resamples).
numpy/scipy/pandas only; seed 2026; 100k replicates.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data" / "phase2" / "q11_barmusic.csv"
OUT = REPO / "scripts" / "phase2" / "out" / "q11_results.json"

CONDITION_LABEL = {
    "normal_72db": "Normal music (72 dB)",
    "high_88db": "High-volume music (88 dB)",
}
PUBLISHED_MEANS = {"glasses": {"normal_72db": 2.6, "high_88db": 3.4},
                   "time_per_glass_min": {"normal_72db": 14.51, "high_88db": 11.45}}

rng = np.random.default_rng(2026)
B = 100_000  # bootstrap / randomization iterations

df = pd.read_csv(DATA, comment="#")
groups = {c: df.loc[df["condition"] == c] for c in CONDITION_LABEL}
print("Question: Does turning up the music in a bar cause people to drink more beer?")
print("Outcome: beer glasses ordered and time to drink a glass, by music volume\n")
print("Reconstructed per-patron data (data/phase2/q11_barmusic.csv):")
print(df.groupby("condition")[["glasses", "time_per_glass_min"]]
      .agg(["count", "mean", "std"]), "\n")

# Sanity: reconstruction reproduces the published condition means exactly.
for col, targets in PUBLISHED_MEANS.items():
    for cond, target in targets.items():
        m = groups[cond][col].mean()
        assert np.isclose(m, target, atol=1e-6), f"{cond} {col}: {m} != {target}"


def two_mean(col, larger_means_more):
    """Two-sample comparison of high vs normal music on outcome `col`.

    diff = high - normal. `larger_means_more` says whether larger values mean more
    drinking (glasses: yes; time per glass: no), used only for prose direction.
    """
    x_a = groups["high_88db"][col].to_numpy(float)
    x_n = groups["normal_72db"][col].to_numpy(float)
    n_a, n_n = x_a.size, x_n.size
    ma, mn = x_a.mean(), x_n.mean()
    sa, sn = x_a.std(ddof=1), x_n.std(ddof=1)
    diff = ma - mn
    se_unpooled = np.sqrt(sa**2 / n_a + sn**2 / n_n)

    # Welch two-sample t + normal-approximation z
    welch = stats.ttest_ind(x_a, x_n, equal_var=False)
    df_welch = (sa**2 / n_a + sn**2 / n_n)**2 / \
        ((sa**2 / n_a)**2 / (n_a - 1) + (sn**2 / n_n)**2 / (n_n - 1))
    z = diff / se_unpooled
    p_z = 2 * stats.norm.sf(abs(z))

    # Randomization test: permute condition labels (all 40 patrons pooled)
    x_all = np.concatenate([x_a, x_n])
    r = rng.random((B, x_all.size))
    perm = np.argsort(r, axis=1)
    perm_diff = x_all[perm[:, :n_a]].mean(axis=1) - x_all[perm[:, n_a:]].mean(axis=1)
    p_rand = np.mean(np.abs(perm_diff) >= abs(diff) - 1e-12)

    # Bootstrap CI for the difference in means (resample each group separately)
    boot_a = rng.choice(x_a, (B, n_a), replace=True).mean(axis=1)
    boot_n = rng.choice(x_n, (B, n_n), replace=True).mean(axis=1)
    boot_ci = np.percentile(boot_a - boot_n, [2.5, 97.5])

    direction = "more" if (diff > 0) == larger_means_more else "less"
    res = {
        "outcome": col,
        "high_88db": {"n": int(n_a), "mean": round(ma, 4), "sd": round(sa, 4)},
        "normal_72db": {"n": int(n_n), "mean": round(mn, 4), "sd": round(sn, 4)},
        "diff_high_minus_normal": round(diff, 4),
        "se_unpooled": round(se_unpooled, 4),
        "welch_t": round(float(welch.statistic), 3),
        "welch_df": round(float(df_welch), 1),
        "p_welch": float(f"{welch.pvalue:.3e}"),
        "z_normal": round(float(z), 3),
        "p_normal": float(f"{p_z:.3e}"),
        "p_randomization": float(f"{p_rand:.3e}"),
        "bootstrap_ci95_diff": [round(boot_ci[0], 4), round(boot_ci[1], 4)],
        "direction": f"high-volume patrons drank {direction} ({col})",
    }
    print(f"--- {col}: {CONDITION_LABEL['high_88db']} (mean {ma:.2f}, SD {sa:.2f}) vs "
          f"{CONDITION_LABEL['normal_72db']} (mean {mn:.2f}, SD {sn:.2f})")
    print(f"    diff (high - normal) = {diff:+.2f}; SE = {se_unpooled:.3f}")
    print(f"    Welch t={welch.statistic:.2f} (df={df_welch:.1f}), p={welch.pvalue:.2e}; "
          f"z={z:.2f}, normal p={p_z:.2e}")
    print(f"    randomization p={p_rand:.2e} ({B} label permutations)")
    print(f"    95% bootstrap CI for diff: ({boot_ci[0]:.2f}, {boot_ci[1]:.2f})\n")
    return res


print("--- Two-mean comparisons (high 88 dB minus normal 72 dB)")
glasses = two_mean("glasses", larger_means_more=True)
time = two_mean("time_per_glass_min", larger_means_more=False)

print("Conclusion:")
print("  Because patrons were randomly assigned to sound levels, this field experiment")
print("  supports a causal claim: turning up the music made young male beer drinkers")
print(f"  drink MORE -- {glasses['normal_72db']['mean']:.1f} -> "
      f"{glasses['high_88db']['mean']:.1f} glasses on average "
      f"(+{glasses['diff_high_minus_normal']:.1f}, 95% bootstrap CI "
      f"{glasses['bootstrap_ci95_diff'][0]:+.2f} to {glasses['bootstrap_ci95_diff'][1]:+.2f},")
print(f"  Welch t={glasses['welch_t']:.2f}, randomization p={glasses['p_randomization']:.3f};")
print(f"  note exact randomization p is 1/{B} at best) -- and FASTER: time per glass fell")
print(f"  from {time['normal_72db']['mean']:.2f} to {time['high_88db']['mean']:.2f} min "
      f"({time['diff_high_minus_normal']:.2f} min, 95% bootstrap CI "
      f"{time['bootstrap_ci95_diff'][0]:+.2f} to {time['bootstrap_ci95_diff'][1]:+.2f},")
print(f"  Welch t={time['welch_t']:.2f}, randomization p={time['p_randomization']:.3f}).")
print("  Caveats: young men (18-25) in 2 French bars only; per-patron spread in the")
print("  reconstruction is a documented assumption (published group means reproduced")
print("  exactly), so test statistics illustrate the method rather than replicate the")
print("  paper's own inferential statistics, which also found both differences significant.")

results = {
    "question": "Does turning up the music in a bar cause people to drink more beer?",
    "outcome": ("Beer consumption per patron: number of glasses ordered and mean time "
                "to drink a glass, under high-volume (88 dB) vs normal (72 dB) bar music."),
    "citation": (
        "Gueguen, N., Jacob, C., Le Guellec, H., Morineau, T., & Lourel, M. (2008), "
        "'Sound level of environmental music and drinking behavior: A field experiment "
        "with beer drinkers', Alcoholism: Clinical and Experimental Research, 32(10), "
        "1795-1798. DOI 10.1111/j.1530-0277.2008.00764.x."
    ),
    "design": ("Naturalistic field experiment: 40 male beer drinkers (18-25) observed in "
               "2 bars in western France over 3 Saturday nights; music volume randomly "
               "set to 72 dB (normal) or 88 dB (high)."),
    "dataset": {
        "path": "data/phase2/q11_barmusic.csv",
        "note": ("Lock5 3e ships no dataset for this question (checked "
                 "lock5stat.com/datapage3e.html; only 'beer' match is PumpkinBeer). CSV "
                 "is a documented reconstruction of per-patron data from the published "
                 "group means (2.6 vs 3.4 glasses; 14.51 vs 11.45 min per glass, via the "
                 "paper abstract and Reuters/HealthDay/Daily Star coverage); balanced "
                 "20/20 assignment assumed; per-patron spread is a documented "
                 "assumption -- provenance in the CSV header."),
    },
    "two_mean": {
        "glasses_consumed": glasses,
        "time_per_glass_min": time,
    },
    "conclusion": (
        "With random assignment of patrons to sound levels, the experiment supports a "
        "causal conclusion: louder music made patrons drink more and faster. Mean "
        "glasses ordered rose from 2.6 (72 dB) to 3.4 (88 dB), diff +0.8 (95% "
        f"bootstrap CI {glasses['bootstrap_ci95_diff'][0]:+.2f} to "
        f"{glasses['bootstrap_ci95_diff'][1]:+.2f}; Welch t={glasses['welch_t']:.2f}, "
        f"p={glasses['p_welch']:.2e}); mean time per glass fell from 14.51 to 11.45 min, "
        f"diff {time['diff_high_minus_normal']:.2f} min (95% bootstrap CI "
        f"{time['bootstrap_ci95_diff'][0]:+.2f} to {time['bootstrap_ci95_diff'][1]:+.2f}; "
        f"Welch t={time['welch_t']:.2f}, p={time['p_welch']:.2e}). Randomization tests "
        "(100k label permutations) agree. Caveats: young male patrons in 2 French bars "
        "only; reconstructed spread assumed (documented)."
    ),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, indent=2) + "\n")
print(f"\nSaved results to {OUT}")
