import serial

with serial.Serial('/dev/ttyACM0',115200, timeout=10) as ser:
    while True:
        userIn = input("Input:")
        ser.write(bytes(userIn,'utf-8'))
