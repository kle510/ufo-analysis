import os
import json
from operator import itemgetter

jsons_list = []
new_jsons_list = []


#get list of jsons
with open('longlat.json') as f:
    for curr in f:
        json_string = curr.replace("\'", '"')
        json_string = json_string.replace("}", '}\n')
        formatted_json = json.loads(json_string)
        formatted_json["index"] = int(formatted_json["index"])
        jsons_list.append(formatted_json)

#sort the dict based on index
sorted_jsons_list = sorted(jsons_list, key=itemgetter("index"))

for curr in sorted_jsons_list:
    curr["index"] = str(curr["index"])
    json_string = str(curr)
    json_string = json_string.replace("\'", '"')
    json_string = json_string.replace("}", '}\n')
    new_jsons_list.append(json_string)



#remove the file and rewrite it
if os.path.exists('longlat.json'):
    os.remove('longlat.json')

output_json = open("longlat.json", 'w')

for curr in new_jsons_list:
    output_json.write(str(curr))

