import cv2
import numpy as np
from config import AnalysisConfig

class DebugVisualizer:
    def __init__(self, config: AnalysisConfig):
        self.config = config

    def draw_contour_approximation(self, image: np.ndarray, contour_approx: np.ndarray | None):
        if contour_approx is not None:
            cv2.drawContours(image, [contour_approx], -1, (0, 255, 0), self.config.DEBUG_LINE_THICKNESS)

    def draw_bounding_box(self, image: np.ndarray, bbox: tuple[int, int, int] | None):
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), self.config.DEBUG_LINE_THICKNESS_STRONG)

    def draw_sticker_rois_and_cells(self, image: np.ndarray, face_bbox: tuple[int, int, int, int] | None, sampling_rois: list[tuple[int, int, int, int]]):
        if not face_bbox or not sampling_rois: return

        x_f, y_f, w_f, h_f = face_bbox
        cell_w = w_f / float(self.config.GRID_COLS)
        cell_h = h_f / float(self.config.GRID_ROWS)

        for r in range(self.config.GRID_ROWS):
            for c in range(self.config.GRID_COLS):
                cx1, cy1 = int(x_f + c * cell_w), int(y_f + r * cell_h)
                cx2, cy2 = int(x_f, (c + 1) * cell_w), int(y_f + (r + 1) * cell_h)
                cv2.rectangle(image, (cx1, cy1), (cx2, cy2), (0, 255, 0), self.config.DEBUG_LINE_THICKNESS)

        for x_s, y_s, w_s, h_s in sampling_rois:
            cv2.rectangle(image, (x_s, y_s), (x_s + w_s, y_s + h_s), (0, 0, 255), self.config.DEBUG_LINE_THICKNESS)

    def annotate_sticker_info(self, image: np.ndarray, color_char: str, 
                              avg_hsv: tuple[int,int,int] | None,
                              roi_for_placement: tuple[int,int,int,int]):
        x, y, w, h = roi_for_placement
        text_pos_char = (x, y - 15 if y > 20 else y + h + 15)
        text_pos_hsv = (x, y - 5 if y > 10 else y + h + 25)

        # Draw character
        cv2.putText(image, color_char, text_pos_char, self.config.DEBUG_TEXT_FONT, 
                    self.config.DEBUG_TEXT_FONT_SCALE_COLOR, self.config.DEBUG_TEXT_COLOR_OUTLINE, 
                    self.config.DEBUG_LINE_THICKNESS_STRONG, cv2.LINE_AA)
        cv2.putText(image, color_char, text_pos_char, self.config.DEBUG_TEXT_FONT, 
                    self.config.DEBUG_TEXT_FONT_SCALE_COLOR, self.config.DEBUG_TEXT_COLOR_FILL, 
                    self.config.DEBUG_LINE_THICKNESS, cv2.LINE_AA)

        if avg_hsv:
            h_val, s_val, v_val = avg_hsv
            hsv_text = f"H{h_val}S{s_val}V{v_val}"
            cv2.putText(image, hsv_text, text_pos_hsv, self.config.DEBUG_TEXT_FONT, 
                        self.config.DEBUG_TEXT_FONT_SCALE_HSV, self.config.DEBUG_TEXT_COLOR_OUTLINE, 
                        self.config.DEBUG_LINE_THICKNESS_STRONG, cv2.LINE_AA)
            cv2.putText(image, hsv_text, text_pos_hsv, self.config.DEBUG_TEXT_FONT, 
                        self.config.DEBUG_TEXT_FONT_SCALE_HSV, self.config.DEBUG_TEXT_COLOR_FILL, 
                        self.config.DEBUG_LINE_THICKNESS, cv2.LINE_AA)
    
    def draw_general_message(self, image: np.ndarray, message: str, position: tuple[int,int]=(10,30)):
        cv2.putText(image, message, position, self.config.DEBUG_TEXT_FONT, 0.6, 
                    self.config.DEBUG_TEXT_COLOR_OUTLINE, self.config.DEBUG_LINE_THICKNESS_STRONG, cv2.LINE_AA)
        cv2.putText(image, message, position, self.config.DEBUG_TEXT_FONT, 0.6, 
                    (0,0,255) if "Error" in message or "Fail" in message else self.config.DEBUG_TEXT_COLOR_FILL, 
                    self.config.DEBUG_LINE_THICKNESS, cv2.LINE_AA)
