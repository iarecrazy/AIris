import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class RunThumb:
	def __init__(self, name, icon):
		self.name = name
		self.icon = icon

class Patient:
	def __init__(self, patientId, procedure, nrOfRuns, containsAnnotations):
		self.patientId 				= patientId
		self.procedure				= procedure
		self.numberOfRuns			= nrOfRuns
		self.containsAnnotations	= containsAnnotations

	def getRunThumbs(self):
		availableNames	= [ "angiography", "cardiac", "hand", "neuro" ]
		availableImages = [ QIcon("./img/angio.jpg"), QIcon("./img/angio1.jpg"), QIcon("./img/angio2.jpg"), QIcon("./img/angio3.jpg")]
		thumbs = []

		for i in range(0, self.numberOfRuns):
			number = int(random.random() * len(availableImages))
			thumbs.append(RunThumb(availableNames[number], availableImages[number]))

		return thumbs

class PatientRepository:
	def __init__(self):
		self.name 				= "Repository Base Class"
		self.type 				= "None"
		self.possibleProcedures = []

	def getPatientList(self):
		return None

	def getPossibleProcedures(self):
		return self.possibleProcedures

class PatientRepositoryStub(PatientRepository):
	def __init__(self):
		super().__init__()

		self.name 				= "Stub Repo Name"
		self.type 				= "Stub Repo Type"
		self.possibleProcedures = ["Unknown", "PCI", "TAVI",  "Aneurysm", "PAD", "Stroke", "Other"]

	def getPossibleProcedures(self):
		return self.possibleProcedures

	def generateRandomPatient(self):
		procedures = ["PCI", "TAVI", "Unknown", "Aneurysm", "PAD", "Stroke"]

		return Patient(int(random.random() * 100000), procedures[int(random.random() * len(procedures))], int(random.random() * 1000), random.random() < 0.5)

	def getPatientList(self):
		patients = []

		for i in range(0, int(random.random()*100) + 5):
			patients.append(self.generateRandomPatient())

		return patients