#include <Stepper.h>

const int stepsPerRevolution = 200; // Steps per revolution for the stepper motor theta motor
const int stepsPerLine = 200; // Steps per for the r motor
const int motor1StepPin = 2; // Motor 1 (theta) step pin
const int motor1DirPin = 3; // Motor 1 (theta) direction pin
const int motor2StepPin = 4; // Motor 2 (r) step pin
const int motor2DirPin = 5; // Motor 2 (r) direction pin

Stepper motorTheta(stepsPerRevolution, motor1DirPin, motor1StepPin); // Theta motor
Stepper motorR(stepsPerLine, motor2DirPin, motor2StepPin);     // R motor

bool shouldSpin = false;
short int spin_step = 0;

void setup() {
  Serial.begin(9600);
  motorTheta.setSpeed(60); // Set speed in RPM
  motorR.setSpeed(60);     // Set speed in RPM
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    processCommand(command);
  }

  if (shouldSpin) {
    stepSpin();
  }
  else
    spin_step = 0;
}

void processCommand(String command) {
  if (command == "SPIN") {
    shouldSpin = true;
  } 
  else if (command == "STOP") {
    shouldSpin = false;
  }
  else if (command.startsWith("MOVE:")) {
    extractAndExecuteMove(command);
  }
}

void extractAndExecuteMove(String command) {
  // Extract r and theta values from command
  int separatorIndex = command.indexOf(',');
  float r = command.substring(5, separatorIndex).toFloat();
  float theta = command.substring(separatorIndex + 1).toFloat();

  executeMove(r, theta);
}

void executeMove(float r, float theta) {
  // Convert polar coordinates to steps for motors
  int thetaSteps = calculateThetaSteps(theta);
  int rSteps = calculateRSteps(r);

  // Move motors
  motorTheta.step(thetaSteps);
  motorR.step(rSteps);
}
