import sys

# modify the search path so we can import files from multiple directories
sys.path.insert(0, './views')
sys.path.insert(0, './models')

from patientview import *
from patientrepository import *

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def createCentralWidget(mainWindow):
	w = QWidget(mainWindow)
	mainWin.setCentralWidget(w)
	return w

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
	centralWidget 		= QWidget (mainWin)
	toolBar 			= QToolBar(mainWin)
	toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

	mainWin.addToolBar(toolBar)
	mainWin.setCentralWidget(centralWidget)

	patientRepository = PatientRepositoryStub()
	patientView = PatientView(centralWidget, toolBar, patientRepository)
	patientView.show()

	mainWin.show()
	sys.exit(app.exec_())	
