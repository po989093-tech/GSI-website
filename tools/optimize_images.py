#!/usr/bin/env python3
"""
Simple image optimizer: generates resized WebP and PNG variants for images in the workspace.
Run from project root.
"""
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / 'images'
OUT_DIR = IMAGES_DIR / 'optimized'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# sizes to generate (widths)
SIZES = [48, 96, 150, 200, 400, 800]

def process_image(p: Path):
    try:
        img = Image.open(p)
    except Exception as e:
        print(f"Skipping {p} (open error): {e}")
        return
    img = img.convert('RGBA') if img.mode in ('LA','P') or img.mode=='RGBA' else img.convert('RGB')
    name = p.stem
    for w in SIZES:
        # maintain aspect ratio
        ratio = w / img.width
        h = max(1, int(img.height * ratio))
        resized = img.resize((w, h), Image.LANCZOS)
        webp_path = OUT_DIR / f"{name}-{w}.webp"
        png_path = OUT_DIR / f"{name}-{w}.png"
        try:
            resized.save(webp_path, 'WEBP', quality=85, method=6)
            resized.save(png_path, 'PNG', optimize=True)
            print(f"Wrote: {webp_path} and {png_path}")
        except Exception as e:
            print(f"Failed to write {name}-{w}: {e}")


def main():
    # process logo.png and any jpg/png in images/projects
    files = []
    logo = IMAGES_DIR / 'logo.png'
    if logo.exists():
        files.append(logo)
    # process project images
    projects_dir = IMAGES_DIR / 'projects'
    if projects_dir.exists():
        for p in projects_dir.iterdir():
            if p.suffix.lower() in ('.png', '.jpg', '.jpeg'):
                files.append(p)
    if not files:
        print('No images found to process.')
        return
    for f in files:
        process_image(f)

if __name__ == '__main__':
    main()
