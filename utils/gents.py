#!/usr/bin/python2

import sys
import cv2
import pdb
import numpy as np
from dsrc import *
from recognizer import *

scount = lambda c: (b'00' if c < 10 else b'0') + bytes(c)

video = sys.argv[1]
if video == '0':
	video = int(video)

od = sys.argv[2]
on = sys.argv[3]

ext = '.pgm'

cam = cv2.VideoCapture(video)

fdb = [i for i in loaddb('attfaces')]
e = cv2.createEigenFaceRecognizer(2500)
d = fdb[0][1]
e.train(d, np.array([1 for j in range(len(d))]))
v = e.getMat('eigenvectors')
v = np.transpose(v)

count = 0
fvalid = True
recognizer = CvFaceRecognizer("faces.xml")
while fvalid:
	fvalid, frame = cam.read()
	if not fvalid:
		break
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = cv2.equalizeHist(frame)
	#nframe = cv2.resize(frame, (20,20))
	#nframe = 
	#vf = np.array([])
	#vf = cv2.normalize(v[0], vf, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
	#vt = vf[:400]
	#vf.shape = (112, 92)
	#vt.shape = (20,20)
	#pdb.set_trace()
	#faces = recognizer.recognize(frame)
	#for x, y, w, h in faces:
	#	cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	cv2.imshow("test", frame)
	#cv2.imshow("eves", vf)
	#cv2.imshow("vt", vt)
	k = cv2.waitKey(30)
	if k == ord(b'q'):
		break
	elif k == ord(b's'):
		if count < 100:
			try:
				print('save %s' % (on+scount(count)))
				cv2.imwrite(od+'/'+on+scount(count)+ext, frame)
				count += 1
			except Exception as e:
				print(e)
