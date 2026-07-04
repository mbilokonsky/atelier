"""The `atelier` command — the pipeline's front door.

  atelier paint <render.png> <aux.npz> <engine> <out.png> [seed] [key=val ...]
  atelier bindings                          # print every engine's knob-binding table
  atelier render <scene.py> <out_dir> [args ...]   # run a scene headless (repo checkout)
  atelier vendor <name> [--install]         # resolve/install blender, mpfb, ...

`paint` and `bindings` are pure Python (numpy + Pillow) and work from any pip install.
`render` and `vendor` drive Blender and expect a repository checkout (they look upward
from the working directory for vendor/manifest.json, or honor ATELIER_ROOT).
"""

import os
import runpy
import subprocess
import sys
from pathlib import Path


def _repo_root():
    env = os.environ.get("ATELIER_ROOT")
    if env and (Path(env) / "vendor" / "manifest.json").exists():
        return Path(env)
    p = Path.cwd()
    for cand in (p, *p.parents):
        if (cand / "vendor" / "manifest.json").exists() and (cand / "core" / "blender" / "runner.py").exists():
            return cand
    return None


def main():
    argv = sys.argv[1:]
    cmd = argv[0] if argv else "help"

    if cmd in ("paint", "bindings"):
        sys.argv = ["atelier-styles"] + (argv[1:] if cmd == "paint" else ["bindings"])
        runpy.run_module("atelier.styles", run_name="__main__", alter_sys=True)
        return 0

    if cmd in ("render", "vendor"):
        root = _repo_root()
        if root is None:
            print("atelier: this command drives Blender and needs a repository checkout.\n"
                  "Run it from inside a clone of the atelier repo (or set ATELIER_ROOT).",
                  file=sys.stderr)
            return 2
        if cmd == "render":
            script = root / "core" / "blender" / "runner.py"
        else:
            script = root / "vendor" / "bootstrap.py"
        return subprocess.call([sys.executable, str(script)] + argv[1:], cwd=str(root))

    print(__doc__)
    return 0 if cmd in ("help", "-h", "--help") else 2


if __name__ == "__main__":
    sys.exit(main())
