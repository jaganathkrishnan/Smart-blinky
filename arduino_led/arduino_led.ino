#define LED_PIN 11  // Use PWM-capable pin (not 13)

void setup() {
    pinMode(LED_PIN, OUTPUT);
    Serial.begin(9600);  // Start serial communication
}

void loop() {
    if (Serial.available() > 0) {  // Check if data is received
        int brightness = Serial.parseInt();  // Read brightness value (0-255)
        brightness = constrain(brightness, 0, 255); // Ensure within range
        analogWrite(LED_PIN, brightness);  // Adjust LED brightness
        Serial.print("LED Brightness: ");
        Serial.println(brightness);  // Print brightness value
    }
}
