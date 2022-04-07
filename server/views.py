from pprint import pprint
import googlemaps
from datetime import datetime
from flask import Blueprint, jsonify, request, json
views = Blueprint('views', __name__)

# Get all stops from CSV
# First line "(Customer ID,Address,City,State,Zip)" was removed from CSV for simplification
stops = {}


start_address = "1560 5th Ave, Bay Shore, NY 11706, USA"
# Google Maps doesn't accept same start / end locations;
end_address = "1557 5th Ave, Bay Shore, NY 11706, USA"

# API key is written here for simplicity
API_KEY = "AIzaSyDU2jziAT798Q4K9dY0E5GM3rNZF7oTfmo"
gmaps = googlemaps.Client(API_KEY)


routes = open("server/Route.csv").read().splitlines()
for line in routes:
    line = line.split(',', 1)
    key = line[0]
    line = line[1]
    stops[key] = line


@views.route('/getStops', methods=['GET', 'POST'])
def getStops():
    return stops


@views.route('/getPath', methods=['GET', 'POST'])
def getPath():
    choices = json.loads(request.data)
    addresses = []
    markers = start_address
    for choice in choices['choices']:
        addresses.append(stops[choice])
        markers = markers + "|" + stops[choice]
    markers = markers + "|" + end_address

    now = datetime.now()

    directions = gmaps.directions(start_address, end_address,
                                  mode="driving",
                                  departure_time=now, waypoints=addresses, optimize_waypoints=True)
    # pprint(directions)
    polyline = directions[0]['overview_polyline']['points']
    polyline = polyline.replace("\\\\", "\\")

    duration = 0
    distance = 0
    for x in directions[0]['legs']:
        duration = duration + x['duration']['value']
        distance = distance + x['distance']['value']

    map_url = "https://maps.googleapis.com/maps/api/staticmap?size=600x600&center={}&markers=color:blue|{}&zoom=10&path=weight:3|color:red|enc:{}&key={}".format(
        start_address, markers, polyline, API_KEY)
    print(map_url)
    return jsonify({
        'map_url': map_url,
        'distance': distance,
        'duration': duration
    })
