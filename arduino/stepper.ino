#include<string.h>


#define MAX_INPUT_LENGTH 50  // Maximum length of input

enum dir {
  CLOCKWISE = HIGH, ANTICLOCKWISE = LOW
};

const int stepsPerRevolution = 200;


//const int resetPin1 = 10;
//const int resetPin2 = 11;

const int dirPin1 = 2;
const int stepPin1 = 3;


const int motor1Factor = 10; //calculate accoding to design
const int motor1Limit1 = motor1Factor*stepsPerRevolution; 
int motorPos1 = 0

const int motor2Factor = 10; //calculate accoding to design
const int motor1Limit2 = motor2Factor*stepsPerRevolution; 
int motorPos2 = 0




void setup()
{
  // Declare pins as Outputs
   Serial.begin(115200);

  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);

//  turnMotor1(200, CLOCKWISE);


}
void loop()
{
   char inputData[MAX_INPUT_LENGTH]; 

//   if (Serial.available() > 0) {
//    readSerialData(inputData, MAX_INPUT_LENGTH);
//    processCommand(inputData);
//  }

  digitalWrite(dirPin1, HIGH);

  for(int x = 0; x < stepsPerRevolution; x++)
  {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(4000);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(4000);
  }

     delay(1500);

  
}



void readSerialData(char *buffer, int maxLength) {
  int index = 0;
  char incomingByte;

 
  // Read each byte until we get a newline or reach the maximum length
  while (index < maxLength - 1) {
    if(Serial.available() > 0){
      incomingByte = Serial.read();

    // Check for newline character (depends on your serial terminal settings)
    if (incomingByte == '\n' || incomingByte == '\r') {
      break;
    }

    // Add the incoming byte to our buffer
    buffer[index] = incomingByte;
    index++;
      
    }
    
  }

  // Null-terminate the buffer to create a valid string
  buffer[index] = '\0';
}


void processCommand(char* command) {

    char tkns[4][10];
    char * pch;

    pch = strtok (command, " ");

    int idx = 0;
    while (pch != NULL && idx < 4)
    {
       strcpy(tkns[idx++], pch);
    }

   char* cmd = tkns[0];

  if (strcmp(cmd, "CIRCLE") == 0) {

    
  }
  //Not tested
  else if (cmd == "GO") {
       int r = atoi(tkns[1]);
       int theta = atoi(tkns[2]);
       
       int rot1[2] = getRotDif(theta);
       turnMotor1(rot1[0], rot1[1]);

       //TODO: move linear actuator
       //turnMotor2(int steps, dir d)

  }
    else if (cmd == "RESET") {
       
       
  }
  else {
    unknownCommand(cmd);
  }
}

void unknownCommand(String command) {
  Serial.println("Unknown command: " + command);
}


int* getRotDif(theta){
    int ret[2];
    int diff = (int) (theta/1.8) - motor1Pos;
    ret[0] = diff<0?-diff:dif;
    ret[1] = diff<0?CLOCKWISE: ANTICLOCKWISE;

    return ret;
    
}

 //Tested
void turnMotor1(int steps, dir d) {
  
  digitalWrite(dirPin1, d);

  // Spin motor slowly
  for(int x = 0; x < steps; x++)
  {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(1000);
  }
}
