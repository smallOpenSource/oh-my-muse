#!/usr/bin/env python3
"""Load an HTML film under a virtual clock and report errors and visible text.

Usage: check_scene.py <html> <duration> [timestamps...]
Without timestamps, inspects every 3 seconds up to duration.
Exits 1 when any page error or failed request was reported.
"""
import json
import re
import sys
from pathlib import Path

VIRTUAL_CLOCK = r"""(() => {
  const EPOCH = Date.now();
  let now = 0;
  const rafs = new Map(); let rafId = 0;
  const timers = new Map(); let timerId = 0;
  const RealDate = Date;
  performance.now = () => now;
  const FakeDate = function (...args) { return args.length ? new RealDate(...args) : new RealDate(EPOCH + now); };
  FakeDate.now = () => EPOCH + now;
  FakeDate.UTC = RealDate.UTC; FakeDate.parse = RealDate.parse; FakeDate.prototype = RealDate.prototype;
  window.Date = FakeDate;
  window.requestAnimationFrame = (cb) => { rafs.set(++rafId, cb); return rafId; };
  window.cancelAnimationFrame = (id) => { rafs.delete(id); };
  window.setTimeout = (cb, ms = 0, ...args) => { const id = ++timerId; timers.set(id, { at: now + Math.max(0, +ms || 0), cb, args, every: 0 }); return id; };
  window.setInterval = (cb, ms = 0, ...args) => { const id = ++timerId; const every = Math.max(1, +ms || 1); timers.set(id, { at: now + every, cb, args, every }); return id; };
  window.clearTimeout = window.clearInterval = (id) => { timers.delete(id); };
  const seen = new WeakMap();
  const step = 1000 / 60;
  window.__seek = (t) => {
    while (now < t - 1e-6) {
      now = Math.min(t, now + step);
      for (;;) {
        let next = null;
        for (const [id, tm] of timers) if (tm.at <= now + 1e-6 && (!next || tm.at < next[1].at)) next = [id, tm];
        if (!next) break;
        const [id, tm] = next;
        if (tm.every) tm.at += tm.every; else timers.delete(id);
        try { typeof tm.cb === "function" ? tm.cb(...tm.args) : (0, eval)(String(tm.cb)); } catch (e) { console.error("timer callback threw: " + (e && e.message)); }
      }
      const cbs = [...rafs.values()]; rafs.clear();
      for (const cb of cbs) { try { cb(now); } catch (e) { console.error("requestAnimationFrame callback threw: " + (e && e.message)); } }
    }
    for (const a of document.getAnimations({ subtree: true })) {
      try { let s = seen.get(a); if (s === undefined) { s = now; seen.set(a, s); } a.pause(); a.currentTime = Math.max(0, now - s); } catch (e) {}
    }
    return now;
  };
})();"""

FORBIDDEN = re.compile(r"<(video|audio|iframe)[\s>]", re.I)


def validate(html):
    if len(html) < 200:
        raise SystemExit("html is too short to be a scene.")
    if not re.search(r"<html[\s>]", html, re.I) and not re.search(r"<body[\s>]", html, re.I):
        raise SystemExit("html must be a complete document (include <html> and <body>).")
    if FORBIDDEN.search(html):
        raise SystemExit("Scenes cannot use <video>, <audio>, or <iframe>.")


SNAPSHOT_JS = """() => {
  const vw = window.innerWidth, vh = window.innerHeight;
  const texts = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const s = (n.textContent || "").replace(/\\s+/g, " ").trim();
    if (!s) continue;
    const el = n.parentElement;
    if (!el) continue;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) < 0.05) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0 || r.right < 0 || r.bottom < 0 || r.left > vw || r.top > vh) continue;
    texts.push(s.slice(0, 80));
  }
  return { visibleText: [...new Set(texts)].join(" | ").slice(0, 1200), bodyBackground: getComputedStyle(document.body).backgroundColor };
}"""


def main(argv):
    if len(argv) < 3:
        print("usage: check_scene.py <html> <duration> [timestamps...]", file=sys.stderr)
        return 2
    html = Path(argv[1]).read_text(encoding="utf-8")
    validate(html)
    duration = float(argv[2])
    stamps = [float(x) for x in argv[3:]] if len(argv) > 3 else [i * 3.0 for i in range(int(duration // 3) + 1)]

    from playwright.sync_api import sync_playwright

    errors = []
    frames = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1, color_scheme="light")
        ctx.add_init_script(VIRTUAL_CLOCK)
        page = ctx.new_page()

        def on_console(m):
            if m.type in ("error", "warning"):
                errors.append(f"console.{m.type}: {m.text}")

        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.on("console", on_console)
        page.on("requestfailed", lambda r: errors.append(f"request failed: {r.url} {r.failure}"))
        page.set_content(html, wait_until="load", timeout=30000)
        page.evaluate("document.fonts.ready")
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        page.evaluate("window.__seek(0)")
        for t in stamps:
            page.evaluate(f"window.__seek({t * 1000})")
            snap = page.evaluate(SNAPSHOT_JS)
            frames.append({"t": t, **snap})
        ctx.close()
        browser.close()

    report = {"ok": not errors, "errors": errors[:20], "frames": frames}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
