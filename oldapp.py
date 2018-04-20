import json, urllib
import requests
import random
import urllib.request
import math
import numpy as np

ID = "AIzaSyD3Grw77GNz2fnPKnU23JWQaoXjeU97iT8"

#Converts addresses to GPS longitude and latitude coordinates
def convertLocationToCoords(groupMember):
    groupMemberCoords = []
    url = None
    for member in groupMember:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + member + '&key=' + ID
        googleResponse = requests.get(url)
        json_data = json.loads(googleResponse.text)
        member_coords = json_data['results'][0]['geometry']['location']
        groupMemberCoords.append(member_coords)
    return groupMemberCoords

#Calculates distance between two addresses
def calculateDistance(orig, dest):
    url = 'https://maps.googleapis.com/maps/' \
          'api/distancematrix/json?units=imperial&origins=' + orig + ',NSW&destinations=' + dest + ',NSW&key=' + ID

    googleResponse = requests.get(url)
    json_data = json.loads(googleResponse.text)
    print(json_data['origin_addresses'][0] + " - " + json_data['destination_addresses'][0])
    thisDist = int(json_data['rows'][0]['elements'][0]['distance']['value'])
    return thisDist

def findConvergence(groupMemberCoords):
    size = len(groupMember)
    lat, lng, X, Y, Z= [], [], [], [], []

    # Do basic math calculations
    for x in range(0, len(groupMember)):
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
    api_key = 'AIzaSyAavEzAtMJulJUW-zw27g4pqZ3u21fLQKg'
    latitude = convergenceCoords['lat']
    longitude = convergenceCoords['lng']
    print("Finding locations at latitude, longitude:{}, {}\n".format(latitude, longitude))
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=1000&type=restaurant&key={}'.format(latitude, longitude, api_key)
    googleResponse = requests.get(url)
    json_data = json.loads(googleResponse.text)
    return json_data['results']
    

groupSize = int(input("Enter number of members: "))
groupMember = []
for x in range(0, groupSize):
    groupMember.append(input("Enter your address: "))

groupMemberCoords = convertLocationToCoords(groupMember)

for x in range(0, len(groupMember)):
    print("Address: {0} | Latitude: {1} | Longitude {2}".format(groupMember[x], str(groupMemberCoords[x]['lat']),str(groupMemberCoords[x]['lng'])))
midpoint = findConvergence(groupMemberCoords)

#print(midpoint)

locations = findLocations(midpoint)
print("Restaurant List: ")
for x in locations:
    print("{} | {}".format(x['name'], x['vicinity']))