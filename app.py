import sqlite3
import uuid
from flask import Flask, flash, redirect, render_template, request, session, abort
from alarm import alarm_clock
import datetime
import random
import os

app = Flask(__name__)

conn = sqlite3.connect('clock.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS user (_id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, hour TEXT, minute TEXT, dn TEXT)')

conn.close()

@app.route("/")
def landing():
	return render_template('landing.html')

@app.route("/alarm")
def alarm():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		try:
			with sqlite3.connect("clock.db") as con:
				cur = con.cursor()
				cur.execute("SELECT hour, minute, dn FROM user WHERE username = '{}'".format(session['user']))
				alarm = cur.fetchall()
				print(alarm)

		except:
			con.rollback()

		finally:
			con.close()
			if alarm[0][0] != None and alarm[0][0] != "None":
				hour = int(alarm[0][0])
				minute = int(alarm[0][1])
				dn = int(alarm[0][2])

				if (dn == 1 and hour < 12):
					hour += 12
				elif (hour == 12 and dn == 0):
					hour -= 12
				time = datetime.time(hour, minute).strftime("%I:%M %p")
				con.close()
				t_sec = alarm_clock(hour, minute, dn)
				return render_template("alert.html", time = time, t_sec = t_sec)
			return render_template('alarm.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
	if request.method == 'POST':
		try:
			password = request.form['password']
			username = request.form['username']
			hidden = uuid.uuid4()
			with sqlite3.connect("clock.db") as con:
				cur = con.cursor()
				cur.execute("SELECT username, password FROM user WHERE username = '{}'".format(username))
				rv = cur.fetchall()
				print(rv)
				hidden = rv[0][1]
				us = rv[0][0]

		except:
			con.rollback()

		finally:
			con.close()
			if (password == 'password' and username == 'admin') or (password == hidden and username == us):
				session['logged_in'] = True
				session['user'] = username
			else:
				msg = "Incorrect Password"
				return render_template("result.html",msg = msg)
			return alarm()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return alarm()

@app.route("/new_user")
def new_user():
	return render_template('new_user.html')

@app.route('/delete',methods = ['DELETE', 'POST'])
def delete():
	if request.method == 'POST':
		try:
			with sqlite3.connect("clock.db") as con:
				cur = con.cursor()
				cur.execute("UPDATE user SET hour = '{}', minute = '{}', dn = '{}' WHERE username = '{}'".format(None, None, None, session['user']) )

				con.commit()
		except:
			con.rollback()

		finally:
			return render_template("alarm.html")
			con.close()

@app.route('/create',methods = ['POST', 'GET'])
def create():
	if request.method == 'POST':
		try:
			user = request.form['username']
			password = request.form['password']
			password_v = request.form['password_v']

			if password != password_v:
				msg = "Passwords did not match"
				return render_template("result.html",msg = msg)

			if password == "" or user == "":
				msg = "All fields required"
				return render_template("result.html",msg = msg)

			with sqlite3.connect("clock.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO user (username, password) VALUES (?,?)", (user,password) )

				con.commit()
				msg = "User Successfully Created. You are now logged in."
				session['logged_in'] = True
				session['user'] = user

		except:
			con.rollback()
			msg = "Username or Password Invalid"

		finally:
			return render_template("result.html",msg = msg)
			con.close()

@app.route("/set", methods = ['POST'])
def set():
	try:
		with sqlite3.connect("clock.db") as con:
			cur = con.cursor()
			cur.execute("SELECT hour, minute, dn FROM user WHERE username = '{}'".format(session['user']))
			alarm = cur.fetchall()
			print(alarm)

			if request.method == 'POST':
				hour = int(request.form['hour'])
				minute = int(request.form['minute'])
				dn = int(request.form['inlineRadioOptions'])
				cur.execute("UPDATE user SET hour = '{}', minute = '{}', dn = '{}' WHERE username = '{}'".format(hour, minute, dn, session['user']) )
				con.commit()

	except:
		con.rollback()

	finally:
		if (dn == 1 and hour < 12):
			hour += 12
		elif (hour == 12 and dn == 0):
			hour -= 12
		time = datetime.time(hour, minute).strftime("%I:%M %p")
		con.close()
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
	app.secret_key = os.urandom(12)
	app.run()
