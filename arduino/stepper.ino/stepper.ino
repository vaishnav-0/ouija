#include<string.h>

#define BUFFER_SIZE 256


char circularBuffer[BUFFER_SIZE]; // Circular buffer to store serial data
int head = 0;  // Head index for the next write
int tail = 0;  // Tail index for the next read




enum motorSpeed{
  MOTOR_SLOW = 4000, MOTOR_MEDIUM = 2000, MOTOR_FAST = 1000
  };


#define ACCEL_STEPS 50
#define MAX_INPUT_LENGTH 50  // Maximum length of input
char commandBuffer[MAX_INPUT_LENGTH];

enum dir {
  CLOCKWISE = HIGH, ANTICLOCKWISE = LOW
};

const int stepsPerRevolution = 200;


const int resetPin1 = 10;
const int dirPin1 = 2;
const int stepPin1 = 3;

const int resetPin2 = 11;
const int dirPin2 = 4;
const int stepPin2 = 5;

const int motor1Limit1 = 925;//.(int)(motor1Factor/2)*stepsPerRevolution;
int motorPos1 = 0;
motorSpeed motorSpeed1 = MOTOR_MEDIUM;

const int motor1Limit2 = 4300;//motor2Factor*stepsPerRevolution;
int motorPos2 = 0;
motorSpeed motorSpeed2 = MOTOR_FAST;

int resetting = 0;
int goCommand = 0;


void setup()
{
  // Declare pins as Outputs
   Serial.begin(115200);

  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(resetPin1, INPUT_PULLUP);

  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(resetPin2, INPUT_PULLUP);


  resetMotor(1);
  resetMotor(2);

}


void loop()
{


   fillBuffer();

   if (isDataAvailable()) {
    int com_avail = readCommandBuffer(commandBuffer, MAX_INPUT_LENGTH);

    if(com_avail){
          processCommand(commandBuffer);

    }

    fillBuffer();

  }else{
      if(goCommand){
        Serial.println("*");
        goCommand = 0;
      }

    }

}


void fillBuffer(){
  while (Serial.available()) {
        if (!isBufferFull()) {
          char incomingByte = Serial.read();
          writeBuffer(incomingByte);

        }else{
          Serial.println("Buffer full");
          break;
        }
  }

}


void writeBuffer(char b) {
  circularBuffer[head] = b;
  head = (head + 1) % BUFFER_SIZE;
}

char readBuffer() {
  char byte = '\0';
  if (isDataAvailable()) { // Check if data is available
    byte = circularBuffer[tail];
    tail = (tail + 1) % BUFFER_SIZE;
  }
  return byte;
}

bool isDataAvailable() {
  return head != tail;
}

bool isBufferFull() {
  return (head + 1) % BUFFER_SIZE == tail;
}


bool isBufferEmpty() {
  return head == tail;
}


int readCommandBuffer(char *buffer, int maxLength) {
  static int index = 0; // Maintain the position across calls
  char incomingByte;


  // Read each byte until we get a newline or reach the maximum length
  //TODO: Handle edge case where full command is not in the buffer
  while (index < maxLength - 1) {
    if(isDataAvailable()){
      incomingByte = readBuffer();

    // Check for newline character (depends on your serial terminal settings)
    if (incomingByte == '\n' || incomingByte == '\r') {
        // Null-terminate the buffer to create a valid string
        buffer[index] = '\0';
        index = 0; // Reset index for next command
        return 1;
    }

    // Add the incoming byte to our buffer
    buffer[index] = incomingByte;
    index++;

    }else{
      return 0;
    }

  }

  return 1;


}


