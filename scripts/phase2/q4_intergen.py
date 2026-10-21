"""Phase 2, Q4: How broadly do experiences of parents affect their future children?

Lock5 source
------------
"Statistics: Unlocking the Power of Data" (Lock5), 3rd ed., poses the chapter question
"How broadly do experiences of parents affect their future children?" and treats it in
Ex. 1.17 "Trans-Generational Effects of Diet": male rats fed a high-fat diet (43% of
calories from fat) fathered daughters that showed early metabolic disease, even though
the daughters themselves ate a normal diet.

Study
-----
Ng, S.-F., Lin, R.C.Y., Laybutt, D.R., Barres, R., Owens, J.A. & Morris, M.J. (2010).
"Chronic high-fat diet in fathers programs beta-cell dysfunction in female rat offspring."
Nature 467(7318), 963-966. doi:10.1038/nature09491

Design: controlled exposure experiment in the founder generation - male Sprague-Dawley
rats on a high-fat diet (HFD, ~43% kcal fat) or control diet, then mated to chow-fed
females. All F1 female offspring were weaned onto the same control diet, so group
differences in the daughters are attributable to the fathers' pre-conception diet
(non-genetic intergenerational transmission). Offspring followed to 12 weeks.

Dataset
-------
No Lock5 dataset exists for this study (checked https://lock5stat.com/datapage3e.html),
so data/phase2/q4_intergen.csv is a documented reconstruction: individual-level values
drawn with a fixed seed and then exactly rescaled so that every group's sample mean and
SD match the published summaries (mean +/- s.e.m., n; SD = s.e.m. * sqrt(n)) reported by
Ng et al. (2010). It reproduces the paper's group-level inference; for education only.

Analyses (numpy / scipy / pandas only)
--------------------------------------
1. Fathers (manipulation check): HOMA-IR, body weight, fasting glucose/insulin -
   Welch two-sample t, randomization test on the difference in means, bootstrap 95% CI.
2. Female offspring (primary): insulinogenic index (glucose-stimulated insulin
   secretion, halved in daughters of HFD fathers), 6-week glucose peak, insulin peak -
   same test battery; day-1 and 12-week body weight as null-comparison outcomes.
3. Offspring islet gene-expression counts (paper: 77 islet genes altered at P < 0.001,
   21 up / 56 down): two-proportion z and chi-square goodness-of-fit vs 50/50 plus
   binomial bootstrap CI.

Output: scripts/phase2/out/q4_results.json + readable console summary.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parents[2]
CSV_PATH = BASE / "data" / "phase2" / "q4_intergen.csv"
OUT_JSON = BASE / "scripts" / "phase2" / "out" / "q4_results.json"

SEED = 2026
NPERM = 100_000
NBOOT = 10_000

# Published group summaries (Ng et al. 2010): variable -> group -> (mean, sem, n).
PUBLISHED = {
    "father": {
        "body_weight_g": {"Control": (550.0, 13.0, 8), "HighFat": (705.0, 17.0, 9)},
        "fasting_glucose_mM": {"Control": (4.71, 0.08, 8), "HighFat": (5.43, 0.16, 9)},
        "fasting_insulin_ng_ml": {"Control": (0.18, 0.02, 8), "HighFat": (0.47, 0.07, 9)},
        "homa_ir": {"Control": (0.88, 0.11, 8), "HighFat": (2.29, 0.18, 9)},
    },
    "offspring": {
        "day1_weight_g": {"Control": (7.08, 0.26, 8), "HighFat": (6.61, 0.15, 9)},
        "body_weight_12wk_g": {"Control": (253.0, 8.0, 8), "HighFat": (260.0, 5.0, 9)},
        "glucose_peak_6wk_mM": {"Control": (12.3, 0.4, 8), "HighFat": (13.6, 0.3, 8)},
        "insulin_peak_6wk_ng_ml": {"Control": (2.7, 0.4, 8), "HighFat": (1.4, 0.3, 8)},
        "insulinogenic_index": {"Control": (86.8, 7.3, 8), "HighFat": (38.7, 5.8, 8)},
    },
}
GTT_6WK = ("glucose_peak_6wk_mM", "insulin_peak_6wk_ng_ml", "insulinogenic_index")
PAPER_P = {  # p values reported by Ng et al. 2010 for the same comparisons
    ("father", "body_weight_g"): "<0.0005", ("father", "fasting_glucose_mM"): "0.002",
    ("father", "fasting_insulin_ng_ml"): "0.002", ("father", "homa_ir"): "<0.0005",
    ("offspring", "day1_weight_g"): "0.07", ("offspring", "body_weight_12wk_g"): "0.92",
    ("offspring", "glucose_peak_6wk_mM"): "0.043",
    ("offspring", "insulin_peak_6wk_ng_ml"): "0.016",
    ("offspring", "insulinogenic_index"): "0.004",
}

# Offspring islet gene-expression counts (paper text, independent units = genes):
# 77 genes altered at P < 0.001 in daughters of HFD fathers; 21 up, 56 down.
GENES_TOTAL, GENES_UP, GENES_DOWN = 77, 21, 56

CITE = ("Ng, S.-F., Lin, R.C.Y., Laybutt, D.R., Barres, R., Owens, J.A. & Morris, M.J. (2010). "
        "Chronic high-fat diet in fathers programs beta-cell dysfunction in female rat offspring. "
        "Nature 467(7318), 963-966. doi:10.1038/nature09491")


def reconstruct(rng: np.random.Generator, mean: float, sem: float, n: int) -> np.ndarray:
    """n values whose sample mean and SD exactly equal the published group mean and SD."""
    x = rng.standard_normal(n)
    x = (x - x.mean()) / x.std(ddof=1)
    return mean + sem * np.sqrt(n) * x


def build_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    for cohort in ("father", "offspring"):
        for group, n in (("Control", 8), ("HighFat", 9)):
            tag = "C" if group == "Control" else "H"
            for i in range(1, n + 1):
                rows.append({"cohort": cohort, "father_diet": group,
                             "rat_id": f"{cohort[0].upper()}-{tag}{i:02d}"})
    df = pd.DataFrame(rows)
    for cohort, feats in PUBLISHED.items():
        for col, spec in feats.items():
            for group in ("Control", "HighFat"):
                mean, sem, n = spec[group]
                vals = reconstruct(rng, mean, sem, n)
                sub = df[(df.cohort == cohort) & (df.father_diet == group)]
                idx = sub.index[:n]  # 6-week GTT run on n = 8 per group (Fig. 2d,e)
                df.loc[idx, col] = vals
    return df


def verify_reconstruction(df: pd.DataFrame) -> None:
    for cohort, feats in PUBLISHED.items():
        for col, spec in feats.items():
            for group, (mean, sem, n) in spec.items():
                vals = df[(df.cohort == cohort) & (df.father_diet == group)][col].dropna()
                assert len(vals) == n, f"{col}/{group}: n={len(vals)} != {n}"
                assert np.isclose(vals.mean(), mean, rtol=1e-8), f"{col}/{group} mean"
                assert np.isclose(vals.std(ddof=1), sem * np.sqrt(n), rtol=1e-8), f"{col}/{group} sd"


def two_group(x: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> dict:
    """x = Control, y = HighFat; tests diff = mean(x) - mean(y) (positive => Control higher)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    nx, ny = len(x), len(y)
    diff = x.mean() - y.mean()
    t, p_two = stats.ttest_ind(x, y, equal_var=False)
    p_greater = stats.ttest_ind(x, y, equal_var=False, alternative="greater").pvalue
    p_less = stats.ttest_ind(x, y, equal_var=False, alternative="less").pvalue
    pooled = np.concatenate([x, y])
    total = pooled.sum()
    labels = np.argsort(rng.random((NPERM, nx + ny)), axis=1)[:, :nx]
    perm_x = pooled[labels].mean(axis=1)
    perm_diff = perm_x - (total - perm_x * nx) / ny
    p_rand_two = float(np.mean(np.abs(perm_diff) >= abs(diff)))
    p_rand_greater = float(np.mean(perm_diff >= diff))
    boot = (x[rng.integers(0, nx, (NBOOT, nx))].mean(axis=1)
            - y[rng.integers(0, ny, (NBOOT, ny))].mean(axis=1))
    ci = np.percentile(boot, [2.5, 97.5])
    sp = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2))
    return {
        "n_control": nx, "n_highfat": ny,
        "mean_control": float(x.mean()), "mean_highfat": float(y.mean()),
        "diff_control_minus_highfat": float(diff),
        "cohens_d": float(diff / sp),
        "welch_t": float(t), "welch_df": float((x.var(ddof=1)/nx + y.var(ddof=1)/ny) ** 2 /
                                              ((x.var(ddof=1)/nx) ** 2 / (nx - 1) + (y.var(ddof=1)/ny) ** 2 / (ny - 1))),
        "p_welch_two_sided": float(p_two), "p_welch_greater": float(p_greater),
        "p_welch_less": float(p_less),
        "p_randomization_two_sided": p_rand_two, "p_randomization_greater": p_rand_greater,
        "bootstrap95CI_diff": [float(ci[0]), float(ci[1])],
    }


