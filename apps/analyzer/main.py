# rubiks_analyzer/main.py
import os
import json # For pretty printing results
import cv2 # For dummy image creation
import numpy as np # For dummy image creation

# Important: Ensure these imports work based on your project structure.
# If running main.py directly from rubiks_analyzer folder, these should be:
from config import AnalysisConfig
from face_analyzer import SingleFaceAnalyzer
from cube_state_builder import CubeStateBuilder
from image_utils import ImageSaver # For dummy image creation

def create_dummy_input_images(config: AnalysisConfig):
    """Creates dummy images in the input folder if they don't exist."""
    os.makedirs(config.INPUT_IMAGE_DIR, exist_ok=True)
    
    # BGR colors for dummy centers
    dummy_center_colors_bgr = {
        "W": (230, 230, 230), "Y": (0, 230, 230),
        "R": (0, 0, 230),   "O": (0, 100, 255),
        "B": (230, 100, 0), "G": (0, 180, 0),
        "X": (128, 128, 128) # Unknown
    }

    for logical_face, info in config.EXPECTED_FACE_INFO.items():
        filename = f"{info['filename_stem']}{config.IMAGE_EXTENSION}"
        filepath = os.path.join(config.INPUT_IMAGE_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Creating dummy image: {filepath}")
            img_size = 300
            dummy_img = np.full((img_size, img_size, 3), (60, 60, 60), dtype=np.uint8) # Dark gray bg
            
            center_char = info["expected_center_char"]
            center_color_bgr = dummy_center_colors_bgr.get(center_char, dummy_center_colors_bgr["X"])

            # Draw a large "face"
            cv2.rectangle(dummy_img, (30,30), (img_size-30, img_size-30), (100,100,100), -1)

            # Draw 9 "stickers" - make center one the expected color
            s_size = (img_size - 60 - 20) // 3 # 20 for 2 gaps
            gap = 10
            offset = 30
            
            for r in range(3):
                for c in range(3):
                    x1 = offset + c * (s_size + gap)
                    y1 = offset + r * (s_size + gap)
                    sticker_color = (np.random.randint(0,256), np.random.randint(0,256), np.random.randint(0,256))
                    if r == 1 and c == 1: # Center sticker
                        sticker_color = center_color_bgr
                    cv2.rectangle(dummy_img, (x1,y1), (x1+s_size, y1+s_size), sticker_color, -1)
            ImageSaver.save(dummy_img, config.INPUT_IMAGE_DIR, filename)


if __name__ == "__main__":
    config = AnalysisConfig()
    
    # Create dummy input images if they don't exist (for testing)
    create_dummy_input_images(config)

    face_analyzer = SingleFaceAnalyzer(config)
    cube_builder = CubeStateBuilder(config)

    print("Starting Rubik's Cube Face Analysis...")
    print(f"Reading images from: {config.INPUT_IMAGE_DIR}")
    print(f"Debug output will be in: {config.DEBUG_OUTPUT_DIR}\n")

    processed_face_count = 0
    for logical_face_key, face_info in config.EXPECTED_FACE_INFO.items():
        image_filename = f"{face_info['filename_stem']}{config.IMAGE_EXTENSION}"
        image_path = os.path.join(config.INPUT_IMAGE_DIR, image_filename)

        print(f"--- Analyzing {logical_face_key}-face ({image_filename}) ---")
        
        if not os.path.exists(image_path):
            print(f"ERROR: Image not found: {image_path}. Marking as unprocessed.")
            cube_builder.set_face_as_unprocessed(logical_face_key)
            print("--------------------------------------\n")
            continue

        analysis_result = face_analyzer.analyze(image_path)

        if analysis_result.get("error"):
            print(f"Error during analysis: {analysis_result['error']}")
            cube_builder.set_face_as_unprocessed(logical_face_key)
        else:
            print(f"  Detected Center: {analysis_result['center_color_char']}")
            print(f"  Grid Colors:")
            for row in analysis_result['grid_colors']:
                print(f"    {row}")
            
            # Verify detected center against expected, if desired
            if analysis_result['center_color_char'] != face_info['expected_center_char'] and \
               analysis_result['center_color_char'] != config.UNKNOWN_COLOR_CHAR:
                print(f"  WARNING: Center color mismatch! Expected {face_info['expected_center_char']}, got {analysis_result['center_color_char']}.")
                # Decide on handling: either use detected or mark error. For now, we'll use the detected.
            
            cube_builder.add_face_data(logical_face_key, analysis_result['grid_colors'])
            processed_face_count +=1
        
        if analysis_result.get("debug_image_path"):
            print(f"  Debug image: {analysis_result['debug_image_path']}")
        print("--------------------------------------\n")

    print("=== Cube State Construction ===")
    if processed_face_count < 6:
        print(f"Warning: Only {processed_face_count} out of 6 faces were successfully processed.")
        
    final_cube_string = cube_builder.get_cube_string()
    print(f"\nFinal 54-character Cube State String (URFDLB order):")
    print(final_cube_string)

    # Example of how to view the string grouped by faces (9 chars per face)
    if len(final_cube_string) == 54:
        print("\nCube String by Face:")
        for i, face_key in enumerate(config.FACE_ORDER_FOR_CUBE_STRING):
            start = i * 9
            end = start + 9
            face_str = final_cube_string[start:end]
            print(f"  {face_key}-face: {face_str[:3]} {face_str[3:6]} {face_str[6:]}")
    else:
        print(f"Error: Final cube string length is {len(final_cube_string)}, expected 54.")

    print("\nAnalysis complete.")