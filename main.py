import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def window():
	# qsrand(QTime.currentTime().msec())
	app 		= QApplication(sys.argv)
	win 		= QWidget()
	grid 		= QGridLayout(win)
	fileList	= QLabel("1")

	color = QColor(255, 0, 0)
	fileList.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

	fileList2	= QLabel("2")
	color = QColor(0, 255, 0)
	fileList2.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

	fileList3	= QLabel("3")
	color = QColor(0,0,255)
	fileList3.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

	fileList4	= QLabel("4")
	color = QColor(255,255,255)
	fileList4.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

	button 		= QPushButton("button")

	# grid.addWidget(widget, row, column, rowSpan, colSpan)
	grid.addWidget(fileList 	, 0, 0)
	grid.addWidget(fileList2	, 0, 1, 1, 3)
	grid.addWidget(fileList3	, 1, 0, 1, 2)
	grid.addWidget(fileList4	, 1, 2, 1, 2)


	win.setGeometry(200, 100, 1000, 600)
	win.setWindowTitle("PyQt")
	win.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	window()
