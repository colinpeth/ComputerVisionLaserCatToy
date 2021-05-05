import serial

class ServoSerial:
    def __init__(self, serialPort='/dev/ttyACM0',baudRate=115200, timeout=10:
            self.serialPort = serial.Serial(serialPort,baudRate,timeout=10)
         
