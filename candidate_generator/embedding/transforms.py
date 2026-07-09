'''
This module defines the build_transform function,
which constructs a series of image transformations
to preprocess images for embedding extraction using
the DINOv2 model. The transformations include resizing,
normalization, and conversion to tensor format,
ensuring that the input images are in the appropriate format
for the model.
'''
from torchvision import transforms


def build_transform(image_size: int = 518):
    '''
    Build a series of image transformations for preprocessing.
    Args:
        image_size (int): The size to which the image will be resized.
    Returns:
        transforms.Compose: A composition of image transformations.
    '''
    return transforms.Compose(
        [
            transforms.Resize(
                (image_size, image_size),
                antialias=True,
            ),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225),
            ),
        ]
    )
