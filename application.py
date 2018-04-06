import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ImageView(QGraphicsView):
	def resizeEvent(self, resizeEvent):
		super().resizeEvent(resizeEvent)
		self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
		# self.fixBackgroundPos()

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

		imagePixItem = QGraphicsPixmapItem(QPixmap("img/angio.jpg")) 

		width 	= imagePixItem.pixmap().width()
		height 	= imagePixItem.pixmap().height()

		scene = QGraphicsScene()
		scene.addItem(imagePixItem)

		# create canvas for showing image in
		self.imageView = ImageView(scene)
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
