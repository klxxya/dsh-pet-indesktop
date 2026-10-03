"""DIAG 专用：macOS runner 段错误后抓取最新 DiagnosticReports .ips 的原生回溯。"""
import glob
import json
import os
import sys


def main() -> int:
    pattern = os.path.expanduser("~/Library/Logs/DiagnosticReports/*.ips")
    files = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not files:
        print("no .ips crash reports found")
        return 0
    latest = files[-1]
    print("=== latest crash report:", latest, "===")
    lines = open(latest, encoding="utf-8", errors="replace").read().splitlines()
    meta = json.loads(lines[0]) if lines else {}
    body = json.loads("\n".join(lines[1:])) if len(lines) > 1 else {}
    print("process:", meta.get("name"), "| exception:", json.dumps(body.get("exception", {})))
    threads = body.get("threads", [])
    ft = body.get("faultingThread", 0)
    images = body.get("usedImages", [])
    print("faultingThread:", ft)
    if ft < len(threads):
        for f in threads[ft].get("frames", [])[:25]:
            idx = f.get("imageIndex")
            img = images[idx] if idx is not None and idx < len(images) else {}
            print("  ", img.get("name", "?"), "::", f.get("symbol", "?"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
