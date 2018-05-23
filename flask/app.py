from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Hospitals')
def list_hospitals():
	return render_template("hospitals.html")

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=6666, debug=True)