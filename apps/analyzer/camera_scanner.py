import cv2
import numpy as np
import color_utils
import cube_model

class CubeScanner:
    """
    Handles scanning the Rubik's Cube faces using the computer's camera.
    """
    def __init__(self, cube: cube_model.Cube):
        self.cube = cube
        self.window_name = "Cube Scanner"
        self.faces_scanned = set()

    def scan_cube(self):
        """
        Opens the camera and guides the user to scan each face of the cube.
        """
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("Error: Could not open video stream.")
            return

        print("\n--- Cube Scanner ---")
        print("Show each face of the Rubik's Cube to the camera.")
        print("Align the face with the grid and press the [SPACEBAR] to scan.")
        print("Press [q] to finish scanning.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            h, w, _ = frame.shape
            cx, cy = w // 2, h // 2
            
            self._draw_ui(frame, cx, cy)

            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                self._scan_face(frame, cx, cy)
                if len(self.faces_scanned) == 6:
                    print("\nAll 6 faces have been scanned!")
                    break
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def _draw_ui(self, frame, cx, cy):
        """
        Draws a 3x3 grid and instructional text on the frame.
        """
        size = 40 
        gap = 5   
        for i in range(-1, 2):
            for j in range(-1, 2):
                x1 = cx + (j * (size + gap)) - (size // 2)
                y1 = cy + (i * (size + gap)) - (size // 2)
                x2 = x1 + size
                y2 = y1 + size
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)
        
        scanned_str = f"Faces Scanned: {len(self.faces_scanned)}/6"
        cv2.putText(frame, scanned_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Align face and press SPACE", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


    def _scan_face(self, frame, cx, cy):
        """
        Scans the colors within the 3x3 grid on the current frame,
        identifies the face by its center color, and updates the cube model.
        """
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        face_matrix = np.full((3, 3), 'U', dtype=str)
        
        size = 40
        gap = 5
        
        for i, row in zip(range(-1, 2), range(3)):
            for j, col in zip(range(-1, 2), range(3)):
                x = cx + (j * (size + gap))
                y = cy + (i * (size + gap))
                h, s, v = hsv_frame[y, x]
                color = color_utils.hsv_to_color(h, s)
                face_matrix[row, col] = color
        
        center_color = face_matrix[1, 1]
        
        face_map = {
            'W': ([0, 1, 0], "White"),
            'G': ([0, 0, -1], "Green"),
            'O': ([-1, 0, 0], "Orange"),
            'B': ([0, 0, 1], "Blue"),
            'R': ([1, 0, 0], "Red"),
            'Y': ([0, -1, 0], "Yellow")
        }
        
        if center_color in face_map:
            vector, color_name = face_map[center_color]
            
            if color_name in self.faces_scanned:
                print(f"{color_name} face has already been scanned. Show a different face.")
                return

            print(f"\nScanned {color_name} face:")
            print(face_matrix)
            self.cube.conf_replacement(vector, face_matrix)
            self.faces_scanned.add(color_name)
        else:
            print("\nCould not identify the center color. Please try again.")
            print("Detected colors:")
            print(face_matrix)