void processCommand(char* command) {

    char tkns[4][10];
    char * pch;

    pch = strtok (command, " ");

    int idx = 0;
    while (pch != NULL && idx < 4)
    {
       strcpy(tkns[idx++], pch);
       pch = strtok (NULL, " ");
    }

   char* cmd = tkns[0];

  if (strcmp(cmd, "CIRCLE") == 0) {
    int center = (motor1Limit2 - 700)/2;
    int ninety = motor1Limit1/2;
    goTogether(center, 0); // 0deg
    goTogether(0, ninety); //90deg
    goTogether(center, motor1Limit1); //180deg
    goTogether(motor1Limit2, ninety); //90deg
    goTogether(center, 0); // 0deg


  }
  //Not tested
  else if (strcmp(cmd, "GO") == 0) {

       goCommand = 1;
       int r = atoi(tkns[1]);
       int theta_steps = atoi(tkns[2]);

       if(strcmp(tkns[3], "M") == 0)
          goTogether(r, theta_steps);
       else{
          goToAngleMotor1(theta_steps);
          goToPositionMotor2(r);
       }



       delay(2000);
//       goCenterMotor2();

//       runTwoMotors(stepsR, direcR, stepsL, direcL);

  }
    else if (strcmp(cmd, "SPEED") == 0) {
       int motor_idx = atoi(tkns[1]);
       char speed = tkns[2][0];
       motorSpeed sp;

       switch(speed){
          case 'S':
              sp = MOTOR_SLOW;
              break;
          case 'M':
              sp = MOTOR_MEDIUM;
              break;
          case 'F':
              sp = MOTOR_FAST;

        }

       if(motor_idx == 1){
          motorSpeed1 = sp;
        }else if(motor_idx == 2){
          motorSpeed2 = sp;
          }
  }
      else if (strcmp(cmd, "RESET_F") == 0) {
         int motor_idx = atoi(tkns[1]);

         resetMotor_F(motor_idx);

      }else if (strcmp(cmd, "RESET") == 0) {
               resetMotor(1);
               resetMotor(2);

      }else if (strcmp(cmd, "RESET_SYNC") == 0) {
               resetMotorTogether();

      }else if (strcmp(cmd, "RESET_M") == 0) {
         int motor_idx = atoi(tkns[1]);

               resetMotor(motor_idx);


      }else if (strcmp(cmd, "CALIB") == 0) {

         int idx = atoi(tkns[1]);
         int steps = atoi(tkns[2]);
         int dir = atoi(tkns[3]);

            switch(idx){
                case 1:
                    if(dir){
                        turnMotor1(steps, CLOCKWISE);
                    }else{
                        turnMotor1(steps, ANTICLOCKWISE);
                    }


                    if(!digitalRead(resetPin1))
                        Serial.println(motorPos1);
                  break;

                case 2:
                    Serial.println("motor2");
                     if(dir){
                        turnMotor2(steps, CLOCKWISE);
                    }else{
                        turnMotor2(steps, ANTICLOCKWISE);
                    }

                    if(!digitalRead(resetPin2))
                        Serial.println(motorPos2);
                  break;
            }


      }else {
        unknownCommand(cmd);
  }


}

void goTogether(int r, int theta){
  int stepsR = getRotSteps(theta);
  int direcR = getRotDir(theta);
  int stepsL = getLinearSteps(r);
  int direcL = getLinearDir(r);
  runTwoMotors(stepsR, direcR, stepsL, direcL);

}


void goToAngleMotor1(float theta){
  int stepsR = getRotSteps(theta);
  int direcR = getRotDir(theta);
  turnMotor1(stepsR, direcR);
}

void goToPositionMotor2(int r){
  int stepsL = getLinearSteps(r);
  int direcL = getLinearDir(r);
  turnMotor2(stepsL, direcL);
}

void goCenterMotor2(){
        int center = motor1Limit2/2;
       int stepsL = getLinearSteps(center);
       int direcL = getLinearDir(center);
       turnMotor2(stepsL, direcL);

 }

void unknownCommand(String command) {
  Serial.println("Unknown command: " + command);
}



void resetMotor_F(int idx){
  switch(idx){
   case 1:
      motorPos1 = 0;
      break;
    case 2:
      motorPos2 = 0;
      break;
   }
 }


int getLinearSteps(int pos){
    int diff = pos - motorPos2;
    return diff<0?-diff:diff;
}

int getLinearDir(int pos){
    int diff = pos - motorPos2;
    return diff<0?ANTICLOCKWISE: CLOCKWISE;
}


int getRotSteps(int steps){
    int diff = steps - motorPos1;
    return diff<0?-diff:diff;
}

int getRotDir(int steps){
    int diff = steps - motorPos1;
    return diff<0?ANTICLOCKWISE: CLOCKWISE;
}


int getNewPos(int curr, int steps, int d){
  return curr + steps*(d*2 - 1);
  }

