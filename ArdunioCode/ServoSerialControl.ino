
#include <Servo.h>

int    ServoUpper = 1000;
int    ServoLower = 2000;
int    servoPanPin = 10; 
int    servoTiltPin = 11; 
int    servoPosPan = 130; 
int    servoPosTilt = 117;

Servo  servoPan;      
Servo servoTilt;


//Range of Motion is 10 to 180
void MoveTiltPosition(int position){
   //int pos = ((ServoUpper-ServoLower)/(180))*position + 1000;
   servoTilt.write(position);
}

//Range of Motion is 10 to 180
void MovePanPosition(int position){
   //int pos = ((ServoUpper-ServoLower)/(180))*position + 1000;
   servoPan.write(position);
}
void setup() {
  Serial.begin(115200);

  servoPan.attach(servoPanPin);
  servoTilt.attach(servoTiltPin);
  servoPan.write(servoPosPan);
  servoTilt.write(servoPosTilt);
  
   
}

char pos[3] = "000";
void loop() {
  char panStr = 'P';
  char tiltStr = 'T';
  
  //char pos[3] = "000";
  char comm = ' ';
  int i = 0;
  while (Serial.available() >= 0) {
    comm = Serial.read();
    if (comm == panStr || comm == tiltStr) {
      while (Serial.available() < 3);
      Serial.readBytes(pos, 3);
      break;
    }
  }
  
  if (panStr == comm){
    String temp = (String)pos;
    int panPos = temp.toInt();

    //Serial.println("The Pan input is " + temp); 
    MovePanPosition(panPos);
  }
  
  else if (tiltStr == comm){
    String temp = (String)pos;
    int tiltPos = temp.toInt();

    //Serial.println("The Tilt input is " + temp); 
    MoveTiltPosition(tiltPos);
  }
  
  //delay(1000);
}
