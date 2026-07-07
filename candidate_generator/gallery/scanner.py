from pathlib import Path
from PIL import Image
import uuid

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


class GalleryScanner:

    def __init__(self, gallery_path: Path):
        self.gallery_path = gallery_path

    def scan(self):

        skus = []
        images = []

        for sku_folder in sorted(self.gallery_path.iterdir()):

            if not sku_folder.is_dir():
                continue

            sku_id = sku_folder.name

            skus.append({
                "sku_id": sku_id
            })

            for image_path in sorted(sku_folder.iterdir()):

                if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                    continue

                width, height = Image.open(image_path).size

                images.append({
                    "image_id": str(uuid.uuid4()),
                    "sku_id": sku_id,
                    "image_path": str(image_path.relative_to(self.gallery_path.parent.parent)),
                    "width": width,
                    "height": height
                })

        return skus, images