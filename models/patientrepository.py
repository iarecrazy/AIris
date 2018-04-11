import random

class Patient:
	def __init__(self, patientId, procedure, nrOfRuns, containsAnnotations):
		self.patientId 				= patientId
		self.procedure				= procedure
		self.numberOfRuns			= nrOfRuns
		self.containsAnnotations	= containsAnnotations

class PatientRepository:
	def __init__(self):
		self.name = "Repository Base Class"
		self.type = "None"

	def getPatientList(self):
		return None

class PatientRepositoryStub(PatientRepository):
	def __init__(self):
		super().__init__()

		self.name = "Stub Repo Name"
		self.type = "Stub Repo Type"

	def generateRandomPatient(self):
		procedures = ["PCI", "TAVI", "Unknown", "Aneurysm", "PAD", "Stroke"]

		return Patient(int(random.random() * 100000), procedures[int(random.random() * len(procedures))], int(random.random() * 1000), random.random() < 0.5)

	def getPatientList(self):
		patients = []

		for i in range(0, int(random.random()*100)):
			patients.append(self.generateRandomPatient())

		return patients