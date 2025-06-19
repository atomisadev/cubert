def hsv_to_color(h, s):
    if s < 100: return "W"
    if h >= 0 and h <= 10: return "R"
    if h > 10 and h <= 25: return "O"
    if h > 25 and h <= 40: return "Y"
    if h > 35 and h <= 75: return "G"
    if h > 75 and h < 130: return "B"
    return "Unknown"

def color_to_rgb(color):
    if color == "R": return (0, 0, 255)
    if color == "O": return (0, 100, 255)
    if color == "Y": return (0, 255, 255)
    if color == "G": return (0, 210, 100)
    if color == "B": return (219, 70, 29)
    if color == "W": return (255, 255, 255)
    return (0, 0, 0)