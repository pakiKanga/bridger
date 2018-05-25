import json, urllib
import requests
import random, string
import urllib.request
import math
import numpy as np
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from bridger import app, db
from BridgerViews.models import UserSession
from locations.models import UserLocation
import os, datetime, json, random

ID = "AIzaSyD3Grw77GNz2fnPKnU23JWQaoXjeU97iT8"
past_subjects = [
 {
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'year_completed': 2016,
   'semester': 1,
   'prescribed_textbook': 'Dummys Guide to Programming',
   'book_id': 1,
   'enjoyability': 4,
   'difficulty' : 5
 }, {
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'year_completed': 2016,
   'semester': 1,
   'prescribed_textbook': 'Dummys Guide to Programming',
   'book_id': 1,

   'enjoyability': 4,
   'difficulty' : 5
 },{
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'year_completed': 2016,
   'semester': 1,
   'prescribed_textbook': 'Dummys Guide to Programming',
   'book_id': 1,
   'enjoyability': 4,
   'difficulty' : 5
 }, {
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'year_completed': 2016,
   'semester': 1,
   'prescribed_textbook': 'Dummys Guide to Programming',
   'book_id': 1,

   'enjoyability': 4,
   'difficulty' : 5
 },
]

curr_subjects = [
 {
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'semester': 1,
   'year_completed': 2018,
   'prescribed_textbook': 'Dummys Guide to Programming',
    'book_id': 1,
   'enjoyability': 4,
   'difficulty' : 5
 },{
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'semester': 1,
   'year_completed': 2018,
   'prescribed_textbook': 'Dummys Guide to Programming',
   'book_id': 1,

   'enjoyability': 4,
   'difficulty' : 5
 },{
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'semester': 1,
   'year_completed': 2018,
   'prescribed_textbook': 'Dummys Guide to Programming',
   'book_id': 1,
   'enjoyability': 4,
   'difficulty' : 5
 },{
   'name': 'Introduction to Programming',
   'subject_code': 'INFO1110',
   'semester': 1,
   'year_completed': 2018,
   'prescribed_textbook': 'Dummys Guide to Programming',
   'book_id': 1,
   'enjoyability': 4,
   'difficulty' : 5
 },
]

universities = [
  {
    'name': 'University of Sydney',
    'logo': 'static/images/usyd.png'
  },{
    'name': 'University of New South Wales',
    'logo': 'static/images/unsw.png'
  },{
    'name': 'University of Technology Sydney',
    'logo': 'static/images/uts.png'
  },{
    'name': 'Macquarie University',
    'logo': 'static/images/mq.png'
  },{
    'name': 'University of Western Sydney',
    'logo': 'static/images/wsu.png'
  },{
    'name': 'Notredame Universtiy',
    'logo': 'static/images/nda.png'
  },{
    'name': 'ACU',
    'logo': 'static/images/acu.png'
  },
]


books = [
    {
    'id': 1,
    'name': 'Dummys Guide to Programming',
    'author': 'Greg Frinklestein',
    'price' : 20
    },
    {
    'id': 2,
    'name': 'A primer to C++',
    'author': 'Jerry Seinfield',
    'price': 20
    },
    {
    'id': 3,
    'name': 'Undefined',
    'author': 'Groot',
    'price': 20
    }
]

max_id = 4

@app.route('/syncSubjects')
def syncSubjects():
    return None


@app.route('/sellBook/<string:book_id>')
def sellBook(book_id):
    for x in books:
        if x['id'] == int(book_id):
            return render_template('sell_resource.html', book=x)
    return render_template('sell_resource.html', book=None)

@app.route('/showSubjects')
def showSubjects():
    return render_template('subject_list.html', past_subjects=past_subjects, curr_subjects=curr_subjects)

@app.route('/buyBook/<string:book_id>')
def buyBook(book_id):
    for x in books:
        if x['id'] == int(book_id):
            return render_template('buy_resource.html', book=x)
    return render_template('buy_resource.html', book=None)

@app.route('/login')
def login():
    return render_template('login_page.html', universities=universities)

@app.route('/loginPage')
def loginPage():
    return render_template('login.html')

@app.route('/messages')
def messages():
    return render_template('messages.html')

@app.route('/completeLogin')
def completeLogin():
    session['username'] = 'user'
    return redirect(url_for('showSubjects'))

@app.route('/register')
def register():
    return render_template('register_page.html', universities=universities)

@app.route('/registerPage')
def registerPage():
    return render_template('register.html')

@app.route('/completeRegister')
def completeRegister():
    return redirect(url_for('showSubjects'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', sidebar=False)


@app.route('/bookListed')
def bookListed():
    viewers = random.randint(500, 1000) 
    return render_template('bookListed.html', viewers=viewers)

@app.route('/commitBook')
def commitBook():
    success = True
    book_name = request.args.get('book_name', 0, type=str)
    author = request.args.get('author', 0, type=str)
    price = request.args.get('price', 0, type=str)
    subject = request.args.get('subject', 0, type=str)
    condition = request.args.get('condition', 0, type=str)

    new_book = {
        'id': max_id,
        'name': book_name,
        'author': author,
        'price' : price
        }
    books.append(new_book)
    for x in books:
        print(x)
    return jsonify(dict(redirect='http://127.0.0.1:5000/bookListed'))

#Function which generates a random ID of a specific size
def id_generator(size, chars=string.ascii_uppercase + string.digits):
    id_val = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
    return id_val

def set_session(session_id):
    session['session_token'] = session_id

#Returns a session if it exists, else None
def return_session(session_id):
    session['session_token'] = session_id
    return session['session_token']

@app.route('/joinSession/<string:session_id>')
def joinSession(session_id):
    curr_session = return_session(session_id)
    if curr_session:
        return render_template('enter_locations.html')
    else:
        flash("Session does not exist.")
    return redirect(url_for('index'))

@app.route('/BridgerViews')
def BridgerViews():
    session_id = id_generator(12)
    curr_date = datetime.datetime.now()
    set_session(session_id)
    return redirect(url_for('joinSession', session_id=session_id))
