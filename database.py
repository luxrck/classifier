import os
import json

import cv2
import numpy
from numpy.linalg import norm
from numpy import zeros, array, matrix

imread = lambda img: cv2.imread(img, cv2.IPL_DEPTH_8U)
dbconffile = "database.json"

class SRCFaceDatabase(object):
	def __init__(self, dburl=""):
		self.dburl = dburl
		self.loaddb(dburl)

	def loaddb(self, dburl):
		if not dburl: return
		items = os.listdir(dburl)
		if dbconffile in items:
			items = list(json.load(open(dburl + '/' + dbconffile)).items())
		else:
			items = [{"class": k, "location": k, "description": k} for k in items]

		for i, db in enumerate(items):
			data = []
			for j in os.listdir(dburl + '/' + db['location']):
				data.append(imread(dburl + '/' + db['location'] + '/' + j))
			db.update({"data": data})
		self.database = items

	def cols(self, i):
		base = 0
		db = self.database
		for j in range(len(db)):
			if j == i:
				break
			base += len(db[j]["data"])
		return range(base, base+len(db[i]["data"]))

	info = lambda self, i: self.database[i]


	def A(self, dim):
		if not getattr(self, 'database'):
			raise AttributeError("SRC Face Database isn't loaded.")
		
		if not dim or len(dim) != 2 or not dim[0] * dim[1]:
			raise ValueError("Image dimention value is not valid.")

		A = array([], dtype='float64')
		r,c = dim[0] * dim[1], 0
		
		for i in self.database:
			d = i['data']
			c += len(d)
			for v in d:
				v = cv2.resize(v, dim)
				v = cv2.normalize(v, dtype=cv2.CV_64F)
				A = numpy.append(A, v[:])
		A.shape = (c, r)
		A = matrix(A)
		return A.T
