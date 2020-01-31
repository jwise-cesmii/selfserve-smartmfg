import requests
import json

myIP = requests.get('http://ip.42.pl/raw').text
print ("IP: " + myIP)

locationdata = requests.get('https://api.ipgeolocation.io/ipgeo?apiKey=c5eb1350abec4b518a808dba26c766f5').text
#print(locationdata)

jsondata = json.loads(locationdata)

print ("city: " + jsondata['city'])
print ("state: " + jsondata['state_prov'])
