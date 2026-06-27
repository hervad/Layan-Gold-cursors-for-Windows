# Credits & attribution

This project is a derivative work in a chain of free-software cursor themes. The artwork and code are inherited from several upstreams, each of which is credited below per their license requirements.

## Upstream chain

1. **KDE Breeze icon theme** — the original silhouette and arrow geometry.
2. **[Capitaine cursors](https://github.com/keeferrourke/capitaine-cursors)** — © 2016 Keefer Rourke and others. Licensed under **LGPL v3** (explicitly extended to artwork; see Capitaine's `COPYING`). The frame-by-frame `progress` and `wait` animation SVGs originate here.
3. **[Layan cursors (Linux)](https://github.com/vinceliuice/Layan-cursors)** — © vinceliuice. A monochrome / themed adaptation of Capitaine.
4. **[Layan cursors for Windows](https://github.com/karaksid/Layan-cursors-for-Windows)** — the Windows `.cur`/`.ani` port via [`win2xcur`](https://pypi.org/project/win2xcur/). Licensed under **GPL v3**.
5. **Layan Gold cursors for Windows** (this repo) — palette v11 (dark-gold orange-shifted), HiDPI sizes 32/40/48/64/96/128 px, edge morphing for crisper outlines.

## Modifications in this repo

- Replaced Layan's original palette with the v11 gold gradient (see `README.md` table).
- Adjusted stroke-width handling and symmetric drop-shadow in `build_gold.py`.
- Added high-DPI sizes (40/48/64/96/128 px) beyond upstream's 32 px.
- Added `morph_cursor_edge.py` for outline anti-aliasing improvements.
- Added `verify_install.py` for post-install sanity checking.

## License

This work is distributed under **GPL v3** (see [`LICENSE`](LICENSE)). The underlying artwork retains its **LGPL v3** roots from Capitaine; per LGPL v3, source files (SVG / build scripts) are included alongside the binaries.
