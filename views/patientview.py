from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# the patient view shows all patients in a selected repository
class PatientView:
	def __init__(self, myWidget, myToolBar, patientRepository):
		self.repo 		= patientRepository
		self.myToolBar 	= myToolBar
		self.myWidget 	= myWidget

	def show(self):	
		l = QListWidget(self.myWidget)

		l.setViewMode 	(QListWidget.IconMode)
		l.setIconSize 	(QSize(100, 100))
		l.setFlow 		(QListView.LeftToRight)
		l.setMovement 	(QListView.Static)
		l.setWrapping 	(False)
		l.setResizeMode (QListWidget.Adjust)

		l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Run 1"));
		l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Run 2"));
		l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Run 3"));
		l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Run 4"));
		l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Run 5"));
		l.addItem(QListWidgetItem(QIcon("img/angio.jpg"),"Run 6"));

		# force height to be exactly 130
		l.setFixedHeight(130)

		# layout the main panel
		boxLayout = QVBoxLayout(self.myWidget)
		boxLayout.addWidget(QLabel(self.repo.name + ": " + self.repo.type))

		# create patient table
		patients = self.repo.getPatientList()
		patientTable = QTableWidget(len(patients), 4)
		patientTable.setHorizontalHeaderLabels(["Patient ID", "Procedure", "# of runs", "Annotations"])

		for i in range(0, len(patients)):
			patientTable.setItem(i, 0, QTableWidgetItem(str(patients[i].patientId)))
			patientTable.setItem(i, 1, QTableWidgetItem(str(patients[i].procedure)))
			patientTable.setItem(i, 2, QTableWidgetItem(str(patients[i].numberOfRuns)))
			patientTable.setItem(i, 3, QTableWidgetItem(str(patients[i].containsAnnotations)))

		self.patientTable = patientTable
		selectionModel = self.patientTable.selectionModel()
		selectionModel.selectionChanged.connect(self.selectionChanged)

		boxLayout.addWidget(patientTable)
		boxLayout.addWidget(QLabel("Patient Runs"))
		boxLayout.addWidget(l)
		
		self.myToolBar.addAction("Patient")

	def hide(self):
		pass

	def selectionChanged(self, selected, deselected):
		modelIndexList = selected.indexes()

		if(len(modelIndexList) > 0):
			col = modelIndexList[0].column()
			columnSelected = self.patientTable.selectionModel().isColumnSelected(col, modelIndexList[0].parent())
	
			if(columnSelected):
				self.patientTable.sortItems(col)

	def remove(self):
		pass
