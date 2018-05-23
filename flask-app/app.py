#!flask/bin/python
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/overview')
def overview():
	return render_template("overview.html")

if __name__ == '__main__':
	app.run(debug=True)
