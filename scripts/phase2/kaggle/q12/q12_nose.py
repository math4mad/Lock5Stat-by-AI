# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "q12_nose.csv").write_text('# data/phase2/q12_nose.csv\n# Lock5 Phase 2, Q12: "Is your nose getting bigger?"\n#\n# Citation: Sforza, C., Grandi, G., De Menezes, M., Tartaglia, G. M., & Ferrario, V. F.\n#   (2011; online 21 Aug 2010), "Age- and sex-related changes in the normal human\n#   external nose", Forensic Science International 204(1-3):205.e1-205.e9,\n#   DOI 10.1016/j.forsciint.2010.07.027 (Functional Anatomy Research Center,\n#   Universita degli Studi di Milano). This is the study cited by Lock5 3e\n#   ("Lock" et al., Statistics: Unlocking the Power of Data), Ch. 4.3 exercise\n#   "Is Your Nose Getting Bigger?" (Ex. 98/100 depending on printing), which quotes\n#   the paper: "Age significantly influenced all analyzed measurements" and reports\n#   p < 0.001 for a positive linear relationship between age and nose size, n = 859.\n#\n# Study design: cross-sectional digital anthropometry. 3D coordinates of soft-tissue\n#   landmarks (nasion n, subnasale sn, pronasale prn, alare al, alar crest ac, ...)\n#   collected with a computerized electromagnetic digitizer (Polhemus 3Draw,\n#   accuracy 0.25 mm) in 859 healthy white Italians (519 men, 340 women) aged\n#   4-73 years (Table 1 spans 4-80 years), 11 non-overlapping age groups.\n#   Headline findings (paper): men larger than women (p<0.01); age influenced all\n#   measurements (p<0.001) - nasal volume, area and linear distances increased from\n#   childhood to old age; male increments generally larger than female.\n#\n# Lock5 3e ships no dataset for this question (checked lock5stat.com/datapage3e.html;\n#   no nose/ear anthropometry dataset exists there).\n#\n# Data provenance: grouped means transcribed from Table 1 of the paper ("Three-\n#   dimensional external nasal morphometry in 519 healthy men"), read from a publicly\n#   accessible copy of the article (jakedorman.net/s/Age-_and_sex-related_changes_i.pdf).\n#   Transcription cross-checked against in-paper ratios: nasal tip protrusion at\n#   51-64 y = 121% of the 18-30 y mean (23.15/19.17 = 120.8% - matches the paper\'s\n#   reported 121%). Group n\'s sum to 519, matching the paper\'s male sample size.\n#   Not reconstructed: Table 2 (340 women) and the nasal-volume row - the only\n#   publicly accessible copy of the article cannot be retrieved in full (no open-\n#   access copy exists per Unpaywall/Semantic Scholar) and its Table 2 / volume\n#   row could not be transcribed with confidence; see Table 1-2 of the paper for\n#   those values.\n#   age_mid = approximate midpoint of each published age span (used as the age\n#   variate in correlation analyses).\n#\n# Units: linear measurements in mm; external nasal surface area in mm^2.\n# Columns: sex; age_group = published age span (years); age_mid = span midpoint;\n#   n = subjects per group; *_mean_mm / *_sd_mm = Table 1 mean and SD;\n#   landmark definitions: height = nasion-subnasale (n-sn); width = alare-alare\n#   (al-al); alar base = alar crest-alar crest (ac-ac); bridge = nasion-pronasale\n#   (n-prn); tip protrusion = pronasale-subnasale (prn-sn).\nsex,age_group,age_mid,n,height_mean_mm,height_sd_mm,width_mean_mm,width_sd_mm,alar_base_mean_mm,alar_base_sd_mm,bridge_mean_mm,bridge_sd_mm,tip_protrusion_mean_mm,tip_protrusion_sd_mm,area_mean_mm2,area_sd_mm2\nmen,4-5,4.5,11,34.50,3.20,23.75,4.85,24.88,5.53,27.58,2.77,14.16,0.92,735,164.40\nmen,6-7,6.5,47,40.04,2.13,25.67,2.46,26.90,2.46,32.49,2.65,15.89,1.46,848,96.50\nmen,8-9,8.5,55,43.03,3.08,26.65,3.42,27.45,2.90,34.79,3.44,16.95,1.74,973,162.40\nmen,10-11,10.5,44,46.83,2.35,26.40,2.40,25.98,2.55,39.70,2.48,16.86,1.83,1194,181.70\nmen,12-13,12.5,82,49.00,3.32,28.73,2.56,27.40,2.29,41.75,3.67,18.30,1.74,1327,180.50\nmen,14-16,15.0,55,50.53,2.84,31.10,3.68,29.23,3.29,44.36,2.68,18.91,1.93,1522,189.10\nmen,18-30,24.0,126,55.65,3.31,32.31,3.31,31.48,3.10,51.00,3.91,19.17,2.15,1643,185.80\nmen,31-40,35.5,66,57.30,4.17,33.86,2.74,33.21,2.36,52.52,4.82,20.24,2.16,1822,182.80\nmen,41-50,45.5,11,58.68,4.04,34.10,2.93,35.24,1.97,52.34,4.38,22.65,3.26,1873,132.70\nmen,51-64,57.5,15,54.79,3.28,35.76,3.09,35.00,2.56,49.34,3.86,23.15,1.93,1866,162.70\nmen,65-80,72.5,7,57.36,3.93,37.10,1.58,37.77,2.31,51.98,3.81,22.57,1.68,1874,188.80\n')
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
#!/usr/bin/env python3
"""Lock5 Phase 2, Q12: "Is your nose getting bigger?"

The Lock5 3e exercise "Is Your Nose Getting Bigger?" (Ch. 4.3, Ex. 98/100) cites
Sforza, C., Grandi, G., De Menezes, M., Tartaglia, G. M., & Ferrario, V. F. (2011;
online 21 Aug 2010), "Age- and sex-related changes in the normal human external
nose", Forensic Science International 204(1-3):205.e1-205.e9, DOI
10.1016/j.forsciint.2010.07.027. Cross-sectional 3D digital anthropometry
(electromagnetic digitizer, Polhemus 3Draw) of 859 healthy white Italians
(519 men, 340 women) aged 4-73 years in 11 age groups; the paper reports
"Age significantly influenced all analyzed measurements" (p < 0.001): nasal
volume, surface area and linear distances increased from childhood to old age.

Citation/provenance: Lock5 3e ships no dataset for this question (checked
lock5stat.com/datapage3e.html), so data/phase2/q12_nose.csv holds a documented
reconstruction: Table 1 grouped means (519 men, 11 age groups) transcribed from
the paper, cross-checked against in-paper ratios; women's Table 2 and the
nasal-volume row were not reliably retrievable from publicly accessible copies
and are excluded (provenance in the CSV header).

Analysis: data are grouped means, so correlation between age-group midpoint and
mean nose measurements (nasal height n-sn primary; nasal width al-al and
external surface area secondary), Pearson r with (a) randomization test -
permuting the measurement means across age groups, seed 2026, 100k replicates,
one-sided (positive) and two-sided p - and (b) bootstrap percentile CI for r
(resampling the age groups with replacement, 100k replicates); plus the
least-squares slope (mm/year) for the primary measure. Repeated on the
adult-only subset (age_mid >= 18) to ask whether growth continues after
skeletal maturity. numpy/scipy/pandas only; seed 2026; 100k replicates.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = _os_cwd  # Kaggle override
DATA = REPO / "data" / "phase2" / "q12_nose.csv"
OUT = REPO / "scripts" / "phase2" / "out" / "q12_results.json"

rng = np.random.default_rng(2026)
B = 100_000  # randomization / bootstrap iterations

df = pd.read_csv(DATA, comment="#")
print("Question: Is your nose getting bigger?")
print("Data: Sforza et al. (2011) Table 1 grouped means, 519 men, 11 age groups "
      "(data/phase2/q12_nose.csv)\n")
print(df[["age_group", "age_mid", "n", "height_mean_mm", "width_mean_mm",
          "area_mean_mm2"]].to_string(index=False), "\n")


def corr_analysis(x, y, label, unit):
    """Pearson r between age and (group-mean) measurement, with randomization p
    and pair-bootstrap percentile CI (resampling age groups with replacement)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    r = float(np.corrcoef(x, y)[0, 1])
    _, p_exact = stats.pearsonr(x, y)
    slope = float(np.polyfit(x, y, 1)[0])

    # Randomization test: permute the measurement means across age groups.
    perm = np.argsort(rng.random((B, n)), axis=1)
    y_perm = y[perm]
    xc = x - x.mean()
    yc = y_perm - y_perm.mean(axis=1, keepdims=True)
    sx = np.sqrt((xc ** 2).sum())
    sy = np.sqrt((yc ** 2).sum(axis=1))
    r_perm = (xc * yc).sum(axis=1) / (sx * sy)
    p_one = float(np.mean(r_perm >= r - 1e-12))
    p_two = float(np.mean(np.abs(r_perm) >= abs(r) - 1e-12))

    # Bootstrap CI for r: resample the (age, mean) pairs with replacement.
    idx = rng.integers(0, n, (B, n))
    xb, yb = x[idx], y[idx]
    xbc = xb - xb.mean(axis=1, keepdims=True)
    ybc = yb - yb.mean(axis=1, keepdims=True)
    num = (xbc * ybc).sum(axis=1)
    den = np.sqrt((xbc ** 2).sum(axis=1) * (ybc ** 2).sum(axis=1))
    r_boot = num / np.where(den > 0, den, np.nan)
    r_boot = r_boot[np.isfinite(r_boot)]
    ci = np.percentile(r_boot, [2.5, 97.5])

    print(f"--- {label} (n groups = {n})")
    print(f"    r = {r:.4f} (Pearson exact p = {p_exact:.2e}); slope = {slope:.4f} {unit}/yr")
    print(f"    randomization p (positive, one-sided) = {p_one:.2e}; "
          f"(two-sided) = {p_two:.2e}  [{B} permutations]")
    print(f"    bootstrap 95% CI for r = ({ci[0]:.4f}, {ci[1]:.4f}) "
          f"[{B} resamples, {len(r_boot)} valid]\n")
    return {"n_groups": n, "pearson_r": round(r, 4),
            "p_pearson_exact": float(f"{p_exact:.2e}"),
            "slope_per_year": round(slope, 4),
            "p_randomization_one_sided": float(f"{p_one:.2e}"),
            "p_randomization_two_sided": float(f"{p_two:.2e}"),
            "bootstrap_ci95": [round(float(ci[0]), 4), round(float(ci[1]), 4)],
            "bootstrap_valid": int(len(r_boot))}


