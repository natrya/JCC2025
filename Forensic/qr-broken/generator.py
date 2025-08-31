#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
from typing import Tuple
from io import BytesIO

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    from PIL import Image, ImageDraw
except Exception as e:
    print("Error: no module named 'qrcode'")
    raise

def make_qr(flag: str, box_size: int = 10, border: int = 4) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,                 
        error_correction=ERROR_CORRECT_H,
        box_size=box_size,
        border=border,                
    )
    qr.add_data(flag)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img

def occlude_rect(img: Image.Image, rel_box: Tuple[float, float, float, float], fill=(255, 255, 255)):
    w, h = img.size
    x0 = int(rel_box[0] * w)
    y0 = int(rel_box[1] * h)
    x1 = int(rel_box[2] * w)
    y1 = int(rel_box[3] * h)
    draw = ImageDraw.Draw(img)
    draw.rectangle([x0, y0, x1, y1], fill=fill)

def add_salt_pepper(img: Image.Image, ratio: float = 0.01):
    if ratio <= 0:
        return
    w, h = img.size
    n = int(w * h * ratio)
    px = img.load()
    for _ in range(n):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        # 50% hitam, 50% putih
        px[x, y] = (0, 0, 0) if random.random() < 0.5 else (255, 255, 255)

def erase_line(img: Image.Image, y_rel: float = 0.52, thickness_rel: float = 0.02, fill=(255, 255, 255)):
    w, h = img.size
    y = int(h * y_rel)
    t = max(1, int(h * thickness_rel))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, max(0, y - t // 2), w, min(h, y + t // 2)], fill=fill)

def corrupt_qr(img: Image.Image) -> Image.Image:
    corrupted = img.copy()
    occlude_rect(corrupted, rel_box=(0.28, 0.35, 0.58, 0.62), fill=(255, 255, 255))
    erase_line(corrupted, y_rel=0.54, thickness_rel=0.018, fill=(255, 255, 255))
    add_salt_pepper(corrupted, ratio=0.15)
    return corrupted

def save_as_png_without_extension(img: Image.Image, path_no_ext: str):
    img.save(path_no_ext, format="PNG")

def main():
    flag = "JCC{iph0n3_16_pr0_max_aku_b1sa_bac4_ini_kok}"
    base = make_qr(flag, box_size=12, border=4)

    base.save("soal.png")

    broken = corrupt_qr(base)

    save_as_png_without_extension(broken, "broken.png")



if __name__ == "__main__":
    main()
