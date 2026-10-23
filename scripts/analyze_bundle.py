#!/usr/bin/env python3
"""Inspect APKM metadata and base APK without publishing copyrighted binaries."""
import argparse,hashlib,json,pathlib,subprocess,tempfile,zipfile
from datetime import datetime,timezone

def digest(b): return hashlib.sha256(b).hexdigest()
def run(args,timeout=600):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
        return {"exit_code":p.returncode,"stdout":p.stdout[:12000],"stderr":p.stderr[:3000]}
    except (OSError,subprocess.TimeoutExpired) as exc:
        return {"error":str(exc)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("bundle",type=pathlib.Path)
    ap.add_argument("--output",type=pathlib.Path,default=pathlib.Path("report"))
    args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    result={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"input_sha256":digest(args.bundle.read_bytes()),"components":[],"findings":[],"limitations":[]}
    terms=["playbackSpeed","playback_speed","playbackRate","not available on this device","setPlaybackParameters","playback speed"]
    with zipfile.ZipFile(args.bundle) as archive, tempfile.TemporaryDirectory() as tmp:
        names=archive.namelist()
        if "base.apk" not in names: raise SystemExit("APKM missing base.apk")
        for name in names:
            if name.endswith(".apk"):
                blob=archive.read(name)
                result["components"].append({"name":name,"size":len(blob),"sha256":digest(blob)})
        base=pathlib.Path(tmp)/"base.apk"
        base.write_bytes(archive.read("base.apk"))
        result["aapt"]=run(["aapt","dump","badging",str(base)],60)
        decoded=pathlib.Path(tmp)/"decoded"
        result["jadx"]=run(["jadx","--no-res","--threads-count","2","-d",str(decoded),str(base)])
        for path in decoded.rglob("*"):
            if not path.is_file() or path.suffix not in (".java",".js",".xml",".json") or path.stat().st_size>2_000_000: continue
            try: lines=path.read_text(encoding="utf-8",errors="replace").splitlines()
            except OSError: continue
            for index,line in enumerate(lines,1):
                matches=[t for t in terms if t.casefold() in line.casefold()]
                if matches:
                    result["findings"].append({"file":str(path.relative_to(decoded)),"line":index,"terms":matches,"excerpt":line.strip()[:240]})
                if len(result["findings"])>=400: break
            if len(result["findings"])>=400:
                result["limitations"].append("Findings truncated at 400")
                break
    result["limitations"].append("Keyword matches alone do not identify the enforcement mechanism or prove a working patch.")
    (args.output/"analysis.json").write_text(json.dumps(result,indent=2))
    report=["# YouTube TV binary investigation","","**Research only: no patch generated.**","",f"Input SHA-256: `{result['input_sha256']}`","","## Components"]
    report += [f"- {c['name']}: {c['size']} bytes, SHA-256 `{c['sha256']}`" for c in result["components"]]
    report += ["","## Package metadata","", "```text",result["aapt"].get("stdout","")[:3000],"```","","## Relevant references"]
    report += [f"- `{x['file']}:{x['line']}` — {', '.join(x['terms'])}: {x['excerpt'].replace(chr(96),chr(39))}" for x in result["findings"][:150]]
    report += ["","## Limitations"]+[f"- {x}" for x in result["limitations"]]
    (args.output/"REPORT.md").write_text("\n".join(report)+"\n")
    print("Analysis completed:",len(result["findings"]),"keyword references")
if __name__=="__main__":main()
