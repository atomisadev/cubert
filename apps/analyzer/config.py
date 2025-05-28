import numpy as np
import os
import cv2

class AnalysisConfig:
    """Configuration settings for the Rubik's Cube face analysis."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_IMAGE_DIR = os.path.join(BASE_DIR, "input_images")
    DEBUG_OUTPUT_DIR = os.path.join(BASE_DIR, "debug_output")

    EXPECTED_FACE_INFO = {
        "U": {"filename_stem": "face-white", "expected_center_char": "W"},
        "R": {"filename_stem": "face-green", "expected_center_char": "G"},
        "F": {"filename_stem": "face-red", "expected_center_char": "R"},
        "D": {"filename_stem": "face-yellow", "expected_center_char": "Y"},
        "L": {"filename_stem": "face-blue", "expected_center_char": "B"},
        "B": {"filename_stem": "face-orange", "expected_center_char": "O"},
    }
    IMAGE_EXTENSION = ".png" 

    DESIRED_IMAGE_WIDTH = 600
    GAUSSIAN_BLUR_KERNEL_SIZE = (7, 7)
    
    CUBE_MASK_LOWER_HSV = np.array([0, 30, 30]) 
    CUBE_MASK_UPPER_HSV = np.array([179, 255, 255])
    MORPH_KERNEL_SIZE = (5, 5)
    MORPH_CLOSE_ITERATIONS = 2
    MIN_CONTOUR_AREA_RATIO = 0.05 
    CONTOUR_APPROX_EPSILON_FACTOR = 0.035

    GRID_ROWS = 3
    GRID_COLS = 3
    STICKER_SAMPLING_AREA_RATIO = 0.5 

    COLOR_DEFINITIONS = {
        "WHITE":  ([0, 0, 155], [179, 80, 255],   "W"),
        "YELLOW": ([20, 100, 100], [35, 255, 255], "Y"),
        "BLUE":   ([90, 80, 70], [130, 255, 255],  "B"),
        "GREEN":  ([40, 70, 60], [85, 255, 255],   "G"), 
        "ORANGE": ([5, 100, 100], [19, 255, 255],  "O"),
        "RED_LOW":([0, 100, 100], [4, 255, 255],   "R"),
        "RED_HIGH":([170, 100, 100], [179, 255, 255],"R"),
    }
    UNKNOWN_COLOR_CHAR = "X"

    DEBUG_TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
    DEBUG_TEXT_FONT_SCALE_COLOR = 0.4
    DEBUG_TEXT_FONT_SCALE_HSV = 0.3
    DEBUG_TEXT_COLOR_OUTLINE = (0,0,0)
    DEBUG_TEXT_COLOR_FILL = (255,255,255)
    DEBUG_LINE_THICKNESS = 1
    DEBUG_LINE_THICKNESS_STRONG = 2

    FACE_ORDER_FOR_CUBE_STRING = ["U", "R", "F", "D", "L", "B"]