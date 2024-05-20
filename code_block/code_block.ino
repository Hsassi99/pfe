#include <Servo.h>
#include <Wire.h>
#include <SoftwareSerial.h>

// Create servo objects to control ESCs
Servo motor1, motor2, motor3, motor4;
// Define the pins connected to the ESCs
const int motorPin1 = 3;
const int motorPin2 = 5;
const int motorPin3 = 6;
const int motorPin4 = 9;

char command;

// Define SoftwareSerial RX and TX pins
const int rxPin = 10;
const int txPin = 11;
SoftwareSerial bluetoothSerial(rxPin, txPin);  // RX, TX

void setup() {
  Serial.begin(9600);   // Initialize Serial for USB communication
  bluetoothSerial.begin(9600);  // Initialize SoftwareSerial for Bluetooth communication
  Wire.begin();         // Initialize I2C communication
  motor1.attach(motorPin1);
  motor2.attach(motorPin2);
  motor3.attach(motorPin3);
  motor4.attach(motorPin4);
  pinMode(7,OUTPUT);
}

void loop() {
  // if (Serial.available() > 0) {
  //   command = Serial.read();  // Read from Serial (USB)
  //   for (int i = 1700; i > 1000; i--) {
  //     stop(i);
  //     delay(25);  // Corrected from Sleep to delay
  //   }
  // }

  if (bluetoothSerial.available() > 0) {
    command = bluetoothSerial.read();  // Read from SoftwareSerial (Bluetooth)
    processCommand(command);
  }
}

void processCommand(char command) {
  switch (command) {
    case 'F':
      digitalWrite(7,HIGH);
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

void forward() {
  motor1.writeMicroseconds(1700);  // Adjust microsecond values to your specific setup
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

void stop(int x) {
  motor1.writeMicroseconds(x);
  motor2.writeMicroseconds(x);
  motor3.writeMicroseconds(x);
  motor4.writeMicroseconds(x);
}
