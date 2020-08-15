#Name:Aditee Dnyaneshwar Dakhane
#StudentID: 1001745502


import base64
import os
import shutil
import csv
import sys
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
import sqlite3 as sql

port = int(os.getenv('PORT', '3000'))
app = Flask(__name__)
conn = sql.connect('StudentsDB.db')
print("database connected")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, '/')

@app.route("/")
def Home():
    return render_template('homepage.html')


@app.route('/retrievedata')
def retrievedata():
   con = sql.connect("StudentsDB.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from studentinfo")
   rows = cur.fetchall()
   return render_template("retrievedata.html",rows = rows)

@app.route("/searchstudent")
def searchstudent():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search():
   fname = request.form['fname']
   con = sql.connect("StudentsDB.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select Name,Pic from studentinfo where Name=?;",[fname])
   rows = cur.fetchall()
   return render_template("search.html",rows = rows)

@app.route("/viewpictures")
def viewpictures():
    return render_template('displayallpictures.html')


@app.route('/displayallpictures',methods=['POST'])
def displayallpictures():
   sal = request.form['sal']
   con = sql.connect("StudentsDB.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select Salary,Pic from studentinfo where Salary<=?;",[sal])
   rows = cur.fetchall()
   return render_template("displayallpictures.html",rows = rows)

@app.route("/insertimage")
def insertimage():
    return render_template('addpicture.html')


@app.route('/addpicture',methods=['POST'])
def addpicture():
    fname = request.form['fname']
    pic = request.form['pic']
    con = sql.connect("StudentsDB.db")
    cur = con.cursor()
    cur.execute("update studentinfo set Pic=? where Name=?;",[pic, fname])
    con.commit()
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from studentinfo where Name=?;",[fname])
    rows = cur.fetchall()
    return render_template("addpicture.html",rows=rows)

@app.route("/newdata")
def newdata():
    return render_template('changekeyword.html')


@app.route('/changekeyword',methods=['POST'])
def changekeyword():
    fname = request.form['fname']
    keyword = request.form['keyword']
    con = sql.connect("StudentsDB.db")
    cur = con.cursor()
    cur.execute("update studentinfo set Keyword=? where Name=?;",[keyword, fname])
    con.commit()
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from studentinfo")
    rows = cur.fetchall()
    return render_template("changekeyword.html",rows=rows)

@app.route("/changedata")
def changedata():
    return render_template('changesalary.html')


@app.route('/changesalary',methods=['POST'])
def changesalary():
    fname = request.form['fname']
    salary = request.form['salary']
    con = sql.connect("StudentsDB.db")
    cur = con.cursor()
    cur.execute("update studentinfo set Salary=? where Name=?;",[salary, fname])
    con.commit()
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from studentinfo")
    rows = cur.fetchall()
    return render_template("changesalary.html",rows=rows)

@app.route("/removedata")
def removedata():
    return render_template('remove.html')


@app.route('/remove',methods=['POST'])
def remove():
    fname = request.form['fname']
    con = sql.connect("StudentsDB.db")
    cur = con.cursor()
    cur.execute("delete from studentinfo where Name=?;",[fname])
    con.commit()
    return render_template("remove.html")

@app.route('/help')
def help():
    text_list = []
    # Python Version
    text_list.append({
        'label': 'Python Version',
        'value': str(sys.version)})
    # os.path.abspath(os.path.dirname(__file__))
    text_list.append({
        'label': 'os.path.abspath(os.path.dirname(__file__))',
        'value': str(os.path.abspath(os.path.dirname(__file__)))
    })
    # OS Current Working Directory
    text_list.append({
        'label': 'OS CWD',
        'value': str(os.getcwd())})
    # OS CWD Contents
    label = 'OS CWD Contents'
    value = ''
    text_list.append({
        'label': label,
        'value': value})
    return render_template('help.html', text_list=text_list, title='help')


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return render_template('404.html', title='404')


@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return render_template('500.html', title='500')

app.run(host='0.0.0.0', port=port, debug=True)