MEASURES = [("height_mean_mm", "Age vs nasal height (n-sn), men, full span 4-80 y", "mm"),
            ("width_mean_mm", "Age vs nasal width (al-al), men, full span 4-80 y", "mm"),
            ("area_mean_mm2", "Age vs external nasal surface area, men, full span 4-80 y", "mm2")]

print("--- Correlations over the full age span (group means)")
full = {col: corr_analysis(df["age_mid"], df[col], label, unit)
        for col, label, unit in MEASURES}

adults = df[df["age_mid"] >= 18]
print("--- Adults only (age_mid >= 18; does growth continue after maturity?)")
adult = {col: corr_analysis(adults["age_mid"], adults[col], label, unit)
         for (col, label, unit), key in zip(
             [("height_mean_mm", "Age vs nasal height, men, adults 18-80 y", "mm"),
              ("width_mean_mm", "Age vs nasal width, men, adults 18-80 y", "mm"),
              ("area_mean_mm2", "Age vs external nasal area, men, adults 18-80 y", "mm2")],
             ["height_mean_mm", "width_mean_mm", "area_mean_mm2"])}

first, last = df.iloc[0], df.iloc[-1]
h_gain = last["height_mean_mm"] - first["height_mean_mm"]
r_full = full["height_mean_mm"]["pearson_r"]
r_adult = adult["height_mean_mm"]["pearson_r"]
p_adult = adult["height_mean_mm"]["p_randomization_one_sided"]

