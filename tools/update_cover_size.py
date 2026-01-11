#Note: This tool still in WIP, needs an IA to calculate the best crop area.


from pathlib import Path
from PIL import Image
from PIL import ImageOps

TARGET_SIZE = (512, 736)
IGNORE_LOWER_RESOLUTION = True

def find_invalid_covers(covers_dir: Path, target_size: tuple) -> list:
    invalid = []
    if not covers_dir.exists():
        raise FileNotFoundError(f"Directory not found: {covers_dir}")

    for p in sorted(covers_dir.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_file():
            continue
        try:
            with Image.open(p) as img:
                if img.size != tuple(target_size):
                    if IGNORE_LOWER_RESOLUTION and (img.width < target_size[0] or img.height < target_size[1]):
                        continue
                    invalid.append(p)
        except Exception:
            invalid.append(p)
    return invalid

def update_cover_sizes(covers_dir: Path, target_size: tuple, files: list = None):
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.LANCZOS

    if files is None:
        iterable = sorted(covers_dir.iterdir(), key=lambda x: x.name.lower())
    else:
        iterable = sorted(files, key=lambda x: x.name.lower())

    for p in iterable:
        if not p.is_file():
            continue
        try:
            with Image.open(p) as img:
                img = ImageOps.exif_transpose(img)

                if img.size != tuple(target_size):
                    new = ImageOps.fit(img, target_size, method=resample, centering=(0.5, 0.5))

                    save_kwargs = {}
                    info = img.info
                    if "icc_profile" in info:
                        save_kwargs["icc_profile"] = info.get("icc_profile")

                    suffix = p.suffix.lower()
                    if suffix in (".jpg", ".jpeg"):
                        if new.mode in ("RGBA", "LA"):
                            background = Image.new("RGB", new.size, (255, 255, 255))
                            background.paste(new, mask=new.split()[-1])
                            new = background
                        else:
                            new = new.convert("RGB")
                        save_kwargs.update({"quality": 95, "optimize": True, "subsampling": 0})
                    elif suffix == ".png":
                        save_kwargs.update({"optimize": True})

                    new.save(p, **save_kwargs)
                    print(f"Updated size for {p.name} to {target_size}.")
        except Exception as e:
            print(f"Error processing {p.name}: {e}")


def main():
    main_root = Path(__file__).parent.parent.resolve()
    covers_dir = main_root / "covers" / "default"

    try:
        invalid_list = find_invalid_covers(covers_dir, TARGET_SIZE)
    except FileNotFoundError as e:
        print(e)
        return

    if invalid_list:
        for n in invalid_list:
            print(" -", n)
        print(f"Found {len(invalid_list)} images with size different from {TARGET_SIZE}:")
        input(f"Press Enter to update {len(invalid_list)} images to the correct size...")
        update_cover_sizes(covers_dir, TARGET_SIZE, invalid_list)

    else:
        print(f"All images in {covers_dir} have size {TARGET_SIZE}.")


if __name__ == "__main__":
    main()