def gene_counts(rng: np.random.Generator) -> dict:
    n, k = GENES_TOTAL, GENES_DOWN
    p_hat = k / n
    z = (p_hat - 0.5) / np.sqrt(0.25 / n)
    boots = rng.binomial(n, p_hat, NBOOT) / n
    lo, hi = np.percentile(boots, [2.5, 97.5])
    chi2, p_chi = stats.chisquare([GENES_UP, k])
    return {
        "source": "Ng et al. 2010, islet microarray of female offspring: 77 genes altered (P < 0.001)",
        "n_genes": n, "n_upregulated": GENES_UP, "n_downregulated": k,
        "prop_downregulated": float(p_hat),
        "two_prop_z_vs_50pct": float(z), "p_two_prop_z_two_sided": float(2 * stats.norm.sf(abs(z))),
        "chi_square_gof": float(chi2), "p_chi_square_gof": float(p_chi),
        "p_binomial_two_sided": float(stats.binomtest(k, n, 0.5).pvalue),
        "bootstrap95CI_prop_down": [float(lo), float(hi)],
    }


def main() -> None:
    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)
    else:
        df = build_dataset()
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CSV_PATH, index=False)
        print(f"[built] reconstructed dataset -> {CSV_PATH}")
    verify_reconstruction(df)
    rng = np.random.default_rng(SEED + 1)

    def group_vals(cohort: str, col: str):
        sub = df[df.cohort == cohort]
        return (sub[sub.father_diet == "Control"][col].dropna().to_numpy(),
                sub[sub.father_diet == "HighFat"][col].dropna().to_numpy())

    fathers, offspring = {}, {}
    for cohort, store in (("father", fathers), ("offspring", offspring)):
        for col in PUBLISHED[cohort]:
            x, y = group_vals(cohort, col)
            res = two_group(x, y, rng)
            res["paper_reported_p"] = PAPER_P[(cohort, col)]
            res["label"] = PUBLISHED[cohort][col]
            store[col] = res

    genes = gene_counts(rng)
    ii = offspring["insulinogenic_index"]
    gp = offspring["glucose_peak_6wk_mM"]
    results = {
        "question": "How broadly do experiences of parents affect their future children?",
        "lock5_reference": ("Statistics: Unlocking the Power of Data (Lock5), 3rd ed., "
                            "Ex. 1.17 'Trans-Generational Effects of Diet'"),
        "study": {
            "citation": CITE,
            "design": ("Controlled experiment: founder male rats randomized to high-fat vs control "
                       "diet, mated to chow-fed females; all F1 daughters weaned onto control diet, "
                       "outcomes at 6-12 weeks (quasi-experimental intergenerational design)."),
        },
        "dataset": {
            "path": str(CSV_PATH),
            "n_rows": int(len(df)),
            "provenance": ("No Lock5 dataset exists for this study (lock5stat.com/datapage3e.html "
                           "checked). Individual-level reconstruction of Ng et al. 2010 group "
                           "summaries (mean +/- s.e.m., n), seeded (rng seed 2026) and exactly "
                           "rescaled to published group mean/SD; education use only."),
            "columns": {"cohort": "father | offspring", "father_diet": "Control | HighFat",
                        "rat_id": "animal identifier",
                        "glucose_peak_6wk_mM/insulin_peak_6wk_ng_ml/insulinogenic_index":
                            "6-week glucose tolerance test, n=8 per group (Fig. 2d,e)"},
        },
        "published_group_summaries": PUBLISHED,
        "fathers_manipulation_check": fathers,
        "offspring_outcomes": offspring,
        "offspring_islet_gene_expression_counts": genes,
        "offspring_islet_morphology_descriptive": {
            "source": "Ng et al. 2010 Table 1 (n = 7 pancreases per group)",
            "total_islet_area_pct": {"Control": 1.17, "HighFat": 0.90, "paper_p": "0.040"},
            "pct_large_islets": {"Control": 18.14, "HighFat": 14.84, "paper_p": "0.031"},
            "pct_small_islets": {"Control": 71.81, "HighFat": 76.08, "paper_p": "0.034"},
            "note": ("paper tests compare animals (n=7/group); islet-level counts would be "
                     "pseudoreplicated, so no islet-level chi-square is reported"),
        },
        "conclusion": (
            "Fathers on the high-fat diet became obese and insulin resistant "
            f"(HOMA-IR {fathers['homa_ir']['mean_highfat']:.2f} vs {fathers['homa_ir']['mean_control']:.2f}, "
            f"p_welch = {fathers['homa_ir']['p_welch_two_sided']:.2e}). Their daughters - despite eating "
            "a control diet and having normal body weight (12-wk weight p = "
            f"{offspring['body_weight_12wk_g']['p_welch_two_sided']:.2f}) - showed halved "
            f"glucose-stimulated insulin secretion (insulinogenic index {ii['mean_highfat']:.1f} vs "
            f"{ii['mean_control']:.1f}, diff {ii['diff_control_minus_highfat']:+.1f}, 95% bootstrap CI "
            f"[{ii['bootstrap95CI_diff'][0]:.1f}, {ii['bootstrap95CI_diff'][1]:.1f}], "
            f"p_rand = {ii['p_randomization_two_sided']:.4f}) and a higher 6-week glucose peak "
            f"({gp['mean_highfat']:.1f} vs {gp['mean_control']:.1f} mM, p_rand = "
            f"{gp['p_randomization_two_sided']:.3f}). Expression changes were broad: {genes['n_downregulated']}"
            f"/{genes['n_genes']} altered islet genes down-regulated (z = {genes['two_prop_z_vs_50pct']:.2f}, "
            f"p = {genes['p_two_prop_z_two_sided']:.1e}). Paternal pre-conception diet measurably "
            "reprograms daughters' metabolic health - experiences of parents do affect future children."),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2) + "\n")

    print(f"\n=== Q4: How broadly do experiences of parents affect their future children? ===")
    print(f"Study: {CITE}\nDataset: {CSV_PATH} ({len(df)} rows, reconstructed from paper summaries)\n")
    print("-- Fathers (manipulation check) --")
    for col in PUBLISHED["father"]:
        r = fathers[col]
        print(f"{col:24s} Control {r['mean_control']:8.2f} vs HighFat {r['mean_highfat']:8.2f} "
              f"t={r['welch_t']:+6.2f} p={r['p_welch_two_sided']:.2e} (paper p {r['paper_reported_p']})")
    print("\n-- Female offspring (all on control diet) --")
    for col in PUBLISHED["offspring"]:
        r = offspring[col]
        star = " *" if r["p_welch_two_sided"] < 0.05 else "  "
        print(f"{col:24s} Control {r['mean_control']:8.2f} vs HighFat {r['mean_highfat']:8.2f} "
              f"t={r['welch_t']:+6.2f} p={r['p_welch_two_sided']:.4f} (paper p {r['paper_reported_p']}){star}")
    r = offspring["insulinogenic_index"]
    print(f"\nInsulinogenic index: diff = {r['diff_control_minus_highfat']:+.1f} "
          f"(95% bootstrap CI {r['bootstrap95CI_diff'][0]:+.1f} to {r['bootstrap95CI_diff'][1]:+.1f}), "
          f"Cohen's d = {r['cohens_d']:.2f}")
    print(f"Randomization test (100k perms): p_two = {r['p_randomization_two_sided']:.4f}")
    print(f"\nIslet gene expression: {genes['n_downregulated']}/{genes['n_genes']} genes down-regulated "
          f"= {genes['prop_downregulated']:.1%}, z = {genes['two_prop_z_vs_50pct']:+.2f}, "
          f"p = {genes['p_two_prop_z_two_sided']:.1e} (95% CI {genes['bootstrap95CI_prop_down'][0]:.3f}-"
          f"{genes['bootstrap95CI_prop_down'][1]:.3f})")
    print(f"\nResults saved -> {OUT_JSON}")


if __name__ == "__main__":
    main()
