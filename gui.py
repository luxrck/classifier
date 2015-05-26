import sys
import threading

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickImageProvider
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent

from recognizer import *
from solver import *

import resources

imread = lambda img: cv2.imread(img, cv2.IPL_DEPTH_8U)

class Recognizer(object):
	def __init__(self, engine, recognizer):
		self.workers = {}
		self.databases = {}
		self.recognizer = recognizer

		self.window = engine.rootObjects()[0]

		self.window.databaseLoad.connect(self.onDatabaseLoad)
		self.window.databaseLoadCancel.connect(self.onDatabaseLoadCancel)
		self.window.faceRecognize.connect(self.onFaceRecognize)
		self.window.faceRecognizeCancel.connect(self.onFaceRecognizeCancel)

	def run(self):
		self.window.show()

	db = lambda self, url: self.databases.get(url.path())

	def onDatabaseLoad(self, dburl):
		def worker():
			path = dburl.path()
			dbs = self.databases
			if not dbs.get(path):
				dbs[path] = SRCFaceDatabase(path)
			self.window.databaseLoadComplete.emit(dburl.fileName(), dburl)
		th = threading.Thread(target=worker)
		th.daemon = True
		th.start()

	def onDatabaseLoadCancel(self, dburl):
		db = self.databases
		if not db.get(source):
			return
		del db[source]

	def onDatabaseChanged(self, dburl):
		self.currentdb = self.db(dburl)

	def onFaceRecognize(self, dburl, source, dbimgsize, threshold):
		def worker():
			db = self.db(dburl)
			img = imread("/tmp/preview_1")
			imgsize = (int(dbimgsize.height()), int(dbimgsize.width()))
			
			d,s = self.recognizer.recognize(db, img, imgsize, threshold)
			
			basedir = db.dburl + '/' + d['location']
			previewimgs = ["file://" + basedir + '/' + i for i in os.listdir(basedir)[:3]]

			self.window.faceRecognizeComplete.emit(source, d, previewimgs)
		worker()

	def onFaceRecognizeCancel(self, source):
		pass

def startgui():
	app = QApplication(sys.argv)

	engine = QQmlApplicationEngine()
	engine.load(QUrl("qrc:/asserts/gui.qml"))

	srcrecog = Recognizer(engine, SRCFaceRecognizer(DALMSolver()))
	#pdb.set_trace()
	srcrecog.run()

	return app.exec_()