print("Conclusion:")
print(f"  Nose size rises steadily across the lifespan: mean nasal height grows from")
print(f"  {first['height_mean_mm']:.1f} mm (age 4-5) to {last['height_mean_mm']:.1f} mm (age 65-80), "
      f"+{h_gain:.1f} mm, and nasal width grows")
print(f"  {first['width_mean_mm']:.1f} -> {last['width_mean_mm']:.1f} mm. Over ages 4-80 the age-nose "
      f"correlation is strong and positive")
print(f"  (height r = {r_full:.2f}, one-sided randomization p = "
      f"{full['height_mean_mm']['p_randomization_one_sided']:.1e}; width r = "
      f"{full['width_mean_mm']['pearson_r']:.2f}; area r = {full['area_mean_mm2']['pearson_r']:.2f}),")
print("  matching the paper's ANOVA (age p < 0.001) and Lock5's quoted p < 0.001. Among")
print(f"  adult age-group means alone (18-80 y, 5 groups) nasal height is flat "
      f"(r = {r_adult:.2f},")
print(f"  one-sided randomization p = {p_adult:.2f}), but nasal width keeps widening "
      f"significantly")
print(f"  (r = {adult['width_mean_mm']['pearson_r']:.2f}, one-sided p = "
      f"{adult['width_mean_mm']['p_randomization_one_sided']:.1e}) and area trends positive "
      f"(r = {adult['area_mean_mm2']['pearson_r']:.2f},")
