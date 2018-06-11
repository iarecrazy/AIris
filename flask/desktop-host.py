import os

from flask import Flask

from app import *

app.config['root_dir'] = 'X:\\'
app.config['tmp_dir'] = 'C:\\Temp'
app.config['path_to_index'] = os.path.join(app.config['tmp_dir'], 'index.json')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
