from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# the patient view shows all patients in a selected repository
class RepoView:
	class PatientEditView:
		def __init__(self, parent, repo, table):
			gridLayout = QGridLayout()
			self.table = table
			self.idLabel = QLabel("-")
			self.currentPatient = None
			self.currentRow = 0
			self.currentColumn = 0

			gridLayout.addWidget(QLabel("Patient Id:"), 0, 0, 1, 1, Qt.AlignRight)
			gridLayout.addWidget(self.idLabel, 0, 1)

			self.procCombo = QComboBox()
			self.procCombo.addItems(repo.getPossibleProcedures())
			self.procCombo.setEnabled(False)
			self.procCombo.currentTextChanged.connect(self.procTextChanged)

			gridLayout.addWidget(QLabel("Procedure:"), 1, 0, 1, 1, Qt.AlignRight)
			gridLayout.addWidget(self.procCombo, 1, 1)

			self.runsLabel = QLabel("-")
			gridLayout.addWidget(QLabel("Number of Runs:"), 2, 0, 1, 1, Qt.AlignRight)
			gridLayout.addWidget(self.runsLabel, 2, 1)

			self.annotationLabel = QLabel("-")
			gridLayout.addWidget(QLabel("Contains Annotations:"), 3, 0, 1, 1, Qt.AlignRight)
			gridLayout.addWidget(self.annotationLabel, 3, 1)

			gridLayout.setColumnStretch	(1, 1)
			gridLayout.setRowStretch	(4, 1)

			parent.addLayout(gridLayout)

		def setPatient(self, patient, row, column):
			self.currentPatient = patient

			print(str(row) + " " + str(column))
			self.currentRow		= row
			self.currentColumn	= column

			self.procCombo.currentTextChanged.disconnect(self.procTextChanged)

			if(patient is None):
				self.idLabel 		.setText 		("-")
				self.procCombo		.setCurrentText	("None")
				self.runsLabel 		.setText 		("-")
				self.annotationLabel.setText 		("-")
				self.procCombo.setEnabled(False)
			else:
				self.idLabel 		.setText 		(str(patient.patientId))
				self.procCombo		.setCurrentText	(patient.procedure)
				self.runsLabel 		.setText 		(str(patient.numberOfRuns))
				self.annotationLabel.setText 		(str(patient.containsAnnotations))
				self.procCombo.setEnabled(True)		

			self.procCombo.currentTextChanged.connect(self.procTextChanged)

		def procTextChanged(self, text):
			if(self.currentPatient is not None):
				self.currentPatient.procedure = text
				item = self.table.item(self.currentRow, self.currentColumn).setText(text)
			
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

		rightPanel = QVBoxLayout()
		patientLayout = QHBoxLayout()
		patientLayout.addWidget(patientTable)
		patientLayout.setStretch(0, 1)
		patientLayout.addLayout(rightPanel)

		self.patientEditView = RepoView.PatientEditView(rightPanel, self.repo, self.patientTable)

		rightPanel.addWidget(QLabel("test"))
		
		boxLayout.addLayout(patientLayout)
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
				self.patientEditView.setPatient(None, 0, 0)
			else:
				# get patient associated with row
				self.myList.clear()
		
				patient = self.patientTable.item(row, 0).data(Qt.UserRole)
				self.patientEditView.setPatient(patient, row, 1)
	
				thumbs = patient.getRunThumbs()

				for i in range(0, len(thumbs)):
					self.myList.addItem(QListWidgetItem(thumbs[i].icon, thumbs[i].name))
			
	def remove(self):
		pass
