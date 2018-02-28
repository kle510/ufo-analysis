import os
import json
from operator import itemgetter

jsons_list = []


#get list of jsons
with open('longlat_test.json') as f:
    for curr in f:
        json_string = curr.replace("\'", '"')
        json_String = json_string.replace("}", '}\n')
        formatted_json = json.loads(json_string)
        jsons_list.append(formatted_json)

#sort the dict based on index
new_jsons_list = sorted(jsons_list, key=itemgetter('index'))



#remove the file and rewrite it
if os.path.exists('longlat_test.json'):
    os.remove('longlat_test.json')

output_json = open("longlat_test.json", 'w')

for curr in new_jsons_list:
    output_json.write(str(curr) + "\n")

