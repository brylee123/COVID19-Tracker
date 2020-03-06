import requests
import json
from datetime import datetime
import pytz
import operator

url = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"

response = json.loads(requests.get(url).text)

infected = {}
for inf in response["features"]:
	region = inf["attributes"]["Country_Region"]

	print(region)

	infected[region] = {}
	infected[region]["Lat"] = inf["attributes"]["Lat"]
	infected[region]["Lon"] = inf["attributes"]["Long_"]
	infected[region]["Confirmed"] = inf["attributes"]["Confirmed"]
	infected[region]["Deaths"] = inf["attributes"]["Deaths"]
	infected[region]["Recovered"] = inf["attributes"]["Recovered"]
	
	unixTime = (inf["attributes"]["Last_Update"])/1000 # Convert to seconds
	infected[region]["Last Updated Unix"] = unixTime

	est = pytz.timezone("US/Eastern")
	estTime = datetime.utcfromtimestamp(unixTime).astimezone(est)
	strTime = estTime.strftime('%Y-%m-%d %I:%M:%S %p (%Z%z)')

	infected[region]["Last Updated Readable"] = strTime

gbl_confirmed = 0
gbl_deaths = 0
gbl_recovered = 0

top10_gross = []

for region in sorted(infected.keys()):

	if len(top10_gross) < 10:
		top10_gross.append((region, infected[region]["Confirmed"]))
	else:
		for i, region_data in enumerate(top10_gross):
			if region_data[1] < infected[region]["Confirmed"]:
				top10_gross.pop(i)
				top10_gross.append((region, infected[region]["Confirmed"]))
				break
	top10_gross.sort(key = operator.itemgetter(1))
	#top10_gross = top10_gross[::-1]

	print(">>> ", region)
	print("Confirmed Cases: ", infected[region]["Confirmed"])
	print("Deaths Reported: ", infected[region]["Deaths"])
	print("Recovered Cases: ", infected[region]["Recovered"])
	print("Last Updated   : ", infected[region]["Last Updated Readable"])
	print("=======================================================")

	gbl_confirmed += infected[region]["Confirmed"]
	gbl_deaths += infected[region]["Deaths"]
	gbl_recovered += infected[region]["Recovered"]


gbl_pop = 7732900000

print("\n\n*******************************************************")
print(">>> Global Statistics (Population = "+str(gbl_pop)+")")
print("Regions/Countries Confirmed : ", len(infected))
print("Global Confirmed : ", gbl_confirmed)
print("Global Deaths    :   ", gbl_deaths)
print("Global Recovered :  ", gbl_recovered)
print("Global Pending   :  ", gbl_confirmed-gbl_deaths-gbl_recovered)
print("Global Death/Recovery Ratio : ", round(gbl_deaths/gbl_recovered,2), "%")
print("Global Infected Ratio       : ", round(gbl_confirmed/gbl_pop,8), "%")
print("Global Death Ratio          : ", round(gbl_deaths/gbl_pop,8), "%")
print("*******************************************************")


us_pop = 327200000
print(">>> United States Statistics (Population = "+str(us_pop)+")")
print("US Confirmed : ", infected["US"]["Confirmed"])
print("US Deaths    :  ", infected["US"]["Deaths"])
print("US Recovered :   ", infected["US"]["Recovered"])
print("US Pending   : ", infected["US"]["Confirmed"]-infected["US"]["Deaths"]-infected["US"]["Recovered"])
print("US Death/Recovery Ratio : ", round(infected["US"]["Deaths"]/infected["US"]["Recovered"],2), "%")
print("US Infected Ratio       : ", round(infected["US"]["Confirmed"]/us_pop,8), "%")
print("US Death Ratio          : ", round(infected["US"]["Deaths"]/us_pop,8), "%")
print("*******************************************************")

print(">>> Top 10 Regions with Most Confirmed Cases")
print("Region\t\t\tConfirmed Infected")
linewidth = 40
for item in top10_gross[::-1]:
	region, inf_pop = item
	space_padding = linewidth-len(region)-len(str(inf_pop))
	print(region+" "*space_padding+str(inf_pop))

print("*******************************************************")
