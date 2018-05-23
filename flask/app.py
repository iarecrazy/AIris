from flask import Flask, url_for, render_template, abort
from util import *
import os

app = Flask(__name__)
app.config['root_dir'] = 'X:/'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Hospitals')
def list_hospitals():
	allDirs = []
	for root, dirs, files in walklevel(app.config['root_dir'], 0):
		for d in dirs:
			allDirs.append(d)

	print(allDirs)
	return render_template("hospitals.html", hospitals=allDirs)

@app.route('/Hospitals/<hospitalname>')
def show_hospital(hospitalname):
	# does directory exist?
	path_to_hospital = os.path.join(app.config['root_dir'], hospitalname)
	if(os.path.exists(path_to_hospital)):
		return render_template('hospital.html', hospital=hospitalname)
	else:
		abort(404)

if __name__ == '__main__':
	app.run()