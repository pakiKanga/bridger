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
import os, datetime, json

ID = "AIzaSyD3Grw77GNz2fnPKnU23JWQaoXjeU97iT8"

@app.route('/syncSubjects')
def syncSubjects():
	return None

@app.route('/showSubjects')
def showSubjects():
	past_subjects = { subject

	}
	return render_template('subject_list.html')
@app.route('/buyBook')
def buyBook():
	return render_template('buy_resource.html')
@app.route('/sellBook')
def sellBook():
	return render_template('sell_resource.html')
	
@app.route("/")
@app.route("/index")
def index():
	session.pop('locations', None)
	session.pop('session_token', None)
	session['locations'] = {'coords': []}
	return render_template('index.html', sidebar=False)

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


@app.route('/calculateConvergence')
def calculateConvergence():
	query = UserLocation.query.filter_by(session_id=session['session_token']).all()
	print(len(query))
	if len(query) < 2:
		flash("We're going to need some locations here!")
		return redirect(url_for('joinSession', session_id=session['session_token']))
	query_results = []
	for x in query:
		query_results.append(x.location_name)
	coords = convertLocationToCoords(query_results)
	midpoint = findConvergence(coords)	
	locations = findLocations(midpoint)
	return render_template('location_list.html', locations=locations, convergence=midpoint, key = app.config['GOOGLE_API_KEY'], session_id=session['session_token'])

#Prepends location to the client's locations list and stores it in the session database
@app.route('/addLocation', methods=['GET', 'POST'])
def addLocation():
	curr_address = request.args.get('curr_address', 0, type=str) #Get jobsb ID from Javascript
	session['locations']['coords'].append(curr_address)
	location_id = id_generator(5)
	curr_location = UserLocation(location_id, session['session_token'], curr_address)
	db.session.add(curr_location)
	db.session.commit()
	session.modified = True
	address_packet = []
	address_packet.append(curr_address)
	return jsonify(convertLocationToCoords(address_packet));

@app.route('/loadLocation', methods=['GET', 'POST'])
def loadLocation():
	curr_address = request.args.get('curr_address', 0, type=str) #Get jobsb ID from Javascript
	address_packet = []
	address_packet.append(curr_address)
	return jsonify(convertLocationToCoords(address_packet));


@app.route('/removeLocation', methods=['GET', 'POST'])
def removeLocation():
	curr_address = request.args.get('curr_address', 0, type=str) #Get jobsb ID from Javascript
	UserLocation.query.filter_by(location_name=curr_address).delete()
	db.session.commit()
	return jsonify("True")

#Converts addresses to GPS longitude and latitude coordinates
def convertLocationToCoords(groupMember):
	groupMemberCoords = []
	url = None
	for member in groupMember:
		url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + member + '&key=' + ID
		googleResponse = requests.get(url)
		json_data = json.loads(googleResponse.text)
		member_coords = json_data['results'][0]['geometry']['location']
		print("Member Coords: ", member_coords, member)
		groupMemberCoords.append(member_coords)
	return groupMemberCoords

#DEPRECATED (i just wanted to use that word it sounds cool)
def calculateDistance(orig, dest):
	url = 'https://maps.googleapis.com/maps/' \
		  'api/distancematrix/json?units=imperial&origins=' + orig + ',NSW&destinations=' + dest + ',NSW&key=' + ID

	googleResponse = requests.get(url)
	json_data = json.loads(googleResponse.text)
	print(json_data['origin_addresses'][0] + " - " + json_data['destination_addresses'][0])
	thisDist = int(json_data['rows'][0]['elements'][0]['distance']['value'])
	return thisDist

def findConvergence(groupMemberCoords):
	size = len(groupMemberCoords)
	lat, lng, X, Y, Z= [], [], [], [], []

	# Do basic math calculations
	for x in range(0, len(groupMemberCoords)):
		# Convert to radians
		lat.append(groupMemberCoords[x]['lat'] * math.pi/180)
		lng.append(groupMemberCoords[x]['lng'] * math.pi/180)

		# Convert to Cartesian Coordinates
		X.append(math.cos(lat[x]) * math.cos(lng[x]))
		Y.append(math.cos(lat[x]) * math.sin(lng[x]))
		Z.append(math.sin(lat[x]))

	# Using weights as 1 and total weights as size
	total_X = np.sum([X])
	total_Y = np.sum([Y])
	total_Z = np.sum([Z])

	longitude = math.atan2(total_Y, total_X)
	hypotenuse = math.hypot(total_X, total_Y)
	latitude = math.atan2(total_Z, hypotenuse)

	# Convert back to degrees
	latitude = latitude * 180/math.pi
	longitude = longitude * 180/math.pi

	return { 'lat' : latitude, 'lng' : longitude }

#Finds locations within a specific vicinity
def findLocations(convergenceCoords):
	api_key = 'AIzaSyAavEzAtMJulJUW-zw27g4pqZ3u21fLQKg'
	latitude = convergenceCoords['lat']
	longitude = convergenceCoords['lng']
	print("Finding locations at latitude, longitude:{}, {}\n".format(latitude, longitude))
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=1000&type=restaurant&key={}'.format(latitude, longitude, api_key)
	print(url)
	googleResponse = requests.get(url)
	json_data = json.loads(googleResponse.text)
	return json_data['results']


