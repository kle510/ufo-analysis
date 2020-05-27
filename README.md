# UFO Analysis
The objective of this study is to understand “Big Data’s Unintended Consequences”, with the underlying idea of joining features of datasets to create a comprehensive understanding of their relationships and conclusions we can draw from them through accuracy and similarity measures. In particular, we are focused on drawing information from Unidentified Flying Object (UFO) data and evaluating key learnings from unioning the UFO data with related datasets. We also analyze the unioning’s effects on the 5 V’s (value, veracity, volume, variety, velocity) and answer related questions about the unintended consequences. The implementation and analysis was done in python (tika-python) and tika similarity. 

## Process
#### Data Set and Feature Selection Rationale
The four data sets we chose to join with the UFO data set are major U.S. airport names, mass shootings in the U.S. over the past 50 years (.csv), U.S. Veterans Affairs Hospitals (.json), and Twitter Sentiments on Airlines (.sqlite). Diversifying the data filetypes helped us to add variety. 

Our group thought of various considerations about the airport data set. Typically, large airport sizes are indicative of population densities. Denser and more populated cities are prone to more airport traffic, which can easily be mistaken for a UFO. A larger population base in an area also increases the chances of a reporting a UFO there. 

Outside of geography and demographics, we also wanted to see if we could draw insight into the persona of the viewer. UFO sightings have been a hotbed topic for what is myth and what is reality for decades. Is there legitimate value in associating a person with mental issues with a crazy occurrence, such as a UFO sighting? We wanted to take the angle of potentially learning about the mental health and mental state of the viewer. 

Mass shootings have been a hot topic in the U.S. lately, and we wanted to see if there was any value in a possible  correlation between a shooter a UFO viewer, two categories of people facing mentally challenging issues. Also, we wanted to understand if there is overlap in the setting of mass shootings with areas of different populations and UFO sightings. Were more shootings and UFO sightings prominent in certain states? The data is collected continuously everytime there is a mass shooting over the years, so we also wanted to address velocity. Were more UFO sightings reported in the same years with more shootings? For this purpose, we chose to featurize each UFO sighting with  “distance of closest shooting” to UFO sighting, “number of shootings in the same state” over the 50 year period, and “number of shootings that same year” (across the US). 

Veterans affairs hospitals were chosen for a similar reason.  There are common stereotypes about veterans having post traumatic stress disorder, so we wanted to see if we could draw a key learning about people who might be seeing things with centers of nearby mental health support.  We wanted to chart regions with higher access to VA hospitals to see if it correlated to the quantity of UFO sightings in the area. Did hospital-dense regions  experience higher UFO sightings? For this purpose, we chose to featurize each UFO sighting with “hospital name”, “distance of hospital” to closest UFO sighting, and “region location” of the hospital. 

To tie it all together, we chose the Twitter sentiments on airlines dataset to see if we could draw value from with how a person feels about an aerial object based on the region they are in. The Twitter sentiments dataset was an interesting choice for this case, because it incorporated of how a user was feeling (explored in the mass shootings and mental hospitals dataset) and conveying that towards airplanes, which can be mistaken for UFOs (explored in the airport dataset). Sentiments are subjective, so there also needed to be a veracity measure when assessing them. For each UFO sighting, we chose to featurize “average airline sentiment per timezone”, “average airline sentiment confidence”, and the “most populous airline per timezone” (to see if there were any biases towards particular airlines). 

#### Feature Extraction Methodology
To get the nearest major airport and the nearest distance, we specifically targeted “large airports” and “US” from the csv columns for type and iso_country from the airport dataset and paired the closest airport with the UFO sighting. We used a csv reader to read the airport-codes.csv file to extract the airport type, country, name, and coordinates (longitude and latitude). A brute force calculation was done to compare the coordinate data of the airport and the ufo sighting, caching the smallest updated distance for each sighting and eventually saving the smallest distance and the corresponding large airport to the updated .tsv file. While calling geopy to retrieve the UFO sighting data, 7110 of the 61067 traces were lost. ~70% were lost due delimiter and formatting of the “location” feature in the ufo-awesome.tsv file, leading to a NoneType return in the geopy geocoding call. The remaining ~30% were lost a result of dropped server calls. 

