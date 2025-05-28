import os
from .config import AnalysisConfig
from .image_utils import ImageLoader, ImageProcessor, ImageSaver
from .detection_utils import ContourDetector, GridDefiner
from .color_analyzer import ColorIdentifier
from .visualization_utils import DebugVisualizer

class SingleFaceAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.image_loader = ImageLoader()
        self.image_processor = ImageProcessor(config)
        self.image_saver = ImageSaver()
        self.contour_detector = ContourDetector(config)
        self.grid_definer = GridDefiner(config)
        self.color_identifier = ColorIdentifier(config)
        self.visualizer = DebugVisualizer(config)

    def analyze(self, image_path: str) -> dict:
        """Analyzes a single face image and then returns the data"""
        image_filename_stem = os.path.splitext(os.path.basename(image_path))[0]
        debug_image_filename = f"{image_filename_stem}_debug{self.config.IMAGE_EXTENSION}"

        result = {
            "face_id": image_filename_stem,
            "grid_colors": [[self.config.UNKNOWN_COLOR_CHAR]*self.config.GRID_COLS for _ in range(self.config.GRID_ROWS)],
            "center_color_char": self.config.UNKNOWN_COLOR_CHAR,
            "debug_image_path": None,
            "error": None
        }

        original_bgr = self.image_loader.load(image_path)
        if original_bgr is None:
            result["error"] = f"Failed to load image: {image_path}"
            return result
        
        debug_bgr_image, blurred_hsv_image = self.image_processor.preprocess(original_bgr)

        contour_approx = self.contour_detector.find_main_face_contour_approx(blurred_hsv_image)
        self.visualizer.draw_contour_approximation(debug_bgr_image, contour_approx)

        if contour_approx is None:
            result["error"] = "Could not find main face contour."
            self.visualizer.draw_general_message(debug_bgr_image, "Error: No Face Contour")
            result["debug_image_path"] = self.image_saver.save(debug_bgr_image, 
                                                               self.config.DEBUG_OUTPUT_DIR, 
                                                               debug_image_filename)
            return result

        face_bbox = self.grid_definer.get_face_bounding_box(contour_approx)
        self.visualizer.draw_bounding_box(debug_bgr_image, face_bbox)

        sticker_rois = self.grid_definer.define_sticker_sampling_rois(face_bbox)
        self.visualizer.draw_sticker_rois_cells(debug_bgr_image, face_bbox, sticker_rois)

        if len(sticker_rois) != self.config.GRID_ROWS * self.config.GRID_COLS:
            result["error"] = f"Incorrect number of sticker ROIs: {len(sticker_rois)}"
            self.visualizer.draw_general_message(debug_bgr_image, f"Error: Grid Fail ({len(sticker_rois)} ROIs)")
            result["debug_image_path"] = self.image_saver.save(debug_bgr_image, 
                                                               self.config.DEBUG_OUTPUT_DIR, 
                                                               debug_image_filename)
            return result
        
        flat_color_chars = []
        for i, roi in enumerate(sticker_rois):
            avg_hsv = self.color_identifier.extract_average_hsv(blurred_hsv_image, roi)
            color_char = self.config.UNKNOWN_COLOR_CHAR
            if avg_hsv:
                color_char = self.color_identifier.get_color_char_from_hsv(avg_hsv)
            flat_color_chars.append(color_char)
            self.visualizer.annotate_sticker_info(debug_bgr_image, color_char, avg_hsv, roi)

        result["grid_colors"] = [flat_color_chars[i:i+self.config.GRID_COLS] for i in range(0, len(flat_color_chars), self.config.GRID_COLS)]

        center_row = self.config.GRID_ROWS // 2
        center_col = self.config.GRID_COLS // 2
        if result["grid_colors"] and len(result["grid_colors"]) > center_row and len(result["grid_colors"][center_row]) > center_col:
            result["center_color_char"] = result["grid_colors"][center_row][center_col]

        result["debug_image_path"] = self.image_saver.save(debug_bgr_image, self.config.DEBUG_OUTPUT_DIR, debug_image_filename)
        return result