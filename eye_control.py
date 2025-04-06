import cv2
import mediapipe as mp
import pyautogui
import time
import math
import os
from datetime import datetime

# Setup
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Constants
blink_threshold = 0.015
click_cooldown = 1.0
zoom_cooldown = 1.0
zoom_sensitivity = 8
screenshot_duration = 2.5

# Timers and state
last_click_time = 0
last_zoom_time = 0
eye_closed_start_time = None
screenshot_taken = False
prev_eye_distance = None

# Helpers
def get_blink_status(landmarks, frame_h):
    top_left = landmarks[159].y * frame_h
    bottom_left = landmarks[145].y * frame_h
    top_right = landmarks[386].y * frame_h
    bottom_right = landmarks[374].y * frame_h
    left_eye_ratio = abs(top_left - bottom_left)
    right_eye_ratio = abs(top_right - bottom_right)
    is_left_closed = left_eye_ratio < blink_threshold * frame_h
    is_right_closed = right_eye_ratio < blink_threshold * frame_h
    return is_left_closed, is_right_closed

def get_eye_distance(landmarks, frame_w):
    left_eye = (landmarks[33].x * frame_w, landmarks[33].y)
    right_eye = (landmarks[263].x * frame_w, landmarks[263].y)
    return math.hypot(left_eye[0] - right_eye[0], left_eye[1] - right_eye[1])

# Main loop
while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    current_time = time.time()

    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Cursor movement
        for id, landmark in enumerate(landmarks[474:478]):
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        # Blink detection
        is_left_closed, is_right_closed = get_blink_status(landmarks, frame_h)

        # Zoom detection
        eye_distance = get_eye_distance(landmarks, frame_w)
        if prev_eye_distance is not None:
            distance_change = eye_distance - prev_eye_distance
            if abs(distance_change) > zoom_sensitivity and (current_time - last_zoom_time > zoom_cooldown):
                if distance_change > 0:
                    pyautogui.hotkey('ctrl', '+')
                    print("🔍 Zoom In")
                else:
                    pyautogui.hotkey('ctrl', '-')
                    print("🔍 Zoom Out")
                last_zoom_time = current_time
        prev_eye_distance = eye_distance

        # Screenshot logic
        if is_left_closed and is_right_closed:
            if eye_closed_start_time is None:
                eye_closed_start_time = current_time
                screenshot_taken = False
            else:
                closed_duration = current_time - eye_closed_start_time
                print(f"[DEBUG] Eyes closed for {closed_duration:.2f} seconds")

                if not screenshot_taken and closed_duration >= screenshot_duration:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"eyes_closed_screenshot_{timestamp}.png"
                    filepath = os.path.join(os.path.expanduser('~'), 'Pictures', filename)
                    try:
                        pyautogui.screenshot(filepath)
                        print(f"📸 Screenshot saved: {filepath}")
                        screenshot_taken = True
                    except Exception as e:
                        print(f"[ERROR] Screenshot failed: {e}")
        else:
            # Reset screenshot timer
            if eye_closed_start_time is not None:
                if (current_time - eye_closed_start_time) > 0.5:
                    eye_closed_start_time = None
                    screenshot_taken = False

            # Clicks
            if current_time - last_click_time > click_cooldown:
                if is_left_closed and not is_right_closed:
                    pyautogui.click()
                    print("🖱️ Left Click via Blink")
                    last_click_time = current_time
                elif is_right_closed and not is_left_closed:
                    pyautogui.click(button='right')
                    print("👉 Right Click via Right Eye Wink")
                    last_click_time = current_time

        # Display eye status
        cv2.putText(frame, f"Left Eye: {'Closed' if is_left_closed else 'Open'}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if is_left_closed else (0, 0, 255), 2)
        cv2.putText(frame, f"Right Eye: {'Closed' if is_right_closed else 'Open'}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if is_right_closed else (0, 0, 255), 2)

    # Display window
    cv2.imshow("Eye Controlled Mouse | Click, Screenshot, Zoom", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()