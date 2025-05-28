import cv2
import numpy as np
from .config import AnalysisConfig

class ColorIdentifier:
    def __init__(self, config: AnalysisConfig):
        self.config = config

    def extract_average_hsv(self, hsv_image: np.ndarray, roi: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
        x, y, w, h = roi
        if w <= 0 or h <= 0: return None
        patch = hsv_image[y : y + h, x : x + w]
        if patch.size == 0: return None
        return tuple[np.mean(patch, axis=(0,1)).astype(int)]
    
    def get_color_char_from_hsv(self, hsv_tuple: tuple[int, int, int]) -> str:
        h, s, v = hsv_tuple
        
        red_low_def = self.config.COLOR_DEFINITIONS["RED_LOW"]
        red_high_def = self.config.COLOR_DEFINITIONS["RED_HIGH"]
        if (red_low_def[0][0] <= h <= red_low_def[1][0] or \
            red_high_def[0][0] <= h <= red_high_def[1][0]) and \
           (red_low_def[0][1] <= s <= red_low_def[1][1]) and \
           (red_low_def[0][2] <= v <= red_low_def[1][2]):
            return red_low_def[2]

        for color_name, (lower, upper, char_code) in self.config.COLOR_DEFINITIONS.items():
            if color_name.startswith("RED_"): continue 
            if lower[0] <= h <= upper[0] and \
               lower[1] <= s <= upper[1] and \
               lower[2] <= v <= upper[2]:
                return char_code
        return self.config.UNKNOWN_COLOR_CHAR