void resetMotor(int idx){
  motorSpeed tmp;
  switch(idx){
   case 1:
      tmp = motorSpeed1;
      motorSpeed1 = MOTOR_SLOW;
      ResetMotor1(motor1Limit1, ANTICLOCKWISE);
      Serial.print("Moved:");
      Serial.println(motorPos1);
      motorSpeed1 = tmp;
      motorPos1 = 0;
      break;
    case 2:

      ResetMotor2(motor1Limit2, ANTICLOCKWISE);
      Serial.print("Moved:");
      Serial.println(motorPos2);
      motorPos2 = 0;
      break;
   }

}

void resetMotorTogether(){
  resetting = 1;
  runTwoMotors(motor1Limit1, ANTICLOCKWISE, motor1Limit2, ANTICLOCKWISE);
  motorPos1 = 0;
  motorPos2 = 0;
  resetting = 0;

}

void turnMotor1(int steps, dir d) {
  turnMotor(stepPin1, dirPin1, &motorPos1, motor1Limit1, steps, d, motorSpeed1, resetPin1, 0);
}

void ResetMotor1(int steps, dir d) {
  turnMotor(stepPin1, dirPin1, &motorPos1, motor1Limit1, steps, d, motorSpeed1, resetPin1, 1);
}

void turnMotor2(int steps, dir d) {
  turnMotor(stepPin2, dirPin2, &motorPos2, motor1Limit2, steps, d, motorSpeed2, resetPin2, 0);
}

void ResetMotor2(int steps, dir d) {
  turnMotor(stepPin2, dirPin2, &motorPos2, motor1Limit2, steps, d, motorSpeed2, resetPin2, 1);
}

 //Tested
void turnMotor(int stepPin, int dirPin, int *pos, int limit, int steps, dir d, int mSpeed, int limitPin, int resetting) {


//  int delta_speed = 500;
  int newPos = getNewPos(*pos, steps, d); // new position if moved step steps

  if(!resetting  && (newPos > limit ||  newPos < 0)){
     Serial.print(newPos);
     Serial.println(": Motion our of limit");
     return;
  }

  int speedCur = mSpeed;// + delta_speed; // Starting speed
//  int accelRate = delta_speed / ACCEL_STEPS;

  digitalWrite(dirPin, d);
  int x;
  for(x = 0; x < steps && (digitalRead(limitPin) || d); x++)
  {
//    Serial.println(speedCur);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(speedCur);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(speedCur);


//    if (x < ACCEL_STEPS && speedCur >= mSpeed) {
//      speedCur -= accelRate;
//    }
//    // Decelerate for last few steps
//    else if (x >= steps - ACCEL_STEPS && speedCur <= mSpeed) {
//      speedCur += accelRate;
//    }

  }
   newPos = getNewPos(*pos, x, d); // new position after movement
  *pos = newPos;

}



void runTwoMotors(int stepsMotor1, dir d1, int stepsMotor2, dir d2) {
    void (*turnFnSmall)(int, dir);
    void (*turnFnBig)(int, dir);

    int maxSteps, minSteps, maxDir, minDir;

    if(stepsMotor1 > stepsMotor2){
          maxSteps = stepsMotor1;
          maxDir = d1;
          minSteps = stepsMotor2;
          minDir = d2;
          turnFnSmall = resetting? &ResetMotor2:&turnMotor2;
          turnFnBig = resetting? &ResetMotor1:&turnMotor1;
    }else{
          maxSteps = stepsMotor2;
          maxDir = d2;
          minSteps = stepsMotor1;
          minDir = d1;
          turnFnSmall = resetting? ResetMotor1 : &turnMotor1;
          turnFnBig = resetting? ResetMotor2: &turnMotor2;
    }

    int bigSteps = maxSteps/minSteps;
    int bigLeft = maxSteps % minSteps;


    for (int i = 0; i < minSteps; i++) {
            turnFnSmall(1, minDir); // Function to step motor 1
            if(bigLeft > 0){
              turnFnBig(bigSteps + 1, maxDir); // Function to step motor 2
              bigLeft--;
            }else{
              turnFnBig(bigSteps, maxDir);
             }
    }
    if(bigLeft > 0)
      turnFnBig(bigLeft, maxDir);
}
