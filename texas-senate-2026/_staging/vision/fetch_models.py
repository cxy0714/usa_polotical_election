"""Download the OpenCV YuNet detector and SFace recogniser ONNX weights.

Model weights are excluded from the Git repository (~37 MB) because they are
third-party binaries; this script restores them.

Sources: opencv/opencv_zoo (Apache-2.0 / MIT as noted in that repo), served through
media.githubusercontent.com so the Git-LFS payload is fetched instead of the pointer.

    python texas-senate-2026/_staging/vision/fetch_models.py
"""
import sys
import urllib.request
from pathlib import Path

MODELS = Path(__file__).resolve().parent / "models"

FILES = [
    ("yunet.onnx",
     "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
     200_000),
    ("sface.onnx",
     "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx",
     30_000_000),
]


def main():
    MODELS.mkdir(parents=True, exist_ok=True)
    for name, url, min_bytes in FILES:
        out = MODELS / name
        if out.exists() and out.stat().st_size >= min_bytes:
            print("ok", name, out.stat().st_size)
            continue
        print("downloading", name, flush=True)
        urllib.request.urlretrieve(url, out)
        size = out.stat().st_size
        if size < min_bytes:
            print("WARNING: suspicious size", size, "- file may be a Git-LFS pointer")
            return 1
        print("wrote", name, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
