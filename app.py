import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, abort
from alarm import alarm_clock
import datetime
import random

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

			if (dn == 1 and hour < 12) or (hour == 12 and dn == 0):
				hour += 12
			time = datetime.time(hour, minute).strftime("%I:%M %p")

		finally:
			t_sec = alarm_clock(hour, minute, dn)
			return render_template("alert.html", time = time, t_sec = t_sec)

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/yt")
def yt():
	num = random.randint(0,84)
	return render_template('yt.html', num = num)

@app.route("/contact")
def contact():
	return render_template('contact.html')

if __name__ == "__main__":
    app.run()
