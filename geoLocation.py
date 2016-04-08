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
	currentLocation = raw_input("What's your current address? ")
	whereToPrompt = raw_input("\nWhat address do you want to get the latitude and longitude of? ")
	myLocation = geolocator.geocode(currentLocation)
	destination = geolocator.geocode(whereToPrompt)
	if location:
		#print currentAddress + "\n"
		print myLocation.address + "\n"
		print((myLocation.latitude, myLocation.longitude))
		print destination.address + "\n"
		print ((destination.latitude, destination.longitude))
	else:
		return "Not able to get address, try again"
