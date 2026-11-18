import cv2

import math_functions


def spawn_item(posx, posy, frame, ball_radius):
    cv2.circle(frame, (posx, posy), ball_radius, (0, 255, 0), 2)


def spawn_cube(frame, cx, cy, size, color=(0, 255, 255)):
    # 1. Perspective offset for the back face
    # We shift it up and to the right by half the size to simulate depth
    depth = size // 2

    # 2. Define the 4 corners of the FRONT face
    f_tl = (cx - size, cy - size)  # Front Top-Left
    f_tr = (cx + size, cy - size)  # Front Top-Right
    f_br = (cx + size, cy + size)  # Front Bottom-Right
    f_bl = (cx - size, cy + size)  # Front Bottom-Left

    # 3. Define the 4 corners of the BACK face (shifted by 'depth')
    b_tl = (cx - size + depth, cy - size - depth)
    b_tr = (cx + size + depth, cy - size - depth)
    b_br = (cx + size + depth, cy + size - depth)
    b_bl = (cx - size + depth, cy + size - depth)

    thickness = 2

    # 4. Draw the FRONT face (4 lines)
    cv2.line(frame, f_tl, f_tr, color, thickness)
    cv2.line(frame, f_tr, f_br, color, thickness)
    cv2.line(frame, f_br, f_bl, color, thickness)
    cv2.line(frame, f_bl, f_tl, color, thickness)

    # 5. Draw the BACK face (4 lines)
    cv2.line(frame, b_tl, b_tr, color, thickness)
    cv2.line(frame, b_tr, b_br, color, thickness)
    cv2.line(frame, b_br, b_bl, color, thickness)
    cv2.line(frame, b_bl, b_tl, color, thickness)

    # 6. Draw the CONNECTING edges (4 lines)
    cv2.line(frame, f_tl, b_tl, color, thickness)
    cv2.line(frame, f_tr, b_tr, color, thickness)
    cv2.line(frame, f_br, b_br, color, thickness)
    cv2.line(frame, f_bl, b_bl, color, thickness)


def finger_point(index_fin, mid_fin, ring_fin, pinky_fin, thumb):
    if (
        index_fin > 55
        and mid_fin < 55
        and ring_fin < 55
        and pinky_fin < 55
        and thumb < 60
    ):
        return True
    return False


def fist(index_fin, mid_fin, ring_fin, pinky_fin):
    if index_fin < 55 and mid_fin < 55 and ring_fin < 55 and pinky_fin < 55:
        return True
    return False


def two_fingers(index_fin, mid_fin, ring_fin, pinky_fin):
    if index_fin > 55 and mid_fin > 55 and ring_fin < 55 and pinky_fin < 55:
        return True
    return False


def is_pinching(pixel_points):
    index_thumb_distance = math_functions.get_euclidean_distance(
        pixel_points[8], pixel_points[4]
    )
    if index_thumb_distance < 55:
        return True
    return False


def is_zoom_in(pixel_points):
    index_thumb_distance = math_functions.get_euclidean_distance(
        pixel_points[8], pixel_points[4]
    )
    if index_thumb_distance < 55:
        return True
    return False


def get_pinch_zoom_distance(pixel_points):
    mid_fin = math_functions.get_euclidean_distance(pixel_points[12], pixel_points[1])
    ring_fin = math_functions.get_euclidean_distance(pixel_points[16], pixel_points[1])
    pinky_fin = math_functions.get_euclidean_distance(pixel_points[20], pixel_points[1])
    thumb = math_functions.get_euclidean_distance(pixel_points[4], pixel_points[0])

    if mid_fin < 55 and ring_fin < 55 and pinky_fin < 55 and thumb > 60:
        return math_functions.get_euclidean_distance(pixel_points[8], pixel_points[4])

    return None
