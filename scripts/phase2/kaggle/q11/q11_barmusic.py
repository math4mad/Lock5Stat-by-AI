# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q11_barmusic.csv").write_text('# data/phase2/q11_barmusic.csv\n# Lock5 Phase 2, Q11: "Does turning up the music in a bar cause people to drink more beer?"\n#\n# Citation: Gueguen, N., Jacob, C., Le Guellec, H., Morineau, T., & Lourel, M. (2008),\n#   "Sound level of environmental music and drinking behavior: A field experiment with\n#   beer drinkers", Alcoholism: Clinical and Experimental Research, 32(10), 1795-1798.\n#   DOI 10.1111/j.1530-0277.2008.00764.x.\n#\n# Design (naturalistic field experiment): 40 male beer drinkers (aged 18-25) observed\n#   in 2 bars in western France over 3 Saturday nights; the bars\' usual top-40 music\n#   was randomly set to the normal level (72 dB) or a high level (88 dB). Outcomes\n#   observed per patron: number of beer glasses ordered and time spent drinking a glass.\n#\n# Published headline results (paper abstract; Reuters / HealthDay / Daily Star\n#   coverage of the July 2008 study): loud music increased the mean number of drinks\n#   ordered, 2.6 -> 3.4 glasses, and cut the mean time to drink a glass,\n#   14.51 -> 11.45 minutes (about 3 minutes faster). Both differences significant.\n#\n# Lock5 3e ships no dataset for this question (checked lock5stat.com/datapage3e.html;\n#   the only "beer" match there is PumpkinBeer, unrelated to this study).\n#\n# No public microdata exists for this study. Rows below are a documented\n#   reconstruction from the published group means:\n#   - n = 20 patrons per condition: the 40 patrons were randomly assigned to the two\n#     sound levels; the exact split is not published, so a balanced 20/20 split is\n#     assumed (documented assumption).\n#   - glasses (integer counts) and time_per_glass_min (minutes) are reconstructed to\n#     reproduce the published condition means exactly (normal: 2.6 glasses and\n#     14.51 min; high: 3.4 glasses and 11.45 min).\n#   - Per-patron spread is NOT published. The reconstructed SDs (glasses ~0.82 vs\n#     ~0.88; time ~2.3 vs ~1.5 min) are documented assumptions chosen to be plausible\n#     for bar patrons. Test statistics below therefore illustrate the Lock5 method on\n#     the published means rather than exactly reproducing the paper\'s inferential\n#     statistics (the paper reports significant differences in both outcomes).\n#\n# Columns: condition = sound-level condition (normal_72db / high_88db);\n#          patron = patron index within condition;\n#          glasses = number of beer glasses ordered during the observation;\n#          time_per_glass_min = average minutes the patron took to drink one glass.\ncondition,patron,glasses,time_per_glass_min\nnormal_72db,1,2,11.25\nnormal_72db,2,3,12.40\nnormal_72db,3,2,13.10\nnormal_72db,4,4,14.85\nnormal_72db,5,1,16.20\nnormal_72db,6,3,10.75\nnormal_72db,7,2,12.95\nnormal_72db,8,2,14.50\nnormal_72db,9,3,15.75\nnormal_72db,10,3,17.30\nnormal_72db,11,2,13.60\nnormal_72db,12,2,11.90\nnormal_72db,13,3,15.10\nnormal_72db,14,4,16.85\nnormal_72db,15,2,12.55\nnormal_72db,16,3,14.20\nnormal_72db,17,2,18.40\nnormal_72db,18,3,13.35\nnormal_72db,19,2,15.95\nnormal_72db,20,4,19.25\nhigh_88db,1,3,8.90\nhigh_88db,2,4,10.25\nhigh_88db,3,3,11.80\nhigh_88db,4,5,12.45\nhigh_88db,5,2,9.60\nhigh_88db,6,4,11.15\nhigh_88db,7,3,12.90\nhigh_88db,8,3,10.50\nhigh_88db,9,4,13.25\nhigh_88db,10,4,11.70\nhigh_88db,11,3,9.85\nhigh_88db,12,3,12.10\nhigh_88db,13,4,10.85\nhigh_88db,14,5,13.70\nhigh_88db,15,2,11.40\nhigh_88db,16,3,9.30\nhigh_88db,17,3,12.65\nhigh_88db,18,4,10.15\nhigh_88db,19,2,12.35\nhigh_88db,20,4,14.15\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
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

REPO = _os_cwd  # Kaggle override
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
