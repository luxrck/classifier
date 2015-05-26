import os
import json

import cv2
import numpy
from numpy.linalg import norm
from numpy import zeros, array, matrix

from database import *

class SRCFaceClassifier(object):
	def __init__(self, solver):
		self.solver = solver

	def classify(self, db, y, imgsize=(16, 16), maxiter=1000):
		def rx(x, i):
			ret = matrix([[0] for j in range(len(x))], dtype='float64')
			for j in db.cols(i):
				ret[j] = x[j]
			return ret
		
		ry = lambda A, x, e, y, i: norm(y-e-A*rx(x,i), 2)

		minclass = lambda A, x, e, y: min((ry(A, x, e, y, i), i) for i in range(len(db.database)))
		
		def sci(x):
			k = len(db.database)
			lx1 = norm(x, 1)
			if not lx1: return 0
			return (k*max(norm(rx(x,i), 1) for i in range(k))/lx1 - 1)/(k-1)

		r, c = imgsize
		s = r * c
		#pdb.set_trace()

		A = db.A(imgsize)
		y = cv2.resize(y, imgsize)

		y.shape = (s, 1)
		#pdb.set_trace()
		y = cv2.normalize(y, dtype=cv2.CV_64F)

		B = numpy.append(A, numpy.eye(s), 1)

		t = self.solver.solve(B, y, maxiter)
		x = t[:-s]
		e = t[-s:]
		#e = zeros((r * c, 1), dtype='float64')
		#pdb.set_trace()

		fci = minclass(A, x, e, y)
		#pdb.set_trace()
		return db.info(fci[1]), sci(x)

class CvFaceRecognizer(object):
	def __init__(self, url):
		self.classifier = cv2.CascadeClassifier(url)

	def recognize(self, img, gray=False):
		if gray:
			img = cv2.cvtColor(img, cv2.COLOR_B2GGRAY)

		return self.classifier.detectMultiScale(img, 1.1, 5, minSize=(30, 30))