import json
import os
import time
from geopy.geocoders import Nominatim



output_file = open("longlat.json", 'a')
error_log = open("error_log_modify.txt", 'a')
index = 0

with open('longlat.json') as f:
    with open('../ufo_awesome_with_airport.json') as g:

        # edit the range and index if we need to write in between
        for i in range(0 ,0):
            next(f)
        for line in f:

            input_json = {}

            ufo_line = g.readline()

            line = line.replace("\'", '"')

            input_json = json.loads(line)

            while (int(input_json["index"]) > index):

                try:
                    ufo_json = json.loads(ufo_line)

                    geolocator = Nominatim()
                    ufo_location = geolocator.geocode(ufo_json["location"])

                    # find closest airport


                    ufo_coordinates = (ufo_location.longitude, ufo_location.latitude)

                    out = {
                        "index": str(index),
                        "location": str(ufo_json["location"]),
                        "coordinates": str(ufo_coordinates)
                    }
                    print(out)



                    output_file.write(str(out) + "\n")
                    #time.sleep(0.3)

                    index = index + 1
                    ufo_line = g.readline()



                except Exception as e:
                    err = str(index) + " " + str(e)
                    print(err)
                    error_log.write(err + "\n")

                    if input_json != {} and input_json["index"] != str(index):
                        pass

                    index = index + 1
                    pass

            index = index + 1

