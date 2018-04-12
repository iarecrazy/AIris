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
			
	def __init__(self, parentWidget, parentLayout, myToolBar, patientRepository):
		self.repo 				= patientRepository
		self.myToolBar 			= myToolBar
		self.parentWidget 		= parentWidget
		self.parentLayout 		= parentLayout
		self.myWidget 			= QWidget(self.parentWidget)
		self.myList				= None
		self.myToolBarAction 	= None

		# keep it hidden until show is called
		self.myWidget.hide()
		
	def create(self):
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

		# filter out the current procedures
		filterBox = QHBoxLayout()
		filterBox.addWidget(QLabel("Filter on:"))

		procBox = QComboBox()

		procedureList = self.repo.getPossibleProcedures()
		procedureListCombo = procedureList.copy()

		procedureListCombo.append("All")

		procBox.addItems(procedureListCombo)
		procBox.setCurrentText("All")
		procBox.currentTextChanged.connect(self.procedureFilterChanged)

		filterBox.addWidget(procBox)
		filterBox.addStretch(1)

		boxLayout.addLayout(filterBox)

		# create patient table
		patients = self.repo.getPatientList()
		patientTable = QTableWidget(0, 4)
		patientTable.setHorizontalHeaderLabels(["Patient ID", "Procedure", "# of runs", "Annotations"])

		# disable table editting
		patientTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.patientTable = patientTable
		self.populateTable("All", patientTable)

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

	def cleanup(self):
		# TODO: remove all widgets and all signal connect so python 
		# can clean up memory
		pass
		
	def show(self):	
		self.myToolBarAction = self.myToolBar.addAction("Current Repository")
		self.myToolBarAction.setEnabled(False)
		self.parentLayout.addWidget(self.myWidget)
		self.myWidget.show()

	def hide(self):
		self.myToolBar.removeAction(self.myToolBarAction )
		self.myWidget.hide()
		self.parentLayout.removeAt(self.myWidget)

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
				# TODO: handle selecting multiple patients
				# get patient associated with row
				self.myList.clear()
		
				patient = self.patientTable.item(row, 0).data(Qt.UserRole)
				self.patientEditView.setPatient(patient, row, 1)
	
				thumbs = patient.getRunThumbs()

				for i in range(0, len(thumbs)):
					self.myList.addItem(QListWidgetItem(thumbs[i].icon, thumbs[i].name))

	def procedureFilterChanged(self, text):
		print("changed")
		nrOfRows = self.patientTable.rowCount()

		for i in range(nrOfRows, 0):
			self.patientTable.removeRow(i)

		self.patientTable.clear()
		self.patientTable.clearContents()
		self.populateTable(text, self.patientTable)
		pass

	def populateTable(self, procFilter, table):
		# create patient table
		patients = self.repo.getPatientList()

		tablePatientList = []

		if(procFilter != "All"):
			for i in range(0, len(patients)):
				if(procFilter == patients[i].procedure):
					tablePatientList.append(patients[i])
		else:
			tablePatientList = patients

		print(len(tablePatientList))
		print(len(patients))

		table.setRowCount(len(tablePatientList))

		# fill table and associate data
		for i in range(0, len(tablePatientList)):
			# TODO: fix sorting for numbers by creating a special TableWidgetItem
			# implemeting __lt__: https://stackoverflow.com/questions/7848683/how-to-sort-data-in-qtablewidget
			table.setItem(i, 0, QTableWidgetItem(str(tablePatientList[i].patientId)))
			table.item 	(i, 0).setData(Qt.UserRole, tablePatientList[i])

			table.setItem(i, 1, QTableWidgetItem(str(tablePatientList[i].procedure)))
			table.item 	(i, 1).setData(Qt.UserRole, tablePatientList[i])
			
			table.setItem(i, 2, QTableWidgetItem(str(tablePatientList[i].numberOfRuns)))
			table.item 	(i, 2).setData(Qt.UserRole, tablePatientList[i])

			table.setItem(i, 3, QTableWidgetItem(str(tablePatientList[i].containsAnnotations)))
			table.item 	(i, 3).setData(Qt.UserRole, tablePatientList[i])
