import cv2
import numpy as np
import color_utils

class CubeDisplay:
    def __init__(self, cube):
        self.cube = cube
        self.window_name = "Virtual Cube"

        try:
            self.img = cv2.imread("fondo.PNG", 1)
            if self.img is None:
                print("Warning: 'fondo.PNG' is not found. Using a black background")
                self.img = np.zeros((600, 800, 3), dtype=np.uint8)
        except Exception as e:
            print(f"Error loading 'fondo.PNG': {e}")
            self.img = np.zeros((600, 800, 3), dtype=np.uint8)

    def run(self):
        print("\nCube display is active. Use the following keys to interact:")
        print("  - F, R, L, U, B, D for clockwise moves.")
        print("  - Shift + key (e.g., 'F') for counter-clockwise moves.")
        print("  - 1, 2, 3, 4 to change the front face (Green, Red, Blue, Orange).")
        print("  - Press 'q' to quit.")

        while True:
            display_img = self.img.copy()
            self._draw_cube(display_img)
            cv2.imshow(self.window_name, display_img)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

            self._handle_input(key)

        cv2.destroyAllWindows()
            
    def _draw_cube(self, image):
        self._draw_face(image, 362, 238, self.cube.Gx)
        self._draw_face(image, 262, 238, self.cube.Ox)
        self._draw_face(image, 162, 238, self.cube.Bx)
        self._draw_face(image, 462, 238, self.cube.Rx)
        
        w_rotations = self.cube._YRot([0, 1, 0])
        self._draw_face(image, 362, 138, np.rot90(self.cube.Wx, k=w_rotations))
        y_rotations = self.cube._YRot([0, -1, 0])
        self._draw_face(image, 362, 338, np.rot90(self.cube.Yx, k=y_rotations))

    def _draw_face(self, image, X, Y, face_matrix):
        size = 22
        gap = 2
        for i in range(3):
            for j in range(3):
                color_name = face_matrix[i, j]
                rgb_color = color_utils.color_to_rgb(color_name)

                x1 = X - (size // 2) + (j * (size + gap)) - size
                y1 = Y - (size // 2) + (i * (size + gap)) - size
                x2 = x1 + size
                y2 = y1 + size

                cv2.rectangle(image, (x1, y1), (x2, y2), rgb_color, -1)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), 1)

    def _handle_input(self, key):
        if key == ord('f'): self.cube.F()
        elif key == ord('F'): self.cube.F_()
        elif key == ord('r'): self.cube.R()
        elif key == ord('R'): self.cube.R_()
        elif key == ord('l'): self.cube.L()
        elif key == ord('L'): self.cube.L_()
        elif key == ord('u'): self.cube.U()
        elif key == ord('U'): self.cube.U_()
        elif key == ord('b'): self.cube.B()
        elif key == ord('B'): self.cube.B_()
        elif key == ord('d'): self.cube.D()
        elif key == ord('D'): self.cube.D_()
        
        elif key == ord('1'):
            print("Front face changed to Green")
            self.cube.front_face_vector = [0,0,-1]
        elif key == ord('2'):
            print("Front face changed to Red")
            self.cube.front_face_vector = [1,0,0]
        elif key == ord('3'):
            print("Front face changed to Blue")
            self.cube.front_face_vector = [0,0,1]
        elif key == ord('4'):
            print("Front face changed to Orange")
            self.cube.front_face_vector = [-1,0,0]