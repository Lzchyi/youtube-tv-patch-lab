#!/usr/bin/env python3
"""Conservative APK metadata and JADX text-reference analysis; never changes the APK."""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

KEYWORDS = ["playbackSpeed", "playback_speed", "setPlaybackSpeed", "speed not available", "unsupported device", "playbackRate", "setPlaybackParameters"]

def run(cmd, timeout=240):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"returncode": p.returncode, "stdout": p.stdout[:12000], "stderr": p.stderr[:3000]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("apk", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("report"))
    args = parser.parse_args()
    apk = args.apk.resolve()
    if not apk.is_file() or apk.suffix.lower() != ".apk":
        parser.error("Provide an existing .apk file")
    args.output.mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256()
    with apk.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(chunk)
    data = {"generated_utc": datetime.now(timezone.utc).isoformat(), "apk_name": apk.name,
            "apk_size_bytes": apk.stat().st_size, "sha256": sha.hexdigest(),
            "keywords": KEYWORDS, "findings": [], "limitations": []}
    if shutil.which("aapt"):
        data["package_metadata"] = run(["aapt", "dump", "badging", str(apk)], 60)
    else:
        data["limitations"].append("aapt unavailable; no package metadata")
    if shutil.which("jadx"):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(["jadx", "--no-res", "-d", tmp, str(apk)], 600)
            data["jadx_result"] = {"returncode": result.get("returncode"), "error": result.get("error"), "stderr": result.get("stderr", "")[:1500]}
            for p in pathlib.Path(tmp).rglob("*"):
                if not p.is_file() or p.suffix not in (".java", ".xml", ".json", ".js"):
                    continue
                try:
                    if p.stat().st_size > 2_000_000:
                        continue
                    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
                    for i, line in enumerate(lines, 1):
                        for keyword in KEYWORDS:
                            if keyword.lower() in line.lower():
                                data["findings"].append({"path": str(p.relative_to(tmp)), "line": i, "keyword": keyword, "excerpt": line.strip()[:220]})
                                if len(data["findings"]) >= 300:
                                    break
                        if len(data["findings"]) >= 300:
                            break
                except OSError:
                    pass
                if len(data["findings"]) >= 300:
                    data["limitations"].append("Findings capped at 300")
                    break
    else:
        data["limitations"].append("jadx unavailable; no decompiled reference search")
    (args.output / "analysis.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    lines = ["# APK research report", "", "**Not evidence of a working patch.**", "", f"APK: `{data['apk_name']}`", f"SHA-256: `{data['sha256']}`", f"Size: {data['apk_size_bytes']} bytes", "", f"Keyword matches: {len(data['findings'])}", ""]
    for finding in data["findings"][:100]:
        lines.append(f"- `{finding['path']}:{finding['line']}` — `{finding['keyword']}` — `{finding['excerpt'].replace(chr(96), chr(39))}`")
    lines += ["", "## Limitations", ""] + [f"- {x}" for x in data["limitations"]]
    lines += ["", "Keyword matches do not establish which code path enforces playback-speed eligibility."]
    (args.output / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()
