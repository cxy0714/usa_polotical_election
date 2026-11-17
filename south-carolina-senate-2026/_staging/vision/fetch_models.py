"""Download the OpenCV YuNet detector and SFace recogniser ONNX weights.

Model weights are excluded from the Git repository (~38 MB) because they are
third-party binaries; this script restores them.

Sources: opencv/opencv_zoo (Apache-2.0 / MIT as noted in that repo), served through
media.githubusercontent.com so the Git-LFS payload is fetched instead of the pointer.

The shell's own network stack is restricted on this machine (curl / Invoke-WebRequest
fail with schannel SEC_E_NO_CREDENTIALS), so every request here goes through
Python's urllib with an explicit User-Agent.

    python south-carolina-senate-2026/_staging/vision/fetch_models.py
"""
import sys
import urllib.request
from pathlib import Path

MODELS = Path(__file__).resolve().parent / "models"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) sc-senate-2026-research/1.0"

FILES = [
    ("yunet.onnx",
     "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
     200_000),
    ("sface.onnx",
     "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx",
     30_000_000),
]


def fetch(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as fh:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            fh.write(chunk)


def main():
    MODELS.mkdir(parents=True, exist_ok=True)
    for name, url, min_bytes in FILES:
        out = MODELS / name
        if out.exists() and out.stat().st_size >= min_bytes:
            print("ok", name, out.stat().st_size)
            continue
        print("downloading", name, flush=True)
        try:
            fetch(url, out)
        except Exception as e:  # noqa: BLE001
            print("FAILED", name, type(e).__name__, e)
            return 1
        size = out.stat().st_size
        if size < min_bytes:
            print("WARNING: suspicious size", size, "- file may be a Git-LFS pointer")
            return 1
        print("wrote", name, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
