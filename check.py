"""Check every recording here against the annotation files beside it.

    uv run python -I check.py [--tickwave BIN] [ROOT]

For each `NAME.annotations.toml` under ROOT (this folder by default): `tickwave annotations check`
holds the files to the recording, and the recording carries those same files. A page shows what a
recording carries, so a file regenerated beside it without bundling again would pass the first check
and still differ on the page. Bundling is deterministic, so a recording carries its files exactly
when bundling it with them again writes the same bytes."""
import argparse
import filecmp
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--tickwave", default="tickwave")
    args = ap.parse_args()
    problems, checked = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for toml in sorted(args.root.rglob("*.annotations.toml")):
            rec = toml.parent / tomllib.loads(toml.read_text())["recording"]
            checked += 1
            run = subprocess.run([args.tickwave, "annotations", "check", str(rec), str(toml)],
                                 capture_output=True, text=True)
            if run.returncode:
                problems.append(f"{toml.relative_to(args.root)}: {(run.stdout + run.stderr).strip()}")
                continue
            again = Path(tmp) / rec.name
            run = subprocess.run([args.tickwave, "bundle", str(rec), str(toml), "-o", str(again)],
                                 capture_output=True, text=True)
            if run.returncode:
                problems.append(f"{rec.relative_to(args.root)}: bundle failed: {(run.stdout + run.stderr).strip()}")
            elif not filecmp.cmp(rec, again, shallow=False):
                problems.append(f"{rec.relative_to(args.root)} carries other annotations than the files"
                                f" beside it: bundle it again (README)")
    for p in problems:
        print(p)
    print(f"{checked} recordings, {len(problems)} problems")
    return 1 if problems or not checked else 0


if __name__ == "__main__":
    sys.exit(main())
