import sys
# from application import Application

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def createCentralWidget(mainWindow):
	# w = QWidget(mainWindow)
	l = QListWidget(mainWindow)
	l.setViewMode(QListWidget.IconMode)
	l.setIconSize(QSize(100, 100))
	l.setFlow(QListView.LeftToRight)
	l.setMovement(QListView.Static)
	l.setWrapping(False)
	l.setResizeMode(QListWidget.Adjust)

	l.addItem(QListWidgetItem(QIcon("img/icon.png"),"Earth"));
	l.addItem(QListWidgetItem(QIcon("img/icon.patient.png"),"Tornado"));
	l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Wallpaper"));
	l.addItem(QListWidgetItem(QIcon("img/icon.png"),"Earth"));
	l.addItem(QListWidgetItem(QIcon("img/icon.patient.png"),"Tornado"));
	l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Wallpaper"));
	mainWin.setCentralWidget(l)
	return l

def createNavigationToolBar(mainWindow):
	# load the patient icon
	t = QToolBar(mainWindow)
	t.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

	# select data
	t.addAction("Patient")

	mainWindow.addToolBar(t)
	return t

if __name__ == '__main__':

	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("img/icon.png"))
	
	# create the main window
	mainWin = QMainWindow()
	mainWin.setGeometry(200, 100, 1000, 600)
	mainWin.setWindowTitle("AIris")

	# content widget
	centralWidget 		= createCentralWidget		(mainWin)
	navigationToolBar	= createNavigationToolBar 	(mainWin)



	mainWin.show()
	sys.exit(app.exec_())	

	# a = Application()
	# a.run()
