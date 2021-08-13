
# The code stub is tskane from the link below and modified to add gesture recognition using
# vector algebra and integration of Twilio and Blinkt! using MQTT
# https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
import paho.mqtt.client as mqtt
# import matplotlib.pyplot as plt
import numpy as np
import argparse
import imutils
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# Orange 0-22  Yellow 22- 38  Green 38-75  Blue 75-130  Violet 130-160  Red 160-179

greenLower = (38, 90, 90)
greenUpper = (70, 225, 255)

pts = deque(maxlen=args["buffer"])

# This is the Publisher
client = mqtt.Client()
client.connect("test.mosquitto.org",1883,600)

alarmTriggered = False

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=1000)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 20:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# update the points queue
	pts.appendleft(center)

	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	isCirclePts = [p for p in pts if p is not None]

	if (len(isCirclePts) > 30):

		vectors = [np.subtract(t, s) for s, t in zip(isCirclePts, isCirclePts[1:])]

		vectors = [vector for vector in vectors if np.linalg.norm(vector) > 5]

        # To find concavity, check vector direction using Right Hand rule
		determ = [np.linalg.det([s, t]) for s, t in zip (vectors, vectors[1:])]

		directionChange = [determ[i] * determ[i + 1] for i in range (len(determ) - 1)]

		# when the movement of the object is insignificant, consider it stationary
		if len(directionChange) < 10:
			alarmTriggered = False
			continue

        # Find the location of negative indices
		negIndices = [i for i, direction in enumerate(directionChange) if direction < 0]

		zigzagCount = len(negIndices)
		zigzagRatio = zigzagCount / len(directionChange)
		if zigzagCount > 0:
			zigzagVariance =  np.var(negIndices)
		else:
			zigzagVariance = 0

		# print ("zigzagCount = " + str(zigzagCount) + " zigzagRatio = " + str(zigzagRatio) + " zigzagVariance = "+ str(zigzagVariance))

		if zigzagCount == 0 or (zigzagRatio < 0.05 and zigzagVariance < 100):
			print('CIRCLE. Alarm = ' + str(alarmTriggered))
			if not alarmTriggered:
				client.publish("safetycam/topic/blinkt", "red")
				os.system(
					'espeak \"ALERT ALERT ALERT ALARM TRIGGERED Someone needs help urgently. Please do the needful at the earliest\"')
				alarmTriggered = True
		else:
			print('NOT CIRCLE')
			alarmTriggered = False


	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()