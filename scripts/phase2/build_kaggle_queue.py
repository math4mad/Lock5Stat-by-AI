#!/usr/bin/env python3
"""Build a Kaggle kernel queue for Phase 2 experiments.

Generates a Kaggle code-kernel package per question (scripts/phase2/kaggle/<q>/)
containing kernel-metadata.json + runner.ipynb (the analysis script wrapped as a
notebook cell). Pushing requires ~/.kaggle/kaggle.json.
Usage: .venv/bin/python scripts/phase2/build_kaggle_queue.py [--push]
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PH2 = REPO / "scripts" / "phase2"
KAGGLE_SLUG = "math4amd"
def discover_questions():
    """Auto-discover qN_<name>.py scripts and matching data CSVs."""
    qs = {}
    for f in sorted(PH2.glob("q*_*.py")):
        q = f.stem.split("_")[0]
        if q in qs:
            continue
        name = f.stem.split("_", 1)[1]  # strip "qN_" prefix
        slug = "lock5-phase2-" + name.replace("_", "-")
        qs[q] = (f.name, name, slug)
    return qs


QUESTIONS = discover_questions()


def make_notebook(script_text: str) -> dict:
    return {"cells": [{"cell_type": "code", "execution_count": None,
                       "metadata": {}, "outputs": [],
                       "source": script_text.splitlines(keepends=True)}],
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                        "name": "python3"},
                         "language_info": {"name": "python", "version": "3.11"}},
            "nbformat": 4, "nbformat_minor": 4}


def make_kaggle_script(script_text: str, csv_name: str) -> str:
    """Inject a self-containment shim: embed the CSV and redirect REPO to cwd."""
    csv_text = (REPO / "data" / "phase2" / csv_name).read_text()
    shim = f'''# ---- Kaggle self-containment shim (auto-inserted by build_kaggle_queue.py) ----
import pathlib as _pl
_os_cwd = _pl.Path.cwd()
(_os_cwd / "data" / "phase2").mkdir(parents=True, exist_ok=True)
(_os_cwd / "scripts" / "phase2" / "out").mkdir(parents=True, exist_ok=True)
(_os_cwd / "data" / "phase2" / "{csv_name}").write_text({csv_text!r})
import os as _os
_os.chdir(_os_cwd)
REPO = _os_cwd  # overridden for Kaggle (original assignment below is ignored)
# ---- end shim ----
'''
    body = (script_text
            .replace("REPO = Path(__file__).resolve().parents[2]",
                     "REPO = _os_cwd  # Kaggle override")
            .replace("ROOT = Path(__file__).resolve().parents[2]",
                     "ROOT = _os_cwd  # Kaggle override")
            .replace("BASE = Path(__file__).resolve().parents[2]",
                     "BASE = _os_cwd  # Kaggle override"))
    return shim + body


def main(push: bool):
    queue = []
    for q, (script, name, slug) in QUESTIONS.items():
        out = PH2 / "kaggle" / q
        out.mkdir(parents=True, exist_ok=True)
        text = (PH2 / script).read_text()
        csv_name = f"{q}_{name}.csv"
        ktext = make_kaggle_script(text, csv_name)
        (out / "runner.ipynb").write_text(json.dumps(make_notebook(ktext)))
        (out / script).write_text(ktext)
        (out / "kernel-metadata.json").write_text(json.dumps({
            "id": f"{KAGGLE_SLUG}/{slug}",
            "title": slug.replace("-", " ").title(),
            "code_file": script,
            "language": "python",
            "kernel_type": "script",
            "is_private": "true",
            "enable_gpu": "false",
            "enable_internet": "true",
            "dataset_sources": [],
            "competition_sources": [],
            "kernel_sources": [],
        }, indent=2))
        queue.append(str(out / "kernel-metadata.json"))
    print("Queue built:")
    print("\n".join(queue))

    if push:
        for q, (script, name, slug) in QUESTIONS.items():
            pkg = PH2 / "kaggle" / q
            r = subprocess.run(["kaggle", "kernels", "push", "-p", str(pkg)],
                               capture_output=True, text=True)
            print(f"[{q}] push: {r.returncode} {r.stdout.strip()[:120]} {r.stderr.strip()[:120]}")
            if r.returncode != 0:
                sys.exit(f"push failed at {q}")


if __name__ == "__main__":
    main("--push" in sys.argv)
