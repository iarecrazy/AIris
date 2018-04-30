import sys
from enum import Enum
from eventhandlers import BoundingBoxEventHandler

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ImageView(QGraphicsView):
	def __init__(self):
		super().__init__(QGraphicsScene())
		self.eventHandler = BoundingBoxEventHandler(self)

	def loadImage(self, filename):
		self.imagePixItem = QGraphicsPixmapItem(QPixmap("img/angio.jpg"))
		self.scene().addItem(self.imagePixItem)
		self.eventHandler.setBoundingRect(self.imagePixItem.boundingRect())

	def resetHover(self):
		if(self.hoveringOverRect != None):
			self.hoveringOverRect.setPen(self.pen)
			self.hoveringOverRect.setBrush(self.brush)
			self.hoveringOverRect = None

	# --- events ---
	def resizeEvent(self, resizeEvent):
		super().resizeEvent(resizeEvent)
		self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

	def mousePressEvent(self, event):
		super().mousePressEvent(event)
		self.eventHandler.mousePressEvent(event)

	def mouseMoveEvent(self, event):
		super().mouseMoveEvent(event)
		self.eventHandler.mouseMoveEvent(event)	

	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		self.eventHandler.mouseReleaseEvent(event)

class Application:
	
	def __init__(self):
		self.app = QApplication(sys.argv)
		self.createMainWindow()
		self.app.setWindowIcon(QIcon("img/icon.png"))

	def loadPixmapFromImage(self, filename):
		return QGraphicsPixmapItem(QPixmap(filename)) 

	def createMainWindow(self):
		# create the main window
		self.win	= QWidget()

		# add the grid for layouting
		self.grid 	= QGridLayout(self.win)

		# annotation item list
		self.itemListLabel = QLabel("Annotation Files")
		self.itemList = QListWidget()

		# create canvas for showing image in 
		self.imageView = ImageView()
		self.imageView.loadImage("img/angio.jpg")
		self.imageView.setBackgroundBrush(QBrush(Qt.black, Qt.SolidPattern));

		# create a list for showing image labels in
		self.labelListLabel = QLabel("Label list")
		self.labelList 		= QListWidget()

		# grid.addWidget(widget, row, column, rowSpan, colSpan)
		self.grid.addWidget(self.itemListLabel	, 0, 0)
		self.grid.addWidget(self.labelListLabel	, 0, 2)

		# grid.addWidget(widget, row, column, rowSpan, colSpan)
		self.grid.addWidget(self.itemList	, 1, 0)
		self.grid.addWidget(self.imageView 	, 1, 1)
		self.grid.addWidget(self.labelList	, 1, 2)

		self.grid.setColumnStretch(0, 5)
		self.grid.setColumnStretch(1, 20)
		self.grid.setColumnStretch(2, 5)

		self.win.setGeometry(200, 100, 1000, 600)
		self.win.setWindowTitle("AIris")
		
	def run(self):
		self.win.show()
		sys.exit(self.app.exec_())
