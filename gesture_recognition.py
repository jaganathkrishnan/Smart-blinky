import cv2
import mediapipe as mp
import serial  # For Arduino communication
import time
import socketio  # WebSocket client for UI updates

# Initialize WebSocket client
sio = socketio.Client()
sio.connect("http://127.0.0.1:5000")  # Ensure `iot_server.py` is running

# Initialize serial communication (Change COM port accordingly, e.g., COM3 for Windows, /dev/ttyUSB0 for Linux/Mac)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Give Arduino some time to start

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_led_state = None

def is_hand_open(hand_landmarks):
    """Check if the hand is open or closed based on distance of fingers from palm."""
    fingertips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    palm_base = mp_hands.HandLandmark.WRIST

    distances = [abs(hand_landmarks.landmark[tip].y - hand_landmarks.landmark[palm_base].y) for tip in fingertips]
    return sum(distances) / len(distances) > 0.1  # Adjust threshold as needed

def gesture_recognition():
    global prev_led_state

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

                is_open = is_hand_open(hand_landmarks)
                new_led_state = is_open  # True if open, False if closed

                if new_led_state != prev_led_state:
                    command = '1' if new_led_state else '0'  # '1' = LED ON, '0' = LED OFF
                    arduino.write(command.encode())  # Send to Arduino
                    sio.emit('led_state', {'state': new_led_state})  # Update UI
                    print(f"Gesture detected: {'OPEN' if new_led_state else 'CLOSED'}")
                    prev_led_state = new_led_state

        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()  # Close serial connection
    sio.disconnect()

if __name__ == '__main__':
    gesture_recognition()
