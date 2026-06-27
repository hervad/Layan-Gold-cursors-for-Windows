# Layan Gold v9 Concrete Patch - Implementation Guide

## VERDICT SUMMARY

**Root Cause:** Sub-pixel stroke-width (0.6) + asymmetric shadow offset → aliasing artifacts + outline visible only on top-left.

**Solution (2 fixes):**
1. **Stroke-width:** 0.6 → 1.0 (eliminates sub-pixel rendering)
2. **Shadow:** Remove offset (dx="0.5" dy="0.8" → dx="0" dy="0") for symmetry

---

## IMPLEMENTATION

### File: `build_gold.py` (NEW)

Contains two critical functions:

#### `goldify_svg(svg_text, render_size=32)`

**Fix 1 — Stroke Width:**
```python
svg_text = re.sub(
    r'stroke-width="0\.6"',
    'stroke-width="1"',
    svg_text
)
```
- Replaces all instances of sub-pixel `stroke-width="0.6"` with `stroke-width="1"`
- At 32×32 viewBox → 32px render: 1 SVG unit ≈ 1 pixel (clean, no aliasing)
- At 64×64 render: scales to ~2px (still acceptable, readable)

**Fix 2 — Shadow Offset:**
```python
svg_text = re.sub(
    r'<feOffset\s+dx="[^"]*"\s+dy="[^"]*"',
    '<feOffset dx="0" dy="0"',
    svg_text
)
```
- Removes offset from `feOffset` filter (was: `dx="0.5" dy="0.8"`)
- Makes shadow symmetric (no bias to top-left corner)
- Outline now extends evenly around body, no asymmetric bare edges

**Also Included:**
- Shadow opacity: 0.35 → 0.40 for better definition
- Color swaps (base palette adjustments if needed)
- Outline color remains #FFF6E0 (already correct per verdict)

---

## MANUAL SVG EDITS (Alternative / Verification)

If your SVGs are in `src/svg/`, apply these regex replacements before running `build_gold.py`:

### Regex 1: Stroke Width
**Find:** `stroke-width="0\.6"`  
**Replace with:** `stroke-width="1"`

### Regex 2: Shadow Offset
**Find:** `<feOffset\s+dx="[^"]*"\s+dy="[^"]*"`  
**Replace with:** `<feOffset dx="0" dy="0"`

---

## RENDER-SIZE-AWARE NOTES

The verdict identified that stroke-width needs to account for render size:

- **32px output (most common):** stroke-width="1" works → ~1 pixel outline
- **64px output (high-DPI):** stroke-width="1" scales → ~2 pixel outline (acceptable)
- **128px output (icon view):** stroke-width="1" scales → ~4 pixels (consider `stroke-width="0.5"` for this)

Current patch uses fixed `stroke-width="1"` for all sizes (a safe middle ground). If you need size-specific stroke widths, modify `goldify_svg(svg_text, render_size)` to calculate:

```python
# Example (not in current patch):
# if render_size == 32:
#     target_stroke = "1"
# elif render_size == 64:
#     target_stroke = "1"
# elif render_size == 128:
#     target_stroke = "0.5"
```

---

## VERIFICATION CHECKLIST

After rendering with the patched SVGs, manually inspect at 32px and 64px:

### On Light Background (#FFFFFF)
- [ ] Outline is visible but clean (not chunky)
- [ ] No aliasing artifacts on curves
- [ ] Shadow blur is symmetric (not offset to top-left)
- [ ] Gold body (#D4AF37 or similar) is readable

### On Dark Background (#333333 or darker)
- [ ] Outline (#FFF6E0) has contrast and is readable
- [ ] Gold body warm-toned
- [ ] Shadow doesn't create halo effect

### Comparison (Before ↔ After)
- [ ] **Before:** Outline visible only on top-left, asymmetric shadow
- [ ] **After:** Outline full around body, symmetric shadow blur

---

## WHAT TO REMOVE

Per verdict: **Do NOT remove the outline entirely.** The outline is necessary for contrast. The problem was rendering quality (sub-pixel stroke → aliasing), not the design choice itself.

If you encounter still-visible aliasing after applying this patch:
1. Verify SVG was modified correctly (check for `stroke-width="1"` in output)
2. Re-render with stroke-width="1.2" (slightly thicker)
3. Use a higher-quality rasterizer (Inkscape's `--export-dpi=300` then downsample, not direct scale)

---

## SUMMARY

| Aspect | Old | New | Reason |
|--------|-----|-----|--------|
| Stroke-width | 0.6 (SVG units) | 1.0 (SVG units) | Sub-pixel → pixel-aligned, no aliasing |
| Shadow offset | dx="0.5" dy="0.8" | dx="0" dy="0" | Asymmetric → symmetric, even outline extension |
| Shadow opacity | 0.35 | 0.40 | Better definition without over-darkening |
| Outline color | #FFF6E0 | #FFF6E0 | ✓ Already correct (industry standard) |

---

## USAGE

```bash
python build_gold.py src/svg/ build/cursors/
```

This processes all SVGs in `src/svg/`, applies goldify fixes, and writes modified SVGs to `build/cursors/`.

Then render these modified SVGs to PNG/CUR using your existing pipeline (e.g., Inkscape, ImageMagick, or CairoSVG).
