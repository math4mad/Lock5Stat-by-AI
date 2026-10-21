# Pheromones analysis: estratetraenol biases gender perception in heterosexual men
# Data: eLife 2021 (Chen et al.) source data, replication of Zhou et al. 2014 (Current Biology)
# Exps 3-5: heterosexual men, within-participant design, NoDrug/saline baseline
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(2026)
xl = pd.ExcelFile("data/raw/elife-59376-fig4-data1-v1.xlsx")
xl4 = pd.ExcelFile("data/raw/elife-59376-fig4-data2-v1.xlsx")

shifts = []
for f, sheet, base in [(xl, "Exp 3-High AQ heterosexual men", "NoDrug"),
                       (xl, "Exp 5-Low AQ heterosexual men", "NoDrug"),
                       (xl4, "Exp 4-High AQ heterosexual men", "SAL")]:
    df = f.parse(sheet)
    s = df[f"{base}.EST.PSE.shift"].dropna().to_numpy()
    shifts.append(pd.DataFrame({"exp": sheet.split("-")[0], "pse_shift": s}))
all_df = pd.concat(shifts, ignore_index=True)
print(all_df.groupby("exp").pse_shift.agg(["count", "mean", "std"]))
print(f"\nPooled: n={len(all_df)}, mean PSE shift = {all_df.pse_shift.mean():.4f} (positive = feminine bias)\n")

# 1) Matched-pairs t-test vs 0 (per experiment and pooled)
for exp, g in all_df.groupby("exp"):
    t, p = stats.ttest_1samp(g.pse_shift, 0, alternative="greater")
    print(f"{exp}: mean shift = {g.pse_shift.mean():+.4f}, t({len(g)-1}) = {t:.2f}, p = {p:.5f}")
t, p_t = stats.ttest_1samp(all_df.pse_shift, 0, alternative="greater")
print(f"Pooled: mean = {all_df.pse_shift.mean():+.4f}, t({len(all_df)-1}) = {t:.2f}, p = {p_t:.6f}\n")

# 2) Permutation (sign-flip) test on pooled
nperm = 100_000
obs = all_df.pse_shift.mean()
s = all_df.pse_shift.to_numpy()
perm = np.array([np.mean(s * rng.choice([-1, 1], len(s))) for _ in range(nperm)])
p_perm = np.mean(perm >= obs)
print(f"Sign-flip permutation test: p = {p_perm:.5f}")

# 3) % participants showing feminine bias (positive shift)
pos = np.mean(s > 0)
k, n = int(np.sum(s > 0)), len(s)
p_bin = stats.binomtest(k, n, 0.5, alternative="greater").pvalue
print(f"Participants biased: {k}/{n} = {pos:.1%}, sign test p = {p_bin:.5f}\n")

# 4) Bootstrap 95% CI of mean shift
boot = np.array([s[rng.integers(0, n, n)].mean() for _ in range(nperm)])
ci = np.percentile(boot, [2.5, 97.5])
print(f"Bootstrap 95% CI for mean PSE shift: ({ci[0]:.4f}, {ci[1]:.4f})")
all_df.to_csv("data/pheromone_pse_shifts.csv", index=False)
np.save("scripts/perm_pher.npy", perm)
np.save("scripts/boot_pher.npy", boot)
pd.DataFrame({"metric": ["t","p_t","p_perm","sign_p","ci_low","ci_high","mean_shift"],
              "value": [t, p_t, p_perm, p_bin, ci[0], ci[1], obs]}).to_csv("analysis_pheromone.csv", index=False)
print("saved analysis_pheromone.csv")
