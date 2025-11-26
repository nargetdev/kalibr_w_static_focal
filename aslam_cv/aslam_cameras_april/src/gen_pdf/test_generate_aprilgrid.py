#!/usr/bin/env python

import os
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
YAML_PATH = os.path.join(SCRIPT_DIR, "april_24x24_size20mm_space0.3.yaml")
GEN_SCRIPT = os.path.join(SCRIPT_DIR, "generate_aprilgrid_from_yaml.py")
OUTPUT_BASENAME = "aprilgrid_24x24_test"


def main():
    if not os.path.isfile(YAML_PATH):
        print(f"[ERROR] YAML config not found: {YAML_PATH}")
        sys.exit(1)

    if not os.path.isfile(GEN_SCRIPT):
        print(f"[ERROR] Generator script not found: {GEN_SCRIPT}")
        sys.exit(1)

    cmd = [
        sys.executable,
        GEN_SCRIPT,
        YAML_PATH,
        "--output",
        OUTPUT_BASENAME,
    ]

    print("[INFO] Running:", " ".join(cmd))

    try:
        subprocess.check_call(cmd, cwd=SCRIPT_DIR)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Generation failed with return code {e.returncode}")
        sys.exit(e.returncode)

    pdf_path = os.path.abspath(os.path.join(SCRIPT_DIR, OUTPUT_BASENAME + ".pdf"))
    if not os.path.isfile(pdf_path):
        print(f"[ERROR] Expected PDF not found: {pdf_path}")
        sys.exit(1)

    print("[INFO] Generated PDF:")
    print(pdf_path)


if __name__ == "__main__":
    main()
