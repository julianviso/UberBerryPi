from geopy.geocoders import Nominatim
from geopy import *
import urllib2
import urllib
import requests

def getIPAddress():
	return requests.get('https://api.ipify.org/?format=json').json()["ip"]

def getCurrentAddress():
	ipAddr = getIPAddress()
	return urllib.urlopen('http://api.hostip.info/get_html.php?ip=' + ipAddr + '&position=true').read()

def getLatLongitudes():
	geolocator = Nominatim()
	whereToPrompt = raw_input("What address do you want to get the latitude and longitude of? ")
	location = geolocator.geocode(whereToPrompt)
	if location:
		#print currentAddress + "\n"
		print location.address + "\n"
		print((location.latitude, location.longitude))
	else:
		print "Not able to get address, try again"
