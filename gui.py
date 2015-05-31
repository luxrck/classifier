import sys
import threading

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickImageProvider
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent

from classifier import *
from solver import *

import resources

imread = lambda img: cv2.imread(img, cv2.IPL_DEPTH_8U)

class Classifier(object):
	def __init__(self, engine, classifier):
		self.workers = {}
		self.databases = {}
		self.classifier = classifier

		self.window = engine.rootObjects()[0]

		self.window.databaseLoad.connect(self.onDatabaseLoad)
		self.window.databaseLoadCancel.connect(self.onDatabaseLoadCancel)
		self.window.faceClassify.connect(self.onFaceClassify)
		self.window.faceClassifyCancel.connect(self.onFaceClassifyCancel)

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

	def onFaceClassify(self, dburl, source, dbimgsize, threshold, cliparea):
		def worker():
			db = self.db(dburl)
			img = imread("/tmp/preview_1")
			x,y,width,height =[cliparea.property(i).toInt() for i in ["x", "y", "width", "height"]]
			img = img[y:y+height, x:x+width]
			#cv2.imwrite("preview_1.jpg", img)
			imgsize = (int(dbimgsize.height()), int(dbimgsize.width()))

			d,s = self.classifier.classify(db, img, imgsize, threshold)

			basedir = db.dburl + '/' + d['location']
			previewimgs = ["file://" + basedir + '/' + i for i in os.listdir(basedir)[:3]]

			self.window.faceClassifyComplete.emit(source, d, previewimgs)
		worker()

	def onFaceClassifyCancel(self, source):
		pass

def startgui():
	app = QApplication(sys.argv)

	engine = QQmlApplicationEngine()
	engine.load(QUrl("qrc:/asserts/gui.qml"))

	classifier = Classifier(engine, SRCFaceClassifier(DALMSolver()))
	classifier.run()

	return app.exec_()
