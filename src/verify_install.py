#!/usr/bin/env python3
"""Verify all dependencies for cursor vein morphing are installed."""

import sys

def verify():
    errors = []

    # Check scipy
    try:
        import scipy.ndimage
        print(f"[OK] scipy.ndimage: {scipy.__version__ if hasattr(scipy, '__version__') else 'installed'}")
    except ImportError as e:
        errors.append(f"scipy: {e}")

    # Check PIL
    try:
        from PIL import Image
        import PIL
        print(f"[OK] PIL (Pillow): {PIL.__version__}")
    except ImportError as e:
        errors.append(f"PIL/Pillow: {e}")

    # Check numpy
    try:
        import numpy
        print(f"[OK] numpy: {numpy.__version__}")
    except ImportError as e:
        errors.append(f"numpy: {e}")

    # Check clickgen
    try:
        import clickgen
        from clickgen.writer import to_cur
        print(f"[OK] clickgen: {clickgen.__version__}")
    except ImportError as e:
        errors.append(f"clickgen or clickgen.writer.to_cur: {e}")

    if errors:
        print("\n[FAIL] MISSING PACKAGES:")
        for err in errors:
            print(f"  - {err}")
        print("\nFix with: pip install scipy pillow numpy clickgen")
        return False

    print("\n[SUCCESS] ALL DEPENDENCIES READY")
    return True

if __name__ == '__main__':
    sys.exit(0 if verify() else 1)
