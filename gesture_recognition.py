import cv2
import mediapipe as mp
import serial
import time

# Initialize Serial Communication
arduino = serial.Serial('COM5', 9600, timeout=1)  # Change COM5 if needed
time.sleep(2)  # Allow Arduino to initialize

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def get_brightness(hand_landmarks):
    """Calculate brightness level (0-255), ensuring CLOSED = 0 and OPEN = 255."""
    fingertips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    palm_base = mp_hands.HandLandmark.WRIST

    distances = [abs(hand_landmarks.landmark[tip].y - hand_landmarks.landmark[palm_base].y) for tip in fingertips]
    avg_distance = sum(distances) / len(distances)

    # Normalize brightness (Scale avg_distance between 0-255)
    min_distance = 0.02  # Smallest possible spread (closed hand)
    max_distance = 0.15  # Largest possible spread (open hand)

    normalized = (avg_distance - min_distance) / (max_distance - min_distance)
    brightness = int(min(max(normalized * 255, 0), 255))  # Ensure within 0-255

    return 255 - brightness  # INVERT brightness (closed = 0, open = 255)

def gesture_recognition():
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                brightness = get_brightness(hand_landmarks)
                arduino.write(f"{brightness}\n".encode())  # Send brightness to Arduino
                print(f"Brightness: {brightness}")

        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == '__main__':
    gesture_recognition()
