import cv2
import numpy as np
import os
import pathlib
from .config import AnalysisConfig

class ImageLoader:
    @staticmethod
    def load(image_path: str) -> np.ndarray | None:
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at ${image_path}")
            return None
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: OpenCV could not read image at ${image_path}")
        return image
    
class ImageSaver:
    @staticmethod
    def save(image: np.ndarray, directory: str, filename: str) -> str | None:
        os.makedirs(directory, exist_ok=True)
        full_path = str(pathlib.Path(directory) / filename)
        try:
            cv2.imwrite(full_path, image)
            return full_path
        except Exception as e:
            print(f"Warning: Could not save image {full_path}: {e}")
            return None
        
class ImageProcessor:
    def __init__(self, config: AnalysisConfig):
        self.config = config

    def resize(self, image: np.ndarray) -> np.ndarray:
        original_height, original_width = image.shape[:2]
        if original_width == 0: return image

        desired_width = self.config.DESIRED_IMAGE_WIDTH
        if original_width < desired_width:
            scale_factor = desired_width / original_width
            desired_height = int(original_height * scale_factor)
        else:
            aspect_ratio = original_height / original_width
            desired_height = int(desired_width * aspect_ratio)

        return cv2.resize(image, (desired_width, desired_height), interpolation=cv2.INTER_AREA)
    
    def convert_to_hsv(self, bgr_image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    
    def apply_gaussian_blur(self, image: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(image, self.config.GAUSSIAN_BLUR_KERNEL_SIZE, 0)
    
    def preprocess(self, bgr_image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Resizes, then creates HSV and blurred HSV versions"""
        resized_bgr = self.resize(bgr_image)
        hsv_image = self.convert_to_hsv(resized_bgr)
        blurred_hsv_image = self.apply_gaussian_blur(hsv_image)
        return self.resize(bgr_image.copy()), blurred_hsv_image