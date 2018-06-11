import os

from flask import Flask

from app import *

app.config['root_dir'] = '/mnt/Clean'
app.config['tmp_dir'] = '/tmp'
app.config['path_to_index'] = os.path.join(app.config['tmp_dir'], 'index.json')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
