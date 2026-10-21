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
KAGGLE_SLUG = "lock5stat-by-ai"
QUESTIONS = {
    "q1": ("q1_handwashing.py", "lock5-phase2-q1-handwashing"),
    "q2": ("q2_turnback.py", "lock5-phase2-q2-turnback"),
    "q3": ("q3_spider.py", "lock5-phase2-q3-spider"),
    "q4": ("q4_intergen.py", "lock5-phase2-q4-intergen"),
    "q5": ("q5_aboveavg.py", "lock5-phase2-q5-aboveavg"),
}


def make_notebook(script_text: str) -> dict:
    return {"cells": [{"cell_type": "code", "execution_count": None,
                       "metadata": {}, "outputs": [],
                       "source": script_text.splitlines(keepends=True)}],
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                        "name": "python3"},
                         "language_info": {"name": "python", "version": "3.11"}},
            "nbformat": 4, "nbformat_minor": 4}


def main(push: bool):
    queue = []
    for q, (script, slug) in QUESTIONS.items():
        out = PH2 / "kaggle" / q
        out.mkdir(parents=True, exist_ok=True)
        text = (PH2 / script).read_text()
        (out / "runner.ipynb").write_text(json.dumps(make_notebook(text)))
        (out / script).write_text(text)
        (out / "kernel-metadata.json").write_text(json.dumps({
            "id": f"{KAGGLE_SLUG}/{slug}",
            "title": slug.replace("-", " ").title(),
            "code_file": script,
            "language": "python",
            "kernel_type": "script",
            "is_private": "true",
            "enable_gpu": "true",
            "enable_internet": "true",
            "dataset_sources": [],
            "competition_sources": [],
            "kernel_sources": [],
        }, indent=2))
        queue.append(str(out / "kernel-metadata.json"))
    print("Queue built:")
    print("\n".join(queue))

    if push:
        for q, (script, slug) in QUESTIONS.items():
            pkg = PH2 / "kaggle" / q
            r = subprocess.run(["kaggle", "kernels", "push", "-p", str(pkg)],
                               capture_output=True, text=True)
            print(f"[{q}] push: {r.returncode} {r.stdout.strip()[:120]} {r.stderr.strip()[:120]}")
            if r.returncode != 0:
                sys.exit(f"push failed at {q}")


if __name__ == "__main__":
    main("--push" in sys.argv)
