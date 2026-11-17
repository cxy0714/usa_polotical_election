#!/usr/bin/env python
"""Identify the two candidates inside the South Carolina keyframes (SFace, cosine).

The first pass only counted faces, so the frame galleries mixed the candidates with moderators,
crowd members and other candidates. This pass gives every face an embedding and asks a
nearest-neighbour question: does it look more like Andrews or like Graham?

References are licensed photographs already in `04_visual_archive/`, filtered to frames where the
candidate is the obvious subject. Anything that does not clear both the similarity floor and the
margin between the two classes is labelled `unknown` rather than guessed.

Output: `10_video_frames/keyframes_identity.csv`
  frame_id, identity, identity_sim, second_identity, second_sim,
  faces, candidate_faces, identity_note

No appearance judgement is made or recorded.
"""
import csv
import os
import re
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MODELS = os.path.join(HERE, "models")
ARCH = os.path.join(ROOT, "04_visual_archive")
KF_CSV = os.path.join(ROOT, "10_video_frames", "keyframes.csv")
OUT_CSV = os.path.join(ROOT, "10_video_frames", "keyframes_identity.csv")

DET_CONF = 0.6
SIM_THRESHOLD = 0.363   # OpenCV's published SFace cosine threshold
MARGIN = 0.05
MIN_FACE_PX = 30

# Photographs where the named candidate is not the subject, or that carry no face at all.
NOISE = re.compile(
    r"signature|butter_cow|okra|democratic_senators|oversight_of_the|kash_patel|"
    r"chuck_grassley|jim_clyburn|tim_scott|departure_october|campaign_building$|"
    r"britt|ts_graham",
    re.I)


def candidate_of(name):
    low = name.lower()
    if "andrew" in low:
        return "ANDREWS"
    if "darline" in low or "graham" in low:
        return "GRAHAM"
    return None


def load_models():
    det = cv2.FaceDetectorYN.create(os.path.join(MODELS, "yunet.onnx"), "", (640, 640),
                                    DET_CONF, 0.3, 200)
    rec = cv2.FaceRecognizerSF.create(os.path.join(MODELS, "sface.onnx"), "")
    return det, rec


def prepare(img):
    """Frames are 960 px wide; doubling the pixels a small podium face occupies is where recall is
    lost on the Graham clips. Detection and embedding must both use the scaled image."""
    if img.shape[1] < 1600:
        return cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    return img


def detect(det, img):
    h, w = img.shape[:2]
    det.setInputSize((w, h))
    _r, faces = det.detect(img)
    return [] if faces is None else list(faces)


def embed(rec, img, face):
    aligned = rec.alignCrop(img, face)
    feat = rec.feature(aligned).flatten().astype(np.float64)
    n = np.linalg.norm(feat)
    return feat / (n if n > 0 else 1.0)


def build_refs(det, rec):
    """Archive photographs plus the documented bootstrap crops, if any."""
    refs = []
    for who in ("andrews", "graham"):
        folder = os.path.join(ARCH, who, "campaign")
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            if NOISE.search(name):
                continue
            label = candidate_of(name)
            if not label:
                continue
            img = cv2.imread(os.path.join(folder, name))
            if img is None:
                continue
            img = prepare(img)
            faces = detect(det, img)
            if not faces:
                continue
            face = max(faces, key=lambda f: f[2] * f[3])
            if face[2] < MIN_FACE_PX:
                continue
            # A reference must be a photograph *of* the candidate, not a group shot where they are
            # one face among many: require the face to occupy at least 3% of the frame.
            if (face[2] * face[3]) / float(img.shape[0] * img.shape[1]) < 0.03:
                continue
            try:
                refs.append((label, embed(rec, img, face), name))
            except cv2.error:
                continue
    extra = os.path.join(HERE, "refs_extra")
    if os.path.isdir(extra):
        for label in sorted(os.listdir(extra)):
            folder = os.path.join(extra, label)
            if not os.path.isdir(folder):
                continue
            for name in sorted(os.listdir(folder)):
                if not name.lower().endswith((".jpg", ".png")):
                    continue
                img = cv2.imread(os.path.join(folder, name))
                if img is None:
                    continue
                img = prepare(img)
                faces = detect(det, img)
                if not faces:
                    continue
                face = max(faces, key=lambda f: f[2] * f[3])
                try:
                    refs.append((label, embed(rec, img, face), "bootstrap:" + name))
                except cv2.error:
                    continue
    return refs


