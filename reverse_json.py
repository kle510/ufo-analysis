import os


# remove the file and rewrite it
if os.path.exists('test.json'):
    os.remove('test.json')

output_json = open("test.json", 'w')

with open('ufo_awesome_with_airport.json') as f:
        for curr in f:
            formatted_json = curr.replace('"', "\'")
            formatted_json = formatted_json.replace("{\'", '{"')
            formatted_json = formatted_json.replace("\':", '":')
            formatted_json = formatted_json.replace("\',", '",')

            formatted_json = formatted_json.replace(": \'", ': "')
            formatted_json = formatted_json.replace(", \'", ', "')
            output_json.write(formatted_json)

