import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ImageView(QGraphicsView):
	def __init__(self):
		super().__init__(QGraphicsScene())
		# define the default boundingbox pen
		self.pen 				= QPen(QColor(255,0,0,128), 5)
		self.brush 				= QBrush(QColor(255,0,0,50))
		self.hoverPen 			= QPen(QColor(255,0,0,228), 10)
		self.hoverBrush			= QBrush(QColor(255,0,0,100))
		
		self.currentRect 		= None
		self.startingPoint  	= None
		self.imagePixItem		= None
		self.hoveringOverRect 	= None

	def loadImage(self, filename):
		self.imagePixItem = QGraphicsPixmapItem(QPixmap("img/angio.jpg"))
		self.scene().addItem(self.imagePixItem)

	def resizeEvent(self, resizeEvent):
		super().resizeEvent(resizeEvent)
		self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
		# self.fixBackgroundPos()

	def mousePressEvent(self, event):
		# start of drawing boundingbox
		if(Qt.LeftButton == event.button()):
			point = self.mapToScene(QPoint(event.x(), event.y()))

			super().mousePressEvent(event)
			# transform pixel view coordinates to scene coordinates
			self.startingPoint = self.mapToScene(QPoint(event.x(), event.y()))
			self.currentRect = self.scene().addRect(QRectF(point.x(), point.y(), 5, 5), self.pen, self.brush)
			self.currentRect.setAcceptHoverEvents(True)

	def mouseMoveEvent(self, event):
		super().mouseMoveEvent(event)
		
		# transform event x,y to scene coordinates
		point = self.mapToScene(QPoint(event.x(), event.y()))
		
		# are we drawing a boundingbox?
		if(self.currentRect != None):
		
			# make sure we're still in the image
			if(self.imagePixItem.contains(point)):

				x = min(point.x(), self.startingPoint.x())
				y = min(point.y(), self.startingPoint.y())

				rect = self.currentRect.setRect(x, y, abs(point.x() - self.startingPoint.x()), abs(point.y() - self.startingPoint.y()))
		else:
			# always reset rect
			self.resetHover()

			# we're not drawing a bounding box, let's check if we hover
			item = self.itemAt(QPoint(event.x(), event.y()))

			if(type(item) == QGraphicsRectItem):

				self.hoveringOverRect = item
				self.hoveringOverRect.setPen(self.hoverPen)
				self.hoveringOverRect.setBrush(self.hoverBrush)

	def resetHover(self):
		if(self.hoveringOverRect != None):
			self.hoveringOverRect.setPen(self.pen)
			self.hoveringOverRect.setBrush(self.brush)
			self.hoveringOverRect = None

	def mouseReleaseEvent(self, event):
		if(Qt.LeftButton == event.button()):
			self.currentRect = None

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

		# width 	= imagePixItem.pixmap().width()
		# height 	= imagePixItem.pixmap().height()

		# scene = QGraphicsScene()
		# scene.addItem(imagePixItem)

		# scene.addRect(QRectF(0, 0, 100, 100), QPen(Qt.red, 5))

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
