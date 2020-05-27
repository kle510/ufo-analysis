# UFO Analysis

## Run in this order:

featurize_airport.py 
<b>Reads in</b>: airport-codes.csv, ufo_awesome.json
<b>Writes out</b>: ufo_awesome_with_airport.json, ufo_awesome_with_airport.tsv

Here, we forgot to cache the longitude and latitude coordinates, so we wrote separate scripts to extract and modify them.

longlat_formatjson.py
<b>Reads in</b>: ufo_awesome_with_airport.json
<b>Writes out</b>: longlat.json

longlat_modify.py
<b>Reads in</b>: long_lat.json
<b>Writes out</b>: longlat.json

featurize_shooting.py
<b>Reads in</b>: mass-shootings.csv, ufo_awesome_with_airport.json
<b>Writes out</b>: ufo_awesome_with_airport_shooting.json, ufo_awesome_with_airport_shooting.tsv

featurize_vahospital.py
<b>Reads in</b>: VAFacilityLocation.json, ufo_awesome_with_airport_shooting.json
<b>Writes out</b>: ufo_awesome_with_airport_shooting_hospital.json, ufo_awesome_with_airport_shooting_hospital.tsv

Here, twitter-sentiment.sqlite is converted to a .csv file in an external program.

featurize_twitter.py
<b>Reads in</b>: twitter-sentiment.csv, ufo_awesome_with_airport_shooting_hospital.json
<b>Writes out</b>: ufo_awesome_with_airport_shooting_hospital_twitter.json, ufo_awesome_with_airport_shooting_hospital_twitter.tsv

Final TSV file:
ufo_awesome_with_airport_shooting_hospital_twitter.tsv
