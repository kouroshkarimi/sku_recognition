'''
This module is responsible for some preprocessing steps for the GIMMatcher class.
It provides functions to read an image from a file, preprocess the image by resizing and normalizing
it.
'''
import numpy as np
import torch
import torchvision.transforms.functional as F
import cv2



def read_image(path, grayscale=False):
    '''
    Read an image from a file and return it as a numpy array.
    If grayscale is True, the image is read in grayscale mode.
    Args:
        path (str): The path to the image file.
        grayscale (bool): Whether to read the image in grayscale mode. Default is False.
    Returns:
        np.ndarray: The image as a numpy array.
    '''
    if grayscale:
        mode = cv2.IMREAD_GRAYSCALE
    else:
        mode = cv2.IMREAD_COLOR
    image = cv2.imread(str(path), mode)
    if image is None:
        raise ValueError(f'Cannot read image {path}.')
    if not grayscale and len(image.shape) == 3:
        image = image[:, :, ::-1]  # BGR to RGB
    return image


def preprocess(image: np.ndarray, grayscale: bool = False, resize_max: int = None,
               dfactor: int = 8):
    '''
    Preprocess the image by resizing and normalizing it.
    Args:
        image (np.ndarray): The image to preprocess.
        grayscale (bool): Whether to convert the image to grayscale. Default is False.
        resize_max (int): The maximum size to resize the image to. Default is None.
        dfactor (int): The factor by which the image size should be divisible. Default is 8.
    Returns:
        tuple: The preprocessed image and the scale factor.
    '''
    image = image.astype(np.float32, copy=False)
    size = image.shape[:2][::-1]
    scale = np.array([1.0, 1.0])

    if resize_max:
        scale = resize_max / max(size)
        if scale < 1.0:
            size_new = tuple(int(round(x*scale)) for x in size)
            image = resize_image(image, size_new, 'cv2_area')
            scale = np.array(size) / np.array(size_new)

    if grayscale:
        assert image.ndim == 2, image.shape
        image = image[None]
    else:
        image = image.transpose((2, 0, 1))  # HxWxC to CxHxW
    image = torch.from_numpy(image / 255.0).float()

    # assure that the size is divisible by dfactor
    size_new = tuple(map(
            lambda x: int(x // dfactor * dfactor),
            image.shape[-2:]))
    image = F.resize(image, size=size_new)
    scale = np.array(size) / np.array(size_new)[::-1]
    scale = torch.tensor(scale)
    return image, scale



def resize_image(image, size, interp):
    '''
    Resize the image to the specified size using the specified interpolation method.
    Args:
        image (np.ndarray): The image to resize.
        size (tuple): The size to resize the image to.
        interp (str): The interpolation method to use. Must start with 'cv2_'.
        Returns:
            np.ndarray: The resized image.
    '''
    assert interp.startswith('cv2_')
    if interp.startswith('cv2_'):
        interp = getattr(cv2, 'INTER_'+interp[len('cv2_'):].upper())
        h, w = image.shape[:2]
        if interp == cv2.INTER_AREA and (w < size[0] or h < size[1]):
            interp = cv2.INTER_LINEAR
        resized = cv2.resize(image, size, interpolation=interp)
    # elif interp.startswith('pil_'):
    #     interp = getattr(PIL.Image, interp[len('pil_'):].upper())
    #     resized = PIL.Image.fromarray(image.astype(np.uint8))
    #     resized = resized.resize(size, resample=interp)
    #     resized = np.asarray(resized, dtype=image.dtype)
    else:
        raise ValueError(
            f'Unknown interpolation {interp}.')
    return resized
