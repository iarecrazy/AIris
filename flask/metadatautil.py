import os
from fileutils import *

def getHospitalInfo(hospitalDir):
	info = {}
	info['GrabberActions'] = {}
	info['NrOfCases'] = 0
	info['NrOfAnnotatedCases'] = 0

	for rootHospital, dirs, files in walklevel(hospitalDir, 0):
		for d in dirs:
			info['GrabberActions'][d] = {}
			grabberPath = os.path.join(hospitalDir, d)

			for rootGrabber, rooms, contracts in walklevel(grabberPath, 0):
				info['GrabberActions'][d]['Contracts'] = contracts

				for room in rooms:
					info['GrabberActions'][d][room] = []
					roomPath = os.path.join(grabberPath, room)

					for rootRoom, cases, f in walklevel(roomPath, 0):
						info['GrabberActions'][d][room] = cases
						info['NrOfCases'] = info['NrOfCases'] + len(cases)

						for case in cases:
							caseDirectory = os.path.join(roomPath, case)
							if os.path.exists(os.path.join(caseDirectory, 'Annotation DL')):
								info['NrOfAnnotatedCases'] = info['NrOfAnnotatedCases'] + 1


	return info

def refreshHospitals(hospitalDir, hospitalsFile):
	hospitals = {}

	for root, dirs, files in walklevel(hospitalDir, 0):

		for d in dirs:
			hospitals[d] = getHospitalInfo(os.path.join(hospitalDir, d))

			json_safe_dump(hospitalsFile, hospitals)

	return hospitals