import os
import json
from geopy.distance import great_circle


def get_hospitals(hospital_features_list):
    with open('VAFacilityLocation.json') as f:
        data = json.load(f)
        for entry in data["VAFacilityData"]:
            hospital_name = entry["name"]
            hospital_latitude = entry["latitude"]
            hospital_longitude = entry["longitude"]
            hospital_region = entry["region"]
            hospital_coordinates = (hospital_longitude, hospital_latitude)
            hospital_features_list.append(
                (hospital_name, hospital_region, hospital_coordinates))
    return hospital_features_list


def updateJSON(hospital_features_list):
    error_log = open("error_log_json.txt", 'a')
    index = 0
    list_of_json_strings = []

    with open('longlat.json') as f:
        with open('ufo_awesome_with_airport_shooting.json') as g:
            for line_a, line_b in zip(f, g):
                try:
                    longlat_json = json.loads(line_a)
                    input_json = json.loads(line_b)
                    # Get the hospital distance: [closest hospital name, closest hospital distance, closest hospital region]
                    ufo_coordinates = (longlat_json["coordinates"])
                    shortest_distance = 9514  # longest distance between any two US territories
                    closest_hospital = []

                    for curr in hospital_features_list:
                        if not all(curr):
                            continue

                        closest_hospital_name = curr[0]
                        closest_hospital_region = curr[1]
                        hospital_coordinates = curr[2]
                        curr_distance = great_circle(
                            ufo_coordinates, hospital_coordinates).miles

                        if curr_distance < shortest_distance:
                            shortest_distance = curr_distance
                            if len(closest_hospital) == 0:
                                closest_hospital.append(closest_hospital_name)
                                closest_hospital.append(shortest_distance)
                                closest_hospital.append(
                                    closest_hospital_region)
                            else:
                                closest_hospital[0] = closest_hospital_name
                                closest_hospital[1] = shortest_distance
                                closest_hospital[2] = closest_hospital_region
                    # append the JSON
                    input_json["closest_hospital_name"] = closest_hospital[0]
                    input_json["closest_hospital_distance"] = closest_hospital[1]
                    input_json["closest_hospital_region"] = closest_hospital[2]
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

# Fix the JSON string formatting


def formatJSON(list_of_json_strings):
    list_of_formatted_json_strings = []
    for curr in list_of_json_strings:
        formatted_json = curr.replace('"', "\'")
        formatted_json = formatted_json.replace("{\'", '{"')
        formatted_json = formatted_json.replace("\':", '":')
        formatted_json = formatted_json.replace("\',", '",')
        formatted_json = formatted_json.replace(": \'", ': "')
        formatted_json = formatted_json.replace(", \'", ', "')
        formatted_json = formatted_json.replace("\'}", '"}\n')
        list_of_formatted_json_strings.append(formatted_json)
    return list_of_formatted_json_strings


def JSONtoTSV(jsons_list):
    error_log = open("error_log_tsv.txt", 'a')
    index = 0
    list_of_tsv_strings = []

    for curr_json in jsons_list:
        try:
            # get rid of double backslash
            input_json = json.loads(curr_json)
            output = str(input_json["sighted_at"]) +\
                "\t" + str(input_json["reported_at"]) +\
                "\t" + str(input_json["location"]) +\
                "\t" + str(input_json["duration"]) +\
                "\t" + str(input_json["description"]) +\
                "\t" + str(input_json["airport_name"]) +\
                "\t" + str(input_json["airport_distance"]) +\
                "\t" + str(input_json["closest_shooting"]) + \
                "\t" + str(input_json["shootings_in_state"]) + \
                "\t" + str(input_json["shootings_per_year"]) + \
                "\t" + str(input_json["closest_hospital_name"]) + \
                "\t" + str(input_json["closest_hospital_distance"]) + \
                "\t" + str(input_json["closest_hospital_region"]) + \
                "\n"
            list_of_tsv_strings.append(output)
            index = index+1
        except Exception as e:
            err = str(index) + " " + str(e)
            print(err)
            error_log.write(err + "\n")
            index = index + 1
            pass
    return list_of_tsv_strings


def writeJSON(jsons_list):
    # Remove the existing file and rewrite it
    if os.path.exists('ufo_awesome_with_airport_shooting_hospital.json'):
        os.remove('ufo_awesome_with_airport_shooting_hospital.json')

    output_json = open("ufo_awesome_with_airport_shooting_hospital.json", 'w')
    for curr in jsons_list:
        output_json.write(curr)


def writeTSV(tsvs_list):
    # Remove the existing file and rewrite it
    if os.path.exists('ufo_awesome_with_airport_shooting_hospital.tsv'):
        os.remove('ufo_awesome_with_airport_shooting_hospital.tsv')

    output_tsv = open("ufo_awesome_with_airport_shooting_hospital.tsv", 'w')
    for curr in tsvs_list:
        output_tsv.write(curr)


if __name__ == "__main__":
    hospital_features_list = []
    get_hospitals(hospital_features_list)
    jsons_list = updateJSON(hospital_features_list)
    tsvs_list = JSONtoTSV(jsons_list)
    writeJSON(jsons_list)
    writeTSV(tsvs_list)
