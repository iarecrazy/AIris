import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Application:
	
	def __init__(self):
		self.app = QApplication(sys.argv)
		self.createMainWindow()
		self.app.setWindowIcon(QIcon("img/icon.png"))


	def createMainWindow(self):
		self.win	= QWidget()

		grid 		= QGridLayout(self.win)

		label	= QLabel("2")

		color = QColor(255, 0, 0)
		label.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

		label2	= QLabel("2")
		color = QColor(0, 255, 0)
		label2.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

		label3	= QLabel("3")
		color = QColor(0,0,255)
		label3.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

		label4	= QLabel("4")
		color = QColor(255,255,255)
		label4.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

		# grid.addWidget(widget, row, column, rowSpan, colSpan)
		grid.addWidget(label 	, 0, 0)
		grid.addWidget(label2	, 0, 1, 1, 3)
		grid.addWidget(label3	, 1, 0, 1, 2)
		grid.addWidget(label4	, 1, 2, 1, 2)

		self.win.setGeometry(200, 100, 1000, 600)
		self.win.setWindowTitle("AIris")
		
	def run(self):
		self.win.show()
		sys.exit(self.app.exec_())
