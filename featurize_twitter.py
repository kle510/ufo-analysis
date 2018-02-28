import os
import csv
import json
import codecs
from geopy.distance import great_circle
import operator


def get_tweets(twitter_features_list):
    #with open('twitter-sentiment.csv', 'r') as csvfile:  # this will close the file automatically.
    with codecs.open('twitter-sentiment.csv', "r", encoding='utf-8', errors='ignore') as csvfile:

        for i in range(0,1):
            next(csvfile)

        file_reader = csv.reader(csvfile)

        #western[0], mountain[1], central[2], eastern[3], discard other
        western_twitter_info = []
        mountain_twitter_info = []
        central_twitter_info = []
        eastern_twitter_info = []



        western_total_airline_sentiment = 0;
        western_total_airline_sentiment_confidence = 0;
        western_total_num_entries = 0;
        western_airline_counter = {}

        mountain_total_airline_sentiment = 0;
        mountain_total_airline_sentiment_confidence = 0;
        mountain_total_num_entries = 0;
        mountain_airline_counter = {}

        central_total_airline_sentiment = 0;
        central_total_airline_sentiment_confidence = 0;
        central_total_num_entries = 0;
        central_airline_counter = {}

        eastern_total_airline_sentiment = 0;
        eastern_total_airline_sentiment_confidence = 0;
        eastern_total_num_entries = 0;
        eastern_airline_counter = {}




        for row in file_reader:

            try:
                timezone_of_tweet = row[14]
                airline_sentiment = row[1]
                airline_sentiment_confidence = float(row[2])
                airline_surveyed = row[3]
                airline_sentiment_score = 0

                if airline_sentiment == "positive":
                    airline_sentiment_score = airline_sentiment_score + 1
                elif airline_sentiment == "negative":
                    airline_sentiment_score = airline_sentiment_score - 1


                if timezone_of_tweet.startswith('Western'):
                    western_total_airline_sentiment = western_total_airline_sentiment + airline_sentiment_score
                    western_total_airline_sentiment_confidence = western_total_airline_sentiment_confidence + airline_sentiment_confidence
                    western_total_num_entries = western_total_num_entries + 1

                    if airline_surveyed in western_airline_counter:
                        western_airline_counter[airline_surveyed] = western_airline_counter[airline_surveyed] + 1
                    else:
                        western_airline_counter[airline_surveyed] = 1
                elif timezone_of_tweet.startswith("Mountain"):
                    mountain_total_airline_sentiment = mountain_total_airline_sentiment + airline_sentiment_score
                    mountain_total_airline_sentiment_confidence = mountain_total_airline_sentiment_confidence + airline_sentiment_confidence
                    mountain_total_num_entries = mountain_total_num_entries + 1

                    if airline_surveyed in mountain_airline_counter:
                        mountain_airline_counter[airline_surveyed] = mountain_airline_counter[airline_surveyed] + 1
                    else:
                        mountain_airline_counter[airline_surveyed] = 1
                elif timezone_of_tweet.startswith("Central"):
                    central_total_airline_sentiment = central_total_airline_sentiment + airline_sentiment_score
                    central_total_airline_sentiment_confidence = central_total_airline_sentiment_confidence + airline_sentiment_confidence
                    central_total_num_entries = central_total_num_entries + 1

                    if airline_surveyed in central_airline_counter:
                        central_airline_counter[airline_surveyed] = central_airline_counter[airline_surveyed] + 1
                    else:
                        central_airline_counter[airline_surveyed] = 1
                elif timezone_of_tweet.startswith("Eastern"):
                    eastern_total_airline_sentiment = eastern_total_airline_sentiment + airline_sentiment_score
                    eastern_total_airline_sentiment_confidence = eastern_total_airline_sentiment_confidence + airline_sentiment_confidence
                    eastern_total_num_entries = eastern_total_num_entries + 1

                    if airline_surveyed in eastern_airline_counter:
                        eastern_airline_counter[airline_surveyed] = eastern_airline_counter[airline_surveyed] + 1
                    else:
                        eastern_airline_counter[airline_surveyed] = 1
                else:
                    continue

            except:
                pass

        western_avg_airline_sentiment = western_total_airline_sentiment / western_total_num_entries
        western_avg_airline_sentiment_confidence = western_total_airline_sentiment_confidence / western_total_num_entries
        western_most_populous_airline = max(western_airline_counter.items(), key=operator.itemgetter(1))[0]

        mountain_avg_airline_sentiment = mountain_total_airline_sentiment / mountain_total_num_entries
        mountain_avg_airline_sentiment_confidence = mountain_total_airline_sentiment_confidence / mountain_total_num_entries
        mountain_most_populous_airline = max(mountain_airline_counter.items(), key=operator.itemgetter(1))[0]

        central_avg_airline_sentiment = central_total_airline_sentiment / central_total_num_entries
        central_avg_airline_sentiment_confidence = central_total_airline_sentiment_confidence / central_total_num_entries
        central_most_populous_airline = max(central_airline_counter.items(), key=operator.itemgetter(1))[0]

        eastern_avg_airline_sentiment = eastern_total_airline_sentiment / eastern_total_num_entries
        eastern_avg_airline_sentiment_confidence = eastern_total_airline_sentiment_confidence / eastern_total_num_entries
        eastern_most_populous_airline = max(eastern_airline_counter.items(), key=operator.itemgetter(1))[0]

        western_twitter_info.append(western_avg_airline_sentiment)
        western_twitter_info.append(western_avg_airline_sentiment_confidence)
        western_twitter_info.append(western_most_populous_airline)

        mountain_twitter_info.append(mountain_avg_airline_sentiment)
        mountain_twitter_info.append(mountain_avg_airline_sentiment_confidence)
        mountain_twitter_info.append(mountain_most_populous_airline)

        central_twitter_info.append(central_avg_airline_sentiment)
        central_twitter_info.append(central_avg_airline_sentiment_confidence)
        central_twitter_info.append(central_most_populous_airline)

        eastern_twitter_info.append(eastern_avg_airline_sentiment)
        eastern_twitter_info.append(eastern_avg_airline_sentiment_confidence)
        eastern_twitter_info.append(eastern_most_populous_airline)




        twitter_features_list.append(western_twitter_info)
        twitter_features_list.append(mountain_twitter_info)
        twitter_features_list.append(central_twitter_info)
        twitter_features_list.append(eastern_twitter_info)



    return twitter_features_list


