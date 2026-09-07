"""
Build a refined owl mark for the ivory/antique-gold proposal cover.

The deck's light-theme owl was tonally crushed (luminance spread of only 48), which is why it
reads as a smudge rather than a mark. This rebuilds it from the full-range brand lockup
(spread 210) and maps that range onto a restrained warm-ink duotone that keeps the wing
feathering and the facial disc legible on ivory paper.
"""
import os

import numpy as np
from PIL import Image

SRC = "/Users/adityalakshmipathy/Documents/Levitatte/images/logo-transparent.png"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "owl_refined.png")

# duotone ramp: deep warm ink -> warm mid -> light warm grey (visible on ivory, never white)
DARK = np.array([32, 28, 23], float)     # shadows / outlines
MID = np.array([94, 86, 74], float)      # body, warm
LIGHT = np.array([176, 168, 154], float) # wing highlights
GAMMA = 0.92                             # slightly open the midtones


def main():
    im = Image.open(SRC).convert("RGBA")
    a = np.asarray(im).astype(float)
    alpha = a[..., 3]

    # 1. isolate the owl: the lockup is owl over wordmark; split at the quietest row
    rows = (alpha > 25).sum(axis=1)
    band = rows[860:975]
    split = 860 + int(np.argmin(band))
    owl = a[:split, :, :]
    print(f"owl/wordmark split at y={split}")

    # 2. trim to actual ink so layout spacing is driven by the mark, not padding
    al = owl[..., 3]
    ys, xs = np.where(al > 12)
    pad = 4
    y0, y1 = max(0, ys.min() - pad), min(owl.shape[0], ys.max() + 1 + pad)
    x0, x1 = max(0, xs.min() - pad), min(owl.shape[1], xs.max() + 1 + pad)
    owl = owl[y0:y1, x0:x1, :]
    print(f"trimmed to {owl.shape[1]}x{owl.shape[0]}")

    # 3. luminance of the original, normalised across its true range
    rgb, al = owl[..., :3], owl[..., 3:4]
    L = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    m = al[..., 0] > 12
    lo, hi = np.percentile(L[m], 1), np.percentile(L[m], 99)
    t = np.clip((L - lo) / max(hi - lo, 1e-6), 0, 1) ** GAMMA
    print(f"source luminance range {lo:.0f}..{hi:.0f} -> remapped over full duotone ramp")

    # 4. three-stop duotone so the midtones stay warm instead of going flat grey
    t3 = t[..., None]
    low = DARK + (MID - DARK) * np.clip(t3 / 0.5, 0, 1)
    high = MID + (LIGHT - MID) * np.clip((t3 - 0.5) / 0.5, 0, 1)
    out_rgb = np.where(t3 < 0.5, low, high)

    out = np.dstack([out_rgb, al]).astype("uint8")
    img = Image.fromarray(out, "RGBA")

    # 5. supersample down for clean edges at print size
    w, h = img.size
    img = img.resize((int(w * 0.75), int(h * 0.75)), Image.LANCZOS)
    img.save(OUT)

    chk = np.asarray(img).astype(float)
    cm = chk[..., 3] > 25
    cl = (0.299 * chk[..., 0] + 0.587 * chk[..., 1] + 0.114 * chk[..., 2])[cm]
    print(f"wrote {OUT} {img.size}")
    print(f"new luminance spread = {cl.max() - cl.min():.0f} (was 48)")
    print(f"aspect = {img.size[0] / img.size[1]:.3f}")


if __name__ == "__main__":
    main()
