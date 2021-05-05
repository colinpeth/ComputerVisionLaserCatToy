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

laser = serial.Serial('/dev/ttyACM0',115200,timeout=0)


# load the object detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=.2)

# create video sources & outputs
input = jetson.utils.videoSource("/dev/video0")
output = jetson.utils.videoOutput("display://0")

# process frames until the user exits
while True:
	# capture the next image
	img = input.Capture()

	# detect objects in the image (with overlay)
	detections = net.Detect(img)


	# print the detections
	#print("detected {:d} objects in image".format(len(detections)))

	for detection in detections:
                #print(detection.ClassID)
                #print(detection.Center)
                #print(detection)
                if detection.ClassID == 88:
                    print("BEAR TIME")
                    print(detection.Center)
                    loc = detection.Center
                    lloc = (720-loc[1])/720
                    newLoc = (lloc*35)+10
                    sendStrTilt = "T"+str(int(newLoc)).rjust(3,"0")

                    PanLoc = (loc[0])/1080
                    newLocP = 105-(PanLoc*60)
                    sendStrPan = "P"+str(int(newLocP)).rjust(3,"0")
                    print(sendStrTilt)
                    laser.write(sendStrTilt.encode())
                    #time.sleep(.1)
                    #laser.flush()

                    print(sendStrPan)
                    laser.write(sendStrPan.encode())
                    #time.sleep(.1)

                    #time.sleep(1)
                    #laser.flush()

	# render the image
	output.Render(img)

	# update the title bar
	# print out performance info
	#net.PrintProfilerTimes()

	# exit on input/output EOS
	#if not input.IsStreaming() or not output.IsStreaming():
		#break


