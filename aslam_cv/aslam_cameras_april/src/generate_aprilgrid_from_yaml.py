#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

import yaml


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate an AprilGrid calibration target PDF (and optionally SVG/EPS) from a Kalibr-style YAML file.",
    )

    parser.add_argument(
        "config",
        help="Path to the AprilGrid YAML configuration file (e.g. april_24x24_size20mm_space0.3.yaml)",
    )

    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help=(
            "Base name for the output files (without extension). "
            "If omitted, the stem of the YAML filename is used."
        ),
    )

    parser.add_argument(
        "--eps",
        action="store_true",
        help="Also generate an EPS file via createTargetPDF.py.",
    )

    parser.add_argument(
        "--svg",
        action="store_true",
        help="Also generate an SVG file via createTargetPDF.py.",
    )

    return parser.parse_args()


def load_aprilgrid_config(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    target_type = data.get("target_type")
    if target_type != "aprilgrid":
        raise ValueError(
            f"Unsupported target_type '{target_type}'. This helper only handles 'aprilgrid'."
        )

    try:
        tag_rows = data["tagRows"]
        tag_cols = data["tagCols"]
        tag_size = data["tagSize"]
        tag_spacing = data["tagSpacing"]
    except KeyError as e:
        raise KeyError(f"Missing required key in AprilGrid YAML: {e}") from e

    return tag_rows, tag_cols, tag_size, tag_spacing


def main():
    args = parse_args()

    yaml_path = os.path.abspath(args.config)
    if not os.path.isfile(yaml_path):
        print(f"[ERROR] YAML file not found: {yaml_path}")
        sys.exit(1)

    try:
        tag_rows, tag_cols, tag_size, tag_spacing = load_aprilgrid_config(yaml_path)
    except Exception as e:
        print(f"[ERROR] Failed to load AprilGrid config from '{yaml_path}': {e}")
        sys.exit(1)

    # Derive output base name if not provided.
    if args.output is not None:
        output_basename = args.output
    else:
        output_basename = os.path.splitext(os.path.basename(yaml_path))[0]

    # Resolve path to the existing createTargetPDF.py script (same directory as this file).
    script_dir = os.path.dirname(os.path.abspath(__file__))
    create_target_script = os.path.join(script_dir, "createTargetPDF.py")

    if not os.path.isfile(create_target_script):
        print(f"[ERROR] createTargetPDF.py not found next to this script: {create_target_script}")
        sys.exit(1)

    # Build command to call the existing generator.
    # Note: createTargetPDF.py expects the output base name as the first positional argument.
    cmd = [
        sys.executable,
        create_target_script,
        output_basename,
        "--type",
        "apriltag",
        "--nx",
        str(tag_cols),
        "--ny",
        str(tag_rows),
        "--tsize",
        str(tag_size),
        "--tspace",
        str(tag_spacing),
        "--tfam",
        "t36h11",
        "--no-text",
    ]

    if args.eps:
        cmd.append("--eps")
    if args.svg:
        cmd.append("--svg")

    print("[INFO] Running:", " ".join(cmd))

    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] createTargetPDF.py failed with return code {e.returncode}")
        sys.exit(e.returncode)

    print("[INFO] Done. Generated:")
    print(f"  {output_basename}.pdf")
    if args.eps:
        print(f"  {output_basename}.eps")
    if args.svg:
        print(f"  {output_basename}.svg")


if __name__ == "__main__":
    main()
