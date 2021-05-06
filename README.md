# ComputerVisionLaserCatToy
This is a computer vision laser cat toy.

# Required Parts:
  - Nvidia Jetson Nano
  - USB Web Camera
  - Arduino Uno
  - 5v Laser Diode
  - 2 Servo Motors
 
 # Assembly:
  - To create the Laser mount I 3D printed the following mount out of PLA and assembled.
      - [Laser Mount](https://www.thingiverse.com/thing:2104280)
  - The arduino Uno software is flashed using the Arduino IDE. The required file is found within the Arduino Folder 
  - The servos are connected to the arduino. The pan is connected to pin 11 and tilt to pin 10. The laser diode and servo motors positive and negative are connected to the arduino using a breadboard.
  - The NVIDA Jetson Nano is flashed with there operating system. Jetson interfaces is required to utilize an external camera. 
  - Connect the Web Cam and Arduino to the onboard usb ports on the jetson
  - Run the PlayTime.py file as a super user and the system should boot and be fully functional.


# Arduino Program
  ### Required Libraries:
  - Servo
  ### Program Flow:
  - The program starts by looking at indivual bytes until it sees a T or P for tilt or pan. It then pulls the following 3 bytes in order to get the position. The program then will move the laser to the desired location and hold until new value is entered. 
  - Reading in indiviual bytes is required in order for the system to be able to read in the new values fast enough.
# Jetson Program (PlayTime.py):
  ### Required Libraries:
  - jetson.inference
  - jetson.utils
  - serial
  - argparse
  - sys
  - time
  - random
  ### Program Flow:
  - This program is a python class called PlayTime. To create a class object you must pass 2 values into the constructor. It requires the serial port for the arduino along with the baudrate. The class itself contains 2 main methods. The first is the RunChase method. This method runs the auto chase system that moves the laser depending on the desired objects location. The other main method is LiveTrack. This will attempt to place the laser on a desired object and track it as it moves in the view of the camera.
  - Within the __init__ method both the panBounds and tiltBounds must be configured. To configure these run computerVision.py to see what the camera sees. Next use serial_send.py in order to move the laser pointer. Find the bounds of how must pan the laser has to the left and the right as well as up and down. Once these values are set the system is fully configured.
  - Extra Options:
      - self.tolerance varaible is a boolean for how close you require the object to be to the laser in order for it to move to another location. I recommed between .3 and .7.
