import os
from fileutils import *

def loadOrCreateIndex(path_to_root, path_to_index):
	index = None

	if os.path.exists(path_to_index):
		index = json_safe_read(path_to_index)
	else:
		index = storeIndex(path_to_root, path_to_index)

	return index

def storeIndex(path_to_root, path_to_index):
	index = createNASIndex(path_to_root)

	json_safe_dump(path_to_index, index)

	return index

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def createNASIndex(hospitalRoot):
	index = {}
	index['GlobalStats'] = {}
	index['GlobalStats']['NrOfCases'] = 0
	index['GlobalStats']['NrOfAnnotatedCases'] = 0
	index['GlobalStats']['NrOfRuns'] = 0
	index['GlobalStats']['NrOfFXDRuns'] = 0
	index['GlobalStats']['NrOfDICOMRuns'] = 0
	index['GlobalStats']['NrOfAnnotatedRuns'] = 0
	index['GlobalStats']['ProcedureTypes'] = {}
	index['Hospitals'] = []
	
	globalStats = index['GlobalStats']

	rootIndex = len(splitall(hospitalRoot)) - 1
	hospitalIndex = rootIndex + 1
	grabberIndex = hospitalIndex + 1
	roomIndex = grabberIndex + 1
	caseIndex = roomIndex + 1
	annotationIndex = caseIndex + 1
	
	currentHospital = None
	
	for dirName, subdirList, files in os.walk(hospitalRoot):
		
		# split the dirName in its subfolder
		directories = splitall(dirName)
	  
		# skip all @eaDirs
		if '@eaDir' in directories:
			continue
		
		directoryIndex = len(directories) 
		

		# hospital dir
		if directoryIndex == hospitalIndex + 1:
			hospital = {}
			index['Hospitals'].append(hospital)
			
			# get the hospital name
			hospital['Name'] = directories[hospitalIndex]
			hospital['NrOfCases'] = 0
			hospital['NrOfAnnotatedCases'] = 0
			hospital['NrOfRuns'] = 0
			hospital['NrOfAnnotatedRuns'] = 0
			hospital['NrOfFXDRuns'] = 0
			hospital['NrOfDICOMRuns'] = 0
			hospital['GrabberActions'] = {}
			hospital['ProcedureTypes'] = {}
			currentHospital = hospital

		elif directoryIndex == grabberIndex + 1:
			currentHospital['GrabberActions'][directories[grabberIndex]] = {}
			currentHospital['GrabberActions'][directories[grabberIndex]]['Contracts'] = files

		elif directoryIndex == roomIndex + 1:
			currentHospital['GrabberActions'][directories[grabberIndex]]['Rooms'] = {}
			currentHospital['GrabberActions'][directories[grabberIndex]]['Rooms'][directories[roomIndex]] = {}
		
		elif directoryIndex == caseIndex + 1:
			currentHospital['GrabberActions'][directories[grabberIndex]]['Rooms'][directories[roomIndex]][directories[caseIndex]] = {}
			currentHospital['GrabberActions'][directories[grabberIndex]]['Rooms'][directories[roomIndex]][directories[caseIndex]]['Description'] = {}
			
			caseFile = os.path.join(dirName, 'case.json')
			
			# if there is a case file
			if os.path.exists(caseFile):
				# add locking
				caseDescription = json_safe_read(caseFile) 
				currentHospital['GrabberActions'][directories[grabberIndex]]['Rooms'][directories[roomIndex]][directories[caseIndex]]['Description'] = caseDescription 
			
				examType = caseDescription['Exam']['Type']
				if examType in currentHospital['ProcedureTypes'].keys():
					currentHospital['ProcedureTypes'][examType] += 1
					globalStats['ProcedureTypes'][examType] += 1
				else:
					currentHospital['ProcedureTypes'][examType] = 1

					if examType not in globalStats['ProcedureTypes'].keys():
						globalStats['ProcedureTypes'][examType] = 1
					else:
						globalStats['ProcedureTypes'][examType] += 1

				# count cases
				currentHospital['NrOfCases'] += 1
				globalStats['NrOfCases'] += 1
		
				for file in files:
					if file.endswith('.fxd'):
						hospital['NrOfFXDRuns'] += 1
						globalStats['NrOfFXDRuns'] += 1
						hospital['NrOfRuns'] += 1
						globalStats['NrOfRuns'] += 1
					elif file.startswith('IM_'):
						hospital['NrOfDICOMRuns'] += 1
						globalStats['NrOfDICOMRuns'] += 1
						hospital['NrOfRuns'] += 1
						globalStats['NrOfRuns'] += 1
			
		elif directoryIndex == annotationIndex + 1:
			if dirName.endswith('Annotation DL'):
				currentHospital['NrOfAnnotatedCases'] += 1
				globalStats['NrOfAnnotatedCases'] += 1
				
				fileDict = {}

				for file in files:
					filename, ext = os.path.splitext(file)

					if filename in fileDict.keys():
						continue
					else:
						fileDict[filename] = True
					
					if ext == '.ann':
						currentHospital['NrOfAnnotatedRuns'] += 1
						globalStats['NrOfAnnotatedRuns'] += 1
					elif ext == '.json':
						currentHospital['NrOfAnnotatedRuns'] += 1
						globalStats['NrOfAnnotatedRuns'] += 1
		

	return index

# Python program to illustrate the intersection
# of two lists using set() method
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def filter_on_procedure(hospitals, proceduretype, tags):

	cases = []

	for hospital in hospitals:
		for action in hospital['GrabberActions']:
			rooms = hospital['GrabberActions'][action]['Rooms']
			for room in rooms:
				for key, case in rooms[room].items():

					if 'Exam' in case['Description'] and (case['Description']['Exam']['Type'] == proceduretype or proceduretype == 'All'):
						casetags = list(case['Description']['Tags'])
						casetags.append('All')

						tagsintersection = intersection(casetags, tags.split(','))
						print(tagsintersection)

						if len(tagsintersection) > 0:
							cases.append(
								{ 
									"Url": "/Hospital/" + hospital['Name'] + "/Action/" + str(action) + "/Room/" + room + "/Case/" + key,
									"Case" : key,
									"Description" : case['Description']
								})

	return cases