import requests
import json

def getlocationLonLat():
  locationdata = requests.get('https://api.ipgeolocation.io/ipgeo?apiKey=c5eb1350abec4b518a808dba26c766f5').text
  jsondata = json.loads(locationdata)
  return "{ \"lon\":" + jsondata['longitude'] + ", \"lat\":" + jsondata['latitude'] + "}";  #{\"lon\":\"-81.20288\", \"lat\":\"41.58339\" }

def getlocationCity():
  locationdata = requests.get('https://api.ipgeolocation.io/ipgeo?apiKey=c5eb1350abec4b518a808dba26c766f5').text
  jsondata = json.loads(locationdata)
  return jsondata['city'] + ", " + jsondata['state_prov']