def sanity(refs):
    import itertools
    same, cross = [], []
    for (l1, f1, _), (l2, f2, _) in itertools.combinations(refs, 2):
        s = float(np.dot(f1, f2))
        (same if l1 == l2 else cross).append(s)
    if same and cross:
        print(f"  ref sanity: same-class mean {np.mean(same):.3f} "
              f"({len(same)} pairs) vs cross-class mean {np.mean(cross):.3f} ({len(cross)} pairs)")


def classify(feat, refs):
    best = {}
    for lab, f, _name in refs:
        s = float(np.dot(feat, f))
        if lab not in best or s > best[lab]:
            best[lab] = s
    ranked = sorted(best.items(), key=lambda kv: kv[1], reverse=True)
    if len(ranked) < 2:
        return ranked[0][0], ranked[0][1], "", -1.0
    return ranked[0][0], ranked[0][1], ranked[1][0], ranked[1][1]


def main():
    det, rec = load_models()
    refs = build_refs(det, rec)
    counts = {}
    for lab, _, _ in refs:
        counts[lab] = counts.get(lab, 0) + 1
    print(f"reference embeddings: {len(refs)} {counts}")
    if not refs:
        print("no references; aborting")
        return 1
    sanity(refs)

    rows = list(csv.DictReader(open(KF_CSV, encoding="utf-8")))
    print(f"keyframes: {len(rows)}")
    out = []
    tally = {}
    for i, row in enumerate(rows, 1):
        path = os.path.join(ROOT, "10_video_frames", row["file"])
        img = cv2.imread(path)
        if img is None:
            out.append(dict(frame_id=row["frame_id"], identity="nofile", identity_sim="unknown",
                            second_identity="", second_sim="", faces="unknown",
                            candidate_faces="0", identity_note="image could not be read"))
            continue
        img = prepare(img)
        faces = detect(det, img)
        if not faces:
            out.append(dict(frame_id=row["frame_id"], identity="noface", identity_sim="unknown",
                            second_identity="", second_sim="", faces="0",
                            candidate_faces="0", identity_note="YuNet found no face above 0.6"))
            tally["noface"] = tally.get("noface", 0) + 1
            continue

        best_cand = ("other", -1.0, "", -1.0)
        cand_faces = 0
        for face in faces:
            if face[2] < MIN_FACE_PX:
                continue
            try:
                feat = embed(rec, img, face)
            except cv2.error:
                continue
            top, top_sim, sec, sec_sim = classify(feat, refs)
            confident = top in ("ANDREWS", "GRAHAM") and top_sim >= SIM_THRESHOLD \
                and (top_sim - sec_sim) >= MARGIN
            if confident:
                cand_faces += 1
                if top_sim > best_cand[1]:
                    best_cand = (top, top_sim, sec, sec_sim)
            elif top in ("ANDREWS", "GRAHAM") and top_sim > best_cand[1]:
                best_cand = ("other", best_cand[1], top, top_sim)

        if best_cand[0] in ("ANDREWS", "GRAHAM"):
            identity = best_cand[0]
            note = f"{cand_faces} candidate face(s) above threshold"
        elif cand_faces == 0 and best_cand[2] in ("ANDREWS", "GRAHAM"):
            identity = "unknown"
            note = (f"below threshold: nearest candidate {best_cand[2]} at "
                    f"cosine {best_cand[3]:.3f}")
        else:
            identity = "other"
            note = "no face cleared the threshold; crowd, moderator or bystander"
        tally[identity] = tally.get(identity, 0) + 1
        out.append(dict(
            frame_id=row["frame_id"], identity=identity,
            identity_sim=(f"{best_cand[1]:.3f}" if best_cand[1] >= 0 else "unknown"),
            second_identity=best_cand[2], second_sim=(f"{best_cand[3]:.3f}" if best_cand[3] >= 0 else ""),
            faces=str(len(faces)), candidate_faces=str(cand_faces), identity_note=note))
        if i % 50 == 0:
            print(f"  {i}/{len(rows)}")

    fields = ["frame_id", "identity", "identity_sim", "second_identity", "second_sim",
              "faces", "candidate_faces", "identity_note"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(f"wrote {OUT_CSV}: {len(out)} rows | {tally}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
