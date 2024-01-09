import cv2
import numpy as np

def apply_mask(image, mask, alpha=0.5):
    """Apply the given mask to the image.
    """
    ic = image.copy()
    for c in range(3):
        ic[:, :, c] = np.where(mask[:,:,c] != 0,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * mask[:, :, c],
                                  image[:, :, c])
    # image = (1 - alpha) * image + alpha * mask
    return ic

def binary_masking(img, height, mask):
    pass