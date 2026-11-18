from enum import Enum

import math_functions


class Gesture(Enum):
    NONE = 0
    SPAWN_ITEM = 1
    MOVE_ITEM = 2
    RESIZE_ITEM = 3
    DELETE_ITEM = 4


INDEX_THRESHOLD = 160
FINGER_THRESHOLD = 160
THUMB_THRESHOLD = 120


def map_gestures(pixel_points):

    index_fin = math_functions.get_angle(
        pixel_points[8], pixel_points[5], pixel_points[0]
    )
    mid_fin = math_functions.get_angle(
        pixel_points[12], pixel_points[9], pixel_points[0]
    )
    ring_fin = math_functions.get_angle(
        pixel_points[16], pixel_points[13], pixel_points[0]
    )
    pinky_fin = math_functions.get_angle(
        pixel_points[20], pixel_points[17], pixel_points[0]
    )
    thumb = math_functions.get_angle(pixel_points[4], pixel_points[2], pixel_points[0])

    if (
        index_fin > INDEX_THRESHOLD
        and mid_fin < FINGER_THRESHOLD
        and ring_fin < FINGER_THRESHOLD
        and pinky_fin < FINGER_THRESHOLD
        and thumb < THUMB_THRESHOLD
    ):
        return Gesture.SPAWN_ITEM
    if (
        index_fin < INDEX_THRESHOLD
        and mid_fin < FINGER_THRESHOLD
        and ring_fin < FINGER_THRESHOLD
        and pinky_fin < FINGER_THRESHOLD
        and thumb < THUMB_THRESHOLD
    ):
        return Gesture.DELETE_ITEM
    if (
        index_fin > INDEX_THRESHOLD
        and mid_fin > FINGER_THRESHOLD
        and ring_fin < FINGER_THRESHOLD
        and pinky_fin < FINGER_THRESHOLD
        and thumb < THUMB_THRESHOLD
    ):
        return Gesture.MOVE_ITEM
    if (
        index_fin > INDEX_THRESHOLD
        and mid_fin < FINGER_THRESHOLD
        and ring_fin < FINGER_THRESHOLD
        and pinky_fin < FINGER_THRESHOLD
        and thumb > THUMB_THRESHOLD
    ):
        return Gesture.RESIZE_ITEM
    return Gesture.NONE

def get_pinch_zoom_angle(pixel_points):
    return math_functions.get_angle(pixel_points[8], pixel_points[0], pixel_points[4])

