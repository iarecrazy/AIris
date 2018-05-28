import sys
import os
from metadatautil import *
from fileutils import *

from flask import Flask, url_for, render_template, abort, send_from_directory

# debug = true

app = Flask(__name__)
app.config['root_dir'] = 'X:/'
app.config['tmp_dir'] = 'C:/Temp'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Hospitals')
def list_hospitals():
	hospitalsFile = os.path.join(app.config['tmp_dir'], 'hospitals.json')
	hospitals = {}

	# after one hour force refresh
	if file_last_modified_longer_than(hospitalsFile, 60*60) is False:
		hospitals = json_safe_read(hospitalsFile)

	if bool(hospitals) is False:
		hospitals = refreshHospitals(app.config['root_dir'], hospitalsFile)

	return render_template("hospitals.html", hospitals=hospitals)

@app.route('/Hospitals/Refresh')
def refresh_cache_hospitals():
	hospitalsFile = os.path.join(app.config['tmp_dir'], 'hospitals.json')
	hospitals = refreshHospitals(app.config['root_dir'], hospitalsFile)

	return render_template("hospitals.html", hospitals=hospitals)

@app.route('/Hospitals/<hospitalname>')
def show_hospital(hospitalname):
	# does directory exist?
	path_to_hospital = os.path.join(app.config['root_dir'], hospitalname)
	if(os.path.exists(path_to_hospital)):

		return render_template("hospital.html", hospital=hospitalname)
	else:
		abort(404)

@app.route('/Hospitals/<hospitalname>/<grabberaction>/<contract>', methods=['GET', 'POST'])
def downloadContract(hospitalname, grabberaction, contract):
    hospitaldir 	= os.path.join(app.config['root_dir'], hospitalname)
    grabberdir 		= os.path.join(hospitaldir, grabberaction)
    contractfile 	= os.path.join(grabberdir, contract)
    return send_from_directory(grabberdir, contract, as_attachment=True)

@app.route('/Hospitals/<hospitalname>/Refresh')
def refresh_cache_hospital(hospitalname):
	return show_hospital(hospitalname)

if __name__ == '__main__':
	app.run()