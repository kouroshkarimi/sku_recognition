'''
This module defines the GalleryScanner class, which is responsible 
for scanning a gallery directory structure to identify SKU folders
and their associated images. It collects metadata about each SKU and image,
including unique identifiers, image paths, and dimensions.
The scanner supports various image formats and organizes the data for
further processing or analysis.
'''
from pathlib import Path
import uuid
from PIL import Image


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


class GalleryScanner:
    '''
    A class to scan a gallery directory for SKU folders and images.
    Attributes:
        gallery_path (Path): The path to the gallery directory.
    Methods:
        scan(): Scans the gallery directory and returns lists of SKUs and images.
    '''
    def __init__(self, gallery_path: Path):
        self.gallery_path = gallery_path

    def scan(self):
        '''
        Scan the gallery directory for SKU folders and images.
        Returns:
            skus (list): A list of dictionaries containing SKU metadata.
            images (list): A list of dictionaries containing image metadata.
        '''
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
