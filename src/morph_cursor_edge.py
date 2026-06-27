#!/usr/bin/env python3
"""Apply asymmetric vein-line morphing to cursor edges.

This module detects the dark vein line in a leaf cursor and creates an
asymmetric morphing mask where the edge follows the vein line instead
of being perfectly round.

Usage:
    python morph_cursor_edge.py input.png output.cur [hotspot_x hotspot_y]
"""

import sys
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
from clickgen.writer import to_cur
from clickgen.cursors import CursorImage, CursorFrame
from pathlib import Path


def detect_vein_line(rgba_img):
    """
    Detect the dark vein line in the leaf cursor.

    Returns:
        list: Ordered (y, x) coordinates along the line from left to right.
              None if no clear vein is detected.
    """
    arr = np.array(rgba_img)
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

    # Vein is darker than the light gold body
    intensity = (r.astype(int) + g.astype(int) + b.astype(int)) / 3.0
    dark_mask = (intensity < 100) & (a > 0)

    if not np.any(dark_mask):
        return None

    # Extract centerline of dark region
    dark_points = np.argwhere(dark_mask)
    vein_line = []

    # Group by x-coordinate, find median y to get smooth line
    for x in sorted(np.unique(dark_points[:, 1])):
        ys = dark_points[dark_points[:, 1] == x, 0]
        vein_line.append((int(np.median(ys)), x))

    return vein_line


def apply_vein_morphing_mask(rgba_img, vein_line=None, feather_width=6):
    """
    Create asymmetric alpha mask following vein line.

    Points below/right of vein → full opacity (opaque)
    Points above/left of vein → fading opacity (gaussian feather)

    Args:
        rgba_img (PIL.Image): Input cursor image in RGBA mode
        vein_line (list): List of (y, x) tuples along vein centerline
        feather_width (int): Gaussian sigma for feathering (pixels)

    Returns:
        PIL.Image: Morphed image with asymmetric alpha channel
    """
    arr = np.array(rgba_img, dtype=np.float32)
    h, w = arr.shape[:2]

    # If no vein detected, use default diagonal line
    if vein_line is None:
        vein_line = [(i, max(3, i // 2)) for i in range(h)]

    # Create morphing mask (1.0 = keep, 0.0 = transparent)
    morph_mask = np.ones((h, w), dtype=np.float32)

    # Build vein line lookup: x -> y
    vein_dict = {x: y for y, x in vein_line}

    for i in range(h):
        for j in range(w):
            # Find vein y-coordinate at this x position (interpolate if needed)
            if j in vein_dict:
                vein_y = vein_dict[j]
            elif j > 0:
                # Linear interpolation between nearest known points
                nearby_xs = sorted([x for x in vein_dict.keys() if x <= j])
                if nearby_xs:
                    vein_y = vein_dict[nearby_xs[-1]]
                else:
                    vein_y = vein_line[0][0] if vein_line else i
            else:
                vein_y = vein_line[0][0] if vein_line else i

            # Distance from vein line (positive = above, negative = below)
            dist_from_vein = i - vein_y

            # Above/left of vein: apply gaussian feather (fade out)
            if dist_from_vein < 0:
                feather = np.exp(-(dist_from_vein ** 2) / (2.0 * feather_width ** 2))
                morph_mask[i, j] *= feather

    # Apply mask to alpha channel
    arr[:, :, 3] = np.clip(arr[:, :, 3] * morph_mask, 0, 255)

    return Image.fromarray(np.uint8(arr), 'RGBA')


def morph_cursor_from_file(input_png, output_cur, hotspot=(8, 8), verbose=True):
    """
    Main pipeline: PNG → vein detection → morphing → CUR write.

    Args:
        input_png (str): Path to input cursor PNG
        output_cur (str): Path to output .cur file
        hotspot (tuple): (x, y) hotspot coordinates
        verbose (bool): Print progress messages

    Returns:
        bool: True if successful
    """
    try:
        # Load
        img = Image.open(input_png).convert('RGBA')
        if verbose:
            print(f"Loaded {input_png}: {img.size}")

        # Detect vein
        vein = detect_vein_line(img)
        if vein:
            if verbose:
                print(f"  Detected vein line: {len(vein)} points")
        else:
            if verbose:
                print(f"  No vein detected; using default morphing")

        # Apply morphing
        morphed = apply_vein_morphing_mask(img, vein, feather_width=6)
        if verbose:
            print(f"  Applied morphing mask")

        # Write CUR (single frame)
        # Create CursorImage: CursorImage(image, hotspot, nominal, re_canvas)
        cur_img = CursorImage(morphed, hotspot=hotspot, nominal=img.size[0])
        frame = CursorFrame([cur_img], delay=0)
        data = to_cur(frame)

        with open(output_cur, 'wb') as f:
            f.write(data)

        if verbose:
            print(f"[OK] Wrote {output_cur}")

        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python morph_cursor_edge.py <input.png> [output.cur] [hotspot_x] [hotspot_y]")
        print("Example: python morph_cursor_edge.py default_64.png default_64_morphed.cur 8 8")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.png', '_morphed.cur')
    hotspot_x = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    hotspot_y = int(sys.argv[4]) if len(sys.argv) > 4 else 8

    success = morph_cursor_from_file(input_file, output_file, (hotspot_x, hotspot_y))
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
