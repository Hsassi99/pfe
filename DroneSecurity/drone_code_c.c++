#include <Servo.h>
#include <Wire.h>

// Create servo objects to control ESCs
Servo motor1, motor2, motor3, motor4;



// Define the pins connected to the ESCs
const int motorPin1 = 3;
const int motorPin2 = 5;
const int motorPin3 = 6;
const int motorPin4 = 9;

char command;

// Gyroscope and accelerometer data
int16_t ax, ay, az, gx, gy, gz;

void setup() {
  Serial.begin(9600);
  Wire.begin();


  // Attach each ESC to its respective pin
  motor1.attach(motorPin1);
  motor2.attach(motorPin2);
  motor3.attach(motorPin3);
  motor4.attach(motorPin4);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();
    Stop();  // Stop all motors before setting new direction
    switch (command) {
      case 'F':
        forward();
        break;
      case 'B':
        back();
        break;
      case 'R':
        right();
        break;
      case 'L':
        left();
        break;
    }
  }

}
void forward() {
  motor1.writeMicroseconds(1700);
  motor2.writeMicroseconds(1700);
  motor3.writeMicroseconds(1700);
  motor4.writeMicroseconds(1700);
}

void back() {
  motor1.writeMicroseconds(1300);
  motor2.writeMicroseconds(1300);
  motor3.writeMicroseconds(1300);
  motor4.writeMicroseconds(1300);
}

void left() {
  motor1.writeMicroseconds(1300);
  motor2.writeMicroseconds(1300);
  motor3.writeMicroseconds(1700);
  motor4.writeMicroseconds(1700);
}

void right() {
  motor1.writeMicroseconds(1700);
  motor2.writeMicroseconds(1700);
  motor3.writeMicroseconds(1300);
  motor4.writeMicroseconds(1300);
}

void Stop() {
  motor1.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
}
