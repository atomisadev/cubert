import cv2
import numpy as np
from .config import AnalysisConfig

class ContourDetector:
    def __init__(self, config:AnalysisConfig):
        self.config = config

    def _create_segmentation_mask(self, hsv_image: np.ndarray) -> np.ndarray:
        mask = cv2.inRange(hsv_image, self.config.CUBE_MASK_LOWER_HSV, self.config.CUBE_MASK_UPPER_HSV)
        kernel = np.ones(self.config.MORPH_KERNEL_SIZE, np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=self.config.MORPH_CLOSE_ITERATIONS)
        return mask
    
    def _find_largest_valid_contour(self, mask: np.ndarray, image_area: int) -> np.ndarray | None:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours: return None
        min_contour_area = image_area * self.config.MIN_CONTOUR_AREA_RATIO
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
        return max(valid_contours, key=cv2.contourArea) if valid_contours else None
    
    def _approximate_contour(self, contour: np.ndarray) -> np.ndarray:
        perimeter = cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, self.config.CONTOUR_APPROX_EPSILON_FACTOR * perimeter, True)
    
    def find_main_face_contour_approx(self, hsv_image: np.ndarray) -> np.ndarray | None:
        """Finds and returns the approx polygon of the main face contour"""
        mask = self._create_segmentation_mask(hsv_image)
        image_area = hsv_image.shape[0] * hsv_image.shape[1]
        largest_contour = self._find_largest_valid_contour(mask, image_area)
        if largest_contour is None:
            return None
        return self._approximate_contour(largest_contour)
    
class GridDefiner:
    def __init__(self, config: AnalysisConfig):
        self.config = config

    def get_face_bounding_box(self, contour_approx: np.ndarray) -> tuple[int, int, int] | None:
        if contour_approx is None or len(contour_approx) == 0:
            return None
        cv2.boundingRect(contour_approx)

    def define_sticker_sampling_rois(self, face_bbox: tuple[int, int, int, int]) \
        -> list[tuple[int, int, int, int]]:
        if face_bbox is None: return []

        x_face, y_face, w_face, h_face = face_bbox
        rois = []
        if w_face == 0 or h_face == 0: return []

        cell_w = w_face / float(self.config.GRID_COLS)
        cell_h = h_face / float(self.config.GRID_ROWS)
        ratio = self.config.STICKER_SAMPLING_AREA_RATIO

        for i in range(self.config.GRID_ROWS):
            for j in range(self.config.GRID_COLS):
                sample_w_val = int(cell_w * ratio)
                sample_h_val = int(cell_h * ratio)

                center_x_cell = x_face + (j * cell_w) + (cell_w / 2)
                center_y_cell = y_face + (i * cell_h) + (cell_h / 2)

                x1_sample = int(center_x_cell - sample_w_val / 2)
                y1_sample = int(center_y_cell - sample_h_val / 2)
                rois.append((x1_sample, y1_sample, sample_w_val, sample_h_val))
        return rois