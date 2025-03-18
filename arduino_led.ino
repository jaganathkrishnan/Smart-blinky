#define LED_PIN 13  // LED connected to pin 13

void setup() {
    pinMode(LED_PIN, OUTPUT);
    Serial.begin(9600);  // Start serial communication
}

void loop() {
    if (Serial.available() > 0) {  // Check if data is received
        char command = Serial.read();
        if (command == '1') {
            digitalWrite(LED_PIN, HIGH);  // Turn LED ON
            Serial.println("LED ON");
        } else if (command == '0') {
            digitalWrite(LED_PIN, LOW);   // Turn LED OFF
            Serial.println("LED OFF");
        }
    }
}