def updateJSON(twitter_features_list):


    error_log = open("error_log_json.txt", 'a')
    index = 0

    list_of_json_strings = []

    with open('longlat.json') as f:
        with open('ufo_awesome_with_airport.json') as g:

            for line_a, line_b in zip(f,g):
                try:
                    longlat_json = json.loads(line_a)
                    input_json = json.loads(line_b)



                    #shooting distance
                    ufo_coordinates = (longlat_json["coordinates"])
                    shortest_distance = 9514  # longest distance between any two US territories
                    number_of_state_shootings = 0
                    number_of_yearly_shootings = 0
                    shooting_coordinates = twitter_features_list[0]



                    for curr in shooting_coordinates:

                        if not all(curr):
                            continue

                        shooting_coordinates = curr
                        curr_distance = great_circle(ufo_coordinates, shooting_coordinates).miles

                        if curr_distance < shortest_distance:
                            shortest_distance = curr_distance

                    #number of shootings in state
                    ufo_state = input_json["location"][-2:]

                    if ufo_state in twitter_features_list[2]:
                        number_of_state_shootings += twitter_features_list[2][ufo_state]


                    #number of shootings per year
                    ufo_year = input_json["sighted_at"][:4]

                    if ufo_year in twitter_features_list[1]:
                        number_of_yearly_shootings += twitter_features_list[1][ufo_year]





                    #append the JSON
                    input_json["closest_shooting"] = shortest_distance
                    input_json["shootings_in_state"] = number_of_state_shootings
                    input_json["shootings_per_year"] = number_of_yearly_shootings



                    list_of_json_strings.append(str(input_json))

                    print(index)
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
            #get rid of double backslash
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

            #print(output)

            list_of_tsv_strings.append(output)

            print(index)
            index = index+1

        except Exception as e:
            err = str(index) + " " + str(e)
            print(err)
            error_log.write(err + "\n")
            index = index + 1
            pass
    return list_of_tsv_strings


def writeJSON(jsons_list):

    #remove the file and rewrite it
    if os.path.exists('ufo_awesome_with_airport_shooting_hospital.json'):
        os.remove('ufo_awesome_with_airport_shooting_hospital.json')

    output_json = open("ufo_awesome_with_airport_shooting_hospital.json", 'w')

    for curr in jsons_list:
        output_json.write(curr)



def writeTSV(tsvs_list):
    if os.path.exists('ufo_awesome_with_airport_shooting_hospital.tsv'):
        os.remove('ufo_awesome_with_airport_shooting_hospital.tsv')

    output_tsv = open("ufo_awesome_with_airport_shooting_hospital.tsv", 'w')

    for curr in tsvs_list:
        output_tsv.write(curr)


if __name__ == "__main__":

    twitter_features_list = []
    get_tweets(twitter_features_list)
    jsons_list = updateJSON(twitter_features_list)
    tsvs_list = JSONtoTSV(jsons_list)

    writeJSON(jsons_list)
    writeTSV(tsvs_list)
