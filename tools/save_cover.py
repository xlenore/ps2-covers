"""
This tool monitors the clipboard for images, then waits for a name to be copied to the clipboard
And saves in covers directory
"""
from pathlib import Path
import sys
import os
import time
import io
import hashlib
from PIL import Image, ImageGrab
import tkinter as tk

SAVE_SIZE = (512, 736)
SCRIPT_DIR = Path(__file__).resolve().parent
SAVE_DIR = SCRIPT_DIR.parent / "covers" / "default"


def compute_fingerprint_from_clipboard_raw(raw):
    if raw is None:
        return None
    if isinstance(raw, (list, tuple)) and raw:
        try:
            return f"FILE:{str(Path(raw[0]).resolve())}"
        except Exception:
            return None
    try:
        if hasattr(raw, "tobytes") or hasattr(raw, "save"):
            buf = io.BytesIO()
            try:
                raw.save(buf, format="PNG")
            except Exception:
                if hasattr(raw, "resize"):
                    raw = raw
                else:
                    return None
                raw.save(buf, format="PNG")
            h = hashlib.md5(buf.getvalue()).hexdigest()
            return f"IMG:{h}"
    except Exception:
        return None
    return None

def get_image_from_clipboard():
    raw = ImageGrab.grabclipboard()
    if raw is None:
        return None, None
    if isinstance(raw, (list, tuple)) and raw:
        try:
            img = Image.open(raw[0])
            fp = compute_fingerprint_from_clipboard_raw(raw)
            return img, fp
        except Exception:
            return None, None
    try:
        if hasattr(raw, "resize") or hasattr(raw, "save"):
            fp = compute_fingerprint_from_clipboard_raw(raw)
            return raw, fp
    except Exception:
        pass
    return None, None


def get_clipboard_text():
    try:
        root = tk.Tk()
        root.withdraw()
        try:
            text = root.clipboard_get()
        except Exception:
            text = None
        root.destroy()
        return text
    except Exception:
        return None

def sanitize_name(name: str) -> str:
    name = os.path.basename(name).strip()
    if name.lower().endswith(".jpg") or name.lower().endswith(".jpeg"):
        name = ".".join(name.split(".")[:-1])
    return "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in name).strip() or "cover"

def main():
    covers_dir = SAVE_DIR
    covers_dir.mkdir(parents=True, exist_ok=True)

    last_fp = None
    print("Waiting for images on the clipboard. Press Ctrl+C to exit.")
    try:
        while True:
            img, fp = get_image_from_clipboard()
            if img is None or fp is None:
                time.sleep(0.5)
                continue
            if fp == last_fp:
                time.sleep(0.5)
                continue

            last_fp = fp
            print("Image detected in the clipboard.")

            print("Waiting for name on the clipboard (must contain '-')...")
            name = None
            while True:
                text = get_clipboard_text()
                if text:
                    cleaned = "".join(text.split())
                    if "-" in cleaned:
                        name = sanitize_name(cleaned)
                        break
                time.sleep(0.5)

            out_path = covers_dir / f"{name}.jpg"

            try:
                img_converted = img.convert("RGB")
                img_resized = img_converted.resize(SAVE_SIZE, Image.LANCZOS)
                img_resized.save(out_path, format="JPEG", quality=95)
            except Exception as e:
                print("Error processing or saving image:", e)
                continue

            print(f"Image saved to: {out_path}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()