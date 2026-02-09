import os
import requests
from PIL import Image
from io import BytesIO

# CONFIG
TOTAL_IMAGES = 200
OUTPUT_DIR = "property_images"
ASPECT_RATIO = (4, 3)  # width : height
BASE_WIDTH = 1200  # resize target
MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1MB

os.makedirs(OUTPUT_DIR, exist_ok=True)


def resize_and_compress(img: Image.Image) -> Image.Image:
    """Resize image to fixed aspect ratio and compress under 1MB"""
    w, h = img.size
    target_w = BASE_WIDTH
    target_h = int(target_w * ASPECT_RATIO[1] / ASPECT_RATIO[0])

    img = img.resize((target_w, target_h), Image.LANCZOS)
    return img


def save_under_1mb(img: Image.Image, path: str):
    """Save JPEG under 1MB by adjusting quality"""
    quality = 95
    while quality > 30:
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size = buffer.tell()

        if size <= MAX_SIZE_BYTES:
            with open(path, "wb") as f:
                f.write(buffer.getvalue())
            return

        quality -= 5

    # fallback save
    img.save(path, format="JPEG", quality=30, optimize=True)


for i in range(1, TOTAL_IMAGES + 1):
    try:
        # Random property-style image
        url = "https://picsum.photos/1600/1200"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = resize_and_compress(img)

        filename = f"property_{i:03}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)

        save_under_1mb(img, filepath)

        print(f"✅ Downloaded {filename}")

    except Exception as e:
        print(f"❌ Failed image {i}: {e}")

print("🎉 Done! All images saved.")
