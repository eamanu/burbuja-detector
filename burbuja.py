"""
Code based on https://www.pyimagesearch.com/
eamanu
"""
from imutils.video import VideoStream
from collections import defaultdict
import argparse
import imutils
import time
import cv2
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1, help="minimum area size")
ap.add_argument("-b", "--buffer", type=int, default=4, help="max buffer size")
args = vars(ap.parse_args())

# WebCam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# estelas = defaultdict(list)

cv2.namedWindow("Thresh", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Thresh",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

key = 0

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"
    if frame is None:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=1080)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
   
    # loop over the contours
    counter = 0
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # ((x, y), radius) = cv2.minEnclosingCircle(c)
        # M = cv2.moments(c)
        # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # estelas[counter].append(center)
        # if len(estelas[counter]) > 10:
        #     estelas[counter].pop(0)
        # (x, y, w, h) = cv2.boundingRect(c)
        # cv2.rectangle(thresh, (x, y), (x + w, y + h), (255,255,255), 2)
        cv2.namedWindow("Thresh", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Thresh",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        
        cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        counter += 1
    if key == ord("q"):
        vs.stop() if args.get("video", None) is None else vs.release()
        cv2.destroyAllWindows()


    # Dibujo estelas
"""
    for k, v in estelas.items():
        if len(v) < 10:
            continue
        i = 0
        for coord_estelas in v:
            if i == 0:
                i += 1
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(thresh, v[i - 1], v[i],
                     (255, 255, 255), thickness)
            cv2.imshow("Thresh", thresh)
            i += 1
            key = cv2.waitKey(1) & 0xFF
"""

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
