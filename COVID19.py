import requests
import json
from datetime import datetime
import pytz

url = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"

response = json.loads(requests.get(url).text)

infected = {}
for i in response["features"]:
	region = i["attributes"]["Country_Region"]

	print(region)

	infected[region] = {}
	infected[region]["Lat"] = i["attributes"]["Lat"]
	infected[region]["Lon"] = i["attributes"]["Long_"]
	infected[region]["Confirmed"] = i["attributes"]["Confirmed"]
	infected[region]["Deaths"] = i["attributes"]["Deaths"]
	infected[region]["Recovered"] = i["attributes"]["Recovered"]
	
	unixTime = (i["attributes"]["Last_Update"])/1000 # Convert to seconds
	infected[region]["Last Updated Unix"] = unixTime

	est = pytz.timezone("US/Eastern")
	estTime = datetime.utcfromtimestamp(unixTime).astimezone(est)
	strTime = estTime.strftime('%Y-%m-%d %I:%M:%S %p (%Z%z)')

	infected[region]["Last Updated Readable"] = strTime

gbl_confirmed = 0
gbl_deaths = 0
gbl_recovered = 0

for region in sorted(infected.keys()):
	print(">>> ", region)
	print("Confirmed Cases: ", infected[region]["Confirmed"])
	print("Deaths Reported: ", infected[region]["Deaths"])
	print("Recovered Cases: ", infected[region]["Recovered"])
	print("Last Updated   : ", infected[region]["Last Updated Readable"])
	print("=======================================================")

	gbl_confirmed += infected[region]["Confirmed"]
	gbl_deaths += infected[region]["Deaths"]
	gbl_recovered += infected[region]["Recovered"]

print("*******************************************************")
print(">>> Global Statistics")
print("Global Confirmed : ", gbl_confirmed)
print("Global Deaths    :  ", gbl_deaths)
print("Global Recovered : ", gbl_recovered)
print("Global Pending   : ", gbl_confirmed-gbl_deaths-gbl_recovered)
print("Global Death/Recovery Ratio:", round(gbl_deaths/gbl_recovered,2), "%")
print("*******************************************************")