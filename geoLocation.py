from geopy.geocoders import Nominatim
from geopy import *

geolocator = Nominatim()
whereToPrompt = raw_input("What address do you want to get the latitude and longitude of? ")
location = geolocator.geocode(whereToPrompt)
if location:
	print location.address
	print((location.latitude, location.longitude))
else:
	print "Not able to get address, try again"
