#!/usr/bin/env python3
"""Render an HTML film to MP4 under a virtual clock.

Usage: render_video.py <html> <duration> <fps> <out.mp4>
Frames go from Playwright (JPEG, quality 92) through a pipe into ffmpeg:
libx264, medium preset, crf 18, yuv420p, faststart.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_scene import VIRTUAL_CLOCK, validate  # noqa: E402


def main(argv):
    if len(argv) < 5:
        print("usage: render_video.py <html> <duration> <fps> <out.mp4>", file=sys.stderr)
        return 2
    html = Path(argv[1]).read_text(encoding="utf-8")
    validate(html)
    duration = min(max(float(argv[2]), 3), 90)
    fps = int(argv[3])
    if fps not in (24, 30):
        raise SystemExit("fps must be 24 or 30.")
    out = Path(argv[4])
    out.parent.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    total = round(duration * fps)
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
        stdin=subprocess.PIPE)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1, color_scheme="light")
            ctx.add_init_script(VIRTUAL_CLOCK)
            page = ctx.new_page()
            page.set_content(html, wait_until="load", timeout=30000)
            page.evaluate("document.fonts.ready")
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            page.evaluate("window.__seek(0)")
            for i in range(total):
                page.evaluate(f"window.__seek({(i * 1000) / fps})")
                frame = page.screenshot(type="jpeg", quality=92)
                ff.stdin.write(frame)
                if (i + 1) % max(1, round(fps * 3)) == 0:
                    print(f"frame {i + 1}/{total}", flush=True)
            ctx.close()
            browser.close()
    finally:
        ff.stdin.close()
    code = ff.wait()
    if code != 0:
        raise SystemExit(f"ffmpeg exited {code}.")
    print(f"saved {out} ({total} frames, {duration}s at {fps}fps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