print("  one-sided p = %.2f) - grouped means have far less power than the study's" %
      adult['area_mean_mm2']['p_randomization_one_sided'])
print("  individual-level test (p < 0.001), and most of the size gain occurs up to ~18 y.")

results = {
    "question": "Is your nose getting bigger?",
    "outcome": ("External nose size with age: nasal height (nasion-subnasale, mm), "
                "nasal width (alare-alare, mm) and external nasal surface area (mm2), "
                "cross-sectional grouped means, 519 men, ages 4-80."),
    "citation": (
        "Sforza, C., Grandi, G., De Menezes, M., Tartaglia, G. M., & Ferrario, V. F. "
        "(2011; online 21 Aug 2010), 'Age- and sex-related changes in the normal human "
        "external nose', Forensic Science International 204(1-3):205.e1-205.e9, "
        "DOI 10.1016/j.forsciint.2010.07.027. Study cited by Lock5 3e, Ch. 4.3 exercise "
        "'Is Your Nose Getting Bigger?' (n = 859: 519 men, 340 women, aged 4-73)."
    ),
    "study_design": (
        "Cross-sectional digital anthropometry; 3D coordinates of soft-tissue nasal "
        "landmarks via electromagnetic digitizer (Polhemus 3Draw, 0.25 mm accuracy); "
        "11 non-overlapping age groups; factorial ANOVA. Headline: men larger than "
        "women (p<0.01); age influenced all measurements (p<0.001), volume/area/linear "
        "distances increased from childhood to old age."
    ),
    "dataset": {
        "path": "data/phase2/q12_nose.csv",
        "note": ("Lock5 3e ships no dataset for this question (checked "
                 "lock5stat.com/datapage3e.html). Documented reconstruction of Table 1 "
                 "grouped means (519 men) transcribed from a publicly accessible copy of "
                 "the article and cross-checked against in-paper ratios; women's Table 2 "
                 "and the nasal-volume row not reliably retrievable and excluded. "
                 "Provenance in CSV header comments."),
    },
    "correlations": {
        "full_span_men_4_to_80": full,
        "adults_only_men_18_to_80": adult,
    },
    "conclusion": (
        f"Across ages 4-80, mean nasal height grows from {first['height_mean_mm']:.1f} mm to "
        f"{last['height_mean_mm']:.1f} mm (+{h_gain:.1f} mm) and width from "
        f"{first['width_mean_mm']:.1f} mm to {last['width_mean_mm']:.1f} mm; age-nose "
        f"correlations are strongly positive (height r = {r_full:.2f}, one-sided "
        f"randomization p = {full['height_mean_mm']['p_randomization_one_sided']:.1e}; "
        f"width r = {full['width_mean_mm']['pearson_r']:.2f}; area r = "
        f"{full['area_mean_mm2']['pearson_r']:.2f}; both p < 0.001), matching the paper's "
        f"p < 0.001 quoted by Lock5. Among adult age-group means only (18-80 y, 5 groups) "
        f"nasal height is flat (r = {r_adult:.2f}, one-sided p = {p_adult:.2f}), but width "
        f"keeps widening significantly (r = {adult['width_mean_mm']['pearson_r']:.2f}, "
        f"one-sided p = {adult['width_mean_mm']['p_randomization_one_sided']:.1e}) and area "
        f"trends positive (r = {adult['area_mean_mm2']['pearson_r']:.2f}, one-sided p = "
        f"{adult['area_mean_mm2']['p_randomization_one_sided']:.2f}): grouped means lack the "
        f"power of the study's individual-level test (p < 0.001), and most of the size "
        f"gain occurs up to ~18 y with continued enlargement most evident in width."
    ),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, indent=2) + "\n")
print(f"Saved results to {OUT}")
