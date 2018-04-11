from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# the patient view shows all patients in a selected repository
class PatientView:
	def __init__(self, myWidget, myToolBar, patientRepository):
		self.repo 		= patientRepository
		self.myToolBar 	= myToolBar
		self.myWidget 	= myWidget
		self.myList		= None

	def show(self):	
		l = QListWidget(self.myWidget)

		l.setViewMode 	(QListWidget.IconMode)
		l.setIconSize 	(QSize(100, 100))
		l.setFlow 		(QListView.LeftToRight)
		l.setMovement 	(QListView.Static)
		l.setWrapping 	(False)
		l.setResizeMode (QListWidget.Adjust)

		self.myList = l

		# force height to be exactly 130
		l.setFixedHeight(140)

		# layout the main panel
		boxLayout = QVBoxLayout(self.myWidget)
		boxLayout.addWidget(QLabel(self.repo.name + ": " + self.repo.type))

		# create patient table
		patients = self.repo.getPatientList()
		patientTable = QTableWidget(len(patients), 4)
		patientTable.setHorizontalHeaderLabels(["Patient ID", "Procedure", "# of runs", "Annotations"])

		# fill table and associate data
		for i in range(0, len(patients)):
			patientTable.setItem(i, 0, QTableWidgetItem(str(patients[i].patientId)))
			patientTable.item 	(i, 0).setData(Qt.UserRole, patients[i])

			patientTable.setItem(i, 1, QTableWidgetItem(str(patients[i].procedure)))
			patientTable.item 	(i, 1).setData(Qt.UserRole, patients[i])
			
			patientTable.setItem(i, 2, QTableWidgetItem(str(patients[i].numberOfRuns)))
			patientTable.item 	(i, 2).setData(Qt.UserRole, patients[i])

			patientTable.setItem(i, 3, QTableWidgetItem(str(patients[i].containsAnnotations)))
			patientTable.item 	(i, 3).setData(Qt.UserRole, patients[i])

		self.patientTable = patientTable
		selectionModel = self.patientTable.selectionModel()
		selectionModel.selectionChanged.connect(self.selectionChanged)

		boxLayout.addWidget(patientTable)
		boxLayout.addWidget(QLabel("Patient Runs"))
		boxLayout.addWidget(l)
		
		self.myToolBar.addAction("Patient")

	def destroy(self):
		pass

	def selectionChanged(self, selected, deselected):
		modelIndexList = selected.indexes()

		if(len(modelIndexList) > 0):
			col = modelIndexList[0].column()
			row = modelIndexList[0].row()
			columnSelected 	= self.patientTable.selectionModel().isColumnSelected	(col, modelIndexList[0].parent())
			rowSelected  	= self.patientTable.selectionModel().isRowSelected 		(row, modelIndexList[0].parent())

			if(columnSelected):
				self.patientTable.sortItems(col)

			if(rowSelected):
				# get patient associated with row
				self.myList.clear()
				patient = self.patientTable.item(row, 0).data(Qt.UserRole)

				thumbs = patient.getRunThumbs()

				for i in range(0, len(thumbs)):
					self.myList.addItem(QListWidgetItem(thumbs[i].icon, thumbs[i].name))

	def remove(self):
		pass
