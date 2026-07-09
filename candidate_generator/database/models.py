'''
This module defines the SKU and GalleryImage data classes, which represent
the structure of SKU and gallery image records in the database.
'''
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class SKU:
    '''
    SKU is a data class that represents a product SKU in the database.
    '''
    sku_id: str
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    barcode: Optional[str] = None
    description: Optional[str] = None
    active: bool = True


@dataclass(slots=True)
class GalleryImage:
    '''
    GalleryImage is a data class that represents a gallery image in the database.
    '''
    image_id: str
    sku_id: str
    image_path: str
    width: int
    height: int
