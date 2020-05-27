# UFO Analysis
Feature Analysis of UFO sighting data through various Python scripts.

## Run in this order:

<p>featurize_airport.py 
<br><b>Reads in</b>: airport-codes.csv, ufo_awesome.json
<br><b>Writes out</b>: ufo_awesome_with_airport.json, ufo_awesome_with_airport.tsv

Here, we forgot to cache the longitude and latitude coordinates, so we wrote separate scripts to extract and modify them.

<p>longlat_formatjson.py
<br><b>Reads in</b>: ufo_awesome_with_airport.json
<br><b>Writes out</b>: longlat.json

<p>longlat_modify.py
<br><b>Reads in</b>: long_lat.json
<br><b>Writes out</b>: longlat.json

<p>featurize_shooting.py
<br><b>Reads in</b>: mass-shootings.csv, ufo_awesome_with_airport.json
<br><b>Writes out</b>: ufo_awesome_with_airport_shooting.json, ufo_awesome_with_airport_shooting.tsv

<p>featurize_vahospital.py
<br><b>Reads in</b>: VAFacilityLocation.json, ufo_awesome_with_airport_shooting.json
<br><b>Writes out</b>: ufo_awesome_with_airport_shooting_hospital.json, ufo_awesome_with_airport_shooting_hospital.tsv

Here, twitter-sentiment.sqlite is converted to a .csv file in an external program.

<p>featurize_twitter.py
<br><b>Reads in</b>: twitter-sentiment.csv, ufo_awesome_with_airport_shooting_hospital.json
<br><b>Writes out</b>: ufo_awesome_with_airport_shooting_hospital_twitter.json, ufo_awesome_with_airport_shooting_hospital_twitter.tsv

<p>Final TSV file:
<br>ufo_awesome_with_airport_shooting_hospital_twitter.tsv
