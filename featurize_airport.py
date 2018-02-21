import os
import csv
import json
from geopy.geocoders import Nominatim
from geopy.distance import great_circle



#read airports.csv
#if name is medium-airport or large-airport, extract coordinates
#for each ufo sighting, calculate distance to the airport in miles
#save new json

def get_airports(airports_list):
    with open('airport-codes.csv', 'r') as csvfile:  # this will close the file automatically.
        airport_reader = csv.reader(csvfile)
        for row in airport_reader:
            airport_type = row[1]
            airport_name = row[2]
            airport_coordinates = row[3] #longitude, latitude
            airport_country = row[6]
            if airport_country == "US":
                if airport_type == "large_airport":
                    #print(airport_name, airport_coordinates)
                    airports_list.append((airport_name, airport_coordinates))

    return airports_list


def updateJSON(airports_list):
    #if os.path.exists('ufo_awesome_with_airport.json'):
    #    os.remove('ufo_awesome_with_airport.json')

    output_json = open("ufo_awesome_with_airport.json", 'a')
    error_log = open("error_log.txt", 'a')

    index = 43698
    #index = 0



    with open('ufo_awesome.json') as f:
        for i in range(0,43697): #dang test, co gi thi hoi Khoi
            next(f)
        for line in f:
            try:
                #print((json.loads(line)))
                input_json = json.loads(line)

                geolocator = Nominatim()
                ufo_location = geolocator.geocode(input_json["location"])

                #find closest airport

                ufo_coordinates = (ufo_location.longitude, ufo_location.latitude)
                #print(ufo_location)
                #print(ufo_coordinates)

                shortest_distance = 9514  # longest distance between any two US territories

                # closest airport in [airport_name, shortest_distance]
                closest_airport = []

                for curr in airports_list:

                    airport_name = curr[0]
                    airport_coordinates = curr[1]
                    curr_distance = great_circle(ufo_coordinates, airport_coordinates).miles
                    #print(ufo_location, curr[0], curr_distance)

                    if curr_distance < shortest_distance:
                        shortest_distance = curr_distance
                        if len(closest_airport) == 0:
                            closest_airport.append(airport_name)
                            closest_airport.append(shortest_distance)
                            #print(ufo_location, closest_airport)
                        else:
                            closest_airport[0] = airport_name
                            closest_airport[1] = shortest_distance
                            #print(ufo_location, closest_airport)

                print(index, ufo_location, closest_airport)


                #edit the JSON
                input_json['airport_name'] = closest_airport[0]
                input_json['airport_distance'] = closest_airport[1]

                output_json.write(str(input_json))
                index = index + 1
            except Exception as e:
                err = "Skipped Data: " + str(index) + " " + str(e)
                print(err)
                error_log.write(err + "\n")
                index = index + 1
                pass




if __name__ == "__main__":

    airports_list = []
    get_airports(airports_list)
    updateJSON(airports_list)
