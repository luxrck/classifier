#!/usr/bin/python2

import sys
import argparse
from urlparse import urlparse
import cv2
import numpy as np
from classifier import *
import pdb
parser = argparse.ArgumentParser(prog="generate faces")
parser.add_argument("-s", "--source", nargs=1, default=["0"], help="video source: default(camera)")
parser.add_argument("-e", "--extension", nargs=1, default=["pgm"], help="output image extension")
parser.add_argument("-o", "--output", nargs=1, help="output class location")
parser.add_argument("-c", "--config", nargs=1, help="face classifier config file")

def main():
	args = args = parser.parse_args(sys.argv[1:])
	video = args.source[0]
	if video == '0': video = int(video)
	clsuri = args.output[0]
	ext = args.extension[0]
	cfg = args.config[0]

	cam = cv2.VideoCapture(video)
	if cfg:
		cvfacerecognizer = CvFaceRecognizer(cfg)

	if os.path.exists(clsuri):
		try:
			os.rmdir(clsuri)
		except:
			os.remove(clsuri)
	os.mkdir(clsuri)

	count = 0
	sstate = False
	while True:
		state, frame = cam.read()
		if not state:
			break
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#frame = cv2.equalizeHist(frame)

		x,y,w,h = (0, 0, -1, -1)

		if cfg:
			results = cvfacerecognizer.recognize(frame)
			if results != tuple() and results.all():
				x,y,w,h = results[0]
				cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0))

		cv2.imshow("preview", frame)

		k = cv2.waitKey(30)

		if sstate:
			save_uri = clsuri + "/" + "%02d"%count + "." + ext
			if cfg and x == y == 0 and w == h == -1:
				continue
			print("save: "+ save_uri)
			cv2.imwrite(save_uri, frame[y:y+h, x:x+w])
			count += 1
			sstate = False
			continue

		# key: q to quit
		if k == ord(b'q'):
			break

		# key: s to save
		elif k == ord(b's'):
			sstate = True
			save_uri = clsuri + "/" + "%02d"%count + "." + ext
			if cfg and x == y == 0 and w == h == -1:
				continue
			print("save: "+ save_uri)
			cv2.imwrite(save_uri, frame[y:y+h, x:x+w])
			count += 1
			sstate = False

if __name__ == "__main__":
	sys.exit(main())
