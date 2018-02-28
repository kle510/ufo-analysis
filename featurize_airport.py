import os
import csv
import codecs
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


    error_log = open("error_log_json.txt", 'a')

    index = 0

    list_of_json_strings = []

    with open('ufo_awesome_test.json') as f:

        #edit the range and index if we need to write in between
        for i in range(0,0):
            next(f)
        for line in f:
            try:
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


                #append the JSON
                input_json["airport_name"] = closest_airport[0]
                input_json["airport_distance"] = closest_airport[1]

                list_of_json_strings.append(str(input_json))

                index = index + 1
            except Exception as e:
                err = str(index) + " " + str(e)
                print(err)
                error_log.write(err + "\n")
                index = index + 1
                pass

        list_of_formatted_json_strings = formatJSON(list_of_json_strings)
        return list_of_formatted_json_strings



#fix the json string formatting
def formatJSON(list_of_json_strings):


    list_of_formatted_json_strings = []

    with open('ufo_awesome_with_airport.json') as f:
        for curr in list_of_json_strings:
            formatted_json = curr.replace("\'", '"')
            formatted_json = formatted_json.replace("}", '}\n')
            list_of_formatted_json_strings.append(formatted_json)

            #output_json.write(str(formatted_json))

    return list_of_formatted_json_strings


def JSONtoTSV(jsons_list):


    error_log = open("error_log_tsv.txt", 'a')

    index = 0
    list_of_tsv_strings = []

    for curr_json in jsons_list:
        try:
            #get rid of double backslash
            input_json = json.loads(curr_json)
            output = str(input_json["sighted_at"]) +\
                     "\t" + str(input_json["reported_at"]) +\
                     "\t" + str(input_json["location"]) +\
                     "\t" + str(input_json["duration"]) +\
                     "\t" + str(input_json["description"]) +\
                     "\t" + str(input_json["airport_name"]) +\
                     "\t" + str(input_json["airport_distance"]) + "\n"

            #print(output)

            list_of_tsv_strings.append(output)

        except Exception as e:
            err = str(index) + " " + str(e)
            print(err)
            error_log.write(err + "\n")
            index = index + 1
            pass
    return list_of_tsv_strings


def writeJSON(jsons_list):

    #remove the file and rewrite it
    if os.path.exists('ufo_awesome_with_airport.json'):
        os.remove('ufo_awesome_with_airport.json')

    output_json = open("ufo_awesome_with_airport.json", 'w')

    for curr in jsons_list:
        output_json.write(curr)



def writeTSV(tsvs_list):
    if os.path.exists('ufo_awesome_with_airport.tsv'):
        os.remove('ufo_awesome_with_airport.tsv')

    output_tsv = open("ufo_awesome_with_airport.tsv", 'w')

    for curr in tsvs_list:
        output_tsv.write(curr)


if __name__ == "__main__":

    airports_list = []
    get_airports(airports_list)
    jsons_list = updateJSON(airports_list)
    tsvs_list = JSONtoTSV(jsons_list)

    writeJSON(jsons_list)
    writeTSV(tsvs_list)