From the mass-shootings.csv dataset, we read out the shooting location, shooting date, and shooting coordinates from the csv columns. Coordinate data was used to calculate distance to nearest hospital in the same manner as airport data, using the geopy miles function. For the shooting location, we parsed out the state name from either the title or the location column, and used a bank of state name variations to get the correct state abbreviation. For shooting date, we parsed out the 4 digits that constituted the year. We then stored the state and year information in frequency count dictionaries, matching the state and year information to that of the UFO data and featurizing the frequency to the UFO data. 

For the VAFacilityLocation.json dataset, we directly extracted the hospital coordinates and also used the geopy miles function to locate the nearest UFO sighting. We then featurized the hospital name and region of the hospital closest  to that UFO sighting. 

We exported the twitter-sentiment.sqlite file to a csv file, and followed similar steps to extract information for airline name, airline sentiment, airline sentiment confidence, and timezone of each tweet. From there, we divided up the extracted data by timezones (pacific, mountain, central, eastern), and calculated the airline count, average sentiment, and average sentiment confidence scores for each timezone. The options for sentiment towards an airline were either positive, neutral, or negative, which we rated with scores of 1, 0, and -1.  The sentiment confidence values were  given in the file and rated on a scale of  0 to 1, with 1 being high confidence. We divided approximate longitudinal sections for the timezones and categorized each UFO sighting with a timezone based on its coordinates. Based off the timezones, the average sentiment, average sentiment confidence, and most populous airlines were featurized. 


## Scripts were run in this order:
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

## Observations and Analysis

<img src="images/table1.png" width="40%" height="40%">

Table 1: UFO Distance to Closest Airport, Shooting, and Hospital


From Table 1, we can expect a high result in UFO occurence to an airport, a mass shooting location, and a VA hospital within 25 miles. The distance matching percentage increases to > 75%  when the distance is increased to 50 miles for closest airport and closest shooting, indicating a level of high confidence. However, we don’t believe this to be because of a mental health correlation, but as a product of population density. In metropolitan and densely populated areas, there is greater access greater healthcare resources and large airports, and a higher chance for large scale shootings to occur. Our findings confirm this.

<img src="images/table1.png" width="40%" height="40%">

Table 2: Year of UFO Sightings and Mass Shootings


Table 2 is somewhat inconclusive. The UFO sightings report ends at 2010, but the most mass shootings have occurred in the US within the past 5 years. Still, we see both reports trending upward in the last 5-10 years of them being reported. 

<img src="images/table1.png" width="40%" height="40%">

Table 3: State of UFO Sightings and Mass Shootings


Table 3’s  result is eye-opening. California, Washington, Texas, and Florida consistently appear in the top 5, with New York, Arizona, Ohio in the top 10. While states such as California, Texas, and New York can be attributed to greater populations, the remaining results show some degree of correlation. Perhaps mental health does play a key. 

<img src="images/table1.png" width="40%" height="40%">

Table 4: Number of VA Hospitals and their Territories Covered


Table 4’s  showed similar results. There is greater access to veteran healthcare in California, Florida, New York, and Ohio. Indicating correlation with the previous two tests. 
 
<img src="images/table1.png" width="40%" height="40%">

Table 5: Twitter Results


Surprisingly, breaking down the Twitter sentiment results by timezone did not provide any conclusive evidence about a relationship to UFO sightings  (Table 5). All 4 regions showed roughly equal levels of dissatisfaction with airlines, the sentimental analysis showed high confidence, and United came out as the most used airline (for Pacific, United was a very close second).

We conclude that the UFO and Mass Shooting Datasets have medium value. But, we believe that the value to understanding UFO sightings is largely due to population density and only to mental health to some degree. There was low value in the features we extracted from the Twitter Sentiments Analysis. 
