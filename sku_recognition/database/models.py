from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class SKU:
    sku_id: str
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    barcode: Optional[str] = None
    description: Optional[str] = None
    active: bool = True


@dataclass(slots=True)
class GalleryImage:
    image_id: str
    sku_id: str
    image_path: str
    width: int
    height: int