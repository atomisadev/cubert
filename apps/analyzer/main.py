import cube_model
import camera_scanner
import cube_display

def main():
    cube = cube_model.Cube()

    scanner = camera_scanner.CubeScanner(cube)
    scanner.scan_cube()

    display = cube_display.CubeDisplay(cube)
    display.run()

if __name__ == "__main__":
    main()