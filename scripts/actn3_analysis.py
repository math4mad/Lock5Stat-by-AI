# Is there a "sprinting gene"? — ACTN3 R577X analysis (Yang et al. 2003)
# Sprint vs Control genotype contingency table analysis
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(2026)
df = pd.read_csv("data/actn3_yang2003.csv")
print(df, "\n")

genotypes = ["RR", "RX", "XX"]
# --- Contingency tables ---
# Sprint vs Control (2 x 3)
tab = df.set_index("group").loc[["Sprint", "Control"]][genotypes].to_numpy()
print("Sprint vs Control table:\n", tab, "\n")

# 1) Chi-square test of homogeneity
chi2, p, dof, exp = stats.chi2_contingency(tab)
print(f"Chi-square: chi2={chi2:.3f}, df={dof}, p-value={p:.5f}")
print("Expected counts:\n", np.round(exp, 1), "\n")

# 2) Permutation test (chi-square statistic) — Lock5 randomization approach
obs_chi2 = chi2
counts_geno = tab.sum(axis=0)
nperm = 100_000
perm_stats = np.empty(nperm)
geno_vec = np.concatenate([np.repeat("RR", counts_geno[0]),
                           np.repeat("RX", counts_geno[1]),
                           np.repeat("XX", counts_geno[2])])
lab_vec = np.array(["Sprint"] * tab[0].sum() + ["Control"] * tab[1].sum())
for i in range(nperm):
    g = geno_vec[rng.permutation(len(geno_vec))]
    ct = np.zeros((2, 3), dtype=int)
    for gi, geno in enumerate(genotypes):
        ct[0, gi] = np.sum(g[lab_vec == "Sprint"] == geno)
        ct[1, gi] = np.sum(g[lab_vec == "Control"] == geno)
    perm_stats[i] = stats.chi2_contingency(ct)[0]
p_perm = np.mean(perm_stats >= obs_chi2)
print(f"Permutation test: p-value = {p_perm:.5f} ({nperm} shuffles)\n")

# 3) Two-proportion comparison: proportion XX genotype
xx_s, n_s = tab[0, 2], tab[0].sum()
xx_c, n_c = tab[1, 2], tab[1].sum()
p_s, p_c = xx_s / n_s, xx_c / n_c
pooled = (xx_s + xx_c) / (n_s + n_c)
se = np.sqrt(pooled * (1 - pooled) * (1 / n_s + 1 / n_c))
z = (p_s - p_c) / se
p_z = 2 * stats.norm.sf(abs(z))
print(f"XX genotype: sprinters {xx_s}/{n_s} = {p_s:.3f} vs controls {xx_c}/{n_c} = {p_c:.3f}")
print(f"Two-proportion z: z={z:.3f}, p-value={p_z:.5f}\n")

# 4) Bootstrap 95% CI for difference in R-allele proportion
r_s = (2 * tab[0, 0] + tab[0, 1]) / (2 * n_s)
r_c = (2 * tab[1, 0] + tab[1, 1]) / (2 * n_c)
print(f"R-allele frequency: sprinters {r_s:.3f} vs controls {r_c:.3f}")
boot = np.empty(nperm)
sprint_alleles = np.array([1] * (2 * tab[0, 0] + tab[0, 1]) + [0] * (2 * tab[0, 2] + tab[0, 1]))
ctrl_alleles = np.array([1] * (2 * tab[1, 0] + tab[1, 1]) + [0] * (2 * tab[1, 2] + tab[1, 1]))
for i in range(nperm):
    bs = sprint_alleles[rng.integers(0, len(sprint_alleles), len(sprint_alleles))]
    bc = ctrl_alleles[rng.integers(0, len(ctrl_alleles), len(ctrl_alleles))]
    boot[i] = bs.mean() - bc.mean()
ci = np.percentile(boot, [2.5, 97.5])
print(f"Bootstrap 95% CI for pR(sprint) - pR(control): ({ci[0]:.3f}, {ci[1]:.3f})\n")

# 5) Endurance group for contrast
tab3 = df[genotypes].to_numpy()
chi3, p3, dof3, _ = stats.chi2_contingency(tab3)
print(f"3-group chi-square: chi2={chi3:.3f}, df={dof3}, p-value={p3:.6f}")

results = pd.DataFrame({
    "metric": ["chi2 (Sprint vs Control)", "p (chi-square)", "p (permutation)",
               "p (two-proportion XX)", "CI low (R allele diff)", "CI high (R allele diff)"],
    "value": [chi2, p, p_perm, p_z, ci[0], ci[1]]
})
results.to_csv("analysis_results.csv", index=False)
print("\nsaved analysis_results.csv")
