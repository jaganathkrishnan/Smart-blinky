# Smart-blinky
A blinky led with gesture based control using arduino and opencv.
# Smart Blinky

## Overview
Smart Blinky is a gesture-controlled LED system using OpenCV, Arduino, and WebSockets. It detects hand gestures using a webcam and controls an LED connected to an Arduino.

## Components Required
- Arduino Uno (or compatible)
- LED
- Resistor (220Ω)
- Jumper wires
- Webcam
- Computer with Python

## Technologies Used
- **Python** (Gesture Recognition, WebSocket Communication)
- **OpenCV** (Hand Detection)
- **MediaPipe** (Hand Landmark Detection)
- **Flask & Socket.IO** (WebSocket Server)
- **Arduino C++** (Microcontroller Code)

## Installation & Setup

### 1. **Install Dependencies**
Ensure you have Python and pip installed, then run:
```sh
pip install opencv-python mediapipe flask flask-socketio pyserial
```

### 2. **Connect Hardware**
- Connect an LED to Arduino pin **13** with a **220Ω** resistor.
- Connect Arduino to PC via USB.

### 3. **Upload Arduino Code**
1. Open `arduino_led.ino` in Arduino IDE.
2. Select the correct board & port.
3. Upload the code.

### 4. **Run the Server**
Start the WebSocket server:
```sh
python iot_server.py
```

### 5. **Run Gesture Recognition**
Execute the Python script:
```sh
python gesture_recognition.py
```

## How It Works
1. **Hand Detection**: The camera captures hand gestures.
2. **Gesture Processing**: MediaPipe detects if the hand is **open** or **closed**.
3. **Arduino Communication**: The script sends `'1'` (LED ON) or `'0'` (LED OFF) via serial.
4. **WebSocket Update**: The server updates the UI in real-time.
## Added a simple html,css based webpage to show result
  To access the page,go to http://127.0.0.1:5000/ after running 
  ```sh
  python iot_server.py
```
## Troubleshooting
- Ensure the correct **COM port** is used in `gesture_recognition.py`.
- If the LED does not respond, check Arduino serial communication.
- If the webcam doesn’t work, verify OpenCV installation.

