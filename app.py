import json, urllib
import requests
import random, string
import urllib.request
import math
import numpy as np
from flask import Flask, render_template, request, jsonify, session
import database.sqlalchemy_insert as db

app = Flask(__name__)
app.secret_key = '\xaa\x8c\xa0\xfd\xd3\xa0C\xf08\xc0\x18\xe2\x80H\xaaQ\x93\t\x12\xc7\x91'
app.config['GOOGLE_API_KEY'] = 'AIzaSyAavEzAtMJulJUW-zw27g4pqZ3u21fLQKg'
app.config.from_object('configmodule.DevelopmentConfig')


@app.route("/")
@app.route("/index")
def index():
	session.pop('locations', None)
	session['locations'] = {'coords': []}

	return render_template('index.html')

# secure and clear function for generating a unique application serial number
def session_id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    session_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
    return session_id

@app.route('/enterLocations')
def enterLocations():
    session = session_id_generator()
    return render_template('enter_locations.html', session=session)

@app.route('/calculateConvergence')
def calculateConvergence():
	coords = convertLocationToCoords(session['locations']['coords'])
	midpoint = findConvergence(coords)
	# locationURL = findLocations(midpoint)
	return render_template('location_list.html', convergence=midpoint, key = app.config['GOOGLE_API_KEY'])

@app.route('/addLocation', methods=['GET', 'POST'])
def addLocation():
	curr_address = request.args.get('curr_address', 0, type=str) #Get jobsb ID from Javascript
	session['locations']['coords'].append(curr_address)
	session.modified = True
	print(session['locations'])
	return jsonify("True");



#Converts addresses to GPS longitude and latitude coordinates
def convertLocationToCoords(groupMember):
	ID = app.config['GOOGLE_API_KEY']
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
	ID = app.config['GOOGLE_API_KEY']
	url = 'https://maps.googleapis.com/maps/' \
'api/distancematrix/json?units=imperial&origins=' + orig + ',NSW&destinations=' + dest + ',NSW&key=' + ID

	googleResponse = requests.get(url)
	json_data = json.loads(googleResponse.text)
	print(json_data['origin_addresses'][0] + " - " + json_data['destination_addresses'][0])
	thisDist = int(json_data['rows'][0]['elements'][0]['distance']['value'])
	return thisDist

# Crunch function
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

def findLocations(convergenceCoords):
    api_key = app.config['GOOGLE_API_KEY']
    latitude = convergenceCoords['lat']
    longitude = convergenceCoords['lng']
    print("Finding locations at latitude, longitude:{}, {}\n".format(latitude, longitude))
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=1000&type=restaurant&key={}'.format(latitude, longitude, api_key)
    #googleResponse = requests.get(url)
    #json_data = json.loads(googleResponse.text)
    return url


if __name__ == "__main__":
    app.run()



# groupSize = int(input("Enter number of members: "))
# groupMember = []
# for x in range(0, groupSize):
#     groupMember.append(input("Enter your address: "))

# groupMemberCoords = convertLocationToCoords(groupMember)

# for x in range(0, len(groupMember)):
#     print("Address: {0} | Latitude: {1} | Longitude {2}".format(groupMember[x], str(groupMemberCoords[x]['lat']),str(groupMemberCoords[x]['lng'])))
# midpoint = findConvergence(groupMemberCoords)

# #print(midpoint)

# locations = findLocations(midpoint)
# print("Restaurant List: ")
# for x in locations:
#     print("{} | {}".format(x['name'], x['vicinity']))
