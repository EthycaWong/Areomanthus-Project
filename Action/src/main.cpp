#include <Arduino.h>
#include <ESP32Servo.h>

const int Claw = 12;
const int Claw2 = 19;

const int wrist = 33;
const int wrist2 = 25;
bool clawState = false;
bool clawState2 = false;
bool wristState = false;
bool wristState2 = false;

Servo myServo;
Servo myServo2;
Servo myServo3;
Servo myServo4;

void setup() {
    Serial.begin(9600);
    myServo.attach(Claw);
    myServo.write(0);
    myServo2.attach(Claw2);
    myServo2.write(0);
    myServo3.attach(wrist);
    myServo3.write(90);
    myServo4.attach(wrist2);
    myServo4.write(90);
}

void loop() {
    if (Serial.available() > 0) {
        char signal = Serial.read();
        if (signal == 'T') {
            clawState = !clawState;
            clawState2 = !clawState2;
            myServo.write(clawState ? 90 : 0);
            myServo2.write(clawState2 ? 90 : 0);
        }

        if (signal == '1') {
            wristState = !wristState;
            wristState2 = !wristState2;
            myServo3.write(wristState ? 0 : 90);
            myServo4.write(wristState2 ? 0 : 90);
        }
    }
}
