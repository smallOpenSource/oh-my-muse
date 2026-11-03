// Symlink availability probe for node:test `skip`.
// True when this machine cannot create a symlink (then symlink-dependent tests skip).
import { mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

let symlinkSkip = false;
try {
  const dir = mkdtempSync(join(tmpdir(), "can-symlink-"));
  writeFileSync(join(dir, "target"), "x");
  symlinkSync(join(dir, "target"), join(dir, "link"));
  rmSync(dir, { recursive: true, force: true });
} catch {
  symlinkSkip = true;
}
export { symlinkSkip };
