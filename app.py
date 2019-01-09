import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, abort
from alarm import alarm_clock

app = Flask(__name__)

@app.route("/")
def landing():
	return render_template('landing.html')

@app.route("/alarm")
def alarm():
	return render_template('alarm.html')

@app.route("/set", methods = ['POST', 'GET'])
def set():
	if request.method == 'POST':
		try:
			print(request)
			hour = int(request.form['hour'])
			minute = int(request.form['minute'])
			dn = int(request.form['inlineRadioOptions'])

		finally:
			if alarm_clock(hour, minute, dn) == True:
				return render_template("alert.html")

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/contact")
def contact():
	return render_template('contact.html')

if __name__ == "__main__":
    app.run()
