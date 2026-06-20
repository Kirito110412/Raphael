def locate_coordinates(bbox_2d: list, scale_factor: float = 1.0) -> tuple:
    """
    Maps bbox_2d to click coordinates (center point).
    """
    x1, y1, x2, y2 = bbox_2d
    center_x = (x1 + x2) / 2 * scale_factor
    center_y = (y1 + y2) / 2 * scale_factor
    return (center_x, center_y)
