#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils
import serial

import argparse
import sys
import time
import random


class PlayTime:
    def __init__(self,serialPort, baudrate):
        self.tiltBounds = [10,41]
        self.panBounds = [53,140]
        self.laserPosition = [0,0] #[pan,tilt]
        self.laserObj = serial.Serial(serialPort,baudrate, timeout=0)
        self.tolerance = .70

    def heightToTilt(self, height):
        position = (720-height)/720
        tilt = (position*(self.tiltBounds[1]-self.tiltBounds[0]))+self.tiltBounds[0]
        return int(tilt)


    def widthToPan(self, width):
        position = (720-width)/720
        pan = (position*(self.panBounds[1]-self.panBounds[0]))+self.panBounds[0]
        return int(pan)
   
    def moveLaser(self, pan, tilt):
        tiltStr = "T"+str(tilt).rjust(3,"0")
        self.laserObj.write(tiltStr.encode())
        self.laserPosition[1]=tilt

        panStr = "P"+str(pan).rjust(3,"0")
        self.laserObj.write(panStr.encode())
        self.laserPosition[0]=pan

        print(tiltStr,"|",panStr)
    
    def isAtPosition(self, position):
        pan = self.widthToPan(position[0])
        tilt = self.heightToTilt(position[1])
        print("Cat Position", pan, tilt)

        Left =int( self.laserPosition[0]*(1-self.tolerance))
        Right =int( self.laserPosition[0]*(1+self.tolerance))
        top =int( self.laserPosition[1]*(1+self.tolerance))
        bottom =int( self.laserPosition[1]*(1-self.tolerance))
        print(top,bottom,Left, Right)
        
        if tilt < top and tilt > bottom:
            print("Tilt Correct")
        if pan > Left and pan < Right: 
            print("Pan Correct")
            if tilt < top and tilt > bottom:
                print("dfjghdksjgkl")
                print("dfjghdksjgkl")
                print("dfjghdksjgkl")
                print("dfjghdksjgkl")
                print("dfjghdksjgkl")
                print("dfjghdksjgkl")
                return True

        return False

        

    def RunChase(self):
        inputObj = jetson.utils.videoSource("/dev/video0")
        output = jetson.utils.videoOutput("display://0")
        net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=.2)

        newPan = random.randint(self.panBounds[0],self.panBounds[1])
        newTilt = random.randint(self.tiltBounds[0],self.tiltBounds[1])
        self.moveLaser(newPan, newTilt)
        self.laserPosition = [newPan, newTilt]
        while True:
            img = inputObj.Capture()
            detections = net.Detect(img)
            for detection in detections:
                if detection.ClassID==1:
                    if self.isAtPosition(detection.Center):
                        newPan = random.randint(self.panBounds[0],self.panBounds[1])
                        newTilt = random.randint(self.tiltBounds[0],self.tiltBounds[1])
                        self.moveLaser(newPan, newTilt)
                        self.laserPosition = [newPan, newTilt]
                        

            output.Render(img)
            
    def LiveTrack(self):
        inputObj = jetson.utils.videoSource("/dev/video0")
        output = jetson.utils.videoOutput("display://0")
        net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=.2)
        while True:
            img = inputObj.Capture()
            detections = net.Detect(img)
            for detection in detections:
                if detection.ClassID==88:
                    pan = self.widthToPan(detection.Center[0])
                    tilt = self.heightToTilt(detection.Center[1])
                    self.moveLaser(pan, tilt)
            output.Render(img)

    def moveLaserTilt(self, tilt, laserObj):
        newTilt = random.randint(10,45)
        return newPan
    def moveLaserPan(self, pan, laserObj):
        newPan = random.randint(45,105)
        return newPan


if __name__ == "__main__":
    run = PlayTime('/dev/ttyACM0',115200)
    run.RunChase()

