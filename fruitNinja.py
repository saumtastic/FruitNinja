import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
import win32api
import pyautogui
from mediapipe.python.solutions.drawing_utils import draw_landmarks

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

video = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        # Corrected unpacking to include the channel
        image_height, image_width, _ = image.shape

        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    normalized_landmark = hand_landmarks.landmark[point]
                    pixel_coordinates_landmark = mp_drawing._normalized_to_pixel_coordinates(
                        normalized_landmark.x, normalized_landmark.y, image_width, image_height)
                    if point == mp_hands.HandLandmark.INDEX_FINGER_TIP and pixel_coordinates_landmark:
                        try:
                            cv2.circle(image, (pixel_coordinates_landmark[0], pixel_coordinates_landmark[1]), 25, (0, 200, 0), 5)
                            index_fingertip_x = pixel_coordinates_landmark[0]
                            index_fingertip_y = pixel_coordinates_landmark[1]
                            win32api.SetCursorPos((index_fingertip_x * 4, index_fingertip_y * 5))
                            pyautogui.mouseDown(button='left')
                        except Exception as e:
                            print(f"Error: {e}")

        cv2.imshow('game', image)
        if cv2.waitKey(100) & 0xFF == 27:
            break

video.release()
cv2.destroyAllWindows()
