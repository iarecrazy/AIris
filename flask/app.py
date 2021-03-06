import sys
import os
import collections

from metadatautil import *
from fileutils import *

from flask import Flask, url_for, render_template, abort, send_from_directory, redirect

app = Flask(__name__)

@app.route('/')
def index():
	index = loadOrCreateIndex(app.config['root_dir'], app.config['path_to_index'])
	cnt = collections.Counter()

	for hospital in index['Hospitals']:
		for action in hospital['GrabberActions']:
			rooms = hospital['GrabberActions'][action]['Rooms']
			for room in rooms:
				for key, case in rooms[room].items():

					if 'Tags' in case['Description']:
						for tag in case['Description']['Tags']:
							cnt[tag] += 1

	poptags = cnt.most_common(10)

	return render_template("hospitals.html", index=index, populartags = poptags)

@app.route('/GenerateIndex')
def generate_index():
	index = storeIndex(app.config['root_dir'], app.config['path_to_index'])

	return redirect('/')

@app.route('/Hospital/<hospitalname>')
def show_hospital(hospitalname):
	index = loadOrCreateIndex(app.config['root_dir'], app.config['path_to_index'])
	
	cnt = collections.Counter()

	for hospital in index['Hospitals']:
		if hospital['Name'] == hospitalname:

			for action in hospital['GrabberActions']:
				rooms = hospital['GrabberActions'][action]['Rooms']
				for room in rooms:
					for key, case in rooms[room].items():

						if 'Tags' in case['Description']:
							for tag in case['Description']['Tags']:
								cnt[tag] += 1

			poptags = cnt.most_common(10)

			return render_template("hospital.html", hospital=hospital, populartags = poptags)

	return abort(404)

@app.route('/Filter/Hospital/<hospitalname>/ProcedureType/<proceduretype>/Tags/<tags>')
def show_procedure_type_cases(hospitalname, proceduretype, tags):
	index = loadOrCreateIndex(app.config['root_dir'], app.config['path_to_index'])

	hospitals = []

	if hospitalname == 'All':
		hospitals = index['Hospitals']
	else:
		for hospital in index['Hospitals']:
			if hospital['Name'] == hospitalname:
				hospitals = [ hospital ]
				break 

	cases = filter_on_procedure(hospitals, proceduretype, tags)

	return render_template("caseview.html", hospitalname=hospitalname, proceduretype=proceduretype, tags=tags, cases=cases)

@app.route('/Contract/<hospitalname>/<grabberaction>/<contract>', methods=['GET', 'POST'])
def downloadContract(hospitalname, grabberaction, contract):
    hospitaldir 	= os.path.join(app.config['root_dir'], hospitalname)
    grabberdir 		= os.path.join(hospitaldir, grabberaction)
    contractfile 	= os.path.join(grabberdir, contract)
    return send_from_directory(grabberdir, contract, as_attachment=True)
