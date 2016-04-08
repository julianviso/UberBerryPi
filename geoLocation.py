from geopy.geocoders import Nominatim
from geopy import *
import urllib
import requests


class geoLocations(object):
    def getIPAddress(self):
        return requests.get('https://api.ipify.org/?format=json').json()["ip"]

    def getCurrentAddress(self):
        ipAddr = geoLocations.getIPAddress()
        return urllib.urlopen('http://api.hostip.info/get_html.php?ip=' + ipAddr + '&position=true').read()

    def getMyAddress(self):
        geolocator = Nominatim()
        currentLocation = raw_input("What's your current address? ")
        myLocation = geolocator.geocode(currentLocation)

        if myLocation:
            return myLocation.latitude, myLocation.longitude
        else:
            return "Not able to get address, try again."

    def getMyDestination(self):
        geolocator = Nominatim()
        whereToPrompt = raw_input("What address do you want to get the latitude and longitude of? ")
        destination = geolocator.geocode(whereToPrompt)

        if destination:
            return destination.latitude, destination.longitude
        else:
            return "Not able to get address, try again."