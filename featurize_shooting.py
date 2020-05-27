import os
import csv
import json
import codecs
from geopy.distance import great_circle


us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

state_bank = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
              "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
              "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
              "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
              "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
              "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
              "New Hampshire", "New Jersey", "New Mexico", "New York",
              "North Carolina", "North Dakota", "Ohio",
              "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
              "South  Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
              "Vermont", "Virginia", "Washington", "West Virginia",
              "Wisconsin", "Wyoming"]


def get_shootings(shooting_features_list):
    with codecs.open('mass-shootings.csv', "r", encoding='utf-8', errors='ignore') as csvfile:
        for i in range(0, 1):
            next(csvfile)
        file_reader = csv.reader(csvfile)

        dict_of_years = {}
        dict_of_states = {}
        list_of_coordinates = []

        for row in file_reader:
            try:
                shooting_location = row[2]
                x = shooting_location.split(",")
                shooting_state_raw = ""
                shooting_state_abbrev = ""

                # If shooting state is numeric code
                if x[0].isdigit():
                    for state in state_bank:
                        if row[1].find(state) != -1:
                            shooting_state_raw = state
                else:
                    shooting_state_raw += x[1].strip()
                print(shooting_state_raw)

                # If state name is already abbreviated
                if len(shooting_state_raw) == 2:
                    shooting_state_abbrev += shooting_state_raw
                else:
                    shooting_state_abbrev += us_state_abbrev[shooting_state_raw]

                if shooting_state_abbrev in dict_of_states:
                    dict_of_states[shooting_state_abbrev] = dict_of_states[shooting_state_abbrev] + 1
                else:
                    dict_of_states[shooting_state_abbrev] = 1

                shooting_date = row[3]
                shooting_year = shooting_date[-4:]

                if shooting_year in dict_of_years:
                    dict_of_years[shooting_year] = dict_of_years[shooting_year] + 1
                else:
                    dict_of_years[shooting_year] = 1

                shooting_latitude = row[11]
                shooting_longitude = row[12]
                shooting_coordinates = (shooting_longitude, shooting_latitude)
                list_of_coordinates.append(shooting_coordinates)
            except:
                pass

    shooting_features_list.append(list_of_coordinates)
    shooting_features_list.append(dict_of_years)
    shooting_features_list.append(dict_of_states)
    return shooting_features_list


def updateJSON(shooting_features_list):

    error_log = open("error_log_json.txt", 'a')
    index = 0
    list_of_json_strings = []

    with open('longlat.json') as f:
        with open('ufo_awesome_with_airport.json') as g:
            for line_a, line_b in zip(f, g):
                try:
                    longlat_json = json.loads(line_a)
                    input_json = json.loads(line_b)
                    # shooting distance
                    ufo_coordinates = (longlat_json["coordinates"])
                    shortest_distance = 9514  # longest distance between any two US territories
                    number_of_state_shootings = 0
                    number_of_yearly_shootings = 0
                    shooting_coordinates = shooting_features_list[0]

                    for curr in shooting_coordinates:
                        if not all(curr):
                            continue
                        shooting_coordinates = curr
                        curr_distance = great_circle(
                            ufo_coordinates, shooting_coordinates).miles
                        if curr_distance < shortest_distance:
                            shortest_distance = curr_distance

                    # Number of shootings in state
                    ufo_state = input_json["location"][-2:]

                    if ufo_state in shooting_features_list[2]:
                        number_of_state_shootings += shooting_features_list[2][ufo_state]

                    # Number of shootings per year
                    ufo_year = input_json["sighted_at"][:4]

                    if ufo_year in shooting_features_list[1]:
                        number_of_yearly_shootings += shooting_features_list[1][ufo_year]

                    # Append the JSON
                    input_json["closest_shooting"] = shortest_distance
                    input_json["shootings_in_state"] = number_of_state_shootings
                    input_json["shootings_per_year"] = number_of_yearly_shootings
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

# fix the json string formatting


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
                "\t" + str(input_json["shootings_per_year"]) + "\n"
            list_of_tsv_strings.append(output)
            index = index + 1
        except Exception as e:
            err = str(index) + " " + str(e)
            print(err)
            error_log.write(err + "\n")
            index = index + 1
            pass
    return list_of_tsv_strings


def writeJSON(jsons_list):
    # Remove the existing file and rewrite it
    if os.path.exists('ufo_awesome_with_airport_shooting.json'):
        os.remove('ufo_awesome_with_airport_shooting.json')

    output_json = open("ufo_awesome_with_airport_shooting.json", 'w')
    for curr in jsons_list:
        output_json.write(curr)


def writeTSV(tsvs_list):
    # Remove the existing file and rewrite it
    if os.path.exists('ufo_awesome_with_airport_shooting.tsv'):
        os.remove('ufo_awesome_with_airport_shooting.tsv')

    output_tsv = open("ufo_awesome_with_airport_shooting.tsv", 'w')
    for curr in tsvs_list:
        output_tsv.write(curr)


if __name__ == "__main__":

    shooting_features_list = []
    get_shootings(shooting_features_list)
    jsons_list = updateJSON(shooting_features_list)
    tsvs_list = JSONtoTSV(jsons_list)
    writeJSON(jsons_list)
    writeTSV(tsvs_list)
