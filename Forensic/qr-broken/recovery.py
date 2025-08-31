#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# recover_qr.py
#
# Recovery preprocessing untuk QR yang terkorupsi parah (salt & pepper 30%).
#
# Dependencies:
#   pip install pillow pyzbar opencv-python
#   (di Linux, pyzbar butuh libzbar0: sudo apt install libzbar0)

import sys
import cv2
import numpy as np
from PIL import Image, ImageFilter
from pyzbar.pyzbar import decode

def preprocess(img: Image.Image) -> Image.Image:
    """
    Bersihkan noise salt & pepper:
    - Convert grayscale
    - Median filter beberapa kali
    - Adaptive threshold
    """
    # ke numpy grayscale
    gray = np.array(img.convert("L"))

    # median filter kuat (hilangin salt pepper)
    cleaned = cv2.medianBlur(gray, 5)   # kernel 5x5

    # adaptive threshold → hitam-putih biner
    bw = cv2.adaptiveThreshold(
        cleaned, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        25,   # block size
        5     # C constant
    )

    # upscale biar scanner gampang
    bw_big = cv2.resize(bw, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)

    return Image.fromarray(bw_big)

def try_decode(img: Image.Image):
    """
    Coba decode QR pakai pyzbar.
    """
    data = decode(img)
    if not data:
        return None
    # ambil semua hasil
    results = []
    for d in data:
        results.append(d.data.decode(errors="ignore"))
    return results

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} soal.broken")
        sys.exit(1)

    path = "broken.png"
    img = Image.open(path)

    # Preprocess
    fixed = preprocess(img)
    fixed.save("recovered.png")
    print("[+] Preprocessed image saved as recovered.png")

    # Try decode
    results = try_decode(fixed)
    if results:
        print("[+] Decode success!")
        for r in results:
            print("    ->", r)
    else:
        print("[-] Decode failed. Coba tweak parameter median/threshold.")

if __name__ == "__main__":
    main()
