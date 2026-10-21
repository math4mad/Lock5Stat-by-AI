# Penguin tagging harm analysis (Saraux et al. 2011, Nature)
# 100 king penguins: 50 steel flipper bands vs 50 electronic tags, 10-year survival
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(2026)
df = pd.read_csv("data/penguin_banding_saraux2011.csv")
b_surv, n_b = df.loc[df.group == "Banded", "survived"].iloc[0], df.loc[df.group == "Banded", "n"].iloc[0]
c_surv, n_c = df.loc[df.group == "NonBanded", "survived"].iloc[0], df.loc[df.group == "NonBanded", "n"].iloc[0]
print(f"Banded:   {b_surv}/{n_b} = {b_surv/n_b:.2f} survived")
print(f"NonBanded: {c_surv}/{n_c} = {c_surv/n_c:.2f} survived\n")

# 1) Fisher's exact test
tab = np.array([[b_surv, n_b - b_surv], [c_surv, n_c - c_surv]])
odds, p_f = stats.fisher_exact(tab, alternative="less")
print(f"Fisher exact (one-sided, harm): OR={odds:.3f}, p={p_f:.5f}")

# 2) Two-proportion z
pooled = (b_surv + c_surv) / (n_b + n_c)
se = np.sqrt(pooled * (1 - pooled) * (1/n_b + 1/n_c))
z = (b_surv/n_b - c_surv/n_c) / se
p_z = stats.norm.cdf(z)  # one-sided: banded < non-banded
print(f"Two-proportion z (one-sided): z={z:.3f}, p={p_z:.5f}")

# 3) Permutation test (difference in proportions)
nperm = 100_000
surv_pool = np.array([1]*(b_surv + c_surv) + [0]*(n_b - b_surv + n_c - c_surv))
obs = b_surv/n_b - c_surv/n_c
perm = np.empty(nperm)
for i in range(nperm):
    g = surv_pool[rng.permutation(len(surv_pool))]
    perm[i] = g[:n_b].mean() - g[n_b:].mean()
p_perm = np.mean(perm <= obs)
print(f"Permutation test: p={p_perm:.5f}\n")

# 4) Bootstrap 95% CI for difference (banded - non-banded)
boot = np.empty(nperm)
for i in range(nperm):
    bb = np.random.default_rng(rng.integers(1e9)).choice([1]*b_surv + [0]*(n_b-b_surv), n_b)
    bc = np.random.default_rng(rng.integers(1e9)).choice([1]*c_surv + [0]*(n_c-c_surv), n_c)
    boot[i] = bb.mean() - bc.mean()
ci = np.percentile(boot, [2.5, 97.5])
print(f"Bootstrap 95% CI for p_banded - p_nonbanded: ({ci[0]:.3f}, {ci[1]:.3f})")
np.save("scripts/perm_penguin.npy", perm)
np.save("scripts/boot_penguin.npy", boot)
pd.DataFrame({"metric": ["z","p_z","p_fisher","p_perm","ci_low","ci_high","odds_ratio"],
              "value": [z, p_z, p_f, p_perm, ci[0], ci[1], odds]}).to_csv("analysis_penguin.csv", index=False)
print("saved analysis_penguin.csv")
