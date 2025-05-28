# rubiks_analyzer/cube_state_builder.py
from .config import AnalysisConfig

class CubeStateBuilder:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        # Stores face data as { "U": [['W','W','W'],...], "R": [...], ... }
        self.faces_data = {face_key: None for face_key in config.FACE_ORDER_FOR_CUBE_STRING}

    def add_face_data(self, logical_face_key: str, grid_colors: list[list[str]]):
        """
        Adds the 3x3 grid data for a specific logical face (U, R, F, D, L, B).
        """
        if logical_face_key not in self.config.FACE_ORDER_FOR_CUBE_STRING:
            print(f"Warning: Invalid logical face key '{logical_face_key}' provided to CubeStateBuilder.")
            return
        
        if not (len(grid_colors) == self.config.GRID_ROWS and 
                all(len(row) == self.config.GRID_COLS for row in grid_colors)):
            print(f"Warning: Invalid grid dimensions for face {logical_face_key}. Filling with UNKNOWN.")
            self.faces_data[logical_face_key] = [[self.config.UNKNOWN_COLOR_CHAR]*self.config.GRID_COLS 
                                                 for _ in range(self.config.GRID_ROWS)]
        else:
            self.faces_data[logical_face_key] = grid_colors
            
    def get_cube_string(self) -> str:
        """
        Constructs the 54-character cube state string based on the URFDLB face order.
        Stickers are read row by row for each face.
        """
        cube_string_list = []
        for face_key in self.config.FACE_ORDER_FOR_CUBE_STRING:
            grid = self.faces_data.get(face_key)
            if grid is None: # Face data was not provided or failed
                print(f"Warning: Data for face '{face_key}' is missing. Filling with UNKNOWNs.")
                cube_string_list.extend([self.config.UNKNOWN_COLOR_CHAR] * (self.config.GRID_ROWS * self.config.GRID_COLS))
            else:
                for row in grid:
                    cube_string_list.extend(row)
        
        return "".join(cube_string_list)

    def set_face_as_unprocessed(self, logical_face_key: str):
        """Marks a face as unprocessed, filling its grid with UNKNOWN characters."""
        if logical_face_key in self.faces_data:
             self.faces_data[logical_face_key] = [[self.config.UNKNOWN_COLOR_CHAR]*self.config.GRID_COLS 
                                                 for _ in range(self.config.GRID_ROWS)]