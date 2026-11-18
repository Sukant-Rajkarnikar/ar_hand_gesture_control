import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import angle_gestures
import distance_gestures
from math_functions import get_euclidean_distance

HAND_CONNECTIONS = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (13, 17),
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),
]

base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
detector = vision.HandLandmarker.create_from_options(options)
cap = cv2.VideoCapture(0)

ball_active = False
ball_radius = 20
ball_x, ball_y = 0, 0

is_zooming = False
start_pinch_dist = 0
start_ball_radius = 0

prev_time = 0
min_fps = float("inf")
max_fps = 0
frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        # Pair each hand's 21 landmarks with its handedness classification
        for hand_landmarks, handedness in zip(
            detection_result.hand_landmarks, detection_result.handedness
        ):
            # 1. Fast list comprehension to convert normalized coordinates to pixels
            pixel_points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]

            # 2. Draw skeleton lines and joint circles
            for start_idx, end_idx in HAND_CONNECTIONS:
                cv2.line(
                    frame,
                    pixel_points[start_idx],
                    pixel_points[end_idx],
                    (255, 255, 255),
                    1,
                )
            for px, py in pixel_points:
                cv2.circle(frame, (px, py), 5, (223, 192, 131), -1)

            # pinch_distance = get_euclidean_distance(pixel_points[4], pixel_points[8])

            # hand_label = handedness[0].category_name
            # if hand_label == "Left": # Physical Right Hand (due to mirror flip)
            #     cv2.putText(frame, f'Thumb and Index finger distance - Right Hand: {pinch_distance:.2f}', (20, 50),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # elif hand_label == "Right": # Physical Left Hand (due to mirror flip)
            #     cv2.putText(frame, f'Thumb and Index finger distance - Left Hand: {pinch_distance:.2f}', (20, 90),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # index_fin = get_euclidean_distance(pixel_points[8], pixel_points[1])
            # cv2.putText(frame, f'Index and Wrist distance:{index_fin:.2f}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # mid_fin = get_euclidean_distance(pixel_points[12], pixel_points[1])
            # cv2.putText(frame, f'Middle and Wrist distance:{mid_fin:.2f}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # ring_fin = get_euclidean_distance(pixel_points[16], pixel_points[1])
            # cv2.putText(frame, f'Ring and Wrist distance:{ring_fin:.2f}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # pinky_fin = get_euclidean_distance(pixel_points[20], pixel_points[1])
            # cv2.putText(frame, f'Pinky and Wrist distance:{pinky_fin:.2f}', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # thumb = get_euclidean_distance(pixel_points[4], pixel_points[0])
            # cv2.putText(frame, f'Thumb and Wrist distance:{thumb:.2f}', (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # if distance_gestures.finger_point(index_fin, mid_fin, ring_fin, pinky_fin, thumb) and not ball_active:
            #     ball_x, ball_y = pixel_points[8]
            #     ball_active = True

            # if distance_gestures.fist(index_fin, mid_fin, ring_fin, pinky_fin):
            #     ball_active = False

            # if ball_active and distance_gestures.two_fingers(index_fin, mid_fin, ring_fin, pinky_fin) and get_euclidean_distance(pixel_points[8], (ball_x, ball_y)) < ball_radius:
            #     ball_x, ball_y = pixel_points[8]

            # zoom_dist = distance_gestures.get_pinch_zoom_distance(pixel_points)
            # if zoom_dist is not None:
            #     if not is_zooming:
            #         is_zooming = True
            #         start_pinch_dist = max(zoom_dist, 1)
            #         start_ball_radius = ball_radius
            #     else:
            #         ratio = zoom_dist / start_pinch_dist
            #         ball_radius = int(start_ball_radius * ratio)
            #         if ball_radius < 10:
            #             ball_radius = 10
            #         elif ball_radius > 250:
            #             ball_radius = 250
            # else:
            #     is_zooming = False

            match angle_gestures.map_gestures(pixel_points):
                case angle_gestures.Gesture.SPAWN_ITEM:
                    if not ball_active:
                        ball_x, ball_y = pixel_points[8]
                        ball_active = True
                case angle_gestures.Gesture.DELETE_ITEM:
                    ball_active = False
                case angle_gestures.Gesture.MOVE_ITEM:
                    if ball_active:
                        ball_x, ball_y = pixel_points[8]
                case angle_gestures.Gesture.RESIZE_ITEM:
                    if ball_active:
                        zoom_angle = angle_gestures.get_pinch_zoom_angle(pixel_points)
                        if zoom_angle is not None:
                            if not is_zooming:
                                is_zooming = True
                                start_pinch_angle = max(
                                    zoom_angle, 1
                                )
                                start_ball_radius = ball_radius
                            else:
                                ratio = zoom_angle / start_pinch_angle
                                ball_radius = int(start_ball_radius * ratio)

                                if ball_radius < 10:
                                    ball_radius = 10
                                elif ball_radius > 250:
                                    ball_radius = 250
                        else:
                            is_zooming = False

    curr_time = time.time()
    if curr_time - prev_time > 0:
        fps = 1 / (curr_time - prev_time)
    else:
        fps = 0
    prev_time = curr_time

    frame_count += 1
    if frame_count > 10:
        min_fps = min(min_fps, fps)
        max_fps = max(max_fps, fps)

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (w - 200, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2,
    )
    if min_fps != float("inf"):
        cv2.putText(
            frame,
            f"Min FPS: {int(min_fps)}",
            (w - 200, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Max FPS: {int(max_fps)}",
            (w - 200, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    if ball_active:
        distance_gestures.spawn_item(ball_x, ball_y, frame, ball_radius)

    cv2.imshow("AR Hand Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
