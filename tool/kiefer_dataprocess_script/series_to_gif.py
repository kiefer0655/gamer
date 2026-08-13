#!/usr/bin/env python3

# for indexed photo, use image%03d.png where %03d is the padded numbers ie image001.png

import argparse
import subprocess
from pathlib import Path


def run_command(cmd):
    print("[RUN]", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Make a GIF from a numbered PNG sequence using ffmpeg."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input filename pattern for ffmpeg, e.g. Fig__Gaussian_Dens_%%06d.png",
    )

    parser.add_argument(
        "--output",
        default="output.gif",
        help="Output GIF filename.",
    )

    parser.add_argument(
        "--framerate",
        type=int,
        default=5,
        help="Frames per second of the GIF.",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=-1,
        help="Output GIF width in pixels. Use -1 to keep original size.",
    )

    parser.add_argument(
        "--palette",
        default="palette.png",
        help="Temporary palette filename.",
    )

    args = parser.parse_args()

    output = Path(args.output)
    palette = Path(args.palette)

    if args.width > 0:
        scale_filter = f"fps={args.framerate},scale={args.width}:-1:flags=lanczos"
    else:
        scale_filter = f"fps={args.framerate}"

    # Step 1: generate palette
    run_command([
        "ffmpeg",
        "-y",
        "-framerate", str(args.framerate),
        "-i", args.input,
        "-vf", f"{scale_filter},palettegen",
        str(palette),
    ])

    # Step 2: use palette to make GIF
    run_command([
        "ffmpeg",
        "-y",
        "-framerate", str(args.framerate),
        "-i", args.input,
        "-i", str(palette),
        "-lavfi", f"{scale_filter}[x];[x][1:v]paletteuse",
        str(output),
    ])
    
    print(f"[DONE] Created {output}")


if __name__ == "__main__":
    main()
