import email
import os
import string
import random

from flask import Flask, request, render_template, redirect,redirect, url_for, send_file, session 
from flask_mail import Mail, Message
from mysql.connector import connect
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='btech19eskcs107@skit.ac.in',
    MAIL_PASSWORD='xcztoaoxkfftuytx'
)
app.secret_key='ghjhjhq/213763fbf'
mail = Mail(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/signup')
def hello_world1():
    return render_template('signup.html')

@app.route('/signup1',methods=['POST'])
def signup1():
    email=request.form.get('email')
    psw=request.form.get('psw')
    connection = connect(host="localhost", database="test1", user="root", password="kalash72", port='3306')
    cur = connection.cursor()
    query1="select * from user where email='{}'".format(email)
    cur.execute(query1)
    data=cur.fetchone()
    if(data==None):
        query2="insert into user(email,password) values('{}','{}')".format(email,psw)
        cur.execute(query2)
        connection.commit()
    else:
        return "This account is already exist"
    return render_template('index.html')

@app.route('/signin01')
def signin01():
    return render_template('signin.html')

@app.route('/signin0')
def hello1():
    return render_template('course_offerings.html')

@app.route('/signin0', methods=['POST'])
def signin0():
    email = request.form.get('email')
    psw = request.form.get('psw')
    connection = connect(host="localhost", database="test1", user="root", password="kalash72", port='3306')
    cur = connection.cursor()
    query1 = "select * from user where email='{}'".format(email)
    cur.execute(query1)
    data = cur.fetchone()
    print(data)
    if data ==None:
        return "You are not registered"
    else:
        if psw == data[1]:
            session['email'] = email
            session['userid'] = data[0]
            return render_template('course_offerings.html', email=email)
        else:
            return "Please Enter correct password"

@app.route('/UserHome')
def userhome():
    return render_template('userHome.html')

@app.route('/askemail')
def askemail():
    return render_template('askemail.html')

@app.route('/logout')
def logout():
    session['email'] = None
    session['userid'] = None
    return render_template('signin.html')


@app.route('/forgetpassword')
def forgetpassword():
    email = request.args.get('email')
    randomnumber = ''
    letter = string.digits
    for i in range(6):
        randomnumber = randomnumber + ''.join(random.choice(letter))
    body = 'Your forget password OTP is ' + randomnumber
    msg = Message(subject='Forget Password Email ', sender='btech19eskcs107@skit.ac.in',recipients=[email], body=body)
    msg.cc = [email]
    mail.send(msg)
    connection = connect(host="localhost", database="test1", user="root", password="kalash72",port='3306')
    cur = connection.cursor()
    query2 = "select * from user where email='{}'".format(email)
    cur.execute(query2)
    data = cur.fetchone()
    if data == None:
        return "You are not registered"
    query1 = "update user set otp ='{}' where email= '{}'".format(randomnumber, email)
    cur.execute(query1)
    connection.commit()
    return render_template('updatepassword.html', email=email)

@app.route('/updatepassword')
def updatepassword():
    email = request.args.get('email')
    otp = request.args.get('otp')
    pwd = request.args.get('pwd')
    connection = connect(host="localhost", database="test1", user="root", password="kalash72", port='3306')
    cur = connection.cursor()
    query1 = "select * from user where email='{}'".format(email)
    cur.execute(query1)
    data = cur.fetchone()
    if int(data[2])==int(otp):
        query2 = "update user set password ='{}' where email= '{}'".format(pwd,email)
        cur.execute(query2)
        connection.commit()
        # return "Your password has been successfully changed"
        return render_template('signin.html')
    else:
        return "Worng OTP"

@app.route('/enroll',methods=['post'])
def enroll():
    courseid=request.form.get('courseID')
    title = request.form.get('title')
    credit = request.form.get('credit')
    email = session['email']
    connection = connect(host="localhost", database="test1", user="root", password="kalash72", port='3306')
    cur = connection.cursor()
    query1="select * from courses where courseid={} and email='{}'".format(courseid,email)
    cur.execute(query1)
    data = cur.fetchone()
    if data==None:
        if 'email' in session:
            email = session['email']
            query = "insert into courses(email,courseid,title,credit) values('{}','{}','{}','{}')".format(email,courseid,title,credit)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            return redirect('/courses')
        else:
            return redirect('/signin0')
    else:
        # return "You are already Enrolled in this course"
        return render_template('enroll.html')

@app.route('/courses')
def myCourses():
    if 'userid' in session:
        email=session['email']
        connection = connect(host="localhost", database="test1", user="root", password="kalash72",port='3306')
        cur = connection.cursor()
        query1 = "select * from courses where email='{}'".format(email)
        cur.execute(query1)
        data=cur.fetchall()
        return render_template('userHome.html',data=data)



@app.route('/UnEnroll')
def deleteUrl():
    if 'email' in session:
        courseid = request.args.get('courseid')
        print(email)
        print('courseid')
        connection = connect(host="localhost", database="test1", user="root", password="kalash72",port='3306')
        cur = connection.cursor()
        query1 = "delete from courses where courseid={} and email='{}'".format(courseid,email)
        cur.execute(query1)
        connection.commit()
        return redirect('/courses')

if __name__ == '__main__':
    app.run()