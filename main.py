import sys

# modify the search path so we can import files from multiple directories
sys.path.insert(0, './views')
sys.path.insert(0, './models')

from patientview import *
from patientrepository import *

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

if __name__ == '__main__':
	# create the main application widget
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("img/logo.png"))
	
	# create the main window & give it a default size, position & title
	mainWin = QMainWindow()
	mainWin.setGeometry(200, 100, 1000, 600)
	mainWin.setWindowTitle("AIris")

	# create the main toolbar
	toolBar 			= QToolBar(mainWin)
	toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
	mainWin.addToolBar(toolBar)

	# create the main content widget & use BoxLayout to make
	# sure its content stretch to max size
	layout 		  = QHBoxLayout()
	centralWidget = QWidget (mainWin)
	centralWidget.setLayout(layout)
	mainWin.setCentralWidget(centralWidget)

	# create fake patientRepository
	patientRepository = PatientRepositoryStub()

	# create view on patientRepository & show its contents
	patientRepoView = RepoView(centralWidget, layout, toolBar, patientRepository)
	patientRepoView.create()
	patientRepoView.show()

	# show the main window & run the app
	mainWin.show()
	sys.exit(app.exec_())	
