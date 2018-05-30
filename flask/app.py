import sys
import os
from metadatautil import *
from fileutils import *

from flask import Flask, url_for, render_template, abort, send_from_directory, redirect

# debug = true

app = Flask(__name__)
app.config['root_dir'] = 'X:/'
app.config['tmp_dir'] = 'C:/Temp'
app.config['path_to_index'] = os.path.join(app.config['tmp_dir'], 'index.json')

@app.route('/')
def index():
	index = loadOrCreateIndex(app.config['root_dir'], app.config['path_to_index'])

	return render_template("hospitals.html", index=index)

@app.route('/Hospitals')
def list_hospitals():
	index = loadOrCreateIndex(app.config['root_dir'], app.config['path_to_index'])

	return render_template("hospitals.html", index=index)

@app.route('/GenerateIndex')
def generate_index():
	index = storeIndex(app.config['root_dir'], app.config['path_to_index'])

	return redirect('/')

@app.route('/Hospitals/<hospitalname>')
def show_hospital(hospitalname):
	index = loadOrCreateIndex(app.config['root_dir'], app.config['path_to_index'])

	for hospital in index['Hospitals']:
		if hospital['Name'] == hospitalname:
			return render_template("hospital.html", hospital=hospital)

	return abort(404)

@app.route('/<hospitalname>/<grabberaction>/<contract>', methods=['GET', 'POST'])
def downloadContract(hospitalname, grabberaction, contract):
    hospitaldir 	= os.path.join(app.config['root_dir'], hospitalname)
    grabberdir 		= os.path.join(hospitaldir, grabberaction)
    contractfile 	= os.path.join(grabberdir, contract)
    return send_from_directory(grabberdir, contract, as_attachment=True)

if __name__ == '__main__':
	app.run()