import json
import os
import time
from geopy.geocoders import Nominatim


output_file = open("longlat.json", 'a')
error_log = open("error_log_longlat.txt", 'a')
index = 51699

with open('ufo_awesome_with_airport.json') as f:

    # Edit the range and index if we need to write in between
    for i in range(0, 51698):
        next(f)
    for line in f:
        try:
            input_json = json.loads(line)
            geolocator = Nominatim()
            ufo_location = geolocator.geocode(input_json["location"])
            # Find the closest airport
            ufo_coordinates = (ufo_location.longitude, ufo_location.latitude)

            out = {
                "index": str(index),
                "location": str(input_json["location"]),
                "coordinates": str(ufo_coordinates)
            }
            print(out)
            output_file.write(str(out) + "\n")
            index = index + 1
            # time.sleep(0.1)
        except Exception as e:
            err = str(index) + " " + str(e)
            print(err)
            error_log.write(err + "\n")
            index = index + 1
            pass
# Get the rest, sort it, and then featurize it
